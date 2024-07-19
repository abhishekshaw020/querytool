import streamlit as st
from PyPDF2 import PdfReader
from duckduckgo_search import ddg

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
    try:
        results = ddg(query, max_results=3)
        if results:
            return ' '.join(result['body'] for result in results)
        else:
            return "No results found."
    except Exception as e:
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
