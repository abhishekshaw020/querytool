import streamlit as st
from PyPDF2 import PdfReader
import openai

openai.api_key = 'sk-None-OrvuMAWtcbGursdUyHXaT3BlbkFJgtjsgyIWowtQdjXzGmU4'

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

def ask_openai(question):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error querying OpenAI: {e}"

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
                        st.warning("Answer not found in PDF, querying OpenAI for further assistance...")
                        openai_result = ask_openai(question)
                        st.write(openai_result)
                else:
                    st.warning("Please enter a question to get an answer.")

if __name__ == "__main__":
    main()
