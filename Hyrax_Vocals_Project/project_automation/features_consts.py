import numpy as np

feat1 = '/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[2]/div/label[1]/label/input'
agg1 = '/html/body/div[1]/div[2]/div/div/div[2]/div[2]/form/div/div[3]/div/label[1]/label/input'

feat_all = np.arange(1, 37, 1)
feat_combo1 = np.array([6, 9, 13, 24, 34, 35])  # AsInWiki test2
feat_combo2 = np.array([1, 10, 13, 20, 24])  # AsInWiki
feat_combo3 = np.array([3, 4, 6, 13, 25, 32, 33, 34, 35])  # test 3
feat_combo4 = np.array([6, 25, 31, 32, 33, 34, 35])  # new osh
feat_combo5 = np.array([1, 6, 9, 10, 13, 20, 24, 34, 35])  # new feat1+feat2
feat_combo6 = np.array([6, 10, 11, 17, 23, 30, 31, 32, 36])  # a, b
agg_all = np.arange(1, 18, 1)
agg_combo1 = np.array([1, 2, 4])
agg_combo2 = []
agg_combo3 = []
agg_combo4 = np.array([1, 2, 3, 6, 11, 12, 13, 14, 15, 16, 17])  #
agg_combo5 = np.array([1, 2, 3, 13, 14, 15, 16, 17])  #
agg_combo6 = np.array([1, 2, 3, 5, 9, 10, 13, 14, 15, 16, 17])
agg_combo7 = np.array([1, 2, 3, 4, 5, 7, 8, 13, 14, 15, 16, 17])  #
agg_combo8 = np.array([13, 14, 15, 16, 17])  #
agg_combo9 = np.array([1, 2])

test1 = [feat_all, agg_all, 'feat_all_agg_all']
test2 = [feat_all, agg_combo5, 'feat_all_agg_5']  # c
test3 = [feat_all, agg_combo7, 'feat_all_agg_7']
test4 = [feat_all, agg_combo8, 'feat_all_agg_8']
test5 = [feat_combo1, agg_all, 'feat_1_agg_all']
test6 = [feat_combo1, agg_combo1, 'feat_1_agg_1']
test7 = [feat_combo1, agg_combo4, 'feat_1_agg_4']
test9 = [feat_combo2, agg_all, 'feat_2_agg_all']
test10 = [feat_combo3, agg_all, 'feat_3_agg_all']
test11 = [feat_combo3, agg_combo1, 'feat_3_agg_1_']
test12 = [feat_combo4, agg_all, 'feat_4_agg_all']
test13 = [feat_combo4, agg_combo1, 'feat_4_agg_1']
test14 = [feat_combo5, agg_all, 'feat_5_agg_all']
test15 = [feat_combo5, agg_combo1, 'feat_5_agg_1']
test16 = [feat_combo6, agg_combo9, 'feat_6_agg_9']  # a
test17 = [feat_combo6, agg_all, 'feat_6_agg_all']  # b

tests_dict = {'feat_all_agg_all': 'test1',
              'feat_all_agg_5': 'test2',
              'feat_all_agg_7': 'test3',
              'feat_all_agg_8': 'test4',
              'feat_1_agg_all': 'test5',
              'feat_1_agg_1': 'test6',
              'feat_1_agg_4': 'test7',
              'feat_2_agg_1': 'test9',
              'feat_3_agg_all': 'test10',
              'feat_3_agg_1_': 'test11',
              'feat_4_agg_all': 'test12',
              'feat_4_agg_1': 'test13',
              'feat_5_agg_all': 'test14',
              'feat_5_agg_1': 'test15',
              'feat_6_agg_9': 'test16',
              'feat_6_agg_all': 'test17'}

# tests_def = [test1, test2, test3, test4, test10, test11, test12, test13, test16, test17]
tests_def = [test5, test6, test7, test10, test11, test12, test13, test14, test15, test16, test17]
# tests = [test1, test2, test3, test4, test5, test6, test7, test10, test11, test12, test13, test15]
# tests = [test2, test3, test4, test5, test6, test7, test10, test11, test12, test13, test15]
# tests = [test2, test3, test4, test5, test6, test7, test10, test11, test12, test13, test15]
# tests = [test17]
tests = tests_def

# ordination consts:
