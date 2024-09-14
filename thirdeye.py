import streamlit as st
import spacy
import random
from io import StringIO
from spacy.pipeline import EntityRuler

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# Add custom entity patterns based on the extracted key phrases from answer key
def add_custom_entities(nlp, answer_key_dict):
    # Create an EntityRuler and add patterns
    if "entity_ruler" in nlp.pipe_names:
        nlp.remove_pipe("entity_ruler")
    
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    
    patterns = []
    for question_num, answer in answer_key_dict.items():
        key_phrases = extract_key_phrases(answer)
        unique_phrases = list(set(key_phrases))
        for phrase in unique_phrases:
            patterns.append({
                "label": "ANSWER",
                "pattern": phrase
            })
    
    ruler.add_patterns(patterns)

# Function to manually extract key phrases (e.g., important nouns, names, dates)
def extract_key_phrases(answer):
    """
    This function extracts key phrases from the answer text.
    """
    doc = nlp(answer)
    key_phrases = []
    
    # Collect named entities (like PERSON, GPE, ORG)
    for ent in doc.ents:
        key_phrases.append(ent.text)
    
    # Optionally add important nouns (e.g., subjects)
    for token in doc:
        if token.pos_ == "NOUN" and token.text not in key_phrases:
            key_phrases.append(token.text)
    
    return key_phrases

# Define a color palette for highlighting
color_palette = ["#FFA07A", "#7FFFD4", "#FF69B4", "#98FB98", "#FFD700", "#ADD8E6"]

def get_color_for_question(question_num):
    """
    Get a consistent color for each question number.
    """
    colors = color_palette
    index = int(question_num[1:]) % len(colors)  # Ensure index is within the color palette range
    return colors[index]

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
        
        # Display the content of uploaded files
        st.subheader("📄 **Answer Key:**")
        st.text_area("Answer Key Content", value=answer_key, height=300)

        st.subheader("📄 **Answer Sheet:**")
        st.text_area("Answer Sheet Content", value=answer_sheet, height=300)

        # Add the "Run" button
        if st.button("Run NER Analysis 🔍"):
            # Split the answer key and answer sheet by questions
            answer_key_dict = split_by_question(answer_key)
            answer_sheet_dict = split_by_question(answer_sheet)

            # Create custom entities for key phrases in each answer key question
            add_custom_entities(nlp, answer_key_dict)

            # Process each question individually
            st.subheader("🖍️ **Highlighted Answer Sheet by Question:**")
            for question_num, answer_text in answer_sheet_dict.items():
                st.markdown(f"### {question_num}:")
                if question_num in answer_key_dict:
                    color = get_color_for_question(question_num)  # Get color for current question
                    highlighted_text = highlight_entities(answer_text, nlp(answer_key_dict[question_num]), color)
                    st.markdown(highlighted_text, unsafe_allow_html=True)
                else:
                    # If no key found for the question, show the original answer
                    st.markdown(answer_text)

def read_file(uploaded_file):
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    return stringio.read()

def split_by_question(text):
    """
    Splits the text by question number (e.g., Q1:, Q2:) and returns a dictionary.
    Assumes the format: "Q1: <answer>"
    """
    questions = {}
    current_question = None
    current_text = []
    
    for line in text.split("\n"):
        if line.strip():  # Process non-empty lines
            if line.startswith("Q"):  # Detect question number
                if current_question:
                    questions[current_question] = "\n".join(current_text)
                current_question = line.split(":")[0].strip()  # e.g., "Q1"
                current_text = [line.split(":")[1].strip()]  # Store the first part of the answer
            else:
                current_text.append(line.strip())  # Add remaining lines of the answer
                
    # Add the last question
    if current_question:
        questions[current_question] = "\n".join(current_text)
    
    return questions

# Function to highlight entities in the answer sheet for a given question
def highlight_entities(answer_sheet, doc_key, color):
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
