# Query Classification Model - Inference Guide

This directory contains everything you need to run inference with your trained query classification model.

## Model Information
- **Accuracy**: 99.84%
- **Classes**: 3 (General Query, Web Query, Task Query)
- **Training Samples**: 6,244
- **Model Type**: Logistic Regression with TF-IDF

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Interactive Mode
```bash
python query_classifier_inference.py
```

### 3. Classify a Single Query
```bash
python query_classifier_inference.py "What is the weather today?"
```

### 4. Batch Processing
```bash
python query_classifier_inference.py --batch queries.txt
```

## Usage Examples

### Interactive Mode
```bash
python query_classifier_inference.py
```
Enter queries to classify. Type 'quit' to exit, 'info' for model details.

### Single Query
```bash
python query_classifier_inference.py "Search for Python tutorials"
```

### Batch Processing
Create a text file with one query per line:
```
What is machine learning?
Search for restaurants
Create a todo list
```

Then run:
```bash
python query_classifier_inference.py --batch queries.txt
```

### Save Results to File
```bash
python query_classifier_inference.py --batch queries.txt --output results.json
```

## Integration Example

```python
from query_classifier_inference import QueryClassifier

# Initialize classifier
classifier = QueryClassifier()

# Classify single query
result = classifier.classify("What is the weather?")
print(f"Class: {result['predicted_class_name']}")
print(f"Confidence: {result['confidence']}")

# Batch classification
queries = ["Query 1", "Query 2", "Query 3"]
results = classifier.classify_batch(queries)
```

## Output Format

Each classification returns:
```python
{
    'query': 'original query',
    'predicted_class': 0,  # 0, 1, or 2
    'predicted_class_name': 'General Query',
    'confidence': 0.9876,
    'probabilities': {
        'General Query': 0.9876,
        'Web Query': 0.0100,
        'Task Query': 0.0024
    }
}
```

## Class Mapping
- **0**: General Query - General questions and information requests
- **1**: Web Query - Web search related queries  
- **2**: Task Query - Task-oriented queries

## Command Line Options

```bash
python query_classifier_inference.py [OPTIONS] [QUERY]

Options:
  --batch FILE          Process queries from file (one per line)
  --model-dir DIR       Model directory (default: classifier)
  --no-probabilities    Hide probability scores
  --output FILE         Save batch results to JSON file
  --help               Show help message
```

## Files Required

Make sure these files are in the `classifier/` directory:
- `query_classifier_model.pkl` - Main model
- `vectorizer.pkl` - Text processor
- `model_info.json` - Model metadata
- `model_info.pkl` - Model info (pickle format)
- `traditional_query_classifier.pkl` - Backup model

## Error Handling

The script includes comprehensive error handling for:
- Missing model files
- Invalid queries
- File I/O errors
- Model loading errors

## Performance

- **Single Query**: ~1-5ms per query
- **Batch Processing**: Optimized for multiple queries
- **Memory Usage**: Minimal (loads models once)
