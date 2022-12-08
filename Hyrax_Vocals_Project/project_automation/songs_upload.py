import time
from selenium.webdriver.common.by import By
import glob
import url
import units_table_elements as ute
import Loading
import songs_elements as se
import open_koe as open
import units_table_consts as const


# this func receives the number of files to be uploaded, the db name and the number of seconds to wait
# between the upload checks. the function checks when the files uploaded are done loading to Koe.
def check_upload2(goal_val, database_name, sleep_val=15):
    driver2 = open.open_koe(url=URL.SONGS_URL, db_name=database_name, window_type=const.HEADLESS)
    for i in range(15):
        units_before_upload = driver2.find_element(By.ID, ute.units_in_table_id).text
        if units_before_upload == str(goal_val):
            driver2.quit()
            print('songs imported successfully.')
            return True
        else:
            time.sleep(sleep_val)
            driver2.refresh()
            Loading.loading_widget_wait(driver2)
    return False


# this func receives the driver, database name and the files path and uploads all the files in the files path to koe.
# only 100 files can be uploaded at once to Koe.
def upload_songs2(driver, database, songs_path):
    driver.find_element(By.ID, ute.upload_songs_btn_id).click()
    files_path = glob.glob(songs_path)
    outer_counter = 0
    inner_counter = 0
    for file in files_path:
        if inner_counter == 100 or outer_counter == len(files_path) - 1:
            driver.find_element(By.XPATH, se.start_btn_xpath).click()
            up_res = check_upload2(outer_counter, database)
            if up_res:
                return up_res
            inner_counter = 0
        driver.find_element(By.CLASS_NAME, se.dz_class).send_keys(file)
        inner_counter += 1
        outer_counter += 1

    driver.find_element(By.XPATH, se.start_btn_xpath).click()
    check_upload2(outer_counter, database)
    driver.find_element(By.XPATH, se.close_btn_xpath).click()
    driver.quit()
