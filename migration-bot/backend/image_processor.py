import os
import requests
import hashlib
import time
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

IMAGE_FOLDER = "images"

downloaded_images = {}


def ensure_image_folder():

    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)


def generate_image_name(image_url):

    """
    Create unique image filename using hash
    """

    url_hash = hashlib.md5(image_url.encode()).hexdigest()

    parsed = urlparse(image_url)

    ext = os.path.splitext(parsed.path)[1]

    if not ext:
        ext = ".jpg"

    return f"{url_hash}{ext}"


def download_image(image_url, retries=3):

    ensure_image_folder()

    # Prevent duplicate downloads
    if image_url in downloaded_images:
        return downloaded_images[image_url]

    filename = generate_image_name(image_url)

    filepath = os.path.join(IMAGE_FOLDER, filename)

    for attempt in range(retries):

        try:

            time.sleep(0.5)

            response = requests.get(
                image_url,
                headers=HEADERS,
                timeout=20,
                stream=True
            )

            if response.status_code != 200:
                continue

            with open(filepath, "wb") as f:

                for chunk in response.iter_content(1024):
                    if chunk:
                        f.write(chunk)

            downloaded_images[image_url] = filepath

            print(f"Image saved: {filename}")

            return filepath

        except Exception as e:

            print(f"Image retry {attempt+1} failed:", e)

            time.sleep(1)

    print("Image failed:", image_url)

    return None