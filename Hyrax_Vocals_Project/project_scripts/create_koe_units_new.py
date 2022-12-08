import csv
import shutil
import constants as const

# this file is the csv of the labeled units, with only rows their filename matched a file name in the recordings dir
INPUT_FILE = const.OUTPUT_FILES_FOLDER + '\\<INSERT CSV FILE NAME>'
# this file is the units file to use in Koe (the INPUT_FILE in a different format)
OUTPUT_FILE = const.OUTPUT_UNITS_FILE
# a list of the column names in the koe units file
COLUMNS_NAMES = const.COLUMNS_NAMES
# a list of all the calls labels
LABELS = const.LABELS


# this func receives a line in the input file and the label of the line,
# and returns the information in the required format.
def format_row(csv_row, unit_lbl):
    # the file name without the suffix '.wav'
    song_name = csv_row[5][:-4]
    # turning start and end time from sec to msec
    start_time_ms = str(round(float(csv_row[2]) * 1000))
    end_time_ms = str(round(float(csv_row[3]) * 1000))
    # the label from the input file
    label_family = csv_row[1].upper()
    label_subfamily = ''
    # the matching label from the LABELS list
    label = str(unit_lbl).upper()
    new_row = [song_name, start_time_ms, end_time_ms, label_family, label_subfamily, label]
    return new_row


# this func goes through the input file lines. if the line has a valid label the function writes the line in the right
# format (using format_row func) in the output file.
def main():
    # opening the input file and creating the output file
    with open(INPUT_FILE, 'r', newline='') as infile, open(OUTPUT_FILE, 'w', newline='') as outfile:
        csv_reader = csv.reader(infile, lineterminator='\n')
        csv_writer = csv.writer(outfile, lineterminator='\n')
        csv_writer.writerow(COLUMNS_NAMES)
        match_counter, no_match_counter = 0, 0
        # for each line of the input file go through the LABELS list and search for a match
        for line in csv_reader:
            bool_match = False
            check_label(line, csv_writer)
            for lbl in LABELS:
                # if there was a match
                if line[1].upper().find(lbl) != -1:
                    bool_match = True
                    new_line = format_row(line, lbl)
                    csv_writer.writerow(new_line)
                    match_counter += 1
                    break
            if bool_match is False:
                no_match_counter += 1

    # copying the output file into the input files folder
    shutil.copyfile(OUTPUT_FILE, const.INPUT_UNITS_FILE)

    print('rows transferred into the new units table: ' + str(match_counter))
    print('rows without matching labels: ' + str(no_match_counter))


if __name__ == '__main__':
    main()
