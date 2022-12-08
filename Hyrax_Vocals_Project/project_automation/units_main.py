import os
from selenium.webdriver.common.by import By
import DBnames
import reset
import units_import
import UnitsCheckUpload
import url
import units_table_consts as const
import units_table_elements as ute
import Loading
import shutil
import open_koe as open

CASE1 = [False, False, False]
CASE2 = [True, True, True]
CASE3 = [True, False, False]
CASE4 = [False, True, False]
CASE5 = [False, False, True]

# CONSTS:
FILES_NUM = const.FILES_NUM
START_INDEX = const.START_INDEX
attempts_limit = const.ATTEMPTS_LIMIT
FILE_NAME_PREFIX = const.FILE_NAME_PREFIX
UNITS_CSV_FOLDER = const.UNITS_CSV_FOLDER
MAX_UNITS_IN_FILE = const.MAX_UNITS_IN_FILE
UNITS_URL = URL.UNITS_URL

##################################
# INSERT VALS:
SOLO = False
DATABASE_NAME = DBnames.SMALL_DB2
##################################


# this func calls the reset_func of the rest module
def call_reset(url, database, run=False):
    database_url = open.get_database_url(url, database)
    if run:
        driver = open.open_koe(url=database_url)
        # calling the reset func
        Reset.reset_func(driver, database_url)


# this func checks how many units there are in the units table before uploading units automatically
def units_first_count(database):
    # database = DATABASE_NAME
    print("running 'units_first_count'...")
    driver = open.open_koe(url=UNITS_URL, db_name=database, window_type=const.HEADLESS)
    Loading.loading_widget_wait(driver)
    units_before_upload = driver.find_element(By.ID, ute.units_in_table_id).text
    print("units_before_upload = " + str(units_before_upload))
    driver.quit()
    return units_before_upload


# [NEW ver] this func uploads one units' file into koe, checks if the upload was successful, and deletes uploaded files
def import_base_actions(driver, file_index, units_before_upload, input_file_name, input_file_path, del_file=True):
    # calling the 'upload_units_file' func from 'ImportUnits2' module to upload the given units file
    UnitsImport.upload_units_file(driver, input_file_path, file_index, no_wait=True)
    # refreshing the page
    driver.refresh()
    # printing the current number of units in table before upload for indication
    print(str(units_before_upload) + " units before upload, max = " + str(int(file_index) * MAX_UNITS_IN_FILE))
    # waiting for the page to load
    Loading.loading_widget_wait(driver)
    # checking the upload
    res = UnitsCheckUpload.check_main(driver, input_file_name, input_file_path, units_before_upload)
    # if the upload was successful - delete the units file from 'divided_units_files' folder
    if res and del_file:
        os.remove(input_file_path)
    return res


# [NEW ver] this func calls the 'import_base_actions' func the number of time specified in 'attempts_limit' var.
def import_while_loop(units_before_upload, for_index, database, units_csv_folder):
    # database = DATABASE_NAME
    # initializing variables
    input_file_name = FILE_NAME_PREFIX + str(for_index) + ".csv"
    input_file_path = units_csv_folder + input_file_name
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
        # driver = open_koe(UNITS_URL, db_name)
        # driver = open_koe_headless(UNITS_URL, db_name)
        driver = open.open_koe(url=UNITS_URL, db_name=database, window_type=const.MINI)
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
def import_for_loop(start_index=START_INDEX, files_num=FILES_NUM, database=DATABASE_NAME,
                    units_csv_folder=UNITS_CSV_FOLDER):
    # db_name = DATABASE_NAME
    # check_upload_driver = open_koe_minimized(UNITS_URL, db_name)
    units_before_upload = units_first_count(database)
    # start_index, files_num = 1, 2
    for i in range(start_index, files_num + 1):
        # import_while_loop(units_before_upload, i, check_upload_driver)
        import_while_loop(units_before_upload, i, database, units_csv_folder)


# the main, calls the 'import_for_loop' func
if SOLO:
    import_for_loop()
