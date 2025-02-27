from github import Github
from github import Auth
import streamlit as st
import base64

_auth = Auth.Token(st.secrets["GITHUB_API_KEY"])
_g = Github(auth=_auth)
_repo = _g.get_repo(st.secrets["GITHUB_REPO"])

def get_tags():
    contents = _repo.get_contents("")
    return [content.name for content in contents]

def get_images(tag):
    contents = _repo.get_contents(tag)
    return [f'https://cdn.jsdelivr.net/gh/zach2077-7/images/{tag}/{content.name}' for content in contents]

def upload_image(file_content, filename, tag):
    content = base64.b64encode(file_content).decode()
    try:
        _repo.create_file(f'{tag}/{filename}', f'upload {filename}', file_content, branch="master")
        return True
    except Exception as e:
        print(f"Error uploading to GitHub: {str(e)}")
        return False