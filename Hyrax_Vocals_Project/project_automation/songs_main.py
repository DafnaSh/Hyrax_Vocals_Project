import units_table_consts as const
import songs_upload
import open_koe as open
import url

# CONSTS:
SONGS_URL = URL.SONGS_URL
EXP_FOLDER_FILES = const.DOWNLOADS_PATH + '*'


# this func receives the db name and the songs files to upload path, opens Koe and calling the upload_songs2 function
# from SongsUpload module.
def open_import_songs(db_name, songs_folder):
    driver = open.open_koe(url=SONGS_URL, db_name=db_name, window_type=const.HEADLESS)
    # driver = open.open_koe(SONGS_URL, db_name)
    SongsUpload.upload_songs2(driver, db_name, songs_folder)
    return driver
