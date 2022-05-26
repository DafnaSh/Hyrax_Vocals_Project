import time
from selenium.webdriver.common.by import By
import csv
import os
import os.path
import glob
import UnitsTableElements as ute
import UnitsTableConsts as const
# CONSTS:
UNITS_CSV_FOLDER = const.UNITS_CSV_FOLDER
FILE_NAME_PREFIX = const.FILE_NAME_PREFIX
SCREENSHOT_PATH = const.SCREENSHOT_PATH
OUTPUT_RELOAD_FILES = const.OUTPUT_RELOAD_FILES
FILES_NUM = const.FILES_NUM
EXP_FOLDER_FILES = const.DOWNLOADS_PATH + "*"
TITLES = const.RELOAD_TITLES


# in case the export file not found - this function tries to download it again, called by 'check_main' func
def find_export(lbl_res, driver):
    i = 7
    while lbl_res == 'export file NOT FOUND' and i >= 1:
        try:
            lbl_res = get_units_export(driver)[1]
            time.sleep(2)
            print("searching for file")
            i -= 1
        except:
            print("export file NOT FOUND")


# SUCCESS CHECK 1 - this func checks if all units in table has information in the 'label' and 'label_family' fields
def get_units_export(driver):
    msg = "PASSED"
    # time.sleep(15)
    # clicking the export btn
    driver.find_element(By.XPATH, ute.export_units_table_xpath).click()
    time.sleep(5)
    bool_success = True
    file_found = False
    missing_counter = 0
    # searching for the file in 'Downloads' folder
    files_path = glob.glob(EXP_FOLDER_FILES)
    for file in files_path:
        if file.find("koe-labelling") != -1:
            exp_file = file
            file_found = True
            # if the export file was found - read it and check the labels
            with open(exp_file, 'r', newline='') as infile:
                csv_reader = csv.reader(infile, lineterminator='\n')
                for line in csv_reader:
                    label_family = line[5]
                    label = line[7]
                    # if there is an empty label in one of the unites the check fails
                    if label_family == '' or label == '':
                        bool_success = False
                        missing_counter += 1
            # deleting the export file after reading it
            os.remove(exp_file)
            break
    if bool_success is False:
        msg = str(missing_counter) + " MISSING LABELS"
    elif file_found is False:
        msg = "export file NOT FOUND"
        bool_success = False
    return bool_success, msg


# SUCCESS CHECK 2 - this func checks the number of units in table before and after uploading the file
def unit_table_counter(driver, file_path, units_before_upload):
    msg = "PASSED"
    # time.sleep(15)
    units_after_upload = driver.find_element(By.ID, ute.units_in_table_id).text
    units_added = int(units_after_upload) - int(units_before_upload)
    read_input = open(file_path, 'r').readlines()
    units_in_file = (len(read_input) - 1)
    # if the num of rows currently in Koe unit table smaller than the num of units in the files uploaded failed.
    if int(units_in_file) != int(units_added):
        msg = str(units_added) + "/" + str(units_in_file)
        return False, msg
    return True, msg


# this func writes the upload checks results into a csv file, called by 'check_main' func
def reload_files_csv(line):
    bool_titles = False
    if os.path.isfile(OUTPUT_RELOAD_FILES) is False:
        bool_titles = True
    with open(OUTPUT_RELOAD_FILES, 'a+') as outfile:
        csv_writer = csv.writer(outfile, lineterminator='\n')
        if bool_titles:
            csv_writer.writerow(TITLES)
        csv_writer.writerow(line)


# this func calls all the funcs in the module, called by 'import_base_actions' func in 'Main'
def check_main(driver, file_name, file_path, units_before_upload):
    driver.implicitly_wait(15)
    time.sleep(5)
    check_lbls = get_units_export(driver)
    if check_lbls[0] is False:
        find_export(check_lbls[1], driver)
    check_units = unit_table_counter(driver, file_path, units_before_upload)
    driver.quit()
    if check_units[0] and check_lbls[0]:
        upload_success = True
        status = 'SUCCESS'
    else:
        upload_success = False
        status = 'FAILURE'
    line = [file_name, status, check_lbls[1], check_units[1]]
    print(line)
    reload_files_csv(line)
    return upload_success
