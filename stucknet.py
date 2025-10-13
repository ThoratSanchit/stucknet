#!/usr/bin/env python3
"""
🤖 STUCKNET - AI Assistant
==========================

Complete AI assistant that classifies queries and routes them to appropriate handlers:
- General Query (0) → general-query.py
- Web Query (1) → web-search.py  
- Task Query (2) → Future configuration

Author: Sanchit Thorat (Agent S)
"""

import sys
import os
from query_classifier_inference import QueryClassifier
from general_query import get_ai_answer
from web_search import fetch_live_results, summarize_results

class StuckNet:
    """
    Main AI Assistant that routes queries to appropriate handlers
    """
    
    def __init__(self):
        """Initialize StuckNet with the query classifier"""
        print("🤖 Initializing StuckNet AI Assistant...")
        try:
            self.classifier = QueryClassifier()
            print("✅ StuckNet ready!")
        except Exception as e:
            print(f"❌ Error initializing StuckNet: {e}")
            sys.exit(1)
    
    def process_query(self, query: str) -> dict:
        """
        Process a user query by classifying and routing to appropriate handler
        
        Args:
            query (str): User's query
            
        Returns:
            dict: Response with type, content, and metadata
        """
        if not query or not query.strip():
            return {
                "type": "error",
                "content": "Please provide a valid query.",
                "metadata": {}
            }
        
        # Classify the query
        classification = self.classifier.classify(query.strip())
        query_type = classification['predicted_class']
        confidence = classification['confidence']
        
        print(f"🔍 Query classified as: {classification['predicted_class_name']} (Confidence: {confidence:.2f})")
        
        # Route to appropriate handler
        if query_type == 0:  # General Query
            return self._handle_general_query(query, classification)
        elif query_type == 1:  # Web Query
            return self._handle_web_query(query, classification)
        elif query_type == 2:  # Task Query
            return self._handle_task_query(query, classification)
        else:
            return {
                "type": "error",
                "content": "Unknown query type.",
                "metadata": {"classification": classification}
            }
    
    def _handle_general_query(self, query: str, classification: dict) -> dict:
        """Handle general knowledge queries"""
        print("🧠 Processing as General Query...")
        try:
            answer = get_ai_answer(query)
            return {
                "type": "general",
                "content": answer,
                "metadata": {
                    "classification": classification,
                    "handler": "general-query.py"
                }
            }
        except Exception as e:
            return {
                "type": "error",
                "content": f"Error processing general query: {str(e)}",
                "metadata": {"classification": classification}
            }
    
    def _handle_web_query(self, query: str, classification: dict) -> dict:
        """Handle web search queries"""
        print("🌐 Processing as Web Query...")
        try:
            # Fetch live search results
            results = fetch_live_results(query, num_results=5)
            
            if not results:
                return {
                    "type": "web",
                    "content": "No search results found for your query.",
                    "metadata": {
                        "classification": classification,
                        "handler": "web-search.py",
                        "results_count": 0
                    }
                }
            
            # Generate AI summary
            summary = summarize_results(query, results)
            
            return {
                "type": "web",
                "content": summary,
                "metadata": {
                    "classification": classification,
                    "handler": "web-search.py",
                    "results_count": len(results),
                    "search_results": results
                }
            }
        except Exception as e:
            return {
                "type": "error",
                "content": f"Error processing web query: {str(e)}",
                "metadata": {"classification": classification}
            }
    
    def _handle_task_query(self, query: str, classification: dict) -> dict:
        """Handle task-oriented queries (future implementation)"""
        print("⚙️ Processing as Task Query...")
        return {
            "type": "task",
            "content": f"Task query detected: '{query}'\n\nTask handling is not yet configured. This feature will be available in future updates.",
            "metadata": {
                "classification": classification,
                "handler": "task-handler (future)",
                "status": "not_implemented"
            }
        }
    
    def interactive_mode(self):
        """Run StuckNet in interactive mode"""
        print("\n" + "="*60)
        print("🤖 STUCKNET AI ASSISTANT - INTERACTIVE MODE")
        print("="*60)
        print("👋 Hello! I'm StuckNet, created by Sanchit Thorat (Software Engineer)")
        print("Ask me anything! I'll classify your query and provide the best response.")
        print("Type 'quit', 'exit', or 'q' to stop.")
        print("Type 'info' to see detailed system information.")
        print("="*60)
        
        while True:
            try:
                query = input("\n💬 You: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Thanks for using StuckNet!")
                    break
                elif query.lower() == 'info':
                    self._show_info()
                    continue
                elif not query:
                    print("Please enter a query.")
                    continue
                
                # Process the query
                response = self.process_query(query)
                self._display_response(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using StuckNet!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def _display_response(self, response: dict):
        """Display the response in a formatted way"""
        print(f"\n🤖 StuckNet ({response['type'].upper()}):")
        print("-" * 50)
        print(response['content'])
        
        # Show metadata if available
        if response['type'] == 'web' and 'search_results' in response['metadata']:
            print(f"\n🌐 Found {response['metadata']['results_count']} search results:")
            for i, result in enumerate(response['metadata']['search_results'][:3], 1):
                print(f"  {i}. {result['title']}")
        
        print("-" * 50)
    
    def _show_info(self):
        """Show system information"""
        print(f"\n🤖 Hello! I am StuckNet, your AI Assistant!")
        print(f"   Created by: Sanchit Thorat (Agent S)")
        print(f"   Creator Role: Software Engineer")
        print(f"   My Purpose: To help you with queries by intelligently routing them")
        print(f"   to the most appropriate handler for fast and accurate responses.")
        print(f"\n📊 StuckNet System Information:")
        print(f"  • Query Classifier: {self.classifier.model_info['description']}")
        print(f"  • Model Accuracy: {self.classifier.model_info['accuracy']:.4f}")
        print(f"  • Available Classes: {', '.join(self.classifier.class_names)}")
        print(f"  • General Handler: general-query.py (for knowledge questions)")
        print(f"  • Web Handler: web-search.py (for real-time web searches)")
        print(f"  • Task Handler: Future implementation (for task-oriented queries)")
        print(f"\n💡 How I Work:")
        print(f"  1. I analyze your query using my 99.84% accurate classifier")
        print(f"  2. I route it to the best handler for your specific need")
        print(f"  3. I provide fast, accurate responses tailored to your query type")
        print(f"\n🚀 Ready to help you with any questions!")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="StuckNet AI Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python stucknet.py                           # Interactive mode
  python stucknet.py "What is machine learning?"  # Single query
        """
    )
    
    parser.add_argument(
        'query', 
        nargs='?', 
        help='Single query to process'
    )
    
    args = parser.parse_args()
    
    # Initialize StuckNet
    assistant = StuckNet()
    
    if args.query:
        # Single query mode
        if args.query.lower() == 'info':
            assistant._show_info()
        else:
            response = assistant.process_query(args.query)
            assistant._display_response(response)
    else:
        # Interactive mode
        assistant.interactive_mode()


if __name__ == "__main__":
    main()
