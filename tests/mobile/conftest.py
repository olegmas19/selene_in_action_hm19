import allure
import pytest

# from allure_commons._allure import StepContext
import allure_commons
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from dotenv import load_dotenv

# from requests import session
from selene import browser, support
import os

# from config import settings
import config
from selene_in_action.resourse import DATA_DIR

from selene_in_action.selene_in_action_api import AndroidApp
from appium import webdriver
from utils.attach import add_screenshot, add_video, add_xml


@pytest.fixture(scope='function')
def android_mobile_management():

    with allure.step("Init app session"):
        load_dotenv('.bstack.env')
        browserstack_user_name = os.getenv('BROWSERSTACK_USER_NAME')
        browserstack_access_key = os.getenv('BROWSERSTACK_ACCESS_KEY')
        print(browserstack_user_name)
        print(browserstack_access_key)
        browser.config.driver = webdriver.Remote(config.remote_url_config(), options=config.to_driver_options())

    browser.config.timeout = float(os.getenv("timeout", "10.0"))
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    session_id = browser.driver.session_id
    add_screenshot(browser.config)
    add_xml(browser.config)


    with allure.step("Tear down app session"):
        browser.quit()

    # if config.context == 'browserstack':
    #     add_video(session_id)


@pytest.fixture(scope='function')
def ios_mobile_management():
    # browserstack_user_name = os.getenv("BROWSERSTACK_USER_NAME")
    # browserstack_access_key = os.getenv("BROWSERSTACK_ACCESS_KEY")
    # browserstack_url = os.getenv("BROWSERSTACK_URL")
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
                "userName": config.browserstack_user_name,
                "accessKey": config.browserstack_access_key,
            },
        }
    )

    browser.config.driver = webdriver.Remote(
        f"http://{config.browserstack_url}/wd/hub", options=options
    )
    browser.config.timeout = float(os.getenv("timeout", "10.0"))
    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    session_id = browser.driver.session_id
    add_screenshot(browser.config)
    add_xml(browser.config)
    add_video(session_id)

    with allure.step("Tear down app session"):
        browser.quit()
