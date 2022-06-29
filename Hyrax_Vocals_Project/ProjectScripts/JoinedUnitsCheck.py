import csv
import shutil
import os
import os.path
import Constants as const
import copy

# this file is the csv of the labeled units, with only rows that their filename matched a file name in the recordings dir
# INPUT_FILE = 'C:\\Users\\dafi2\\Desktop\\project\\matched_folders_rows.csv'
# INPUT_FILE = const.INPUT_MATCHED_FILES
INPUT_FILE = const.OUTPUT_FILES_FOLDER + "\\valid_units.csv"
# this file is the units file to use in Koe (the INPUT_FILE in a different format)
OUTPUT_FILE = const.OUTPUT_FILES_FOLDER + "\\valid_unique_units.csv"
OUTPUT_TO_COPY = const.OUTPUT_FILES_FOLDER + "\\unique_unit_files.csv"
OUTPUT_JOINED = const.OUTPUT_FILES_FOLDER + "\\joined_units.csv"
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

joined = []
long_dur_list = []
not_valid_list = []
clean_info_list = []
valid_list = []
good_valid_list = []
DUR_LIMIT = 40
LBLS_DUR_LIMIT = 15
SET_LIMIT_DUR = {'HTC', 'CS', 'GW'}
FILTER_DUR = False
LBLS_DUR = False
# FILTER_DUR = False
songs_list = []
contra_list = []
contra_lines = []
clean_lines_list = []
unique_recordings = []
final_list = []
final_joined_count = []
units_list = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
clean_units_list = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
SET_HTC_HC_H = {'HTC', 'HC', 'H'}
SET_GWB_GW = {'GWB', 'GW'}
SET_GWH_HW = {'GWH', 'HW'}
SET_BAD_LABELS = {'GWHGS', 'GWHGW', 'GWHL', 'GWHM', 'GWHS', 'WHO',  'HWS', 'GWS', 'HWM', 'HWL'}


# this func validates the start and end time and the units duration
def duration_validation(line, clean_line, filter_dur=FILTER_DUR, filter_dur_lbl=LBLS_DUR ):
    bool_passed = True
    unit_duration = float(line[end_index]) - float(line[start_index])
    if filter_dur:
        if unit_duration >= DUR_LIMIT:
            long_dur_list.append(line)
            bool_passed = False
    if filter_dur_lbl:
        if LBLS_DUR:
            if clean_line[label_index] in SET_LIMIT_DUR:
                if line[duration_index] <= LBLS_DUR_LIMIT or find_unique_recordings(clean_line):
                    return True
                else:
                    return False
    return bool_passed, unit_duration


# this func finds duplicated units
def get_clean_line(line, lbl):
    clean_line = line.copy()
    clean_name1 = clean_line[name_index].split(".wav")[0]
    clean_name2 = clean_name1.split(" ")[0]
    clean_line[name_index] = clean_name2
    clean_line[label_index] = lbl
    # clean_lines_list.append(clean_line)
    return clean_line


def filter_joined_unit5(units, clean_units):
    visited_list = []
    approved_list = []
    counter_contained = 0
    counter_crossing = 0
    # for unit, clean_units in range(len(zipped)):
    if len(units) == 0:
        print("\nNo units of label", LABELS[units_list.index(units)])
        final_list.append(approved_list)
        final_joined_count.append(len(approved_list))
        return
    for i in range(len(units)):
        if units[i] not in visited_list:
            for j in range(i+1, len(units)):
                if units[j] not in visited_list:
                    lbl_i = clean_units[i][label_index]
                    lbl_j = clean_units[j][label_index]
                    name_i = units[i][name_index]
                    name_j = units[j][name_index]
                    if lbl_i == lbl_j and name_i == name_j:
                        start_i = float(units[i][start_index])
                        end_i = float(units[i][end_index])
                        dur_i = float(units[i][duration_index])
                        start_j = float(units[j][start_index])
                        end_j = float(units[j][end_index])
                        dur_j = float(units[j][duration_index])
                        if start_i == start_j or (end_i > start_j and end_i >= end_j) or (end_j > start_i and end_j >= end_i):
                            joined.append([units[i], units[j]])
                            counter_contained += 1
                            if dur_j < dur_i:
                                visited_list.append(units[i])
                                break
                            else:
                                visited_list.append(units[j])
                        # elif (end_i > start_j and (start_j + (end_j - end_i)) >= 10) \
                        #         or (end_j > start_i and (start_i + (end_i - end_j)) >= 10):
                        #     print("elif")
                        #     counter_crossing += 1
                        #     visited_list.append(units[i])
                        #     visited_list.append(units[j])
                        #     break
            approved_list.append(units[i])
            visited_list.append(units[i])
    print("\nResults for label", LABELS[units_list.index(units)], "(out of", len(units), "units):")
    # print("units in total:", len(units), "counter_contained", counter_contained, "counter_crossing",
    print("units contained in each other: ", counter_contained, ", unique units count: ", len(approved_list))
    final_list.append(approved_list)
    final_joined_count.append(len(approved_list))


# this func validates the units label
def get_label(line):
    for bad_lbl in SET_BAD_LABELS:
        if str(line[label_index]).upper().find(bad_lbl) != -1:
            return ''
    for i in range(0, len(LABELS)):
        lbl = LABELS[i]
        # if there was a match
        if str(line[label_index]).upper().find(lbl) != -1:
            return lbl


def find_unique_recordings(clean_line):
    if clean_line[name_index] not in unique_recordings:
        unique_recordings.append(clean_line[name_index])
        return True
    return False


# counting the calls in all valid units
def count_lbls2():
    title1 = "\nValid Calls Count"
    title2 = str(title1) + " - After filtering duration [up to " + str(DUR_LIMIT) + " secs]: "
    if FILTER_DUR:
        print(title2)
    else:
        print(str(title1) + ": ")
    # "TRILL": 0, "WHINE": 1, "COO": 2, "CS": 3, "GR": 4, "GWB": 5, "GWH": 6, "HW": 7, "HC": 8, "HTC": 9, "SQ": 10,
    # "WB": 11, "GW":  12, "B": 13, "H": 14
    units_lbls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    total = 0
    for lbl in range(len(LABELS)):
        units_lbls[lbl] = final_joined_count[lbl]
        total += final_joined_count[lbl]
        print("* " + str(LABELS[lbl]) + ": " + str(final_joined_count[lbl]))
    print("Grouped Calls:")
    print("HTC + HC + H: " + str(int(units_lbls[9] + units_lbls[8] + units_lbls[14])))
    print("GWB + GW: " + str(int(units_lbls[5] + units_lbls[12])))
    print("GWH + HW: " + str(int(units_lbls[6] + units_lbls[7])))
    print("\nUnits In Total: ", total)
    return units_list


# counting the calls in all valid units
def lines_by_lbls(line, clean_line):
    for lbl in range(len(LABELS)):
        if clean_line[label_index] == (LABELS[lbl]):
            units_list[lbl].append(line)
            clean_units_list[lbl].append(clean_line)


# def create_koe_unit(line, lbl):
#     # the file name without the suffix '.wav'
#     song_name = line[name_index][:-4]
#     # turning start and end time from sec to msec
#     start_time_ms = str(round(float(line[start_index])*1000))
#     end_time_ms = str(round(float(line[end_index])*1000))
#     # the label from the input file
#     label_family = line[label_index].upper()
#     label_subfamily = ''
#     # the matching label from the LABELS list
#     label = str(lbl)
#     row = [song_name, start_time_ms, end_time_ms, label_family, label_subfamily, label]
#     return row


# opening the input file and creating the output file
lbls_list = []
with open(INPUT_FILE, 'r', newline='') as infile, open(OUTPUT_FILE, 'w', newline='') as outfile, \
        open(OUTPUT_JOINED, 'w', newline='') as outfile2, open(OUTPUT_TO_COPY, 'w', newline='') as outfile3:
    csv_reader = csv.reader(infile, lineterminator='\n')
    csv_writer = csv.writer(outfile, lineterminator='\n')
    csv_writer2 = csv.writer(outfile2, lineterminator='\n')
    csv_writer3 = csv.writer(outfile3, lineterminator='\n')
    # csv_writer.writerow(COLUMNS_NAMES)
    # for each line of the input file go through the LABELS list and search for a match
    i = 0
    for line in csv_reader:
        if i != 0:
            line_lbl = get_label(line)
            clean_line = get_clean_line(line, line_lbl)
            dur_res = duration_validation(line, clean_line)[0]
            if dur_res:
                lines_by_lbls(line, clean_line)
                clean_lines_list.append(clean_line)
                valid_list.append(line)
                lbls_list.append(line_lbl)
                if line[name_index] not in songs_list:
                    songs_list.append(line[name_index])
                    csv_writer3.writerow([line[name_index]])
        i += 1
    zipped_lists = zip(units_list, clean_units_list)
    for units, clean_units in zipped_lists:
        filter_joined_unit5(units, clean_units)
        # if LABELS[units_list.index(units)] == 'COO':
        #     break
    # print(joined)
    for i in joined:
        # print("\n", i[0], i[1])
        csv_writer2.writerow([i[0], i[1]])
    # exit(1)
    count_lbls2()
    for sub_list in final_list:
        for line in sub_list:
            csv_writer.writerow(line)
    # for i in joined:
    #     csv_writer.writerow(i[0], i[1])

# filter_joined_unit4()
# # printing the validity check results
# print("\nVALIDITY CHECK RESULTS:")
# print("The number of units that passed the validity check: " + str(valid_counter) + ", from "
#       + str(len(songs_list)) + " recordings")
# print("The number of unique recordings: " + str(len(unique_recordings)))
# print("The number of units that failed the validity check: " + str(not_valid_counter))
# print("\nUnits failed due to the flowing reasons: ")
# print("* Duplicated units: " + str(len(duplications_list)))
# print("after filtering the duplications:")
# print("* No matching labels: " + str(len(unmatched_lbls_list)))
# # print("* [wasn't filtered] Contracting labels: " + str(len(contra_list)))
# print("* Negative duration: " + str(len(negative_dur_list)))
# if FILTER_DUR:
#     print("* Duration over " + str(DUR_LIMIT) + " secs: " + str(len(long_dur_list)))
#
# #os.system("pause")
exit(1)
