import csv
import constants as const

# this file is the csv of the labeled units, only with rows their filename matched a file name in the recordings dir
INPUT_FILE = const.INPUT_LOGFILE
# this file is the units file to use in Koe (the INPUT_FILE in a different format)
OUTPUT_FILE = const.OUTPUT_FILES_FOLDER + '\\valid_units.csv'
# this file is a list of the unique relevant wav files
OUTPUT_TO_COPY = const.OUTPUT_FILES_FOLDER + '\\files_to_copy.csv'
# a list of the column names in the koe units file
COLUMNS_NAMES = const.COLUMNS_NAMES
# a list of all the calls labels
LABELS = const.LABELS
# the indices of the columns of the input file [LABEL_INDEX, START_INDEX, END_INDEX, DURATION_INDEX, NAME_INDEX]
LABEL_INDEX = 1
START_INDEX = 2
END_INDEX = 3
DURATION_INDEX = 4
NAME_INDEX = 5
# duration_validation constants
DUR_LIMIT = 60
FILTER_DUR = True
# FILTER_DUR = False
# units labels constants
SET_HTC_HC_H = const.SET_HTC_HC_H
SET_GWB_GW = const.SET_GWB_GW
SET_GWH_HW = const.SET_GWH_HW
SET_BAD_LABELS = {'GWHGS', 'GWHGW', 'GWHL', 'GWHM', 'GWHS', 'WHO', 'HWS', 'GWS', 'HWM', 'HWL'}

# lists initialization
unmatched_lbls_list = []
negative_dur_list = []
long_dur_list = []
duplications_list = []
not_valid_list = []
clean_info_list = []
valid_list = []
songs_list = []
contra_list = []
contra_lines = []
valid_clean_final = []
unique_recordings = []


# this func validates the start and end time and the units duration
def duration_validation(line, filter_dur=FILTER_DUR):
    bool_passed = True
    unit_duration = float(line[END_INDEX]) - float(line[START_INDEX])
    if unit_duration <= 0:
        negative_dur_list.append(list)
        bool_passed = False
    if filter_dur:
        if unit_duration >= DUR_LIMIT:
            long_dur_list.append(line)
            bool_passed = False
    return bool_passed, unit_duration


# this func finds duplicated units
def find_duplications(line):
    clean_name_line = line.copy()
    clean_name1 = clean_name_line[NAME_INDEX].split(".wav")[0]
    clean_name2 = clean_name1.split(" ")[0]
    clean_name_line[NAME_INDEX] = clean_name2
    if clean_name_line in clean_info_list:
        duplications_list.append(line)
        return False, clean_name_line
    else:
        clean_info_list.append(clean_name_line)
        return True, clean_name_line.copy()


# this func validates the units label
def get_label(line):
    for bad_lbl in SET_BAD_LABELS:
        if str(line[LABEL_INDEX]).upper().find(bad_lbl) != -1:
            return False, ''
    matching_lbl = ''
    for i in range(0, len(LABELS)):
        lbl = LABELS[i]
        # if there was a match
        if str(line[LABEL_INDEX]).upper().find(lbl) != -1:
            matching_lbl = lbl
            return True, matching_lbl
    unmatched_lbls_list.append([line, line[LABEL_INDEX]])
    return False, matching_lbl


# this function calls all validation funcs
def validation(line):
    res3 = find_duplications(line)
    if res3[0]:
        res1 = duration_validation(line)
        res2 = get_label(line)
        line_lbl = res2[1]
        clean_line = res3[1]
        if res1[0] and res2[0] and res3[0]:
            clean_line[LABEL_INDEX] = line_lbl
            valid_clean_final.append(clean_line)
            find_unique_recordings(clean_line)
            valid_list.append(line)
            return True, line_lbl, clean_line
        else:
            not_valid_list.append(line)
            return False, ''
    return False, ''


# this func creates a list of files with unique "clean" name (without "copy" in it)
def find_unique_recordings(clean_line):
    if clean_line[NAME_INDEX] not in unique_recordings:
        unique_recordings.append(clean_line[NAME_INDEX])
        return True
    return False


# this func looking for the same unit with different label
def find_contradicting_lbls():
    clean_list = valid_clean_final
    contra_counter = 0
    for i in range(len(clean_list)):
        for j in range(i + 1, len(clean_list)):
            if clean_list[i] != clean_list[j] and clean_list[i][DURATION_INDEX] == clean_list[j][DURATION_INDEX]:
                if (clean_list[i][NAME_INDEX] != clean_list[j][NAME_INDEX]
                        and clean_list[i][START_INDEX] == clean_list[j][START_INDEX]
                        and clean_list[i][END_INDEX] == clean_list[j][END_INDEX]
                        and clean_list[i][LABEL_INDEX] != clean_list[j][LABEL_INDEX]):
                    contra_counter += 1
                    contra_lines.append(clean_list[i])
                    contra_lines.append(clean_list[j])
                    contra_list.append(str(contra_counter) + '. First line: ' + str(clean_list[i])
                                       + ', Second line: ' + str(clean_list[j]))


# counting the calls in all valid units
def count_lbls(labels_list):
    title1 = '\nValid Calls Count'
    title2 = str(title1) + ' - After filtering duration [up to ' + str(DUR_LIMIT) + ' secs]: '
    if FILTER_DUR:
        print(title2)
    else:
        print(str(title1) + ': ')
    # "TRILL": 0, "WHINE": 1, "COO": 2, "CS": 3, "GR": 4, "GWB": 5, "GWH": 6, "HW": 7, "HC": 8, "HTC": 9, "SQ": 10,
    # "WB": 11, "GW":  12, "B": 13, "H": 14
    units_lbls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for u_lbl in labels_list:
        for lbl in range(len(LABELS)):
            if u_lbl == (LABELS[lbl]):
                units_lbls[lbl] += 1
    for lbl in range(len(LABELS)):
        print('* ' + str(LABELS[lbl]) + ': ' + str(units_lbls[lbl]))
    print('Grouped Calls:')
    print('HTC + HC + H: ' + str(int(units_lbls[9] + units_lbls[8] + units_lbls[14])))
    print('GWB + GW: ' + str(int(units_lbls[5] + units_lbls[12])))
    print('GWH + HW: ' + str(int(units_lbls[6] + units_lbls[7])))


# printing the validity check results
def print_validation_results(valid_counter, songs_list, not_valid_counter):
    # printing the validity check results
    print('\nVALIDITY CHECK RESULTS:')
    print('The number of units that passed the validity check: ' + str(valid_counter) + ', from '
          + str(len(songs_list)) + ' recordings')
    print('The number of unique recordings: ' + str(len(unique_recordings)))
    print('The number of units that failed the validity check: ' + str(not_valid_counter))
    print('\nUnits failed due to the flowing reasons: ')
    print('* Duplicated units: ' + str(len(duplications_list)))
    print('after filtering the duplications:')
    print('* No matching labels: ' + str(len(unmatched_lbls_list)))
    # print("* [wasn't filtered] Contracting labels: " + str(len(contra_list)))
    print('* Negative duration: ' + str(len(negative_dur_list)))
    if FILTER_DUR:
        print('* Duration over ' + str(DUR_LIMIT) + ' secs: ' + str(len(long_dur_list)))


# opening the input file and creating the output files
def main():
    lbls_list = []
    with open(INPUT_FILE, 'r', newline='') as infile, open(OUTPUT_FILE, 'w', newline='') as outfile, \
            open(OUTPUT_TO_COPY, 'w', newline='') as outfile2:
        csv_reader = csv.reader(infile, lineterminator='\n')
        csv_writer = csv.writer(outfile, lineterminator='\n')
        csv_writer2 = csv.writer(outfile2, lineterminator='\n')
        valid_counter, not_valid_counter, i = 0, 0, 0

        # for each line of the input file go through the LABELS list and search for a match
        for line in csv_reader:
            if i != 0:
                bool_match = False
                valid_line = validation(line)
                if valid_line[0]:
                    bool_match = True
                    if line[NAME_INDEX] not in songs_list:
                        songs_list.append(line[NAME_INDEX])
                        csv_writer2.writerow([line[NAME_INDEX]])
                    lbl = valid_line[1]
                    lbls_list.append(lbl)
                    csv_writer.writerow(line)
                    valid_counter += 1
                if bool_match is False:
                    not_valid_counter += 1
            i += 1
        count_lbls(lbls_list)
        # find_contradicting_lbls()
        # copying the output file into the input files folder
        # shutil.copyfile(OUTPUT_FILE, const.INPUT_UNITS_FILE)

    print_validation_results(valid_counter, songs_list, not_valid_counter)


if __name__ == '__main__':
    main()
