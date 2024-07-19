import streamlit as st
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PdfReader(uploaded_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ' '
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def search_internet(query):
    url = "https://api.duckduckgo.com/"
    params = {
        'q': query,
        'format': 'json',
        'pretty': 1,
        'no_redirect': 1,
        'no_html': 1,
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'AbstractText' in data and data['AbstractText']:
                return data['AbstractText']
            elif 'RelatedTopics' in data and data['RelatedTopics']:
                return ' '.join(topic['Text'] for topic in data['RelatedTopics'][:3])
            else:
                return "No results found."
        else:
            return f"Failed to retrieve results. Status code: {response.status_code}"
    except requests.exceptions.Timeout:
        return "Error during web search: Timeout occurred."
    except requests.exceptions.RequestException as e:
        return f"Error during web search: {e}"

def main():
    st.title("Query Tool by Aingenious")
    
    uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        if text:
            st.text_area("Extracted Text", text, height=250)
            
            question = st.text_input("Ask a question:")
            if st.button("Answer Question"):
                if question:
                    # Simple text search in PDF
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
