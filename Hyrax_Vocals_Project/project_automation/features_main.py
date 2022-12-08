import time
from selenium.webdriver.common.by import By
import url
import features_consts as FC
import open_koe as open

# CONSTS:
SONGS_URL = URL.SONGS_URL
FEATURES_URL = URL.FEATURES_URL
ORDINATION_URL = URL.ORDINATION_URL


# this func chooses the acoustic features by clicking on their elements
def choosing_feats(driver, feat):
    for i in feat:
        path = '/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[' + str(i) + "]/label/input"
        feat_cb = driver.find_element(By.XPATH, str(path))
        tries = 20
        bool_try_again = True
        while bool_try_again is True and tries >= 1:
            try:
                feat_cb.click()
                bool_try_again = False
            except:
                tries -= 1
                time.sleep(2)
                print('feat exp')


# this func chooses the aggregation method by clicking on their elements
def choosing_aggs(driver, agg):
    for i in agg:
        path = '/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[3]/div/label[' + str(i) + "]/label/input"
        agg_cb = driver.find_element(By.XPATH, str(path))
        tries = 20
        bool_try_again = True
        while bool_try_again is True and tries >= 1:
            try:
                agg_cb.click()
                bool_try_again = False
            except:
                tries -= 1
                time.sleep(2)
                print('agg exp')


# this func select features and aggregation
def select_features(driver, test):
    feat = test[0]
    agg = test[1]
    name = test[2]
    name_filed_id = 'id_name'
    feat_submit_btn_id = 'schedule-btn'

    choosing_feats(driver, feat)
    choosing_aggs(driver, agg)

    driver.find_element(By.ID, name_filed_id).send_keys(str(name))
    time.sleep(5)
    try:
        driver.find_element(By.ID, feat_submit_btn_id).click()
        time.sleep(5)
    except:
        print("couldn't submit")


# this func opens Koe in the features and aggregation page
def open_unit_features(database):
    driver = open.open_koe(url=SONGS_URL, db_name=database)
    # driver = open.open_koe(url=SONGS_URL, db_name=database, window_type=const.HEADLESS)
    driver.get(FEATURES_URL)
    return driver


# this func receives a list of different features and aggregation combinations,
# the function opens koe using the open_unit_features function and chooses features and aggregations using the
# select_features function
def feat_loop(db_name, tests):
    driver = open_unit_features(db_name)
    for test in tests:
        select_features(driver, test)
        print(str(FC.tests_dict[test[2]]), " - ", test[2], ': features selection is done.')
        driver.refresh()
        time.sleep(5)
