from pathlib import Path
import allure
import pytest
import allure_commons
from appium.options.ios import XCUITestOptions
from dotenv import load_dotenv
from selene import browser, support
import os
import config
from appium import webdriver
from utils.attach import add_screenshot, add_video, add_xml

env_file = Path(__file__).parent / f".env.bstack"
load_dotenv(env_file)


@pytest.fixture(scope="function")
def android_mobile_management():

    with allure.step("Init app session"):
        browser.config.driver = webdriver.Remote(
            config.remote_url_config(), options=config.to_driver_options()
        )

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


@pytest.fixture(scope="function")
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
