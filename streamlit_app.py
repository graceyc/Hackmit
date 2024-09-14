Jacqueline Wang
jacquelinewangyujia
Online
leprials, Yepi, mkmmm, Grace

leprials — Today at 5:02 PM
Idt it'll work on the cloud tbh
Just the local instance
So do the "streamlit run yourfilename.py" command
I think thats it
Inside your vs code
Grace — Today at 5:05 PM
we are trying now
leprials — Today at 5:05 PM
Ok lmkkk
Grace — Today at 5:10 PM
i don't think we fixed the problem 😭 😭 😭 😭 😭
leprials — Today at 5:10 PM
Same issue?
mkmmm — Today at 5:11 PM
Image
the hello world one works
but we are still trying very hard to make this one apply to our project
leprials — Today at 5:12 PM
Check their API page and look at text input
Should be an example
Yepi — Today at 5:12 PM
You’re going to want to store the input text in a variable
mkmmm — Today at 5:13 PM
in this program?
where could i check the api
leprials — Today at 5:13 PM
https://docs.streamlit.io/develop/api-reference/text/st.header
st.header - Streamlit Docs
st.header displays text in header formatting.
st.header - Streamlit Docs
Idk which one it is
But this site
Grace — Today at 5:14 PM
Image
the old one looks like this rn
is this what we want?
leprials — Today at 5:15 PM
Yeah, but make it bigger so you can put full json
Grace — Today at 5:18 PM
wdym by making it bigger?
leprials — Today at 5:19 PM
Larger input box
Well give it the full json from the site
And have your code find the link to the pdf
Jacqueline Wang — Today at 5:24 PM
we are currently working upstairs. let us know when you come back and we will come down again
leprials — Today at 5:29 PM
We're coming back now so we'll send what entrance were at
Yepi — Today at 5:30 PM
Can you guys open the door plz
leprials — Today at 5:30 PM
Image
Image
Helpppppp
Yepi — Today at 5:31 PM
Grace — Today at 5:31 PM
where are u
Yepi — Today at 5:32 PM
Uh
Image
leprials — Today at 5:32 PM
Image
Yepi — Today at 5:33 PM
This entrance
leprials — Today at 5:33 PM
Ok
Yepi — Today at 5:33 PM
We’re in
leprials — Today at 5:33 PM
Were in
Same entrance
To library
Plz
Grace — Today at 5:33 PM
Ok we are back
import streamlit as st
import requests

st.title("Download File from URL")

url = st.text_input("Enter the URL of the file you want to download:")

if st.button("Download"):
    if url:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors
            file_name = "/Users/graceyuan/Downloads/" + url.split("/")[-1]
            with open(file_name, "wb") as file:
                file.write(response.content)
            st.success(f"File saved as {file_name}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a valid URL.")
Grace — Today at 6:00 PM
import streamlit as st
import json

# Page configuration
st.set_page_config(
    page_title="eMail - IT",
Expand
message.txt
5 KB
Grace — Today at 6:22 PM
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
... (83 lines left)
Collapse
message.txt
7 KB
﻿
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
message.txt
7 KB
