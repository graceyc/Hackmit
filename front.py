import streamlit as st
import json
import base64
import requests
import os
import time  # For unique filenames
from autofill import fill_pdf_form
from sign import sign_pdf

# Page configuration
st.set_page_config(
    page_title="eMail - IT",
    page_icon=":email:",
    layout="wide",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Style for the overall app background */
    .stApp {
        background-color: #e0e4eb;
        padding-top: 40px;
    }

    /* Style for the smaller navigation bar */
    .navbar {
        background-color: #007bff;
        padding: 5px;
        border-radius: 5px;
        margin-bottom: 20px;
    }

    .navbar .stRadio > div {
        display: flex;
        justify-content: flex-start;
    }

    .stRadio div[role='radiogroup'] {
        flex-direction: row;
    }

    .stRadio label {
        background-color: #007bff;
        color: white;
        padding: 5px 15px;
        font-size: 14px;
        border-radius: 5px;
        margin-right: 10px;
        transition: background-color 0.3s ease;
        cursor: pointer;
    }

    .stRadio label:hover {
        background-color: #0056b3;
    }

    /* Style for the text area */
    .stTextArea>div>textarea {
        background-color: #f5f7fa;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    /* Style for buttons */
    .stButton>button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #0056b3;
    }

    /* Style for success and error messages */
    .stSuccess {
        color: #28a745;
        font-size: 18px;
    }

    .stError {
        color: #dc3545;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navigation bar using radio buttons
page = st.radio("", ["Home", "About"], key="navigation", index=0, label_visibility="collapsed")

if page == "Home":
    st.title("eMail - IT")
    st.markdown(
        """
        **E-Mail Attachment Autofiller!** :email:

        Enter your email data in JSON format in the text area below, and click **Submit** to parse it and download the PDF attachments.

        **Note:** The email data will be saved as `email_data.json` in your working directory.
        """
    )

    # Input and button for the Home page
    with st.container():
        json_input = st.text_area(
            "Email Data (JSON):",
            height=300,
            placeholder="Paste your email JSON data here..."
        )

        if st.button("Submit"):
            if json_input:
                try:
                    # Parse the JSON input
                    json_data = json.loads(json_input)

                    # Save the JSON data to a file
                    file_name = "email_data.json"
                    with open(file_name, "w") as file:
                        json.dump(json_data, file, indent=2)

                    # Define the download directory
                    download_dir = "DownloadedPDFs"
                    os.makedirs(download_dir, exist_ok=True)  # Create the directory if it doesn't exist

                    # Iterate through the 'parts' to find PDFs
                    pdf_files = []
                    parts = json_data.get("payload", {}).get("parts", [])
                    for part in parts:
                        # Check if there's an attachment link
                        if 'attachmentLink' in part and part['attachmentLink']:
                            attachment_link = part['attachmentLink']
                            filename = part.get("filename", "attachment.pdf")
                            # Ensure filename is valid
                            if not filename.lower().endswith('.pdf'):
                                filename += '.pdf'
                            file_path = os.path.join(download_dir, filename)

                            # Download the PDF from the attachment link
                            response = requests.get(attachment_link)
                            if response.status_code == 200:
                                with open(file_path, "wb") as pdf_file:
                                    pdf_file.write(response.content)
                                pdf_files.append(filename)
                            else:
                                st.error(f"Failed to download {filename} from {attachment_link}. Status Code: {response.status_code}")
                        # Check if the content is in base64 format and not empty
                        elif part.get("mimeType") == "application/pdf" and part.get("content"):
                            content = part['content']
                            filename = part.get("filename", "attachment.pdf")
                            # Ensure filename is valid
                            if not filename.lower().endswith('.pdf'):
                                filename += '.pdf'
                            file_path = os.path.join(download_dir, filename)
                            try:
                                # Decode the base64 content
                                decoded_content = base64.b64decode(content)
                                if decoded_content:  # Ensure content is not empty
                                    with open(file_path, "wb") as pdf_file:
                                        pdf_file.write(decoded_content)
                                    pdf_files.append(filename)
                                else:
                                    st.warning(f"Skipped downloading {filename} because the content is empty.")
                            except Exception as e:
                                st.error(f"Failed to decode the content of {filename}: {e}")
                        else:
                            # Skip parts that are not PDFs or have no content/link
                            continue

                    if pdf_files:
                        # Display the list of downloaded PDFs with their paths
                        st.success(f"Downloaded PDF attachments have been saved to the `{download_dir}` folder:")
                        for pdf in pdf_files:
                            pdf_path = os.path.join(download_dir, pdf)
                            st.text(pdf_path)

                        # Use the entire JSON input as the additional_text
                        additional_text = json_input

                        # Define the path to the signature image
                        signature_image = 'signature.png'
                        if not os.path.exists(signature_image):
                            st.error(f"Signature image `{signature_image}` not found. Please ensure it exists in the working directory.")
                        else:
                            # Process the PDFs
                            signed_pdfs = []
                            for pdf in pdf_files:
                                input_pdf = os.path.join(download_dir, pdf)
                                # Create unique filenames to avoid overwriting
                                timestamp = int(time.time())
                                filled_pdf = os.path.join(download_dir, f"filled_{timestamp}_{pdf}")
                                signed_pdf = os.path.join(download_dir, f"signed_filled_{timestamp}_{pdf}")

                                # Step 1: Fill the PDF form with the provided additional text (JSON)
                                fill_pdf_form(input_pdf, filled_pdf, additional_text)

                                # Step 2: Sign the filled PDF
                                sign_pdf(filled_pdf, signed_pdf, signature_image)

                                signed_pdfs.append(signed_pdf)

                                st.info(f"Processed and signed: {signed_pdf}")

                            if signed_pdfs:
                                st.success("All PDFs have been processed and signed successfully!")

                                # Provide download links and view PDFs
                                st.markdown("### Processed PDFs:")
                                for signed_pdf in signed_pdfs:
                                    pdf_name = os.path.basename(signed_pdf)

                                    # Read the PDF file
                                    with open(signed_pdf, "rb") as f:
                                        pdf_data = f.read()

                                    # Provide a single download button with a unique key
                                    st.download_button(
                                        label=f"Download {pdf_name}",
                                        data=pdf_data,
                                        file_name=pdf_name,
                                        mime="application/pdf",
                                        key=f"download_{pdf_name}"
                                    )

                                    st.markdown(f"**{pdf_name}**")

                                    # Encode PDF to base64 for embedding
                                    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
                                    pdf_display_url = f"data:application/pdf;base64,{base64_pdf}"

                                    # Display the PDF using an iframe without a key
                                    st.components.v1.iframe(
                                        pdf_display_url,
                                        width=700,
                                        height=500,
                                        scrolling=True
                                    )

                            else:
                                st.warning("No signed PDFs were generated.")
                    else:
                        st.warning("No valid PDF attachments found with a valid download link or non-empty base64 content.")
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON format: {e}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Please enter valid JSON data.")

elif page == "About":
    st.title("About eMail - IT")
    st.markdown(
        """
        **eMail Autofiller** automatically parses and downloads any PDF attachments within an e-mail JSON, simplifying the process of filling out forms when relevant information is already in the email.

        ### Features:
        - **Download PDF:** Extract PDF attachments from the email JSON.
        - **Parse Forms:** Identify and check the forms in the PDF.
        - **AI-Powered Parsing:** Use OpenAI to analyze the rest of the email and match it with the PDF forms.
        - **Auto-fill Forms:** Fill out forms, including signatures, for any required fields.

        ### Developers:
        - **Keming Miao**
        - **Grace Yuan**
        - **Jacqueline Wang**

        ### Tech Stack:
        - **Front End:** Streamlit
        - **Back End:** Streamlit 
        - **Python, ChatGPT**
        """
    )
