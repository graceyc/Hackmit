import streamlit as st
import requests

st.title("Download File from URL")

url = st.text_input("Enter the URL of the file you want to download:")

if st.button("Download"):
    if url:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors
            file_name = url.split("/")[-1]
            with open(file_name, "wb") as file:
                file.write(response.content)
            st.success(f"File saved as {file_name}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please enter a valid URL.")

