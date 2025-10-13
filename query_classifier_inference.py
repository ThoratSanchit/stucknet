#!/usr/bin/env python3
"""
Query Classification Model Inference Script
==========================================

A complete inference script for the trained query classification model.
Supports single query classification, batch processing, and interactive mode.

Model Details:
- 3 classes: General Query (0), Web Query (1), Task Query (2)
- 99.84% test accuracy
- Logistic Regression with TF-IDF vectorization
- Trained on 6,244 samples

Usage:
    python query_classifier_inference.py                    # Interactive mode
    python query_classifier_inference.py "your query here"  # Single query
    python query_classifier_inference.py --batch file.txt   # Batch processing
"""

import os
import sys
import json
import argparse
from typing import List, Dict
import numpy as np
from joblib import load


class QueryClassifier:
    """
    Query Classification Model for inference.
    """
    
    def __init__(self, model_dir: str = "classifier"):
        """
        Initialize the query classifier.
        
        Args:
            model_dir (str): Directory containing model files
        """
        self.model_dir = model_dir
        self.model = None
        self.vectorizer = None
        self.model_info = None
        self.class_names = None
        
        # Load all model components
        self._load_models()
    
    def _load_models(self):
        """Load all model files and validate their presence."""
        required_files = {
            'model': 'query_classifier_model.pkl',
            'vectorizer': 'vectorizer.pkl',
            'info': 'model_info.json'
        }
        
        # Check if all required files exist
        missing_files = []
        for name, filename in required_files.items():
            filepath = os.path.join(self.model_dir, filename)
            if not os.path.exists(filepath):
                missing_files.append(filepath)
        
        if missing_files:
            raise FileNotFoundError(
                f"Missing required model files: {', '.join(missing_files)}\n"
                f"Please ensure all model files are in the '{self.model_dir}' directory."
            )
        
        try:
            # Create a simple TraditionalQueryClassifier class
            class TraditionalQueryClassifier:
                def __init__(self, *args, **kwargs):
                    pass
            
            # Add it to the main module
            sys.modules['__main__'].TraditionalQueryClassifier = TraditionalQueryClassifier
            
            # Load the main model
            model_path = os.path.join(self.model_dir, 'query_classifier_model.pkl')
            model_wrapper = load(model_path)
            
            # Extract the actual model from the wrapper
            if hasattr(model_wrapper, 'model'):
                self.model = model_wrapper.model
                print(f"✓ Loaded model from {model_path}")
            else:
                self.model = model_wrapper
                print(f"✓ Loaded model from {model_path}")
            
            # Load the vectorizer
            vectorizer_path = os.path.join(self.model_dir, 'vectorizer.pkl')
            self.vectorizer = load(vectorizer_path)
            print(f"✓ Loaded vectorizer from {vectorizer_path}")
            
            # Load model info
            info_path = os.path.join(self.model_dir, 'model_info.json')
            with open(info_path, 'r') as f:
                self.model_info = json.load(f)
            
            self.class_names = self.model_info['class_names']
            
            print(f"✓ Loaded model info: {self.model_info['description']}")
            print(f"✓ Model accuracy: {self.model_info['accuracy']:.4f}")
            print(f"✓ Classes: {', '.join(self.class_names)}")
            
        except Exception as e:
            raise RuntimeError(f"Error loading model files: {str(e)}")
    
    def classify(self, query: str) -> Dict:
        """
        Classify a single query.
        
        Args:
            query (str): The query to classify
            
        Returns:
            Dict: Classification result with class, confidence, and probabilities
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
        
        # Vectorize the query
        query_vector = self.vectorizer.transform([query.strip()])
        
        # Get prediction and probabilities
        prediction = self.model.predict(query_vector)[0]
        probabilities = self.model.predict_proba(query_vector)[0]
        
        # Get confidence (max probability)
        confidence = float(np.max(probabilities))
        
        # Create result dictionary
        result = {
            'query': query.strip(),
            'predicted_class': int(prediction),
            'predicted_class_name': self.class_names[prediction],
            'confidence': confidence,
            'probabilities': {
                self.class_names[i]: float(prob) 
                for i, prob in enumerate(probabilities)
            }
        }
        
        return result
    
    def classify_batch(self, queries: List[str]) -> List[Dict]:
        """
        Classify multiple queries in batch.
        
        Args:
            queries (List[str]): List of queries to classify
            
        Returns:
            List[Dict]: List of classification results
        """
        if not queries:
            raise ValueError("Queries list cannot be empty")
        
        # Filter out empty queries
        valid_queries = [q.strip() for q in queries if q and q.strip()]
        if not valid_queries:
            raise ValueError("No valid queries provided")
        
        # Vectorize all queries at once
        query_vectors = self.vectorizer.transform(valid_queries)
        
        # Get predictions and probabilities
        predictions = self.model.predict(query_vectors)
        probabilities = self.model.predict_proba(query_vectors)
        
        # Create results
        results = []
        for i, (query, pred, probs) in enumerate(zip(valid_queries, predictions, probabilities)):
            confidence = float(np.max(probs))
            
            result = {
                'query': query,
                'predicted_class': int(pred),
                'predicted_class_name': self.class_names[pred],
                'confidence': confidence,
                'probabilities': {
                    self.class_names[j]: float(prob) 
                    for j, prob in enumerate(probs)
                }
            }
            results.append(result)
        
        return results


def print_classification_result(result: Dict, show_probabilities: bool = True):
    """Print a single classification result in a formatted way."""
    print(f"\n{'='*60}")
    print(f"Query: {result['query']}")
    print(f"Predicted Class: {result['predicted_class_name']} (Class {result['predicted_class']})")
    print(f"Confidence: {result['confidence']:.4f} ({result['confidence']*100:.2f}%)")
    
    if show_probabilities:
        print("\nClass Probabilities:")
        for class_name, prob in result['probabilities'].items():
            print(f"  {class_name}: {prob:.4f} ({prob*100:.2f}%)")
    print(f"{'='*60}")


def interactive_mode(classifier: QueryClassifier):
    """Run the classifier in interactive mode."""
    print("\n" + "="*60)
    print("QUERY CLASSIFIER - INTERACTIVE MODE")
    print("="*60)
    print("Enter queries to classify. Type 'quit', 'exit', or 'q' to stop.")
    print("Type 'info' to see model information.")
    print("="*60)
    
    while True:
        try:
            query = input("\nEnter query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            elif query.lower() == 'info':
                print(f"\nModel Information:")
                print(f"  Type: {classifier.model_info.get('model_type', 'unknown')}")
                print(f"  Accuracy: {classifier.model_info.get('accuracy', 0.0):.4f}")
                print(f"  Training Samples: {classifier.model_info.get('training_samples', 0)}")
                print(f"  Description: {classifier.model_info.get('description', '')}")
                print(f"  Classes: {', '.join(classifier.class_names)}")
                continue
            elif not query:
                print("Please enter a query.")
                continue
            
            # Classify the query
            result = classifier.classify(query)
            print_classification_result(result)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


def main():
    """Main function to handle command line arguments and run the classifier."""
    parser = argparse.ArgumentParser(
        description="Query Classification Model Inference",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python query_classifier_inference.py
  python query_classifier_inference.py "What is the weather today?"
  python query_classifier_inference.py --batch queries.txt
        """
    )
    
    parser.add_argument(
        'query', 
        nargs='?', 
        help='Single query to classify'
    )
    parser.add_argument(
        '--batch', 
        type=str, 
        help='File containing queries to classify (one per line)'
    )
    parser.add_argument(
        '--model-dir', 
        type=str, 
        default='classifier',
        help='Directory containing model files (default: classifier)'
    )
    parser.add_argument(
        '--no-probabilities', 
        action='store_true',
        help='Hide probability scores in output'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize classifier
        print("Loading Query Classification Model...")
        classifier = QueryClassifier(model_dir=args.model_dir)
        print("Model loaded successfully!\n")
        
        # Handle different modes
        if args.batch:
            # Batch processing mode
            if not os.path.exists(args.batch):
                print(f"Error: Batch file '{args.batch}' not found.")
                sys.exit(1)
            
            with open(args.batch, 'r', encoding='utf-8') as f:
                queries = [line.strip() for line in f if line.strip()]
            
            if not queries:
                print("Error: No valid queries found in batch file.")
                sys.exit(1)
            
            print(f"Processing {len(queries)} queries...")
            results = classifier.classify_batch(queries)
            
            # Print results
            for i, result in enumerate(results, 1):
                print(f"\n[{i}/{len(results)}]")
                print_classification_result(result, not args.no_probabilities)
        
        elif args.query:
            # Single query mode
            result = classifier.classify(args.query)
            print_classification_result(result, not args.no_probabilities)
        
        else:
            # Interactive mode
            interactive_mode(classifier)
    
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
