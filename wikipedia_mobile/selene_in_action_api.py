import base64
import os
from pathlib import Path
import requests
from dotenv import load_dotenv
from wikipedia_mobile.resourse import DATA_DIR


class AndroidApp:

    @staticmethod
    def get_apk_app():
        load_dotenv(
            dotenv_path=Path(__file__).resolve().parent.parent / f".env.credentials"
        )
        url = "https://api-cloud.browserstack.com/app-automate/upload"
        token = f"{os.getenv('USER_NAME')}:{os.getenv('ACCESS_KEY')}"
        encoded_credentials = base64.b64encode(token.encode("utf-8")).decode("utf-8")

        payload = {}
        files = [
            (
                "file",
                (
                    "app-alpha-universal-release.apk",
                    open(DATA_DIR + "/app-alpha-universal-release.apk", "rb"),
                    "application/octet-stream",
                ),
            )
        ]
        headers = {"Authorization": f"Basic {encoded_credentials}"}

        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files
        )
        result = response.json().get("app_url")
        return result
