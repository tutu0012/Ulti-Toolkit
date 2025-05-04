import os
import json

data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'UltiToolKit', '0_0_3_data')
issetuppedbool_dir = os.path.join(data_dir, 'isSettuped_bool')
issetuppedbool_file = os.path.join(issetuppedbool_dir, 'ISSETUPPED_BOOL.json')

def make_issettuped_dir():
    os.makedirs(issetuppedbool_dir, exist_ok=True)

def make_issettuped_files_in_dir():
    if not os.path.exists(issetuppedbool_file):
        with open(issetuppedbool_file, 'w') as f:
            json.dump({"setupped": False}, f)