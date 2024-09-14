# Third-Eye: Automated Answer Key Verifier

**Third-Eye** is a powerful Streamlit application designed to help you analyze answer sheets by comparing them with an answer key using Named Entity Recognition (NER). This application highlights key elements from the answer key in the answer sheet to ensure accurate and efficient grading.

## Features

- **Upload Answer Key and Answer Sheet**: Seamlessly upload text files containing the answer key and the answer sheet.
- **Custom Entity Recognition**: Use spaCy's NER capabilities with custom rules to highlight key phrases from the answer key.
- **Consistent Highlighting**: Get consistent color highlighting for key phrases across questions.
- **Display and Verification**: View the content of both files before running the analysis and check highlighted results.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Streamlit
- spaCy
- Required spaCy model (`en_core_web_md`)

