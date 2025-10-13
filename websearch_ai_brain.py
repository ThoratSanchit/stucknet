from googleapiclient.discovery import build
import os
import google.generativeai as genai

# ----------------------------
# Google Custom Search Setup
# ----------------------------
# Your OAuth2 credentials (for reference)
OAUTH2_CREDENTIALS = {
    "web": {
        "client_id": "730337567359-m4vmnubvhtdnc65mv15ogkfi323b4ihc.apps.googleusercontent.com",
        "project_id": "ai-email-agent-461405",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": ["http://localhost:3000/"]
    }
}

# API Key for Google Custom Search (Custom Search API uses API keys, not OAuth2)
GOOGLE_API_KEY = "AIzaSyDIKUhle3oJayp-_6TzdBvZQfK9zF_fkcY"
CSE_ID = "d172dde743acc48e1"  # replace with your CSE ID

def google_search(query, num_results=5):
    """Return top search results from Google Custom Search API"""
    try:
        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        results = service.cse().list(q=query, cx=CSE_ID, num=num_results).execute()
        return results.get("items", [])
    except Exception as e:
        print(f"Error in Google Search: {str(e)}")
        print("\nTo fix this error:")
        print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
        print("2. Select project: ai-email-agent-461405")
        print("3. Enable 'Custom Search API'")
        print("4. Wait a few minutes for the API to propagate")
        return []

# ----------------------------
# Gemini AI Summarization Setup
# ----------------------------
GEMINI_API_KEY = "AIzaSyB8QqJqJqJqJqJqJqJqJqJqJqJqJqJqJq"  # replace with your key


def setup_gemini():
    """Initialize Gemini AI client"""
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel('gemini-pro')

def summarize_search_results(query, search_results):
    """Use Gemini AI to summarize search results"""
    model = setup_gemini()
    
    # Format search results for summarization
    results_text = ""
    for i, result in enumerate(search_results, 1):
        results_text += f"{i}. {result.get('title', 'No title')}\n"
        results_text += f"   {result.get('snippet', 'No snippet')}\n"
        results_text += f"   URL: {result.get('link', 'No URL')}\n\n"
    
    prompt = f"""
    Based on the following search results for the query "{query}", provide a comprehensive summary:
    
    {results_text}
    
    Please provide:
    1. A brief overview of what was found
    2. Key points from the results
    3. Any relevant insights or conclusions
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {str(e)}"

# ----------------------------
# Main Web Search Brain Function
# ----------------------------
def web_search_brain(query, num_results=5):
    """
    Main function that performs web search and AI summarization
    
    Args:
        query (str): The search query
        num_results (int): Number of search results to fetch
    
    Returns:
        dict: Contains search results and AI summary
    """
    try:
        # Perform Google search
        print(f"Searching for: {query}")
        search_results = google_search(query, num_results)
        
        if not search_results:
            return {
                "query": query,
                "search_results": [],
                "summary": "No search results found for this query.",
                "status": "no_results"
            }
        
        # Generate AI summary
        print("Generating AI summary...")
        summary = summarize_search_results(query, search_results)
        
        return {
            "query": query,
            "search_results": search_results,
            "summary": summary,
            "status": "success"
        }
        
    except Exception as e:
        return {
            "query": query,
            "search_results": [],
            "summary": f"Error processing search: {str(e)}",
            "status": "error"
        }

# ----------------------------
# Example Usage
# ----------------------------
if __name__ == "__main__":
    # Example query
    test_query = "latest developments in artificial intelligence"
    
    # Perform web search with AI summarization
    result = web_search_brain(test_query)
    
    print(f"\nQuery: {result['query']}")
    print(f"Status: {result['status']}")
    print(f"\nSummary:\n{result['summary']}")
    
    if result['search_results']:
        print(f"\nFound {len(result['search_results'])} results:")
        for i, item in enumerate(result['search_results'], 1):
            print(f"{i}. {item.get('title', 'No title')}")
            print(f"   {item.get('link', 'No URL')}")
