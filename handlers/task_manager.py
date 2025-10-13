#!/usr/bin/env python3
"""
Task Management Handler for StuckNet
Handles task creation, listing, and due date checking
"""

import json
import os
from datetime import datetime, timedelta
import re
import threading
import time
from typing import List, Dict, Optional
import google.generativeai as genai

# Configure Gemini AI for intelligent due time setting
GEMINI_API_KEY = "AIzaSyCCBtgHUredWvS1QvbWyhwmCbHdydLABzk"
genai.configure(api_key=GEMINI_API_KEY)

# Task storage file
TASKS_FILE = "tasks.json"

def ai_set_due_time(task_title: str, created_at: str) -> Optional[str]:
    """Use AI to intelligently set due time based on task content and creation time"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = f"""
        Analyze this task and suggest an appropriate due time based on the task content and urgency.
        
        Task: "{task_title}"
        Created at: {created_at}
        
        Consider:
        1. Task urgency (urgent tasks should be due sooner)
        2. Task type (calls, meetings, reports, etc.)
        3. Time of day when created
        4. Business hours (9 AM - 6 PM)
        
        Return ONLY a datetime in ISO format (YYYY-MM-DDTHH:MM:SS) or "null" if no due time should be set.
        Examples:
        - "2025-10-13T21:00:00" (today at 9 PM)
        - "2025-10-14T09:00:00" (tomorrow at 9 AM)
        - "null" (no due time)
        
        Response:"""
        
        response = model.generate_content(prompt)
        ai_suggestion = response.text.strip()
        
        # Validate the AI response
        if ai_suggestion.lower() == "null":
            return None
        
        try:
            # Try to parse the datetime
            due_time = datetime.fromisoformat(ai_suggestion.replace('Z', '+00:00'))
            return due_time.isoformat()
        except ValueError:
            # If AI response is invalid, use fallback logic
            return fallback_due_time(task_title, created_at)
            
    except Exception as e:
        print(f"AI due time setting failed: {e}")
        return fallback_due_time(task_title, created_at)

def fallback_due_time(task_title: str, created_at: str) -> Optional[str]:
    """Fallback logic for setting due times when AI fails"""
    now = datetime.now()
    title_lower = task_title.lower()
    
    # Urgent keywords
    urgent_keywords = ["urgent", "asap", "immediately", "now", "emergency"]
    if any(keyword in title_lower for keyword in urgent_keywords):
        return (now + timedelta(hours=1)).isoformat()
    
    # Call-related tasks
    if "call" in title_lower:
        return (now + timedelta(hours=2)).isoformat()
    
    # Meeting-related tasks
    if "meeting" in title_lower or "appointment" in title_lower:
        return (now + timedelta(days=1)).isoformat()
    
    # Report-related tasks
    if "report" in title_lower or "submit" in title_lower:
        return (now + timedelta(days=2)).isoformat()
    
    # Default: due in 24 hours
    return (now + timedelta(days=1)).isoformat()

# Global reminder thread
reminder_thread = None
reminder_active = False

def start_reminder_system():
    """Start the background reminder system"""
    global reminder_thread, reminder_active
    
    if reminder_active:
        return
    
    reminder_active = True
    reminder_thread = threading.Thread(target=reminder_worker, daemon=True)
    reminder_thread.start()
    print("🔔 Reminder system started!")

def stop_reminder_system():
    """Stop the background reminder system"""
    global reminder_active
    reminder_active = False
    print("🔕 Reminder system stopped!")

def reminder_worker():
    """Background worker that checks for due tasks and sends reminders"""
    global reminder_active
    
    while reminder_active:
        try:
            tasks = load_tasks()
            now = datetime.now()
            
            for task in tasks:
                if task.get("due_time"):
                    due_time = datetime.fromisoformat(task["due_time"])
                    
                    # Check if task is due (within 5 minutes)
                    if due_time <= now + timedelta(minutes=5) and due_time > now - timedelta(minutes=5):
                        send_reminder(task)
                        # Mark as reminded to avoid spam
                        task["reminded"] = True
                        save_tasks(tasks)
            
            # Sleep for 1 minute before next check
            time.sleep(60)
            
        except Exception as e:
            print(f"Reminder system error: {e}")
            time.sleep(60)

def send_reminder(task: Dict):
    """Send a reminder for a due task"""
    title = task["title"]
    due_time = datetime.fromisoformat(task["due_time"])
    
    print(f"\n🔔 REMINDER: {title}")
    print(f"⏰ Due: {due_time.strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    # Generate AI-powered reminder message
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""
        Create a friendly, motivating reminder message for this task:
        Task: "{title}"
        Due: {due_time.strftime('%Y-%m-%d %H:%M')}
        
        Make it encouraging and actionable. Keep it under 100 characters.
        """
        
        response = model.generate_content(prompt)
        reminder_message = response.text.strip()
        print(f"💬 AI Reminder: {reminder_message}")
        
    except Exception as e:
        print(f"💬 Reminder: Time to work on '{title}'!")

def ai_enhance_task(task: Dict) -> Dict:
    """Use AI to enhance task with due time and priority"""
    if not task.get("due_time"):
        print("🤖 AI is analyzing your task to set an appropriate due time...")
        ai_due_time = ai_set_due_time(task["title"], task["created_at"])
        if ai_due_time:
            task["due_time"] = ai_due_time
            print(f"✅ AI set due time: {datetime.fromisoformat(ai_due_time).strftime('%Y-%m-%d %H:%M')}")
        else:
            print("ℹ️ AI determined no due time needed for this task")
    
    return task

def load_tasks() -> List[Dict]:
    """Load tasks from JSON file"""
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_tasks(tasks: List[Dict]):
    """Save tasks to JSON file"""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def parse_due_time(text: str) -> Optional[str]:
    """Parse due time from natural language"""
    text = text.lower()
    now = datetime.now()
    
    # Tomorrow at specific time
    if "tomorrow" in text:
        tomorrow = now + timedelta(days=1)
        # Extract time
        time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm)?', text)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            period = time_match.group(3)
            
            if period == 'pm' and hour != 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
                
            due_time = tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
            return due_time.isoformat()
        else:
            # Default to 9 AM tomorrow
            due_time = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
            return due_time.isoformat()
    
    # Specific date and time
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})\s+(\d{1,2}):(\d{2})', text)
    if date_match:
        date_str = date_match.group(1)
        hour = int(date_match.group(2))
        minute = int(date_match.group(3))
        try:
            due_time = datetime.strptime(f"{date_str} {hour:02d}:{minute:02d}", "%Y-%m-%d %H:%M")
            return due_time.isoformat()
        except ValueError:
            pass
    
    # Today at specific time
    if "today" in text:
        time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm)?', text)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2)) if time_match.group(2) else 0
            period = time_match.group(3)
            
            if period == 'pm' and hour != 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
                
            due_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            return due_time.isoformat()
    
    # At specific time (today by default) - handle both "8:36 pm" and "8 36 pm" formats
    time_match = re.search(r'at\s+(\d{1,2})[: ](\d{2})\s*(am|pm)', text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2))
        period = time_match.group(3)
        
        if period == 'pm' and hour != 12:
            hour += 12
        elif period == 'am' and hour == 12:
            hour = 0
            
        due_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        return due_time.isoformat()
    
    return None

def extract_task_title(text: str) -> str:
    """Extract task title from natural language"""
    # Remove common task prefixes
    prefixes = [
        "add task", "remind me to", "remind me", "remember me to", "remember me", 
        "hey remember me to", "hey remember me", "hey remind me to", "hey remind me",
        "task:", "todo:", "i need to", "i have to", "i should", "i must"
    ]
    
    text = text.lower().strip()
    
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
            break
    
    # Remove due time information
    text = re.sub(r'\b(tomorrow|today|at \d{1,2}:\d{2}|am|pm)\b', '', text)
    text = re.sub(r'\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}', '', text)
    
    return text.strip().title()

def add_task(query: str) -> str:
    """Add a new task with AI enhancement"""
    tasks = load_tasks()
    
    # Extract task title
    title = extract_task_title(query)
    if not title:
        return "❌ Could not extract task title. Please specify what you need to do."
    
    # Parse due time from user input
    due_time = parse_due_time(query)
    
    # Create task
    task = {
        "title": title,
        "created_at": datetime.now().isoformat(),
        "due_time": due_time
    }
    
    # Use AI to enhance the task if no due time was specified
    if not due_time:
        task = ai_enhance_task(task)
    
    tasks.append(task)
    save_tasks(tasks)
    
    # Start reminder system if not already running
    start_reminder_system()
    
    # Response
    if task.get("due_time"):
        due_dt = datetime.fromisoformat(task["due_time"])
        due_str = due_dt.strftime("%Y-%m-%d %H:%M")
        return f"✅ Task added: '{title}', due at {due_str}"
    else:
        return f"✅ Task added: '{title}' (no deadline)"

def list_tasks() -> str:
    """List all tasks"""
    tasks = load_tasks()
    
    if not tasks:
        return "📝 No tasks found. Add a task to get started!"
    
    response = "📝 Your Tasks:\n"
    for i, task in enumerate(tasks, 1):
        title = task["title"]
        if task.get("due_time"):
            due_dt = datetime.fromisoformat(task["due_time"])
            due_str = due_dt.strftime("%Y-%m-%d %H:%M")
            response += f"{i}. {title} | Due: {due_str}\n"
        else:
            response += f"{i}. {title} | No deadline\n"
    
    return response.strip()

def check_due_tasks() -> str:
    """Check for tasks that are due now"""
    tasks = load_tasks()
    now = datetime.now()
    due_tasks = []
    
    for task in tasks:
        if task.get("due_time"):
            due_dt = datetime.fromisoformat(task["due_time"])
            # Check if task is due (within 5 minutes of current time)
            if due_dt <= now + timedelta(minutes=5):
                due_tasks.append(task)
    
    if not due_tasks:
        return "✅ No tasks are due right now."
    
    response = "⏰ Tasks due now:\n"
    for task in due_tasks:
        response += f"- {task['title']}\n"
    
    return response.strip()

def is_task_query(query: str) -> bool:
    """Check if query is task-related"""
    task_keywords = [
        "add task", "remind me", "remember me", "show tasks", "list tasks", 
        "check due tasks", "what tasks are due", "my tasks",
        "todo", "task:", "reminder", "remind", "remember"
    ]
    
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in task_keywords)

def handle_task_query(query: str) -> str:
    """Handle task-related queries"""
    query_lower = query.lower()
    
    if any(keyword in query_lower for keyword in ["add task", "remind me", "remember me"]):
        return add_task(query)
    elif any(keyword in query_lower for keyword in ["show tasks", "list tasks", "my tasks"]):
        return list_tasks()
    elif any(keyword in query_lower for keyword in ["check due tasks", "what tasks are due"]):
        return check_due_tasks()
    else:
        return "❓ I can help you with tasks. Try: 'add task', 'show tasks', or 'check due tasks'"
