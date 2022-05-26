import csv
import shutil
import os
import os.path
import Constants as const
import copy

# this file is the csv of the labeled units, with only rows that their filename matched a file name in the recordings dir
# INPUT_FILE = 'C:\\Users\\dafi2\\Desktop\\project\\matched_folders_rows.csv'
# INPUT_FILE = const.INPUT_MATCHED_FILES
INPUT_FILE = const.INPUT_LOGFILE
# this file is the units file to use in Koe (the INPUT_FILE in a different format)
OUTPUT_FILE = const.OUTPUT_FILES_FOLDER + "\\valid_units.csv"
# OUTPUT_FILE = const.OUTPUT_UNITS_FILE
# a list of the column names in the koe units file
COLUMNS_NAMES = const.COLUMNS_NAMES
# a list of all the calls labels
LABELS = const.LABELS

label_index = 1
start_index = 2
end_index = 3
duration_index = 4
name_index = 5

indices = [label_index, start_index, end_index, duration_index, name_index]

unmatched_lbls_list = []
negative_dur_list = []
long_dur_list = []
duplications_list = []
missing_info_list = []
not_valid_list = []
clean_info_list = []
no_match_list = []
valid_list = []
DUR_LIMIT = 60
FILTER_DUR = True
# FILTER_DUR = False
songs_list = []
contra_list = []
contra_lines = []
valid_clean_final = []
SET_HTC_HC_H = {'HTC', 'HC', 'H'}
SET_GWB_GW = {'GWB', 'GW'}
SET_GWH_HW = {'GWH', 'HW'}
unique_recordings = []

# this func validates the start and end time and the units duration
def duration_validation(line, filter_dur=FILTER_DUR):
    bool_passed = True
    unit_duration = float(line[end_index]) - float(line[start_index])
    if unit_duration <= 0:
        negative_dur_list.append(list)
        bool_passed = False
    if filter_dur:
        if unit_duration > DUR_LIMIT:
            long_dur_list.append(line)
            bool_passed = False
    return bool_passed


# this func finds duplicated units
def find_duplications(line):
    clean_name_line = line.copy()
    clean_name1 = clean_name_line[name_index].split(".wav")[0]
    clean_name2 = clean_name1.split(" ")[0]
    clean_name_line[name_index] = clean_name2
    if clean_name_line in clean_info_list:
        duplications_list.append(line)
        return False, clean_name_line
    else:
        clean_info_list.append(clean_name_line)
        return True, clean_name_line.copy()


# this func validates the units label
def get_label(line):
    matching_lbl = ''
    for i in range(0, len(LABELS)):
        lbl = LABELS[i]
        # if there was a match
        if str(line[label_index]).upper().find(lbl) != -1:
            matching_lbl = lbl
            return True, matching_lbl
    unmatched_lbls_list.append([line, line[label_index]])
    return False, matching_lbl

   
# this function calls all validation funcs
def validation(line):
    res3 = find_duplications(line)
    if res3[0]:
        res1 = duration_validation(line)
        res2 = get_label(line)
        line_lbl = res2[1]
        clean_line = res3[1]
        if res1 and res2[0] and res3[0]:
            clean_line[label_index] = line_lbl
            valid_clean_final.append(clean_line)
            find_unique_recordings(clean_line)
            valid_list.append(line)
            return True, line_lbl, clean_line
        else:
            not_valid_list.append(line)
            # print(line)
            return False, ''
    return False, ''


def find_unique_recordings(clean_line):
    if clean_line[name_index] not in unique_recordings:
        unique_recordings.append(clean_line[name_index])


# this func looking for the same unit with different label
def find_contradicting_lbls():
    clean_list = valid_clean_final
    contra_counter = 0
    for i in range(len(clean_list)):
        for j in range(i+1, len(clean_list)):
            if clean_list[i] != clean_list[j] and clean_list[i][duration_index] == clean_list[j][duration_index]:
                if (clean_list[i][name_index] != clean_list[j][name_index]
                        and clean_list[i][start_index] == clean_list[j][start_index]
                        and clean_list[i][end_index] == clean_list[j][end_index]
                        and clean_list[i][label_index] != clean_list[j][label_index]):
                    contra_counter += 1
                    contra_lines.append(clean_list[i])
                    contra_lines.append(clean_list[j])
                    contra_list.append(str(contra_counter) + ". First line: " + str(clean_list[i])
                                       + ", Second line: " + str(clean_list[j]))


# counting the calls in all valid units
def count_lbls():
    title1 = "\nValid Calls Count"
    title2 = str(title1) + " - After filtering duration [up to " + str(DUR_LIMIT) + " secs]: "
    if FILTER_DUR:
        print(title2)
    else:
        print(str(title1) + ": ")
    # "TRILL": 0, "WHINE": 1, "COO": 2, "CS": 3, "GR": 4, "GWB": 5, "GWH": 6, "HW": 7, "HC": 8, "HTC": 9, "SQ": 10,
    # "WB": 11, "GW":  12, "B": 13, "H": 14
    units_lbls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for u_lbl in lbls_list:
        for lbl in range(len(LABELS)):
            if u_lbl == (LABELS[lbl]):
                units_lbls[lbl] += 1
    for lbl in range(len(LABELS)):
        print("* " + str(LABELS[lbl]) + ": " + str(units_lbls[lbl]))
    print("Grouped Calls:")
    print("HTC + HC + H: " + str(int(units_lbls[9] + units_lbls[8] + units_lbls[14])))
    print("GWB + GW: " + str(int(units_lbls[5] + units_lbls[12])))
    print("GWH + HW: " + str(int(units_lbls[6] + units_lbls[7])))


# opening the input file and creating the output file
lbls_list = []
with open(INPUT_FILE, 'r', newline='') as infile, open(OUTPUT_FILE, 'w', newline='') as outfile:
    csv_reader = csv.reader(infile, lineterminator='\n')
    csv_writer = csv.writer(outfile, lineterminator='\n')
    # csv_writer.writerow(COLUMNS_NAMES)
    valid_counter = 0
    not_valid_counter = 0
    # for each line of the input file go through the LABELS list and search for a match
    # i = 1
    i = 0
    for line in csv_reader:
        if i != 0:
            bool_match = False
            valid_line = validation(line)
            if valid_line[0]:
                bool_match = True
                if line[name_index] not in songs_list:
                    songs_list.append(line[name_index])
                lbl = valid_line[1]
                lbls_list.append(lbl)
                # new_row = create_koe_unit(line, lbl)
                csv_writer.writerow(line)
                valid_counter += 1
            if bool_match is False:
                not_valid_counter += 1
        i += 1
    count_lbls()
    # find_contradicting_lbls()
    # copying the output file into the input files folder
    # shutil.copyfile(OUTPUT_FILE, const.INPUT_UNITS_FILE)

# printing the validity check results
print("\nVALIDITY CHECK RESULTS:")
print("The number of units that passed the validity check: " + str(valid_counter) + ", from "
      + str(len(songs_list)) + " recordings")
# print("The number of unique recordings: " + str(len(unique_recordings)))
print("The number of units that failed the validity check: " + str(not_valid_counter))
print("\nUnits failed due to the flowing reasons: ")
print("* Duplicated units: " + str(len(duplications_list)))
print("after filtering the duplications:")
print("* No matching labels: " + str(len(unmatched_lbls_list)))
# print("* [wasn't filtered] Contracting labels: " + str(len(contra_list)))
print("* Negative duration: " + str(len(negative_dur_list)))
if FILTER_DUR:
    print("* Duration over " + str(DUR_LIMIT) + " secs: " + str(len(long_dur_list)))

#os.system("pause")
exit(1)
