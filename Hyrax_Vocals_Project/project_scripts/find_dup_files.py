import filecmp
import glob
import os.path

PATH = '<INSERT PATH>'

# this script checks if there are copies of the same file under different name in the desired path.

# going through the REC_DIR folders and files
# and creating a list of all the file with the suffix '.wav'
files_path = glob.glob(PATH + '*')
files_names = os.listdir(PATH)
dup_count = 0
# comparing between all the files in the path, in order to see if there are duplicated files under different names
for i in range(len(files_path)):
    for j in range(i + 1, len(files_path)):
        res = filecmp.cmp(str(PATH) + str(files_names[i]), str(PATH) + str(files_names[j]), shallow=False)
        if res is True:
            dup_count += 1
print('dup_count', dup_count)
