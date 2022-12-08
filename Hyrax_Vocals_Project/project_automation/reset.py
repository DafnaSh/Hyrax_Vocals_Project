import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import glob
import shutil
import units_table_elements as ute
import units_table_consts as const

SCREENSHOTS_FOLDER_FILES = const.SCREENSHOTS_FOLDER + "*"
OUTPUT_RELOAD_FILES = const.OUTPUT_RELOAD_FILES
ORIGI_UNITS_FOLDER = const.PROJECT_SCRIPTS_UNITS
TARGET_UNITS_FOLDER = const.UNITS_CSV_FOLDER
TARGET_UNITS_FOLDER_FILES = const.UNITS_CSV_FOLDER + "*"
FAILED_PATH_FILES = const.FAILED_PATH + "*"


# deleting units:
def reset_units(driver, url):
    if driver.current_url == const.UNITS_URL:
        wait = WebDriverWait(driver, 15)
        time.sleep(10)
        units_uploaded_element = wait.until(EC.visibility_of_element_located((By.ID, ute.units_in_table_id)))
        units_uploaded_text = units_uploaded_element.text
        if str(units_uploaded_text) != '0':
            wait.until(EC.element_to_be_clickable((By.XPATH, ute.checkbox_xpath))).click()
            driver.find_element(By.ID, 'delete-segments-btn').click()
            driver.find_element(By.ID, 'dialog-modal-yes-button').click()
            time.sleep(5)
            print("units table reset is done")
        else:
            print('units table is already empty')
    else:
        print('WRONG URL')
    driver.quit()


# deleting screenshots
def reset_screenshots():
    files_path = glob.glob(SCREENSHOTS_FOLDER_FILES)
    for file in files_path:
        os.remove(file)
    print('screenshots deletion is done')


# deleting reload file
def reset_reload_file():
    if os.path.isfile(OUTPUT_RELOAD_FILES):
        os.remove(OUTPUT_RELOAD_FILES)
        print('reload file was deleted')
    else:
        print('reload file not found')


# replacing the existing units files of 'ProjectAutomation' with the units files from 'ProjectScripts'
def reset_units_files():
    # deleting the exiting units files
    files_path = glob.glob(TARGET_UNITS_FOLDER_FILES)
    for file in files_path:
        os.remove(file)
    os.rmdir(TARGET_UNITS_FOLDER)
    # copying all the units files
    shutil.copytree(ORIGI_UNITS_FOLDER, TARGET_UNITS_FOLDER)
    print('units reset is done')


# deleting failed units
def reset_failed_units():
    files_path = glob.glob(FAILED_PATH_FILES)
    for file in files_path:
        os.remove(file)
    print('failed units deletion is done')


# this function calls all the reset functions
def reset_func(driver, url, case=None):
    # reset_units(driver, url)  # 1. deleting all units in Koe units table
    reset_screenshots()  # 2. deleting all screenshots
    reset_reload_file()  # 3. deleting the reload file
    reset_units_files()  # 4. copying the units files
    reset_failed_units()  # 5. deleting failed units
    print('reset is done')
