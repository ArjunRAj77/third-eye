import streamlit as st
import spacy
import spacy_streamlit
import random
from io import StringIO

# Load spaCy model for NER (using small English model)
nlp = spacy.load("en_core_web_sm")

# Define random color generator for highlighting
def random_color():
    colors = ["#FFA07A", "#7FFFD4", "#FF69B4", "#98FB98", "#FFD700", "#ADD8E6"]
    return random.choice(colors)

# Streamlit App
def main():
    # Main heading with emojis and description
    st.title("👁️ **Third-Eye**: Your Automated Answer Key Verifier 🔍")
    st.write("""
    Welcome to **Third-Eye**, an intelligent application that helps you analyze 
    your answer sheets by comparing them with the answer key using 
    **Named Entity Recognition (NER)**. Upload your answer key and answer sheet, 
    and let the **Third-Eye** spot the key elements! 🎯
    """)

    # Sidebar for file uploads
    st.sidebar.header("📂 Upload Your Files")
    answer_key_file = st.sidebar.file_uploader("Upload Answer Key 📑", type=["txt"])
    answer_sheet_file = st.sidebar.file_uploader("Upload Answer Sheet 📝", type=["txt"])

    # Initialize the run button only when files are uploaded
    if answer_key_file and answer_sheet_file:
        # Read uploaded files
        answer_key = read_file(answer_key_file)
        answer_sheet = read_file(answer_sheet_file)

        # Display uploaded content with emojis
        st.subheader("📜 **Answer Key**:")
        st.write(answer_key)

        st.subheader("📋 **Answer Sheet**:")
        st.write(answer_sheet)

        # Add the "Run" button
        if st.button("Analyse 🔍"):
            # Process Answer Key using NER
            st.subheader("🔑 **Extracted Key Elements from Answer Key:**")
            doc_key = nlp(answer_key)
            spacy_streamlit.visualize_ner(doc_key, labels=nlp.get_pipe("ner").labels)

            # Highlight the key elements in the answer sheet
            st.subheader("🖍️ **Highlighted Answer Sheet:**")
            highlighted_answer_sheet = highlight_entities(answer_sheet, doc_key)
            st.markdown(highlighted_answer_sheet, unsafe_allow_html=True)

def read_file(uploaded_file):
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    return stringio.read()

# Function to highlight entities in the answer sheet
def highlight_entities(answer_sheet, doc_key):
    """
    Function to highlight key entities in the answer sheet text, 
    preserving the original format with spacing and line breaks.
    """
    doc_sheet = nlp(answer_sheet)  # Process the answer sheet using spaCy
    highlighted_text = ""  # We'll build the highlighted text here

    # Loop through each token in the answer sheet
    for token in doc_sheet:
        found_match = False
        for ent in doc_key.ents:
            # If the token matches an entity in the answer key
            if token.text == ent.text:
                color = random_color()  # Generate random color for the entity
                highlighted_text += f'<mark style="background-color: {color};">{token.text}</mark>{token.whitespace_}'
                found_match = True
                break
        if not found_match:
            # Preserve the original token and whitespace if no match is found
            highlighted_text += token.text + token.whitespace_

    # Replace newlines (\n) with HTML line breaks (<br>) to preserve line spacing
    highlighted_text = highlighted_text.replace("\n", "<br>")

    # Return the highlighted text wrapped in <pre> to preserve original formatting
    return f"<pre>{highlighted_text}</pre>"

if __name__ == "__main__":
    main()
