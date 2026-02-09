import streamlit as st
import PyPDF2
from PIL import Image
from langchain_core.messages import HumanMessage

def handle_pdf_upload(state, chat_title, messages):
    uploaded_pdfs = st.file_uploader("Upload PDF", type=["pdf"], accept_multiple_files=True, key="pdf")
    if uploaded_pdfs:
        for pdf_file in uploaded_pdfs:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text() or ""
            messages.append(HumanMessage(content=f"[PDF Uploaded: {pdf_file.name}]\n\n{pdf_text[:1000]}..."))
            state.uploaded_files[chat_title]["pdf"].append(pdf_file.name)

def handle_image_upload(state, chat_title, messages):
    uploaded_images = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key="img")
    if uploaded_images:
        for img_file in uploaded_images:
            img = Image.open(img_file)
            st.image(img, caption=f"Uploaded: {img_file.name}", use_column_width=True)
            messages.append(HumanMessage(content=f"[Image Uploaded: {img_file.name}]"))
            state.uploaded_files[chat_title]["images"].append(img_file.name)