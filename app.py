import streamlit as st #for frontend building framework
#import openai #using open AI API
import PyPDF2 #For reading the PDF
from langdetect import detect #Langdect to detect the language
from googletrans import Translator #using the google translate to translate the detected language to English

# Set your OpenAI API Key
#openai.api_key = "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"  # Replace with your OpenAI API key


# Function to detect language and translate the document
def detect_language_and_translate(doc_text):
    if not doc_text.strip():
        st.error("The document is empty. Please upload a valid document.") #Detecting wether the document is empty or not.
        return ""

    # Detect the language
    try:
        detected_lang = detect(doc_text)
        st.write(f"Detected Language: {detected_lang}") #Giving the output for the the language detected and making it as the output.
    except Exception as e:
        st.error(f"Error detecting language: {e}") #Returnig the error if the model is failed to detect the language
        return ""

    # Translate text to English
    translator = Translator()
    try:
        translation = translator.translate(doc_text, src=detected_lang, dest='ru')
        return translation.text
    except Exception as e:
        st.error(f"Error during translation: {e}")
        return ""


# Function to use OpenAI's GPT-3.5 model for answering questions based on document text
# def answer_question_with_openai(doc_text, question):
#     try:
#         # Send the document text and question to OpenAI's API
#         response = openai.Completion.create(
#             model="gpt-3.5-turbo",  # Use "gpt-3.5-turbo" instead of "gpt-4"
#             prompt=f"Answer the following question based on the document:\n\nDocument: {doc_text}\n\nQuestion: {question}\nAnswer:",
#             max_tokens=200,
#             temperature=0.7
#         )
#         return response['choices'][0]['text'].strip()
#     except Exception as e:
#         st.error(f"Error during OpenAI API call: {e}")
#         return "Sorry, I couldn't fetch an answer at this moment."


# Streamlit app
def main():
    st.title('Document Translator')

    # Upload document
    uploaded_file = st.file_uploader("Choose a document", type=["txt", "pdf"])

    if uploaded_file is not None:
        # Read the document based on its file type
        if uploaded_file.type == "text/plain":
            doc_text = uploaded_file.getvalue().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            doc_text = ""
            for page in reader.pages:
                doc_text += page.extract_text()

        # Display document content
        st.subheader("Document Content:")
        st.write(doc_text)

        # Detect language and translate to English
        if doc_text:
            translated_text = detect_language_and_translate(doc_text)
            if translated_text:
                st.subheader("Translated to English:")
                st.write(translated_text)

                # # Ask user for a question
                # question = st.text_input("Ask a question about the document:")
                #
                # if question:
                #     # Get the answer from OpenAI
                #     answer = answer_question_with_openai(translated_text, question)
                #     st.subheader("Answer:")
                #     st.write(answer)


if __name__ == '__main__':
    main()
