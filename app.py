__import__('pysqlite3')
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
import re
import streamlit as st
import wikipedia
import openai
from langchain_groq import ChatGroq

# Set your OpenAI API Key
openai.api_key = "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"

# Define chatbot logic
def rule_based_chatbot(user_input):
    """
    Responds to user input using:
    - Rule-based responses
    - Wikipedia search for general knowledge
    - OpenAI GPT fallback for broader coverage
    """
    # Rule-based responses for specific queries
    responses = {
        r"hi|hello|hey": "Hello! How can I assist you today?",
        r"how are you": "I'm here to assist you! How can I help?",
        r"what is your name": "I'm a chatbot created to assist you.",
        r"what can you do": "I can answer almost any question you ask!",
        r"who created you": "I was created as a project demonstration.",
        r"bye|exit|quit": "Goodbye! Have a wonderful day!",
        r"tell me a joke": "Why did the chicken join a band? Because it had the drumsticks!",
    }

    # Match user input to predefined patterns
    for pattern, response in responses.items():
        if re.search(pattern, user_input, re.IGNORECASE):
            return response

    # Search for the answer on Wikipedia
    try:
        search_results = wikipedia.search(user_input, results=1)
        if search_results:
            summary = wikipedia.summary(search_results[0], sentences=2)
            return f"Here's what I found on Wikipedia:\n{summary}"
    except Exception as e:
        st.warning("Wikipedia search failed. Trying another method...")

    # Fallback to OpenAI GPT for broader questions
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
        )
        return completion["choices"][0]["message"]["content"]
    except Exception as e:
        return "I'm sorry, I couldn't find an answer. Could you rephrase or ask something else?"

# Streamlit UI
st.title("Rule-Based Chatbot by Ruhi")
st.write("Ask me anything, and I'll do my best to answer using rule-based logic, Wikipedia, and GPT!")

# User input
user_input = st.text_input("Enter your question:")
if user_input:
    response = rule_based_chatbot(user_input)
    st.write(f"**Chatbot:** {response}")

# Footer
st.sidebar.header("About the Chatbot")
st.sidebar.write("""
This chatbot can:
- Answer specific predefined questions using rules.
- Fetch general knowledge from Wikipedia.
- Use GPT for broader queries.
""")
