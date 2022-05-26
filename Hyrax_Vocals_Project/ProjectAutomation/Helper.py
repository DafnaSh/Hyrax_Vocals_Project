import UnitsTableConsts as const
import os
import os.path


def get_inputfile_name(file_index):
    return const.FILE_NAME_PREFIX + str(file_index) + ".csv"


def get_inputfile_path(file_index):
    file_path = const.UNITS_CSV_FOLDER + get_inputfile_name(file_index)
    if os.path.isfile(file_path):
        return file_path
    return ''


def get_failedfile_path(file_index):
    file_path = const.FAILED_PATH + get_inputfile_name(file_index)
    if os.path.isfile(file_path):
        return file_path
    return ''


def find_file(file_index):
    path1 = get_inputfile_path(file_index)
    path2 = get_failedfile_path(file_index)
    if path1 != '':
        print("the file is in 'divided_units_files' folder")
        return path1
    elif path2 != '':
        print("the file is in 'failed' folder")
        return path2
    else:
        print('file not found')
        return ''


def get_inputfile_count_i(file_index):
    file_path = get_inputfile_path(file_index)
    read_input = open(file_path, 'r').readlines()
    units_in_file = (len(read_input) - 1)
    return units_in_file


def get_inputfile_count_p(file_path):
    read_input = open(file_path, 'r').readlines()
    units_in_file = (len(read_input) - 1)
    return units_in_file
