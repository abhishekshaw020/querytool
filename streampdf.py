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
    url = "https://html.duckduckgo.com/html/"
    params = {'q': query}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            st.write("HTML content fetched successfully.")  # Debugging line to check HTML content
            snippets = soup.find_all('a', class_='result__snippet')
            if snippets:
                return ' '.join(snippet.get_text() for snippet in snippets[:3])  # return the first 3 results
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
