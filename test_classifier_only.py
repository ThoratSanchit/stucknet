#!/usr/bin/env python3
"""
Test the query classifier without web search dependencies
"""

from query_classifier_inference import QueryClassifier

def test_classifier():
    """Test the query classifier with various queries"""
    print("Testing Query Classifier...")
    
    # Initialize classifier
    classifier = QueryClassifier()
    
    # Test queries
    test_queries = [
        "What is the weather today?",
        "Search for Python tutorials online", 
        "Create a todo list for my project",
        "How do I install pip?",
        "Find restaurants near me",
        "Schedule a meeting for tomorrow",
        "What is machine learning?",
        "Google search for AI news",
        "Add item to shopping list"
    ]
    
    print(f"\n{'='*80}")
    print("QUERY CLASSIFICATION RESULTS")
    print(f"{'='*80}")
    
    for i, query in enumerate(test_queries, 1):
        result = classifier.classify(query)
        
        # Determine action based on classification
        if result['predicted_class'] == 0:  # General Query
            action = "🤔 Handle with general knowledge"
        elif result['predicted_class'] == 1:  # Web Query  
            action = "🔍 Use websearch_ai_brain.py for web search"
        elif result['predicted_class'] == 2:  # Task Query
            action = "✅ Handle with task-specific response"
        
        print(f"\n{i}. Query: {query}")
        print(f"   Class: {result['predicted_class_name']} (Confidence: {result['confidence']:.3f})")
        print(f"   Action: {action}")
    
    print(f"\n{'='*80}")
    print("SYSTEM READY!")
    print("• General Queries (Class 0) → Handle with general responses")
    print("• Web Queries (Class 1) → Use websearch_ai_brain.py (after enabling APIs)")
    print("• Task Queries (Class 2) → Handle with task-specific responses")
    print(f"{'='*80}")

if __name__ == "__main__":
    test_classifier()
