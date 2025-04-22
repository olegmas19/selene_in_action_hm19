import os
from pathlib import Path
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
from pydantic import BaseModel
from wikipedia_mobile.resourse import DATA_DIR


class Config(BaseModel):
    context: str
    remote_url: str = os.getenv("REMOTE_URL")
    device_name: str = os.getenv("DEVICE_NAME")
    udid: str = os.getenv("UDID")
    appWaitActivity: str = os.getenv("APP_WAIT_ACTIVITY")
    app_local: str = DATA_DIR + os.getenv("APP")
    app_bstack: str = os.getenv("APP")
    platformName: str = os.getenv("PLATFORM_NAME")
    platformVersion: str = os.getenv("PLATFORM_VERSION")

    def to_driver_options(self, context):
        options = UiAutomator2Options()

        if context == "bstack":
            load_dotenv(
                dotenv_path=Path(__file__).resolve().parent / f".env.credentials"
            )
            options.load_capabilities(
                {
                    "remote_url": self.remote_url,
                    "platformName": self.platformName,
                    "platformVersion": self.platformVersion,
                    "deviceName": self.device_name,
                    "app": self.app_bstack,
                    "appWaitActivity": self.appWaitActivity,
                    "bstack:options": {
                        "projectName": "First Python project",
                        "buildName": "browserstack-build-1",
                        "sessionName": "BStack first_test",
                        "userName": os.getenv("USER_NAME"),
                        "accessKey": os.getenv("ACCESS_KEY"),
                    },
                }
            )
        elif context == "local_emulator":
            options.load_capabilities(
                {
                    "remote_url": self.remote_url,
                    "appWaitActivity": self.appWaitActivity,
                    "udid": self.udid,
                    "app": self.app_local,
                }
            )
        elif context == "local_real":
            options.load_capabilities(
                {
                    "remote_url": self.remote_url,
                    "appWaitActivity": self.appWaitActivity,
                    "udid": self.udid,
                    "app": self.app_local,
                }
            )

        return options


config = Config(context="bstack")
