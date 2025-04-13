import base64
import os
import requests
from dotenv import load_dotenv
from selene_in_action.resourse import DATA_DIR


class AndroidApp:

    @staticmethod
    def get_apk_app():
        load_dotenv()
        url = "https://api-cloud.browserstack.com/app-automate/upload"
        browserstack_user_name = os.getenv("BROWSERSTACK_USER_NAME")
        browserstack_access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
        token = f"{browserstack_user_name}:{browserstack_access_key}"
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
