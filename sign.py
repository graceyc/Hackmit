import fitz  # PyMuPDF

def sign_pdf(input_pdf, output_pdf, signature_image):
    # Open the PDF document
    doc = fitz.open(input_pdf)

    # Keywords to search for signature fields
    keywords = ["Signature", "Sign Here", "Authorized Signatory"]

    # Iterate over each page in the PDF
    for page_number in range(len(doc)):
        page = doc[page_number]
        found = False  # Flag to check if a keyword was found on the page

        # Search for each keyword on the page
        for keyword in keywords:
            text_instances = page.search_for(keyword)

            # If instances are found, insert the signature image
            if text_instances:
                found = True
                for inst in text_instances:
                    x0, y0, x1, y1 = inst  # Get the coordinates of the text instance

                    # Adjust the position and size of the signature image as needed
                    image_width = 150  # Adjust the width of the signature image
                    image_height = 50  # Adjust the height of the signature image

                    # Adjust the vertical position
                    vertical_adjustment = 0  # Adjust this value to fine-tune the position

                    # Calculate the average top y coordinate
                    average_top_y = y1 - (image_height / 2) + vertical_adjustment

                    # Create the image rectangle
                    image_rect = fitz.Rect(
                        x0,
                        average_top_y,
                        x0 + image_width,
                        average_top_y + image_height
                    )

                    # Insert the signature image into the PDF
                    page.insert_image(image_rect, filename=signature_image)

        if not found:
            print(f"No signature field found on page {page_number + 1}.")

    # Save the modified PDF to a new file
    doc.save(output_pdf)
    print(f"Signature inserted. The signed PDF is saved as '{output_pdf}'.")

# Remove or comment out the main block
# if __name__ == "__main__":
#     sign_pdf("test.pdf", "signed_pdf_file.pdf", "signature.png")
