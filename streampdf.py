import streamlit as st
from PyPDF2 import PdfReader
import requests

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
    api_key = 'b0aa738ca511dad054f104718ad1df75550db7551970eace9a852d3f1cfbf13a'
    url = "https://serpapi.com/search"
    params = {
        'q': query,
        'engine': 'duckduckgo',
        'api_key': api_key,
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'organic_results' in data and data['organic_results']:
                return ' '.join(result['snippet'] for result in data['organic_results'][:3] if 'snippet' in result)
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
