import streamlit as st
import time
from storage import upload_image


# Initialize session state for password
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False

st.title("Upload Image")

# Add password protection
if not st.session_state.is_authenticated:
    password = st.text_input("Enter password", type="password")
    if st.button("Login"):
        if password == st.secrets["UPLOAD_PASSWORD"]:
            st.session_state.is_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
else:
    st.write("Upload your image to the photo wall")
    uploaded_files = st.file_uploader(
        "Choose an image", 
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'heic'],
        accept_multiple_files=True
    )

    if uploaded_files is not None and len(uploaded_files) > 0:
        # Display the uploaded image
        _, preview, _ = st.columns([0.15, 0.7, 0.15])
        with preview:
            cols = st.columns(3)
            for idx, uploaded_file in enumerate(uploaded_files):
                with cols[idx % 3]:
                    st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)
        
        # Add tag input
        tag = st.text_input("Add a tag for your image", 
                           placeholder="e.g., nature")
        
        # Add a button to confirm upload
        if st.button("Upload to Gallery"):
            if not tag:
                st.warning("Please add a tag for your image")
            else:
                with st.spinner("Uploading..."):
                    success_count = 0
                    fail_count = 0
                    for uploaded_file in uploaded_files:
                        try:
                            # Generate new filename with tag and milliseconds timestamp
                            file_extension = uploaded_file.name.split('.')[-1].lower()
                            new_filename = f"{time.time_ns()}.{file_extension}"
                            
                            # Get the file content
                            file_content = uploaded_file.getvalue()
                            if upload_image(file_content, new_filename, tag):
                                success_count += 1
                            else:
                                fail_count += 1
                        except Exception as e:
                            st.error(f"Error uploading {uploaded_file.name}: {str(e)}")
                            fail_count += 1
                    if success_count > 0:
                        st.success(f"Successfully uploaded {success_count} images!")
                    if fail_count > 0:
                        st.error(f"Failed to upload {fail_count} images")