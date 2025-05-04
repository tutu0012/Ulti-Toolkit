import os
import json

data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'UltiToolKit', '0_0_3_data')
keypressattr_dir = os.path.join(data_dir, 'keypressattr')
isactive_file = os.path.join(keypressattr_dir, 'ISACTIVE.json')

def make_keypressattr_dir():
    os.makedirs(keypressattr_dir, exist_ok=True)

def make_keypressattr_files_in_dir():
    if not os.path.exists(isactive_file):
        with open(isactive_file, 'w') as f:
            json.dump({"active": True}, f)