# Step 1: Use the official Python image as the base image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements file and install dependencies
COPY requirements.txt .

# Install system dependencies and install spaCy model en_core_web_md
RUN apt-get update && apt-get install -y \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download en_core_web_md \
    && apt-get clean

# Step 4: Copy the entire project code into the container
COPY . .

# Step 5: Expose the Streamlit port (8501)
EXPOSE 8501

# Step 6: Run the Streamlit app
CMD ["streamlit", "run", "third_eye.py", "--server.port=8501", "--server.address=0.0.0.0"]
