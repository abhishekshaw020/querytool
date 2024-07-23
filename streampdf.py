import streamlit as st
from PyPDF2 import PdfReader
import openai

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

def answer_question_with_openai(question, context, api_key):
    openai.api_key = api_key

    prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        return f"Error with OpenAI API: {e}"

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
                        st.warning("Answer not found in PDF, generating a response using OpenAI...")
                        api_key = "sk-None-OrvuMAWtcbGursdUyHXaT3BlbkFJgtjsgyIWowtQdjXzGmU4"  # Replace with your actual OpenAI API key
                        result = answer_question_with_openai(question, text, api_key)
                        st.write(result)
                else:
                    st.warning("Please enter a question to get an answer.")

if __name__ == "__main__":
    main()
