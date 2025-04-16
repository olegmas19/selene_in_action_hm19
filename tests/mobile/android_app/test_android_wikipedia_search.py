import os

from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from dotenv import load_dotenv
from selene import browser, have


def test_android_search_appium(android_mobile_management):

    with step('Type search'):
        browser.all((AppiumBy.CLASS_NAME, 'android.widget.Button')).second.should(have.text('Skip')).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Appium')

    with step('Verify content found'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Appium'))

def test_android_search_github_click_link(android_mobile_management):

    with step('Type search'):
        browser.all((AppiumBy.CLASS_NAME, 'android.widget.Button')).second.should(have.text('Skip')).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('GitHub')

    with step('Verify content found and click the link'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('GitHub')).click()


def test_env():
    load_dotenv('.env.bstack')
    browserstack_user_name = os.getenv('BROWSERSTACK_USER_NAME')
    browserstack_access_key = os.getenv('BROWSERSTACK_ACCESS_KEY')
    print(browserstack_user_name)
    print(browserstack_access_key)

