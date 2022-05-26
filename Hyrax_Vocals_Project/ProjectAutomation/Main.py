import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import Login
import Reset
import ImportUnits2
import CheckUpload
import UnitsTableConsts as const
import UnitsTableElements as ute
import Loading
import shutil
# CONSTS for units url:
DATABASE_NAME = const.DATABASE_NAME
UNITS_URL = const.UNITS_URL
# CONSTS for ImportUnits
FILES_NUM = const.FILES_NUM
START_INDEX = const.START_INDEX
attempts_limit = const.ATTEMPTS_LIMIT
FILE_NAME_PREFIX = const.FILE_NAME_PREFIX
UNITS_CSV_FOLDER = const.UNITS_CSV_FOLDER
MAX_UNITS_IN_FILE = const.MAX_UNITS_IN_FILE


# this func opens Koe in the Unit Table page
def open_units_table_final(headless=False):
    # setting the driver
    if headless:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(15)
    else:
        driver = webdriver.Chrome()
        driver.implicitly_wait(15)
    # login to Koe:
    Login.login_func(driver)
    # opening the units' table page in koe:
    driver.get(UNITS_URL)
    Loading.loading_widget_wait(driver)
    return driver


def call_reset(run=False):
    if run:
        driver = open_units_table_final()
        # calling the reset func
        Reset.reset_func(driver)


def units_first_count():
    print("running 'units_first_count'...")
    driver = open_units_table_final(headless=True)
    Loading.loading_widget_wait(driver)
    units_before_upload = driver.find_element(By.ID, ute.units_in_table_id).text
    print("units_before_upload = " + str(units_before_upload))
    driver.quit()
    return units_before_upload


# [OLD ver] the three funcs combined
def import_for_while_action_old():
    units_before_upload = units_first_count()
    for i in range(START_INDEX, FILES_NUM + 1):
        input_file_name = FILE_NAME_PREFIX + str(i) + ".csv"
        input_file_path = UNITS_CSV_FOLDER + input_file_name
        attempts_counter = 0
        upload_next = False
        print("\nFile No. " + str(i))
        while upload_next is False and attempts_counter < attempts_limit:
            attempts_counter += 1
            driver = open_units_table_final()
            if attempts_counter == 1:
                units_before_upload = driver.find_element(By.ID, ute.units_in_table_id).text
            ImportUnits2.upload_units_file_1(driver, i, True)
            driver.refresh()
            print(str(units_before_upload) + " units before upload, max = " + str(int(i) * 150))
            Loading.loading_widget_wait(driver)
            res = CheckUpload.check_main(driver, input_file_name, input_file_path, units_before_upload)
            if res:
                os.remove(input_file_path)
                upload_next = True
            else:
                print("attempts counter: " + str(attempts_counter))
        if attempts_counter >= attempts_limit and upload_next is False:
            print('FAILING to upload ' + str(input_file_name))
            shutil.move(input_file_path, const.FAILED_PATH + str(input_file_name))


# [NEW ver] this func uploads one units' file into koe, checks if the upload was successful and deletes uploaded files
def import_base_actions(driver, file_index, units_before_upload, input_file_name, input_file_path):
    # calling the 'upload_units_file' func from 'ImportUnits2' module to upload the given units file
    ImportUnits2.upload_units_file(driver, input_file_path, file_index, no_wait=True)
    # refreshing the page
    driver.refresh()
    # printing the current number of units in table before upload for indication
    print(str(units_before_upload) + " units before upload, max = " + str(int(file_index) * MAX_UNITS_IN_FILE))
    # waiting for the page to load
    Loading.loading_widget_wait(driver)
    # checking the upload
    res = CheckUpload.check_main(driver, input_file_name, input_file_path, units_before_upload)
    # if the upload was successful - delete the units file from 'divided_units_files' folder
    if res:
        os.remove(input_file_path)
    return res


# [NEW ver] this func calls the 'import_base_actions' func the number of time specified in 'attempts_limit' var.
def import_while_loop(units_before_upload, for_index):
    # initializing variables
    input_file_name = FILE_NAME_PREFIX + str(for_index) + ".csv"
    input_file_path = UNITS_CSV_FOLDER + input_file_name
    # making sure the input file is in the given file path
    if os.path.isfile(input_file_path) is False:
        return None
    # initializing variables
    attempts_counter = 0
    upload_next = False
    # printing the file num for indication
    print("\nFile No. " + str(for_index))
    # the attempt_loop
    while upload_next is False and attempts_counter < attempts_limit:
        driver = open_units_table_final()
        attempts_counter += 1
        # getting the current number of units in table before the first upload attempts
        if attempts_counter == 1:
            units_before_upload = driver.find_element(By.ID, ute.units_in_table_id).text
        # receiving the upload result from 'import_base_actions' func
        res = import_base_actions(driver, for_index, units_before_upload, input_file_name, input_file_path)
        if res:
            upload_next = True
            return True
        else:
            # printing the failed attempts count for indication
            print("attempts counter: " + str(attempts_counter))
    if attempts_counter >= attempts_limit and upload_next is False:
        # printing the file num for indication
        print('FAILING to upload ' + str(input_file_name))
        shutil.move(input_file_path, const.FAILED_PATH + str(input_file_name))
        return False


# [NEW ver] this func calls the 'import_while_loop' for each file in the given 'start_index' and 'files_num' range
def import_for_loop(start_index=START_INDEX, files_num=FILES_NUM):
    units_before_upload = units_first_count()
    for i in range(start_index, files_num + 1):
        import_while_loop(units_before_upload, i)


# the main, calls the 'import_for_loop' func
if __name__ == '__main__':
    # calling the import process
    import_for_loop()
    # opening the upload results file
    os.startfile(const.OUTPUT_RELOAD_FILES)
    exit(1)
