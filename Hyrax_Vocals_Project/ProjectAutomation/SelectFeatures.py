import time
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import FeaturesConsts as fc
import Loading
from selenium.webdriver.support.select import Select


def select_features(driver, test):
    feat = test[0]
    agg = test[1]
    name = test[2]
    for i in feat:
        path = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[" + str(i) + "]/label/input"
        driver.find_element(By.XPATH, str(path)).click()
    for i in agg:
        path = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[3]/div/label[" + str(i) + "]/label/input"
        driver.find_element(By.XPATH, str(path)).click()
    driver.find_element(By.ID, 'id_name').send_keys(str(name))
    driver.find_element(By.ID, 'schedule-btn').click()
    # select_ordination(driver, test)



def select_ordination(driver, test, dataset):
    name = test[2]
    dd_val = str(dataset) + ": " + name + " | Completed"
    Loading.ordination_selection(driver, dd_val)
    # driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[1]/div').click()
    # driver.find_element(By.LINK_TEXT, name).click()
    # driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[1]/div/div[1]/input').send_keys(str(name) + Keys.ENTER)
    driver.find_element(By.ID, 'id_method_2').click()
    # driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div/div/button').click()



