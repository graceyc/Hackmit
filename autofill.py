import os
import json
import requests
import re
from dotenv import load_dotenv
from fillpdf import fillpdfs
from pypdf import PdfReader

def decode_field_flags(field_flags):
    """
    Decodes the field flags integer into a list of flag names.
    """
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
    # Add more flags as needed
    return flag_info

def process_fields(fields, field_list):
    """
    Recursively processes PDF form fields to extract detailed parameters.
    """
    for field in fields:
        field_info = {}
        field_name = field.get('/T')
        field_type = field.get('/FT')
        kids = field.get('/Kids')

        if field_name:
            field_info['name'] = str(field_name)
        if field_type:
            field_info['type'] = str(field_type)

        # Get the field's dictionary entries
        max_len = field.get('/MaxLen')
        default_value = field.get('/DV')
        field_flags = field.get('/Ff')
        options = field.get('/Opt')
        additional_actions = field.get('/AA')

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

def extract_pdf_fields(pdf_path):
    """
    Extracts form fields from the PDF and returns a list of field parameters.
    """
    pdf = PdfReader(pdf_path)
    field_list = []
    acroform = pdf.trailer['/Root'].get('/AcroForm')
    if acroform:
        fields = acroform.get('/Fields')
        if fields:
            process_fields(fields, field_list)
        else:
            print("No form fields found in the PDF.")
            exit(1)
    else:
        print("No AcroForm found in the PDF.")
        exit(1)
    return field_list

def get_form_data_from_chatgpt(field_list, additional_text=None):
    """
    Sends a prompt to ChatGPT to generate sample data based on field parameters and additional text.
    """
    fields_json = json.dumps(field_list, indent=2)

    if additional_text:
        prompt = (
            "You are provided with a list of PDF form fields with their names, types, and parameters in JSON format, "
            "as well as additional text related to the PDF content. "
            "Please generate a JSON object with data to populate each field appropriately based on the provided text. "
            "If the text doesn't contain information for certain fields, make up reasonable data for them. If you dont know, make something up. DO NOT LEAVE IT EMPTY. DO NOT WRITE N/A"
            "Ensure the keys in your JSON match the 'name' values from the provided data. "
            "Consider parameters like maximum length, default values, and options when generating the data.\n\n"
            "Please output only the JSON object without any code formatting, code fences, or additional text.\n\n"
            f"Field Data:\n{fields_json}\n\nAdditional Text:\n{additional_text}"
        )
    else:
        prompt = (
            "You are provided with a list of PDF form fields with their names, types, and parameters in JSON format. "
            "Please generate a JSON object with sample data to populate each field appropriately based on its type and parameters. If you dont know, make something up. DO NOT LEAVE IT EMPTY. DO NOT WRITE N/A"
            "Ensure the keys in your JSON match the 'name' values from the provided data. "
            "Consider parameters like maximum length, default values, and options when generating the sample data.\n\n"
            "Please output only the JSON object without any code formatting, code fences, or additional text.\n\n"
            f"Field Data:\n{fields_json}"
        )

    # The rest of the function remains the same
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print("Please set the OPENAI_API_KEY in your .env file.")
        exit(1)

    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}',
    }
    data = {
        'model': 'gpt-4o',  # Use 'gpt-4' if you have access
        'messages': [
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.7,
        'max_tokens': 1000,  # Adjust as needed
    }

    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        completion = response.json()
        message_content = completion['choices'][0]['message']['content']
        print("ChatGPT Response:")
        print(message_content)
        try:
            # Remove code fences if they exist
            message_content = message_content.strip()
            if message_content.startswith("```") and message_content.endswith("```"):
                # Extract JSON content between code fences
                message_content = re.sub(r'^```(?:json)?\n', '', message_content)
                message_content = re.sub(r'\n```$', '', message_content)
            form_data = json.loads(message_content)
            print("\nParsed Form Data:")
            print(json.dumps(form_data, indent=2))
            return form_data
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON from ChatGPT response: {e}")
            exit(1)
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        exit(1)


def populate_pdf_fillpdf(pdf_path, output_path, form_data):
    """
    Fills the PDF form using fillpdf and flattens it to make filled fields visible.
    """
    # Fill the PDF form
    fillpdfs.write_fillable_pdf(pdf_path, output_path, form_data)

    # Flatten the PDF to make the form fields visible
    fillpdfs.flatten_pdf(output_path, output_path)

    print(f"Filled PDF saved as {output_path}")

def main():
    pdf_path = 'test.pdf'  # Path to your input PDF file
    output_pdf_path = 'filled_test.pdf'  # Path for the output filled PDF

    # Extract field parameters from the PDF
    field_list = extract_pdf_fields(pdf_path)

    # Print detailed field information
    print("Extracted PDF Form Fields with Parameters:")
    print(json.dumps(field_list, indent=2))

    # Generate sample data using ChatGPT
    form_data = get_form_data_from_chatgpt(field_list)

    # Fill the PDF form with the generated data
    populate_pdf_fillpdf(pdf_path, output_pdf_path, form_data)

def fill_pdf_form(input_pdf, output_pdf, additional_text=None):
    pdf_path = input_pdf
    output_pdf_path = output_pdf

    # Extract field parameters from the PDF
    field_list = extract_pdf_fields(pdf_path)

    # Print detailed field information
    print("Extracted PDF Form Fields with Parameters:")
    print(json.dumps(field_list, indent=2))

    # Generate sample data using ChatGPT
    form_data = get_form_data_from_chatgpt(field_list, additional_text)

    # Fill the PDF form with the generated data
    populate_pdf_fillpdf(pdf_path, output_pdf_path, form_data)

