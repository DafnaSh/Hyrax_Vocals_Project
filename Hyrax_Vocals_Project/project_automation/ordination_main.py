import time
import Loading
import url
import features_consts as FC
import open_koe as open

# CONSTS:
SONGS_URL = URL.SONGS_URL
FEATURES_URL = URL.FEATURES_URL
ORDINATION_URL = URL.ORDINATION_URL


# this func receives the driver, classification (test) and thr db name, and get calls the loading function with the
# name the classification to select from the drop doen
def select_ordination(driver, test, dataset):
    name = test[2]
    dd_val = str(dataset) + ': ' + name + ' | Completed'
    Loading.ordination_selection2(driver, dd_val)


# this func opens the select ordination page in Koe
def open_select_ordination(database):
    driver = open.open_koe(url=SONGS_URL, db_name=database)
    driver.get(ORDINATION_URL)
    return driver


# this func receives the db name and the list of classification names to ordinate ('tests')
def ord_loop(db_name, tests):
    driver = open_select_ordination(db_name)
    for test in tests:
        select_ordination(driver, test, db_name)
        print(str(FC.tests_dict[test[2]]), ' - ', test[2], ': ordination is done.')
        time.sleep(5)
