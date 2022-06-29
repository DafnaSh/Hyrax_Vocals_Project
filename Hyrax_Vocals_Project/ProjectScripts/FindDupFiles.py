import csv
import filecmp
import glob
import shutil
import os
import os.path
import Constants as const
PATH = "C://Users/dafi2/Desktop/ProjectRecordings/new_dataset2/"
dup_count = 0
# going through the REC_DIR folders and files
# and creating a list of all the file with the suffix '.wav'
files_path = glob.glob(PATH+'*')
files_names = os.listdir(PATH)
for i in range(len(files_path)):
    for j in range(i+1, len(files_path)):
        res = filecmp.cmp(str(PATH) + str(files_names[i]), str(PATH) + str(files_names[j]), shallow=False)
        if res is True:
            dup_count += 1
print("dup_count", dup_count)

