import time
from selenium.webdriver.common.by import By


# this func receives the driver and features and aggregation combination to select in Koe
def select_features(driver, test):
    time.sleep(5)
    feat = test[0]
    agg = test[1]
    name = test[2]
    for i in feat:
        path = '/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[' + str(i) + ']/label/input'
        time.sleep(5)
        driver.find_element(By.XPATH, str(path)).click()
    for i in agg:
        path = '/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[3]/div/label[' + str(i) + ']/label/input'
        driver.find_element(By.XPATH, str(path)).click()
    driver.find_element(By.ID, 'id_name').send_keys(str(name))
    driver.find_element(By.ID, 'schedule-btn').click()




