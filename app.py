import spacy
import os
import spacy
from spacy.tokens import DocBin
from pdf2image import convert_from_path
import pytesseract
import random
import streamlit as st 

# Load the spaCy model
nlp = spacy.load("model-best")

# Function to convert PDF to images and save them in a folder
def pdf_to_images(pdf_file_path, output_folder):
    images = convert_from_path(pdf_file_path)

    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
        image.save(image_path, "JPEG")

    return images


def extract_named_entities(text):
   

    doc = nlp(text)
    
    entities = []
    for ent in doc.ents:
        # Get the confidence score from the Span object
        
        entities.append((ent.text, ent.label_.upper()))
    return entities


def extract_text_from_image(img):
  
    return pytesseract.image_to_string(img)
  

def save_uploaded_file(uploaded_file):
    # Create a temporary directory to save the uploaded file
    temp_dir = "temp1"  # Replace with your desired temporary directory name
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Save the uploaded file to the temporary directory
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    return file_path

def main():
    
    


    st.title("PDF Named Entity Recognition with spaCy")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    
    if uploaded_file:
        # Save the uploaded PDF file and get the path of the saved file
        saved_file_path = save_uploaded_file(uploaded_file)
        # Save the uploaded file to a temporary folder
        
        temp_dir = os.path.abspath("temp")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Save the uploaded file to the "temp" directory
        with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getvalue())

        # Get the file path of the uploaded PDF
        pdf_file_path = os.path.join(temp_dir, uploaded_file.name)

        output_folder = os.path.join(temp_dir, "images")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        images = pdf_to_images(os.path.join("temp", uploaded_file.name), output_folder)
        if not os.path.exists("output"):
            os.makedirs("output")
        

        images = pdf_to_images(saved_file_path, "output")

        for i, image in enumerate(images):
            st.subheader(f"Processing Page {i + 1}")
            # Perform OCR on the image to extract text
            text= extract_text_from_image(image)
           
            # Perform NER on the extracted text to identify named entities
            # entities = extract_named_entities(text)
            
            # # Display named entities using spaCy displacy.render
            # html = spacy.displacy.render(entities, style="ent", page=True, minify=True)
            # st.write(html, unsafe_allow_html=True)
            entities = extract_named_entities(text)

        # Display named entities using spaCy displacy.render
        html = spacy.displacy.render(nlp(text), style="ent", page=True, minify=True)
        st.write(html, unsafe_allow_html=True)

        # Display the named entities list with confidence scores
        st.subheader("Named Entities with Confidence Scores:")
        for entity_text, entity_label in entities:
            st.write(f"{entity_text}: {entity_label} ")
        

# Run the app
if __name__ == "__main__":
    main()
