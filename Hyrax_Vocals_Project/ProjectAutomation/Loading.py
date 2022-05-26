import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import UnitsTableElements as ute
import UnitsTableConsts as const
EXIT = const.EXIT
BREAK = const.BREAK
CONTINUE = const.CONTINUE
NOTHING = const.NOTHING
REFRESH = const.REFRESH


# LOADING WIDGET
def loading_widget_wait(driver, sleep_val=10):
    sleep_val = 5
    try:
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, ute.loading_widget_id)))
        WebDriverWait(driver, 60).until(EC.invisibility_of_element((By.ID, ute.loading_widget_id)))
    except ElementNotVisibleException:
        time.sleep(int(sleep_val))
        print(str(const.exc_elemNotVisible) + " loading widget not visible/invisible, waiting 10 secs...")
    except TimeoutException:
        time.sleep(int(sleep_val))
        print(str(const.exc_timeout) + " loading widget not visible/invisible, waiting 10 secs...")
    except NoSuchElementException:
        time.sleep(int(sleep_val))
        print(str(const.exc_noSuchElement) + "loading widget not visible/invisible, waiting 10 secs...")


# ImportUnits - CLICKING IMPORT
def try_click_import(msg, driver, wait_val=3):
    wait = WebDriverWait(driver, int(wait_val))
    try:
        driver.find_element(By.ID, ute.open_import_csv_btn_id).click()
        wait.until(EC.visibility_of_element_located((By.ID, ute.process_btn_id)))
        return BREAK
    except TimeoutException:
        print(str(const.exc_timeout) + str(msg))
        return CONTINUE
    except ElementNotVisibleException:
        print(str(const.exc_elemNotVisible) + str(msg))
        return CONTINUE
    except ElementNotInteractableException:
        print(str(const.exc_elemNotInteractable) + str(msg))
        return CONTINUE
    except ElementClickInterceptedException:
        print(str(const.exc_elemClick) + str(msg))
        return CONTINUE


# ImportUnits - UNITS UPLOAD
def try_units_upload(driver, wait_val=30):
    wait = WebDriverWait(driver, int(wait_val))
    try:
        wait.until(EC.visibility_of_element_located((By.ID, ute.importable_rows_id)))
        return CONTINUE
    except TimeoutException:
        print(str(const.exc_timeout) + " importable rows are not visible, exiting func...")
        return EXIT
    except ElementNotVisibleException:
        print(str(const.exc_elemNotVisible) + " importable rows are not visible, exiting func...")
        return EXIT


# ImportUnits - CLICK PROCESS
def try_click_process(driver, wait_val=10):
    wait = WebDriverWait(driver, int(wait_val))
    try:
        wait.until(EC.element_to_be_clickable((By.ID, ute.process_btn_id))).click()
    except TimeoutException:
        print(str(const.exc_timeout) + " process btn not clickable , no action [refresh is next]")
    except ElementNotInteractableException:
        print(str(const.exc_elemNotInteractable) + " process btn not clickable, no action [refresh is next]")
    return NOTHING


#  ImportUnits - AFTER IMPORT
def wait_after_import(driver, wait_val=60):
    wait = WebDriverWait(driver, int(wait_val))
    try:
        wait.until(EC.invisibility_of_element((By.ID, ute.upload_csv_modal_id)))
        loading_widget_wait(driver)
    except TimeoutException:
        print(str(const.exc_timeout) + " upload_csv_modal didn't close, no action [refresh is next]")
        # driver.refresh()
    except ElementNotVisibleException:
        print(str(const.exc_elemNotVisible) + " upload_csv_modal didn't close/open, no action [refresh is next]")
        # driver.refresh()
    except NoSuchElementException:
        print(str(const.exc_noSuchElement) + " upload_csv_modal didn't close/open, no action [refresh is next]")
