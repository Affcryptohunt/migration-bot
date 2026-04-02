import os
import requests
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

IMAGE_FOLDER = "images"


def ensure_image_folder():
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)


def get_image_filename(image_url):

    parsed = urlparse(image_url)
    filename = os.path.basename(parsed.path)

    if not filename:
        filename = "product_image.jpg"

    return filename


def download_image(image_url):

    ensure_image_folder()

    filename = get_image_filename(image_url)

    filepath = os.path.join(IMAGE_FOLDER, filename)

    try:

        response = requests.get(
            image_url,
            headers=HEADERS,
            timeout=15,
            stream=True
        )

        if response.status_code != 200:
            print(f"Image failed: {image_url}")
            return None

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Image saved: {filename}")

        return filepath

    except Exception as e:

        print(f"Image download error: {e}")

        return None