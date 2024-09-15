import os
from autofill import fill_pdf_form
from sign import sign_pdf

def process_pdfs(additional_text):
    input_folder = 'DownloadedPDFs'       # Path to the folder containing PDFs
    signature_image = 'signature.png'     # Path to your signature image

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):  # Only process PDF files
            input_pdf = os.path.join(input_folder, filename)
            filled_pdf = os.path.join(input_folder, f"filled_{filename}")
            signed_pdf = os.path.join(input_folder, f"signed_filled_{filename}")

            # Step 1: Fill the PDF form with the provided additional text
            fill_pdf_form(input_pdf, filled_pdf, additional_text)

            # Step 2: Sign the filled PDF
            sign_pdf(filled_pdf, signed_pdf, signature_image)
            print(f"Processed and signed: {signed_pdf}")

# Example usage
if __name__ == '__main__':
    additional_text = input("Enter the additional text to fill the PDFs: ")
    process_pdfs(additional_text)
