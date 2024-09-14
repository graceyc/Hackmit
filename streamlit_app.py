import streamlit as st
import json
import base64
import requests

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
        json_input = st.text_area("Email Data (JSON):", height=300, placeholder="Paste your email JSON data here...")

        if st.button("Submit"):
            if json_input:
                try:
                    # Parse the JSON input
                    json_data = json.loads(json_input)

                    # Save the JSON data to a file
                    file_name = "email_data.json"
                    with open(file_name, "w") as file:
                        json.dump(json_data, file, indent=2)
                    
                    # Iterate through the 'parts' to find PDFs
                    pdf_files = []
                    for part in json_data.get("payload", {}).get("parts", []):
                        # Check if there's an attachment link
                        if 'attachmentLink' in part:
                            attachment_link = part['attachmentLink']
                            response = requests.get(attachment_link)
                            if response.status_code == 200:
                                filename = part.get("filename", "attachment.pdf")
                                with open(filename, "wb") as pdf_file:
                                    pdf_file.write(response.content)
                                pdf_files.append(filename)
                            else:
                                st.error(f"Failed to download {filename} from {attachment_link}")
                        # Check if the content is in base64 format
                        elif part.get("mimeType") == "application/pdf" and 'content' in part:
                            content = part['content']
                            filename = part.get("filename", "attachment.pdf")
                            try:
                                with open(filename, "wb") as pdf_file:
                                    pdf_file.write(base64.b64decode(content))
                                pdf_files.append(filename)
                            except Exception as e:
                                st.error(f"Failed to decode the content of {filename}: {e}")

                    if pdf_files:
                        st.success(f"Downloaded PDF attachments: {', '.join(pdf_files)}")
                    else:
                        st.warning("No PDF attachments found with a valid download link or base64 content.")
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
