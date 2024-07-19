import streamlit as st
from PyPDF2 import PdfReader
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime

def load_history():
    """Load the history of uploaded PDFs from a JSON file."""
    try:
        with open('history.json', 'r') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    return history

def save_history(history):
    """Save the history of uploaded PDFs to a JSON file."""
    with open('history.json', 'w') as f:
        json.dump(history, f)

def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file."""
    try:
        pdf_file = BytesIO(uploaded_file.getvalue())
        reader = PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ' '  # Append space if no text is extracted
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def search_internet(query):
    """Performs a web search and returns the top results."""
    url = "https://html.duckduckgo.com/html/"
    params = {'q': query}
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        while response.status_code == 202:
            time.sleep(10)  # Wait for 10 seconds before retrying
            response = requests.get(url, params=params, headers=headers)  # Retry the request
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            snippets = soup.find_all('a', class_='result__snippet')
            if snippets:
                return ' '.join(snippet.get_text() for snippet in snippets[:3])
            else:
                return "No relevant results found."
        else:
            return f"Failed to retrieve results. Status code: {response.status_code}"
    except Exception as e:
        return f"Error during web search: {e}"

def main():
    """Main function to run the Streamlit app."""
    st.title("PDF Reader and Query Tool")
    
    # Sidebar for uploading history
    st.sidebar.title("Upload History")
    history = load_history()
    if history:
        for item in history:
            st.sidebar.markdown(f"* {item['filename']} on {item['date']}")
    else:
        st.sidebar.write("No uploads yet.")
    
    uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")
    if uploaded_file is not None:
        filename = uploaded_file.name
        date_uploaded = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = extract_text_from_pdf(uploaded_file)
        
        # Update history
        history.append({'filename': filename, 'date': date_uploaded})
        save_history(history)
        
        if text:
            st.text_area("Extracted Text", text, height=250)
            question = st.text_input("Ask a question about the PDF content:")
            if st.button("Answer Question"):
                if question:
                    if question.lower() in text.lower():
                        st.success("Answer found in PDF.")
                        st.write(question)  # Simplified response for demonstration
                    else:
                        st.warning("Answer not found in PDF, searching on the internet...")
                        result = search_internet(question)
                        st.write(result)
                else:
                    st.warning("Please enter a question to get an answer.")

if __name__ == "__main__":
    main()
