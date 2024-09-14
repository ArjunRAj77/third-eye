import streamlit as st
import spacy
import spacy_streamlit
from io import StringIO

# Load spaCy model for NER (using small English model)
nlp = spacy.load("en_core_web_sm")

# Streamlit App
def main():
    st.title("Answer Key Highlighter using NER")
    
    # File upload for Answer Key
    st.sidebar.header("Upload Files")
    answer_key_file = st.sidebar.file_uploader("Upload Answer Key", type=["txt"])
    answer_sheet_file = st.sidebar.file_uploader("Upload Answer Sheet", type=["txt"])
    
    if answer_key_file and answer_sheet_file:
        # Read uploaded files
        answer_key = read_file(answer_key_file)
        answer_sheet = read_file(answer_sheet_file)

        # Show the uploaded content
        st.subheader("Answer Key:")
        st.write(answer_key)

        st.subheader("Answer Sheet:")
        st.write(answer_sheet)

        # Process Answer Key using NER
        st.subheader("Extracted Key Elements from Answer Key:")
        doc_key = nlp(answer_key)
        spacy_streamlit.visualize_ner(doc_key, labels=nlp.get_pipe("ner").labels)

        # Highlight the key elements in the answer sheet
        st.subheader("Highlighted Answer Sheet:")
        highlighted_answer_sheet = highlight_entities(answer_sheet, doc_key)
        st.markdown(highlighted_answer_sheet, unsafe_allow_html=True)

def read_file(uploaded_file):
    # Reading file as string content
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    return stringio.read()

def highlight_entities(answer_sheet, doc_key):
    """
    Function to highlight key entities in the answer sheet text.
    """
    doc_sheet = nlp(answer_sheet)
    highlighted_text = answer_sheet

    # Extract entities from the answer key and highlight them in the answer sheet
    for ent in doc_key.ents:
        # Use HTML mark tags to highlight the key entities
        highlighted_text = highlighted_text.replace(ent.text, f'<mark>{ent.text}</mark>')

    return highlighted_text

if __name__ == "__main__":
    main()
