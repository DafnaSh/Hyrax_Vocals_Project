import time

import numpy as np

from selenium.webdriver.common.by import By

feat1 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[1]/label/input"
feat2 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[2]/label/input"
feat3 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[3]/label/input"
feat4 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[4]/label/input"
feat5 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[5]/label/input"
feat6 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[6]/label/input"
feat7 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[7]/label/input"
feat8 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[8]/label/input"
feat9 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[9]/label/input"
feat10 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[10]/label/input"
feat11 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[11]/label/input"
feat12 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[12]/label/input"
feat13 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[13]/label/input"
feat14 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[14]/label/input"
feat15 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[15]/label/input"
feat16 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[16]/label/input"
feat17 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[17]/label/input"
feat18 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[18]/label/input"
feat19 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[19]/label/input"
feat20 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[20]/label/input"
feat21 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[21]/label/input"
feat22 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[22]/label/input"
feat23 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[23]/label/input"
feat24 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[24]/label/input"
feat25 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[25]/label/input"
feat26 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[26]/label/input"
feat27 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[27]/label/input"
feat28 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[28]/label/input"
feat29 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[29]/label/input"
feat30 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[30]/label/input"
feat31 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[31]/label/input"
feat32 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[32]/label/input"
feat33 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[33]/label/input"
feat34 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[34]/label/input"
feat35 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[35]/label/input"
feat36 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[36]/label/input"

agg1 = "/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[3]/div/label[1]/label/input"

feat_all = np.arange(1, 37, 1)
feat_combo1 = np.array([6, 9, 13, 24, 34, 35])  # AsInWiki test2
# feat_combo2 = np.array([1, 10, 13, 20, 24])  # AsInWiki
feat_combo3 = np.array([3, 4, 6, 13, 25, 32, 33, 34, 35])  # test 3
feat_combo4 = np.array([6, 25, 31, 32, 33, 34, 35])  # new osh
feat_combo5 = np.array([1, 6, 9, 10, 13, 20, 24, 34, 35])  # new feat1+feat2
agg_all = np.arange(1, 18, 1)
agg_combo1 = np.array([1, 2, 4])
agg_combo2 = []
agg_combo3 = []
agg_combo4 = np.array([1, 2, 3, 6, 11, 12, 13, 14, 15, 16, 17])  #
agg_combo5 = np.array([1, 2, 3, 13, 14, 15, 16, 17])  #
agg_combo6 = np.array([1, 2, 3, 5, 9, 10, 13, 14, 15, 16, 17])
agg_combo7 = np.array([1, 2, 3, 4, 5, 7, 8, 13, 14, 15, 16, 17])  #
agg_combo8 = np.array([13, 14, 15, 16, 17])  #

test1 = [feat_all, agg_all, 'feat_all_agg_all']
test2 = [feat_all, agg_combo5, 'feat_all_agg_5']
test3 = [feat_all, agg_combo7, 'feat_all_agg_7']
test4 = [feat_all, agg_combo8, 'feat_all_agg_8']
test5 = [feat_combo1, agg_all, 'feat_1_agg_all']
test6 = [feat_combo1, agg_combo1, 'feat_1_agg_1']
test7 = [feat_combo1, agg_combo4, 'feat_1_agg_4']
# test9 = [feat_combo2, agg_all, 'feat_2_agg_1' ]
test10 = [feat_combo3, agg_all, 'feat_3_agg_all']
test11 = [feat_combo3, agg_combo1, 'feat_3_agg_1_']
test12 = [feat_combo4, agg_all, 'feat_4_agg_all']
test13 = [feat_combo4, agg_combo1, 'feat_4_agg_1']
test14 = [feat_combo5, agg_all, 'feat_5_agg_all']
test15 = [feat_combo5, agg_combo1, 'feat_5_agg_1']

# tests = [test1, test2, test3, test4, test5, test6, test7, test10, test11, test12, test13, test15]
tests = [test2, test3, test4, test5, test7, test10, test11, test12, test13, test14, test15]





