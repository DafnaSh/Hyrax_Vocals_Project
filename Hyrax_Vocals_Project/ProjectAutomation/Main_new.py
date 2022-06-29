import filecmp
import glob
import time
import os

import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import selenium.common.exceptions
from selenium.webdriver.support import expected_conditions as EC
import Login
import Reset
import ImportUnits
import ImportUnits2
import CheckUpload
import SelectFeatures
import UnitsTableConsts as const
import UnitsTableElements as ute
import Loading
import shutil
import Helper
import UploadSongs
import CreateDataBase as cdb
import UnitsFromSongs
import FeaturesConsts as fc

CASE1 = [False, False, False]
CASE2 = [True, True, True]
CASE3 = [True, False, False]
CASE4 = [False, True, False]
CASE5 = [False, False, True]


import pandas as pd
# CONSTS for units url:
# DATABASE_NAME = const.DATABASE_NAME
# DATABASE_NAME = const.DATABASE_NAME
# UNITS_URL = const.UNITS_URL
# CONSTS for ImportUnits
FILES_NUM = const.FILES_NUM
START_INDEX = const.START_INDEX
attempts_limit = const.ATTEMPTS_LIMIT
FILE_NAME_PREFIX = const.FILE_NAME_PREFIX
UNITS_CSV_FOLDER = const.UNITS_CSV_FOLDER
TESL_URL = 'https://koe.io.ac.nz/syllables/?database=new_new&#!'
MAX_UNITS_IN_FILE = const.MAX_UNITS_IN_FILE
# UNITS_URL = TESL_URL
DB_URL = "https://koe.io.ac.nz/dashboard/#!"
SONGS_URL = "https://koe.io.ac.nz/songs/?database=|&#!"
UNITS_URL = "https://koe.io.ac.nz/syllables/?database=|&#!"
FEATURES_URL = "https://koe.io.ac.nz/extraction/feature/#!"
ORDINATION_URL = "https://koe.io.ac.nz/extraction/ordination/#!"
DATABASE1 = 'new_dataset'
DATABASE2 = 'new_dataset2'
DATABASE3 = 'small_dataset1'
DATABASE_NAME = DATABASE3


def get_database_url(url, database=None):
    if url.find("database=") != -1 and database is not None:
        split_url = url.split("|")
        database_url = split_url[0] + database + split_url[1]
    else:
        database_url = url
    return database_url


# FOR TESTS
def open_units_table_test():
    driver = webdriver.Chrome()
    driver.implicitly_wait(15)
    wait = WebDriverWait(driver, 60)
    # login to Koe:
    Login.login_func(driver)
    # opening the units' table page in koe:
    url = 'https://koe.io.ac.nz/syllables/?database=new_new&#!'
    driver.get(url)
    Loading.loading_widget_wait(driver)
    # input_file_name = 'units_part_1.csv'
    # input_file_path = UNITS_CSV_FOLDER + input_file_name
    # CheckUpload.check_main(driver, input_file_name, input_file_path, 9450)
    # ImportUnits2.upload_units_file(driver, 1, True)
    # time.sleep(30)
    print("OK")
    return driver


# FOR TESTS
def check_file_import(file_index):
    database = DATABASE_NAME
    file_path = Helper.get_inputfile_path(file_index)
    if file_path != '':
        current_table_count = units_first_count()
        units_in_file = Helper.get_inputfile_count_p(file_path)
        # if current_table_count < units_in_file * i:
        #     print("")
        driver = open_koe(UNITS_URL, database)
        # CheckUpload.check_main(driver, input_file_name, input_file_path, 9450)
        # ImportUnits2.upload_units_file(driver, 1, True)
        # time.sleep(30)
    print("OK")
    #return driver


# FOR TESTS
def check_last_import():
    database = DATABASE_NAME
    driver = webdriver.Chrome()
    driver.implicitly_wait(15)
    wait = WebDriverWait(driver, 60)
    # login to Koe:
    Login.login_func(driver)
    # opening the units' table page in koe:
    url = 'https://koe.io.ac.nz/syllables/?database=new_new&#!'
    driver.get(url)
    Loading.loading_widget_wait(driver)
    # input_file_name = 'units_part_1.csv'
    # input_file_path = UNITS_CSV_FOLDER + input_file_name
    # CheckUpload.check_main(driver, input_file_name, input_file_path, 9450)
    # ImportUnits2.upload_units_file(driver, 1, True)
    # time.sleep(30)
    print("OK")
    return driver


def open_koe(url, database=None):
    database_url = get_database_url(url, database)
    driver = webdriver.Chrome()
    driver.implicitly_wait(15)
    # login to Koe:
    Login.login_func(driver)
    # opening the units' table page in koe:
    driver.get(database_url)
    Loading.loading_widget_wait(driver)
    return driver


def open_koe_headless(url, database=None):
    database_url = get_database_url(url, database)
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    headless_driver = webdriver.Chrome(options=options)
    headless_driver.implicitly_wait(15)
    # login to Koe:
    Login.login_func(headless_driver)
    # opening the units' table page in koe:
    headless_driver.get(database_url)
    Loading.loading_widget_wait(headless_driver)
    return headless_driver


def open_koe_minimized(url, database=None):
    database_url = get_database_url(url, database)
    mini_driver = webdriver.Chrome()
    mini_driver.minimize_window()
    mini_driver.implicitly_wait(15)
    # login to Koe:
    Login.login_func(mini_driver)
    # opening the units' table page in koe:
    mini_driver.get(database_url)
    Loading.loading_widget_wait(mini_driver)
    return mini_driver


def call_reset(url, database, run=False):
    database_url = get_database_url(url, database)
    if run:
        driver = open_koe(database_url)
        # calling the reset func
        Reset.reset_func(driver, database_url)


def units_first_count():
    database = DATABASE_NAME
    print("running 'units_first_count'...")
    driver = open_koe_headless(UNITS_URL, database)
    Loading.loading_widget_wait(driver)
    units_before_upload = driver.find_element(By.ID, ute.units_in_table_id).text
    print("units_before_upload = " + str(units_before_upload))
    driver.quit()
    return units_before_upload


# [NEW ver] this func uploads one units' file into koe, checks if the upload was successful, and deletes uploaded files
def import_base_actions(driver, file_index, units_before_upload, input_file_name, input_file_path, del_file=True):
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
    if res and del_file:
        os.remove(input_file_path)
    return res


# [NEW ver] this func calls the 'import_base_actions' func the number of time specified in 'attempts_limit' var.
def import_while_loop(units_before_upload, for_index):
    database = DATABASE_NAME
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
        # driver = open_koe(UNITS_URL, database)
        # driver = open_koe_headless(UNITS_URL, database)
        driver = open_koe_minimized(UNITS_URL, database)
        attempts_counter += 1
        # getting the current number of units in table before the first upload attempts
        if attempts_counter == 1:
            units_before_upload = driver.find_element(By.ID, ute.units_in_table_id).text
        # receiving the upload result from 'import_base_actions' func
        # res = import_base_actions(driver, for_index, units_before_upload, input_file_name, input_file_path, check_driver)
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
    # database = DATABASE_NAME
    # check_upload_driver = open_koe_minimized(UNITS_URL, database)
    units_before_upload = units_first_count()
    # start_index, files_num = 1, 2
    for i in range(start_index, files_num + 1):
        # import_while_loop(units_before_upload, i, check_upload_driver)
        import_while_loop(units_before_upload, i)


def open_import_songs():
    database = DATABASE_NAME
    # database_name = "small_dataset1"
    driver = open_koe_headless(SONGS_URL, database)
    UploadSongs.upload_songs(driver, database)
    return driver


def open_unit_features(test, select_feat=True, select_ordination=True):
    database = DATABASE2
    driver = open_koe(SONGS_URL, database)

    if select_feat:
        driver.get(FEATURES_URL)
        SelectFeatures.select_features(driver, test)

    if select_ordination:
        driver.get(ORDINATION_URL)
        SelectFeatures.select_ordination(driver, test, database)



    # for i in range(1, 37):
    #     path = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[" + str(i) + "]/label/input"
    #     driver.find_element(By.XPATH, str(path)).click()
    # for i in range(1, 18):
    #     path = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[3]/div/label[" + str(i) + "]/label/input"
    #     driver.find_element(By.XPATH, str(path)).click()
    # time.sleep(60)



def open_create_database(name, fft_val=None):
    driver = open_koe(DB_URL)
    cdb.new_database(driver, name, fft_val)
    return driver


def create_db_with_songs_and_units(db_name, fft_window, output_name, case):
    driver = open_create_database(db_name, fft_window)
    songs_url = "https://koe.io.ac.nz/songs/?database=" + str(db_name) + "&#!"
    driver.get(songs_url)
    Loading.loading_widget_wait(driver)
    UploadSongs.upload_songs(driver)
    time.sleep(5)
    res_file = UploadSongs.download_songs_csv(driver)
    if res_file[0] is True:
        UnitsFromSongs.main(input=res_file[1], output=output_name, case=case)
    # os.remove(res_file[1])


def create_db_with_songs_and_units_outer():
    db_names = ["small_dataset1", "small_dataset2", "small_dataset3", "small_dataset4", "small_dataset5"]
    fft_windows = [None, None, None, None, None]
    outputs = ['koe_units_from_songs1.csv', 'koe_units_from_songs2.csv', 'koe_units_from_songs3.csv',
               'koe_units_from_songs4.csv', 'koe_units_from_songs5.csv']
    cases = [CASE1, CASE2, CASE3, CASE4, CASE5]
    for i in range(len(db_names)):
        create_db_with_songs_and_units(db_names[i], fft_windows[i], outputs[i], cases[i])





# the main, calls the 'import_for_loop' func
if __name__ == '__main__':
    # tests = []
    tests = [fc.test5, fc.test7, fc.test10, fc.test11, fc.test12, fc.test13,
             fc.test14, fc.test15]
    for i in tests:
        open_unit_features(i, False, True)
        print("ordination for: ", i[2])
        time.sleep(120)
    # ddelement.select_by_value('1')


    # driver.get_screenshot_as_file("screenshot.png")
    # import_for_loop()
    # database = 'small_dataset4'
    # database = 'small_dataset4'

    # driver = open_koe_headless(SONGS_URL, database)
    # UploadSongs.upload_songs2(driver, database)

    # feat_all = np.arange(1, 37, 1)
    # print(feat_all)
    # res = filecmp.cmp('C://Users/dafi2/Desktop/New folder/a.wav', 'C://Users/dafi2/Desktop/New folder/c.wav', shallow=False)
    # print(res)
    # exit(1)
    # open_unit_features()
    # time.sleep(120)
    # open_import_songs()
    # PROJ_AUTO_PATH = os.getcwd()
    # print(PROJ_AUTO_PATH)
    # exit(1)
    # call_reset(True)
    # call_reset()
    #t ry3()
    # os.startfile(const.OUTPUT_RELOAD_FILES)



    #############################
    # import_for_loop()
    #############################
    # exit(1)
    # getting the action from user
    # print("Press '1' for ImportUnits or type 'reset' for Reset")  # in cmd enter is ''
    # action = input()
    # if action == '1':
    #     call_import()
    # if action == 'reset':
    #     print("Are you sure you want to reset? [Enter]")  # in cmd enter is ''
    #     action = input()
    #     if action == '':
    #         call_reset()
    #     else:
    #         exit(1)
    # if action == 'resett':
    #     call_reset()

