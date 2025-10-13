import google.generativeai as genai

# -------------------------------
# 🔑 Configure Gemini AI
# -------------------------------
GEMINI_API_KEY = "AIzaSyCmXJhLlnIShrui2gM5zJVvvnSBv7bnl4w"  # Replace with your Gemini key
genai.configure(api_key=GEMINI_API_KEY)

# -------------------------------
# 🧠 Function: Get AI answer directly
# -------------------------------
def get_ai_answer(question):
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are a helpful AI assistant.
Answer the following question concisely and factually:

Question: {question}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error generating answer: {str(e)}"

# -------------------------------
# 🚀 Main: Ask question from console
# -------------------------------
if __name__ == "__main__":
    while True:
        question = input("💬 Ask your question (or type 'exit' to quit): ")
        if question.lower() == "exit":
            break

        answer = get_ai_answer(question)
        print("\n📝 AI Answer:\n")
        print(answer)
        print("\n" + "-"*50 + "\n")
