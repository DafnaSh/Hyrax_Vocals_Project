from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import os.path
import glob

import Login
import UnitsTableElements as ute
import UnitsTableConsts as const
import Loading
import SongsElements as se
import Screenshots
SONGS_PATH = "C://Users/dafi2/Desktop/ProjectRecordings/new trainig set/*"
# SONGS_PATH = "C://Users/dafi2/Desktop/ProjectRecordings/new_dataset2/*"
# SONGS_PATH = "C://Users/dafi2/Desktop/ProjectRecordings/whine/*"
EXP_FOLDER_FILES = const.DOWNLOADS_PATH + "*"


def check_upload(goal_val, database_name, sleep_val=15):
    # sleep_val = 120
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver2 = webdriver.Chrome(options=options)
    # driver2 = webdriver.Chrome()
    driver2.implicitly_wait(15)
    # login to Koe:
    Login.login_func(driver2)
    # opening the units' table page in koe:
    driver2.get(("https://koe.io.ac.nz/songs/?database="+database_name+"&#!"))
    Loading.loading_widget_wait(driver2)
    for i in range(15):
        units_before_upload = driver2.find_element(By.ID, ute.units_in_table_id).text
        print("units = " + str(units_before_upload))
        if units_before_upload == str(goal_val):
            driver2.quit()
            print("break")
            break
        else:
            time.sleep(sleep_val)
            driver2.refresh()
            Loading.loading_widget_wait(driver2)
            # print(units_before_upload)
    # return units_before_upload


def upload_songs(driver, database, songs_path=SONGS_PATH):
    driver.find_element(By.ID, ute.upload_songs_btn_id).click()
    files_path = glob.glob(songs_path)
    outer_counter = 0
    inner_counter = 0
    # files_count = len(os.listdir("C://Users/dafi2/Desktop/ProjectRecordings/new trainig set/"))
    # print(files_count)
    files_list = [file for file in files_path]
    # print(len(files_list))
    # while outer_counter <= len(files_path) - 1:
    print(files_list.index("file_1_812_(2013_06_12-05_45_14)_BSWMUW29297 - Copy.wav"))
    for i in range(2315, len(files_list)):
        print(files_list[i])
        # if outer_counter <= len(files_list):
        if inner_counter <= 99 and outer_counter <= len(files_list) - 1:
            driver.find_element(By.CLASS_NAME, 'dz-hidden-input').send_keys(files_list[i])
            inner_counter += 1
            outer_counter += 1
        else:
            driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div[2]/div[1]/button").click()
            check_upload(outer_counter, database)
            inner_counter = 0
            # time.sleep(5)
    driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div[2]/div[1]/button").click()
    check_upload(outer_counter, database)
    driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div[2]/div[3]/button").click()
    # driver.find_element(By.CLASS_NAME, 'dz-hidden-input').send_keys("C://Users/dafi2/Desktop/project/new_dataset/file_421_(2013_06_10-00_09_07)_BSWMUW47751.wav")
    time.sleep(90)
    # driver.execute_script("document.getElementById('file-upload-form').style.display = null;")


def upload_songs2(driver, database, songs_path=SONGS_PATH):
    driver.find_element(By.ID, ute.upload_songs_btn_id).click()
    files_path = glob.glob(songs_path)
    outer_counter = 0
    inner_counter = 0
    for file in files_path:
        if inner_counter == 100 or outer_counter == len(files_path) - 1:
            driver.find_element(By.XPATH, se.start_btn_xpath).click()
            check_upload(outer_counter, database)
            inner_counter = 0
        driver.find_element(By.CLASS_NAME, se.dz_class).send_keys(file)
        inner_counter += 1
        outer_counter += 1

    driver.find_element(By.XPATH, se.start_btn_xpath).click()
    check_upload(outer_counter, database)
    driver.find_element(By.XPATH, se.close_btn_xpath).click()
    time.sleep(90)


def download_songs_csv(driver, url=None):
    driver.find_element(By.XPATH, "/html/body/div[1]/nav/div[1]/div[5]/button[2]").Click()
    time.sleep(5)
    # searching for the file in 'Downloads' folder
    files_path = glob.glob(EXP_FOLDER_FILES)
    for file in files_path:
        if file.find("koe-sequences") != -1:
            return True, file
    return False, ''


