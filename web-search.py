import requests
import google.generativeai as genai

# -------------------------------
# 🔑 Configure Gemini AI
# -------------------------------
GEMINI_API_KEY = "AIzaSyCmXJhLlnIShrui2gM5zJVvvnSBv7bnl4w"  # Replace with your Gemini key
genai.configure(api_key=GEMINI_API_KEY)

# -------------------------------
# 🔑 SerpAPI Key
# -------------------------------
SERPAPI_KEY = "fd85e2fdb7b0be584be00033c7af6b81a1635a0b3288352ba74f4d359e382b83"  # Replace with your SerpAPI key

# -------------------------------
# 🌐 Function: Fetch Live Search Results
# -------------------------------
def fetch_live_results(query, num_results=5):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": num_results
    }

    response = requests.get(url, params=params).json()
    results = []

    for r in response.get("organic_results", []):
        results.append({
            "title": r.get("title"),
            "snippet": r.get("snippet"),
            "link": r.get("link")
        })

    return results

# -------------------------------
# 🧠 Function: Summarize with Gemini
# -------------------------------
def summarize_results(query, results):
    model = genai.GenerativeModel("gemini-2.5-flash")
    formatted_results = ""
    for i, r in enumerate(results, 1):
        formatted_results += f"{i}. {r['title']}\n{r['snippet']}\nURL: {r['link']}\n\n"

    prompt = f"""
    You are a helpful AI assistant.
    Based on the following web search results for "{query}", create a concise, factual summary.
    Include main insights, trends, and key information.

    Search Results:
    {formatted_results}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error during summarization: {str(e)}"

# -------------------------------
# 🚀 Main Function
# -------------------------------
if __name__ == "__main__":
    query = input("💬 What do you want to search for? ")

    print(f"\n🔍 Fetching live Google search results for: {query}\n")
    results = fetch_live_results(query, num_results=5)

    if not results:
        print("⚠️ No results found.")
    else:
        print("🌐 Top Results:")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['title']} ({r['link']})")

        print("\n🧠 Generating AI summary...\n")
        summary = summarize_results(query, results)
        print("📝 Summary:\n")
        print(summary)
