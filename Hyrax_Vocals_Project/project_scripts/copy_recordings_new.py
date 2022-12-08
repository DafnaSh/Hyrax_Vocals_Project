import csv
import glob
import shutil
import os.path
import constants as const

# this script copy files from one location to another using a cvs file containing the files names,
# the origin path and the target path.

# REC_DIR is the dir path
ROOT_DIR = const.COPY_TARGERT_FOLDER
# INPUT_FILE: the csv file we read from
INPUT_FILE = const.OUTPUT_FILES_FOLDER + '\\<INSERT CSV FILE NAME>'
# OUTPUT_MATCHED_FILES: the csv file we write the rows in INPUT_FILE with a file name that matched a file name in dir
OUTPUT_MATCHED_FILES = const.OUTPUT_MATCHED_FILES
NEW_DATASET_PATH = const.COPY_TARGERT_FOLDER2


# this func copy a file form the dir (original location) to the desired location (target)
def copy_file_to_target(dir_file):
    original = dir_file[1]
    target = NEW_DATASET_PATH + dir_file[0]
    shutil.copyfile(original, target)


# this func checks if a file was copied already form dir to target
def check_if_file_name_unique(file_name, unique_files_list):
    if file_name not in unique_files_list:
        unique_files_list.append(file_name)
        return True
    return False


# this func compare between a file's name in dir_files_list (the files in the original location)
# and a file's names in INPUT_FILE. if the names are the same, the file listed in the INPUT_FILE exists in dir.
def compare_csv_to_dir(name_from_csv, name_from_dir, csv_line, csv_writer):
    if name_from_csv in name_from_dir[0]:
        csv_writer.writerow(csv_line)
        return True
    return False


# going through the REC_DIR folders and files
# and creating a list of all the file with the suffix '.wav'
def get_dir_files_names():
    # counter_dir_files variable counts all the wav files in the given dir ("original location")
    counter_dir_files = 0
    # dir_files_list variable is a list of all wav files path in dir
    origi_dir_files_list = []
    files_path = glob.glob(ROOT_DIR + '*')
    for file in files_path:
        # if the file type is wav
        if file[-4:].lower().find(".wav") != -1:
            p = file
            f = file.split("\\")[-1]
            # if the path created from subdir + file name exists: add the tuple (file name, file path) to dir_files_list
            if os.path.isfile(p):
                origi_dir_files_list.append((f, p))
                counter_dir_files += 1
    return origi_dir_files_list


# the main func: opens csv files, gets a files names list of the files in dir, compares the names in the input
# and in dir list, writes the output and copy files (using the funcs above)
def main():
    dir_files_list = get_dir_files_names()
    # counts each row in the csv with a matching dir filename
    counter_matched_rows = 0
    # counts all the matching files in csv and dir
    counter_matched_files = 0
    # a list of all the matching files in csv and dir
    matched_files_list = []

    # opening the units csv file as INPUT_FILE and creating the OUTPUT_MATCHED_FILES file.
    with open(INPUT_FILE, 'r', newline='') as infile, open(OUTPUT_MATCHED_FILES, 'w', newline='') as outfile:
        csv_reader = csv.reader(infile, lineterminator='\n')
        csv_writer = csv.writer(outfile, lineterminator='\n')
        # for each line in the csv: check if the file name is in "dir_files_list"
        for line in csv_reader:
            file_name_csv = line[0]
            for i in range(0, len(dir_files_list)):
                file_from_dir = dir_files_list[i]
                is_file_in_dir = compare_csv_to_dir(file_name_csv, file_from_dir, line, csv_writer)
                if is_file_in_dir:
                    counter_matched_rows += 1
                    is_file_unique = check_if_file_name_unique(file_name_csv, matched_files_list)
                    if is_file_unique:
                        counter_matched_files += 1
                        copy_file_to_target(file_from_dir)
                    break
    # copying the output file into the input files folder
    # shutil.copyfile(OUTPUT_MATCHED_FILES, const.INPUT_MATCHED_FILES)

    print('rows with matching file names count: ' + str(counter_matched_rows))
    print('matched files count: ' + str(counter_matched_files))
    # os.system("pause")


if __name__ == '__main__':
    main()
