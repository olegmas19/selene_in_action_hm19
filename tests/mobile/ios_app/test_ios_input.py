from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have


def test_ios_input(ios_mobile_management):

    with step('Вводим текст'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Text Button")).click()
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Text Input")).click().send_keys('hello@browserstack.com')

    with step('Проверяем введенное значение'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Text Input")).should(have.text('hello@browserstack.com'))
