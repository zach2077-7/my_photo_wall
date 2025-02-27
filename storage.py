from github import Github
from github import Auth
from PIL import Image, ImageOps
from urllib.parse import urlparse
from io import BytesIO
import streamlit as st
import base64
import os
import hashlib
import requests

_repo = Github(auth=Auth.Token(st.secrets["GITHUB_API_KEY"])).get_repo(st.secrets["GITHUB_REPO"])

CACHE_DIR = ".cache/images"
os.makedirs(CACHE_DIR, exist_ok=True)

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

def load_image(image_url):
    def get_cached_path(url):
        url_hash = hashlib.md5(url.encode()).hexdigest()
        extension = os.path.splitext(urlparse(url).path)[1]
        return os.path.join(CACHE_DIR, f"{url_hash}{extension}")
    cache_path = get_cached_path(image_url)
    if os.path.exists(cache_path):
        print(f"Loading image from cache: {cache_path}")
        return Image.open(cache_path)
    print(f"Downloading image from URL: {image_url}")
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = ImageOps.exif_transpose(img)
    img.save(cache_path, format=img.format or 'PNG')
    return img