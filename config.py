import os
from pathlib import Path
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
from selene_in_action.resourse import DATA_DIR
from selene_in_action.selene_in_action_api import AndroidApp

context = os.getenv("context", "browserstack")


def load_environment():
    env_file = Path(__file__).parent / f".env.{context}"
    load_dotenv(env_file)


def remote_url_config():
    load_environment()
    if context == "browserstack":
        return os.getenv("BROWSERSTACK_URL")
    if context in ["local_emulator", "local_real"]:
        return os.getenv("REMOTE_URL")


def to_driver_options():
    options = UiAutomator2Options()
    load_environment()

    if context == "browserstack":
        browserstack_user_name = os.getenv("BROWSERSTACK_USER_NAME")
        browserstack_access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
        options.load_capabilities({
            "platformName": "android",
            "platformVersion": "9.0",
            "deviceName": "Google Pixel 3",
            "app": AndroidApp.get_apk_app(),
            "appWaitActivity": "org.wikipedia.*",
            "bstack:options": {
                "projectName": "First Python project",
                "buildName": "browserstack-build-1",
                "sessionName": "BStack first_test",
                "userName": browserstack_user_name,
                "accessKey": browserstack_access_key,
            },
        })

    elif context in ["local_emulator", "local_real"]:
        local_device_name = os.getenv("LOCAL_DEVICE_NAME")
        options.load_capabilities({
            "deviceName": local_device_name,
            "app": DATA_DIR + "/app-alpha-universal-release.apk",
            "appWaitActivity": "org.wikipedia.*",
        })

    return options