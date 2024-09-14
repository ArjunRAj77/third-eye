FROM python:3.9-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install spaCy model
RUN python -m spacy download en_core_web_md

# Copy the rest of the application code
COPY . .

# Expose the port and run the app
EXPOSE 8501
CMD ["streamlit", "run", "third_eye.py"]
