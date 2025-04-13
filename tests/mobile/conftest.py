import base64
import pytest
import requests
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
from selene import browser
import os
from selene_in_action.selene_in_action_api import AndroidApp
from selene_in_action.resourse import DATA_DIR




@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    result = AndroidApp.get_apk_app()

    browserstack_user_name = os.getenv("BROWSERSTACK_USER_NAME")
    browserstack_access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    browserstack_url = os.getenv("BROWSERSTACK_URL")
    options = UiAutomator2Options().load_capabilities(
        {
            # Specify device and os_version for testing

            "platformName": "android",
            "platformVersion": "9.0",
            "deviceName": "Google Pixel 3",
            "app": result,

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

    # browser.config.driver = webdriver.Remote("http://hub.browserstack.com/wd/hub", options=options)
    browser.config.driver_remote_url = f'http://{browserstack_url}/wd/hub'
    browser.config.driver_options = options

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    yield

    browser.quit()
