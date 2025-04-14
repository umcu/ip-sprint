import json, sys

def process_json(notebook):
    """Clear output cells from Jupyter notebook saved in JSON format."""
    if isinstance(notebook, dict):
        if 'cells' in notebook.keys():
            for cell in notebook['cells']:
                if 'outputs' in cell.keys():
                    cell['outputs'] = []
        else:
            return None
    else:
        return None
    return notebook

"""Clear output cells from Jupyter notebook passed in sys.argv (one file only)"""
# process argument(s)
if len(sys.argv) == 1:
    print('\tError: provide Jupyter notebook file path')
    sys.exit(1)

filename, processor = None, None
for arg in sys.argv[1:]:
    if arg[0] != '-':
        filename = arg
if filename is None:
    print('\tError: no file name')
    sys.exit(1)

extension = filename.lower().split(".")[-1]
if extension == "ipynb":
    processor = process_json
else:
    print('\tError: file should have extension .ipynb')
    sys.exit(1)

# open notebook file
try:
    read_file = open(filename)
except Exception as error:
    print(f"\tError: file cannot be read {error}")
    sys.exit(1)

try:
    contents = json.load(read_file)
except Exception as error:
    print("\tError: contents cannot be parsed {error}")
    sys.exit(1)
read_file.close()

test = True
if test:
    print(f"clean notebook {filename}")
    sys.exit(0)

# process notebook contents, overwrite notebook if successful
contents = processor(contents)
if contents is not None:
    with open(filename, 'w') as write_file:
        json.dump(contents, write_file, indent=1)
else:
    if processor is process_json:
        print("\tError: error in process notebook contents")
    sys.exit(1)

sys.exit(0)