import os

from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv

from selene_in_action.resourse import DATA_DIR
from selene_in_action.selene_in_action_api import AndroidApp




context = os.getenv('context', 'browserstack')

browserstack_user_name = os.getenv('browserstack_userName', 'bsuser_DkuYhf')
browserstack_access_key = os.getenv('browserstack_accesskey', 'xbGJNGGpERiLURjfvAVM')
appBstack = os.getenv('app', AndroidApp.get_apk_app())

def remote_url_config():
    if context == 'browserstack':
        return os.getenv('remote_url', 'http://hub.browserstack.com/wd/hub')
    if context == 'local_emulator' or context == 'local_real':
        return os.getenv('remote_url', 'http://127.0.0.1:4723/wd/hub')


appWaitActivity = os.getenv('appWaitActivity', 'org.wikipedia.*')
# deviceName = os.getenv('deviceName')
appLocal = os.getenv('app', DATA_DIR + "/app-alpha-universal-release.apk")
browserstack_url = os.getenv('browserstack_url', 'hub.browserstack.com')


def to_driver_options():
        options = UiAutomator2Options()

        if context == 'browserstack':
            options.load_capabilities(
                {
                    # Specify device and os_version for testing
                    "platformName": "android",
                    "platformVersion": "9.0",
                    "deviceName": "Google Pixel 3",
                    "app": appBstack,
                    "appWaitActivity": appWaitActivity,
                    # Set other BrowserStack capabilities
                    "bstack:options": {
                        "projectName": "First Python project",
                        "buildName": "browserstack-build-1",
                        "sessionName": "BStack first_test",
                        # Set your access credentials
                        "userName": browserstack_user_name,
                        "accessKey": browserstack_access_key,
                    },
                }
            )
        elif context == 'local_emulator':
            options.load_capabilities(
                {
                    # Specify device and os_version for testing
                    "deviceName": "emulator-5554",
                    "app": appLocal,
                    "appWaitActivity": appWaitActivity,
                }
            )
        elif context == 'local_real':
            options.load_capabilities(
                {
                    # Specify device and os_version for testing
                    "deviceName": "1d0aea237d74",
                    "app": appLocal,
                    "appWaitActivity": appWaitActivity,
                }
            )
        return options


# from pydantic_settings import BaseSettings
#
#
# class Settings(BaseSettings):
#     browserstack_user_name: str
#     browserstack_access_key: str
#     browserstack_url: str
#
# settings = Settings(_env_file='.bstack.env')
