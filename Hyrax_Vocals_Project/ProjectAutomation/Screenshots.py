from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
import UnitsTableElements as ute
import UnitsTableConsts as const
alerts_names = ["_success", "_warning", "_danger"]


# checking for units recognition success and failure indicators
def is_displayed(element):
    element_display = element.get_attribute('style')
    if str(element_display) != 'display: none;':
        return True
    else:
        return False


def create_name(file_num, action, alert_name):
    return "units_" + str(file_num) + str(action) + str(alert_name)


def only_screenshot(element, el_name):
    path = const.SCREENSHOT_PATH + str(el_name) + ".png"
    element.screenshot(path)


def element_screenshot(element, el_name):
    if is_displayed(element):
        path = const.SCREENSHOT_PATH + str(el_name) + ".png"
        element.screenshot(path)


def get_elements(driver):
    success_element = driver.find_element(By.XPATH, ute.units_success_alert_xpath)
    warning_element = driver.find_element(By.XPATH, ute.units_warning_alert_xpath)
    danger_element = driver.find_element(By.XPATH, ute.units_danger_alert_xpath)
    # creating a list of elements
    alert_elements = [success_element, warning_element, danger_element]
    # creating a list of elements texts
    alert_elements_texts = [success_element.text, success_element.text, danger_element.text]
    # creating a list of elements names
    return alert_elements, alert_elements_texts


def alerts_check(alert_elements, alerts_names, file_num, action):
    for j in range(len(alert_elements)):
        element_screenshot(alert_elements[j], create_name(file_num, action, str(alerts_names[j])))


def after_upload(upload_elements, file_num):
    action = "_upload"
    alerts_check(upload_elements, alerts_names, file_num, action)


def after_process_ver1(success_text, driver, file_num):
    wait = WebDriverWait(driver, 30)
    action = '_process'
    el_name = '_success'
    success_element = driver.find_element(By.XPATH, ute.units_success_alert_xpath)
    try:
        wait.until(lambda x: success_text != success_element.text)
        element_screenshot(success_element, create_name(file_num, action, el_name))
        return False
    except TimeoutException as ex:
        only_screenshot(driver.find_element_by_tag_name('body'), 'unit_' + str(file_num) + '_page')
        print(str(const.exc_timeout) + " 'process success text' doesn't show, do nothing")
        return True


def after_process2(up_elements_text, file_num, driver, wait):
    action = "_process"
    pro_elements = get_elements(driver)[0]
    for j in range(len(pro_elements)):
        if up_elements_text[j] != '':
            print(str(up_elements_text[j]))
            wait.until(lambda x: up_elements_text != pro_elements[j].text)
            if pro_elements[j].text != '':
                name = create_name(file_num, action, str(alerts_names[j]))
                element_screenshot(pro_elements[j], name)
                print(str(pro_elements[j].text))
        elif up_elements_text[j] == '':
            name = create_name(file_num, action, str(alerts_names[j]))
            element_screenshot(pro_elements[j], name)
