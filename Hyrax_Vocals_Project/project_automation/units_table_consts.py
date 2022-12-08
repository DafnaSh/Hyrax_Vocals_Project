import os.path
import re
import Helper

# PROJ PATH:
PROJ_AUTO_PATH = os.getcwd()

# open koe
HEADLESS = 'headless'
MINI = 'mini'

# import
UNITS_CSV_FOLDER = PROJ_AUTO_PATH + '/divided_units_files/'  # import + reset
FILE_NAME_PREFIX = 'units_part_'
SCREENSHOTS_FOLDER = PROJ_AUTO_PATH + '/alerts_screenshots/'
SCREENSHOT_PATH = SCREENSHOTS_FOLDER + 'alert_'
OUTPUT_RELOAD_FILES = PROJ_AUTO_PATH + '/reupload_files.csv'  # import + reset
DOWNLOADS_PATH = 'C://Users/dafi2/Downloads/'  # import + reset
FAILED_PATH = PROJ_AUTO_PATH + '/failed/'

# songs
SONGS_PATH = '<INSERT PATH>'

# reset
PROJECT_SCRIPTS_UNITS = '<INSERT PATH>'

# checkUpload:
RELOAD_TITLES = ['file_name', 'status', 'check_units', 'check_lbls']

# main
DATABASE_NAME = 'new_dataset'
UNITS_URL = 'https://koe.io.ac.nz/syllables/?database=' + str(DATABASE_NAME) + "&#!"
FILES_NUM = len(next(os.walk(UNITS_CSV_FOLDER))[2])
if FILES_NUM != 0:
    files_names = os.listdir(UNITS_CSV_FOLDER)
    files_indices = []
    for i in files_names:
        file_num = re.findall('[\d]+', str(i))[0]
        files_indices.append(int(file_num))
    files_indices.sort()
    START_INDEX = files_indices[0]
else:
    START_INDEX = 0
    print('No Units Files In Directory')
    exit(1)
ATTEMPTS_LIMIT = 3

# loading:
EXIT = 'exiting func'
BREAK = 'break'
CONTINUE = 'continue'
NOTHING = 'nothing'
REFRESH = 'refresh'

exc_timeout = 'exception: [Timeout]'
exc_elemNotInteractable = 'exception: [NotIntractable]'
exc_elemNotVisible = 'exception: [notVisible]'
exc_elemClick = 'exception: [ClickIntercepted]'
exc_noSuchElement = 'exception: [NoSuchElement]'

MAX_UNITS_IN_FILE = Helper.get_inputfile_count_i(START_INDEX)