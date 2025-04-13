import allure
import pytest

# from allure_commons._allure import StepContext
import allure_commons
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions

# from requests import session
from selene import browser, support
import os
from selene_in_action.selene_in_action_api import AndroidApp
from appium import webdriver
from utils.attach import add_screenshot, add_video, add_xml


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
    with allure.step("Init app session"):
        browser.config.driver = webdriver.Remote(
            f"http://{browserstack_url}/wd/hub", options=options
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

    browser.config.driver = webdriver.Remote(
        f"http://{browserstack_url}/wd/hub", options=options
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
