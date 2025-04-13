import pytest
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from selene import browser
import os
from selene_in_action.selene_in_action_api import AndroidApp
from appium import webdriver



@pytest.fixture()
def android_mobile_management():
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
            "appWaitActivity": "org.wikipedia.*",
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

    browser.config.driver = webdriver.Remote(f"http://{browserstack_url}/wd/hub", options=options)
    browser.config.timeout = float(os.getenv("timeout", "10.0"))

    session_id = browser.driver.session_id
    print(session_id)

    yield

    browser.quit()


@pytest.fixture()
def ios_mobile_management():
    browserstack_user_name = os.getenv("BROWSERSTACK_USER_NAME")
    browserstack_access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    browserstack_url = os.getenv("BROWSERSTACK_URL")
    options = XCUITestOptions().load_capabilities(
        {
            "app": "bs://sample.app",
            # Specify device and os_version for testing
            "platformName": "ios",
            "deviceName": "iPhone 11",
            "platformVersion": "13",
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

    browser.config.driver = webdriver.Remote(f"http://{browserstack_url}/wd/hub", options=options)
    browser.config.timeout = float(os.getenv("timeout", "10.0"))

    yield

    browser.quit()
