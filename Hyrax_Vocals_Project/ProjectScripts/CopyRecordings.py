import csv
import shutil
import os.path
import Constants as const

# counts each row in the csv with a matching dir filename
counter_matched_rows = 0
# counts all the wav files in the given dir
counter_dir_files = 0
# counts all the matching files in csv and dir
counter_matched_files = 0
# a list of all wav files path in dir
dir_files_list=[]
# a list of all the matching files in csv and dir
matched_files_list=[]
# REC_DIR is the dir path
ROOTDIR = const.REC_DIR
# INPUT_FILE is the csv file we read from 
INPUT_FILE = const.INPUT_LOGFILE
# OUTPUT_MATCHED_FILES is the csv file we write all the rows in INPUT_FILE with a file name that matched a file name in dir
OUTPUT_MATCHED_FILES = const.OUTPUT_MATCHED_FILES
NEW_DATASET_PATH = const.COPY_TARGERT_FOLDER

# going through the REC_DIR folders and files
# and creating a list of all the file with the suffix '.wav' 
for subdir, dirs, files in os.walk(ROOTDIR):
    for file in dirs:
        for f in files:
            # if the file type is wav
            if f[-4:].lower().find(".wav") != -1:
                p = subdir + "/" + f
                # if the path created from subdir + file name exsists - add the tuple (file name, file path) to "dir_files_list"
                if os.path.isfile(p):
                    dir_files_list.append((f,p))
                    counter_dir_files += 1


# copying the relevant files:
# opening the units csv file as INPUT_FILE and OUTPUT_MATCHED_FILES to write the file names that found both in csv and the dir
with open(INPUT_FILE, 'r', newline='') as infile, open(OUTPUT_MATCHED_FILES, 'w', newline='') as outfile:
    csv_reader = csv.reader(infile, lineterminator='\n')
    csv_writer = csv.writer(outfile, lineterminator='\n')
    counter = 0
    # for each line in the csv: check if its label column isn't empty and if the file name is in "dir_files_list"
    for line in csv_reader:
        counter += 1 
        file_name_csv = line[5]
        if line[1] != '':  
            for i in range(0, len(dir_files_list)):
                if file_name_csv in dir_files_list[i][0]:
                    counter_matched_rows += 1
                    csv_writer.writerow(line)
                    if file_name_csv not in matched_files_list:
                        counter_matched_files += 1
                        matched_files_list.append(file_name_csv)
                        original = dir_files_list[i][1]
                        # target = 'C:/Users/dafi2/Desktop/project/new_dataset/' + dir_files_list[i][0]
                        target = NEW_DATASET_PATH + dir_files_list[i][0]
                        shutil.copyfile(original, target)
                    break
        print(counter)
# copying the output file into the input files folder
shutil.copyfile(OUTPUT_MATCHED_FILES, const.INPUT_MATCHED_FILES)

print("rows with matching file names count: " + str(counter_matched_rows))
print("matched files count: " + str(counter_matched_files))
os.system("pause")