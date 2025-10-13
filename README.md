# 🤖 StuckNet - AI Assistant

**Created by: Sanchit Thorat (Software Engineer)**

An intelligent AI assistant that classifies queries and routes them to appropriate handlers for fast, accurate responses.

## 🚀 Features

- **99.84% Accurate Query Classification** - Routes queries intelligently
- **Human-like Greeting Responses** - Natural conversation starters
- **Real-time Web Search** - DuckDuckGo integration with AI summarization
- **General Knowledge** - Gemini AI for knowledge questions
- **Fast Response Time** - Optimized for speed
- **Interactive & Command-line Modes** - Flexible usage options

## 📁 Project Structure

```
jarvice/
├── main.py                    # Main entry point
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── src/                      # Core source code
│   ├── stucknet.py          # Main AI assistant
│   └── query_classifier_inference.py  # Query classifier
├── handlers/                 # Query handlers
│   ├── general_query.py     # General knowledge handler
│   └── web_search.py        # Web search handler
├── classifier/              # Trained model files
│   ├── query_classifier_model.pkl
│   ├── vectorizer.pkl
│   └── model_info.json
├── dataset/                 # Training data
│   └── query_dataset.csv
└── docs/                    # Documentation
    └── README_inference.md
```

## 🛠️ Installation

1. **Clone the repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Interactive Mode
```bash
python main.py
```

### Single Query
```bash
python main.py "What is machine learning?"
python main.py "Search for latest AI news"
python main.py "hello"
```

### System Information
```bash
python main.py --info
```

## 🎯 How It Works

1. **Query Classification** - 99.84% accurate ML model classifies queries into:
   - **General Query (0)** → Knowledge questions → `general_query.py`
   - **Web Query (1)** → Search requests → `web_search.py`
   - **Task Query (2)** → Task-oriented → Future implementation

2. **Smart Routing** - Queries are routed to the most appropriate handler

3. **Fast Response** - Optimized for speed with intelligent caching

## 🔧 Query Types

### General Queries
- "What is machine learning?"
- "How does photosynthesis work?"
- "Explain quantum computing"

### Web Queries
- "Search for latest AI news"
- "Find restaurants near me"
- "What's the weather today?"

### Greetings (Special Handling)
- "Hello"
- "Hi StuckNet"
- "Hey bro"

## 📊 Model Information

- **Accuracy**: 99.84%
- **Training Samples**: 6,244
- **Model Type**: Logistic Regression with TF-IDF
- **Classes**: 3 (General, Web, Task)

## 🛠️ Development

### Adding New Handlers
1. Create handler in `handlers/` directory
2. Update `stucknet.py` to include new handler
3. Add routing logic in `process_query()` method

### Training New Models
1. Update training data in `dataset/`
2. Retrain classifier
3. Update model files in `classifier/`

## 📝 API Reference

### StuckNet Class
- `process_query(query)` - Process a single query
- `interactive_mode()` - Start interactive chat
- `_show_info()` - Display system information

### Handlers
- `general_query.py` - General knowledge responses
- `web_search.py` - Web search and summarization

## 🤝 Contributing

Created by Sanchit Thorat (Agent S) - Software Engineer

## 📄 License

Private Project - All Rights Reserved

---

**StuckNet - Your Intelligent AI Assistant** 🤖
