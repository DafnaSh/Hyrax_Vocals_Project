import constants as const

# this script splits a csv file to sub files with a certain number of columns (determined by ROWS_LIMIT value)

# the file to split into subfiles
INPUT_FILE = const.INPUT_UNITS_FILE
# number of rows in each file
ROWS_LIMIT = const.ROWS_LIMIT
# the prefix of the files' names
file_name = const.OUTPUT_DIV_UNITS + '\\units_part_'

# opening the input file
csvfile = open(INPUT_FILE, 'r').readlines()
# files counter
file_num = 1
# counting the number of rows to split
for i in range(1, len(csvfile)):
    if i % ROWS_LIMIT == 1:
        # if this is not the first file created,
        # add the names of the columns to the current output file
        if i != 0:
            output_file = open(file_name + str(file_num) + '.csv', 'a+')
            output_file.writelines(csvfile[0])
            output_file.close()
        # adding the relevant rows from the input file
        output_file = open(file_name + str(file_num) + '.csv', 'a+')
        output_file.writelines(csvfile[i:i + ROWS_LIMIT])
        file_num += 1
        print(i)
        i += ROWS_LIMIT

print(str(file_num - 1) + ' files were created')

# copying all the output files into the 'ProjectAutomation'
# shutil.copytree(const.OUTPUT_DIV_UNITS, const.INPUT_DIV_UNITS)
