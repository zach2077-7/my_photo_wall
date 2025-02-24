import streamlit as st
import requests
import base64
import os
import time
from dotenv import load_dotenv
from github import Github
from github import Auth

load_dotenv()

# Initialize session state for password
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False

def upload_to_github(file_content, filename, tag):
    auth = Auth.Token(os.getenv("GITHUB_API_KEY"))
    g = Github(auth=auth)
    repo = g.get_repo(os.getenv("GITHUB_REPO"))
    content = base64.b64encode(file_content).decode()
    try:
        repo.create_file(f'{tag}/{filename}', f'upload {filename}', file_content, branch="main")
        return True
    except Exception as e:
        print(f"Error uploading to GitHub: {str(e)}")
        return False

st.title("Upload Image")

# Add password protection
if not st.session_state.is_authenticated:
    password = st.text_input("Enter password", type="password")
    if st.button("Login"):
        if password == os.getenv("UPLOAD_PASSWORD"):
            st.session_state.is_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
else:
    st.write("Upload your image to the photo wall")
    uploaded_file = st.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'heic'])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Preview", use_container_width=True)
        
        # Add tag input
        tag = st.text_input("Add a tag for your image", 
                           placeholder="e.g., nature, family, vacation")
        
        # Add a button to confirm upload
        if st.button("Upload to Gallery"):
            if not tag:
                st.warning("Please add a tag for your image")
            else:
                with st.spinner("Uploading..."):
                    try:
                        # Generate new filename with tag and milliseconds timestamp
                        file_extension = uploaded_file.name.split('.')[-1].lower()
                        new_filename = f"{time.time_ns()}.{file_extension}"
                        
                        # Get the file content
                        file_content = uploaded_file.getvalue()
                        success = upload_to_github(file_content, new_filename, tag)
                        
                        if success:
                            st.success("Image uploaded successfully!")
                        else:
                            st.error("Failed to upload image")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")