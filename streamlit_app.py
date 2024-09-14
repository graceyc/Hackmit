import streamlit as st
import os
import json
import requests
import re
from dotenv import load_dotenv
from fillpdf import fillpdfs
from pypdf import PdfReader

# Streamlit app title and description
st.title("📄 PDF Form Filler with AI")
st.write(
    "Easily extract fields from PDF forms, generate sample data using OpenAI's GPT, and fill the form. "
    "Upload a PDF, let AI handle the details, and download the filled form!"
)

# File uploader for PDF
pdf_file = st.file_uploader("Upload a PDF file with form fields:", type=["pdf"])

# Helper function to decode field flags
def decode_field_flags(field_flags):
    flags = int(field_flags)
    flag_info = []
    if flags & (1 << 0):
        flag_info.append('ReadOnly')
    if flags & (1 << 1):
        flag_info.append('Required')
    if flags & (1 << 12):
        flag_info.append('Password')
    if flags & (1 << 13):
        flag_info.append('FileSelect')
    if flags & (1 << 14):
        flag_info.append('DoNotSpellCheck')
    if flags & (1 << 15):
        flag_info.append('DoNotScroll')
    if flags & (1 << 17):
        flag_info.append('Comb')
    return flag_info

# Helper function to process fields
def process_fields(fields, field_list):
    for field in fields:
        field_info = {}
        field_name = field.get('/T')
        field_type = field.get('/FT')
        kids = field.get('/Kids')

        if field_name:
            field_info['name'] = str(field_name)
        if field_type:
            field_info['type'] = str(field_type)

        max_len = field.get('/MaxLen')
        default_value = field.get('/DV')
        field_flags = field.get('/Ff')
        options = field.get('/Opt')

        if max_len:
            field_info['max_length'] = int(max_len)
        if default_value:
            field_info['default_value'] = str(default_value)
        if field_flags:
            field_info['field_flags'] = decode_field_flags(field_flags)
        if options:
            field_info['options'] = [str(option) for option in options]

        field_list.append(field_info)

        if kids:
            process_fields(kids, field_list)

# Extract PDF fields
def extract_pdf_fields(pdf_path):
    pdf = PdfReader(pdf_path)
    field_list = []
    acroform = pdf.trailer['/Root'].get('/AcroForm')
    if acroform:
        fields = acroform.get('/Fields')
        if fields:
            process_fields(fields, field_list)
    return field_list

# Get form data from ChatGPT
def get_form_data_from_chatgpt(field_list):
    fields_json = json.dumps(field_list, indent=2)
    prompt = (
        "You are provided with a list of PDF form fields with their names, types, and parameters in JSON format. "
        "Please generate a JSON object with sample data to populate each field appropriately based on its type and parameters. "
        "Ensure the keys in your JSON match the 'name' values from the provided data. "
        "Consider parameters like maximum length, default values, and options when generating the sample data.\n\n"
        "Please output only the JSON object without any code formatting, code fences, or additional text.\n\n"
        f"Field Data:\n{fields_json}"
    )

    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        st.error("Please set the OPENAI_API_KEY in your .env file.")
        return None

    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}',
    }
    data = {
        'model': 'gpt-3.5-turbo',  # Use 'gpt-4' if you have access
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.7,
        'max_tokens': 1000,
    }

    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        completion = response.json()
        message_content = completion['choices'][0]['message']['content']
        try:
            message_content = message_content.strip()
            form_data = json.loads(message_content)
            return form_data
        except json.JSONDecodeError:
            st.error("Failed to parse JSON from ChatGPT response.")
            return None
    else:
        st.error(f"Request failed with status code {response.status_code}.")
        return None

# Fill PDF
def populate_pdf_fillpdf(pdf_path, output_path, form_data):
    fillpdfs.write_fillable_pdf(pdf_path, output_path, form_data)
    fillpdfs.flatten_pdf(output_path, output_path)
    return output_path

# Main app logic
if pdf_file:
    with st.spinner("Extracting fields from PDF..."):
        field_list = extract_pdf_fields(pdf_file)
        st.success("Fields extracted successfully!")
        st.json(field_list)

        if st.button("Generate Sample Data and Fill PDF"):
            with st.spinner("Generating sample data using ChatGPT..."):
                form_data = get_form_data_from_chatgpt(field_list)
                if form_data:
                    st.success("Sample data generated successfully!")
                    st.json(form_data)

                    with st.spinner("Filling the PDF with sample data..."):
                        output_pdf_path = "filled_test.pdf"
                        filled_pdf_path = populate_pdf_fillpdf(pdf_file, output_pdf_path, form_data)
                        if filled_pdf_path:
                            st.success("PDF filled successfully!")
                            st.download_button(
                                label="Download Filled PDF",
                                data=open(filled_pdf_path, "rb").read(),
                                file_name="filled_test.pdf",
                                mime="application/pdf"
                            )
                        else:
                            st.error("Failed to fill the PDF.")
