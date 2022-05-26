import csv
import shutil
import os
import os.path
import Constants as const

# this file is the csv of the labeled units, with only rows that their filename matched a file name in the recordings dir
# INPUT_FILE = 'C:\\Users\\dafi2\\Desktop\\project\\matched_folders_rows.csv'
INPUT_FILE = const.INPUT_MATCHED_FILES
# this file is the units file to use in Koe (the INPUT_FILE in a different format)
OUTPUT_FILE = const.OUTPUT_UNITS_FILE
# a list of the column names in the koe units file
COLUMNS_NAMES = const.COLUMNS_NAMES
# a list of all the calls labels
LABELS = const.LABELS
cs_set = {"cs", "c"}


bad_times_counter = 0
# opening the input file and creating the output file
with open(INPUT_FILE, 'r', newline='') as infile, open(OUTPUT_FILE, 'w', newline='') as outfile:
    csv_reader = csv.reader(infile, lineterminator='\n')
    csv_writer = csv.writer(outfile, lineterminator='\n')
    csv_writer.writerow(COLUMNS_NAMES)
    match_counter = 0
    no_match_counter = 0
    # for each line of the input file go through the LABELS list and search for a match 
    for line in csv_reader:
        bool_match = False
        for lbl in LABELS:
            # if there was a match
            if line[1].lower().find(lbl) != -1:
                bool_match = True
                if lbl in cs_set:
                    lbl = "cs"
                # the file name without the suffix '.wav'
                song_name = line[5][:-4]
                # turning start and end time from sec to msec
                start_time_ms = str(round(float(line[2])*1000))
                end_time_ms = str(round(float(line[3])*1000))
                if int(end_time_ms) - int(start_time_ms) <= 0:
                    bad_times_counter += 1
                    break
                # the label from the input file
                label_family = line[1].upper()
                label_subfamily = ''
                # the matching label from the LABELS list
                label = str(lbl).upper()
                new_row = [song_name, start_time_ms, end_time_ms, label_family , label_subfamily, label]
                csv_writer.writerow(new_row)
                match_counter += 1 
                break
        if bool_match is False:
            no_match_counter += 1
# copying the output file into the input files folder
shutil.copyfile(OUTPUT_FILE, const.INPUT_UNITS_FILE)

print("bad times: " + str(bad_times_counter))
print("rows transferred into the new units table: " + str(match_counter))
print("rows without matching labels: " + str(no_match_counter))
os.system("pause")

