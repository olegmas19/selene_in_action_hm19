import os
from pathlib import Path

import allure
import requests
from dotenv import load_dotenv


def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(
        body=png, name="Screenshot", attachment_type=allure.attachment_type.PNG
    )


def add_xml(browser):
    xml_dump = browser.driver.page_source
    allure.attach(
        body=xml_dump, name="XML screen", attachment_type=allure.attachment_type.XML
    )


def add_video(session_id):
    env_file = Path(__file__).parent / f".env.bstack"
    load_dotenv(env_file)
    browserstack_user_name = os.getenv("BROWSERSTACK_USER_NAME")
    browserstack_access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    browserstack_session = requests.get(
        url=f"https://api.browserstack.com/app-automate/sessions/{session_id}.json",
        auth=(browserstack_user_name, browserstack_access_key),
    ).json()
    video_url = browserstack_session["automation_session"]["video_url"]

    allure.attach(
        "<html><body>"
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        "</video>"
        "</body></html>",
        name="video recording",
        attachment_type=allure.attachment_type.HTML,
    )
