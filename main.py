#!/usr/bin/env python3
"""
🤖 STUCKNET - AI Assistant
==========================

Main entry point for StuckNet AI Assistant
Created by: Sanchit Thorat (Software Engineer)

Usage:
    python main.py                    # Interactive mode
    python main.py "your query here"  # Single query
    python main.py --info             # Show system info
"""

import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from stucknet import StuckNet

def main():
    """Main entry point for StuckNet"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="StuckNet AI Assistant - Intelligent Query Router",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Interactive mode
  python main.py "What is machine learning?"  # Single query
  python main.py --info                    # Show system information
        """
    )
    
    parser.add_argument(
        'query', 
        nargs='?', 
        help='Single query to process'
    )
    parser.add_argument(
        '--info', 
        action='store_true',
        help='Show system information'
    )
    
    args = parser.parse_args()
    
    # Initialize StuckNet
    assistant = StuckNet()
    
    if args.info:
        # Show system info
        assistant._show_info()
    elif args.query:
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
