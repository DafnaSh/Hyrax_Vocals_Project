# general:
INPUT_FILES_FOLDER = 'C:\\Users\\dafi2\\Desktop\\ProjectScripts\\scripts_inputs'
OUTPUT_FILES_FOLDER = 'C:\\Users\\dafi2\\Desktop\\ProjectScripts\\scripts_outputs'
PROJECT_AUTO = 'C:\\Users\\dafi2\\Desktop\\ProjectAutomation'

# CopyRecordings:
REC_DIR = 'C:\\Users\\dafi2\\Desktop\\project\\vlads recordings\\FemHyrax Labeled Vocals\\FemHyrax Labeled Vocals'
INPUT_LOGFILE = INPUT_FILES_FOLDER + '\\original_logfile.csv'
OUTPUT_MATCHED_FILES = OUTPUT_FILES_FOLDER + '\\matched_folders_rows.csv'
COPY_TARGERT_FOLDER = 'C:\\Users\\dafi2\\Desktop\\ProjectRecordings\\new_dataset\\'

# CreatekoeUnits:
INPUT_MATCHED_FILES = INPUT_FILES_FOLDER + '\\matched_folders_rows.csv'
OUTPUT_UNITS_FILE = OUTPUT_FILES_FOLDER + '\\koe_units.csv'
COLUMNS_NAMES = ["song", "start_time_ms", "end_time_ms", "label_family", "label_subfamily", "label"]
# LABELS = ["trill", "whine", "coo", "cs", "gr", "gwb", "gwh", "hw", "hc", "htc", "sq", "wb", "gw", "b", "h"]
LABELS = ["TRILL", "WHINE", "COO", "CS", "GR", "GWB", "GWH", "HW", "HC", "HTC", "SQ", "WB", "GW", "B", "H"]

# Divide:
INPUT_UNITS_FILE = INPUT_FILES_FOLDER + '\\koe_units.csv'
#INPUT_UNITS_FILE = INPUT_FILES_FOLDER + '\\koe_units_copy.csv'
#INPUT_UNITS_FILE = 'C:\\Users\\dafi2\\Desktop\\koe_units_copy.csv'
ROWS_LIMIT = 150
OUTPUT_DIV_UNITS = OUTPUT_FILES_FOLDER + '\\divided_units_files'
INPUT_DIV_UNITS = PROJECT_AUTO + '\\divided_units_files'
