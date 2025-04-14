#!/usr/bin/python3

import json, os
from os.path import join, splitext

def read_file(path: str) -> str:
    """Read entire file, return content as one string.

    Arguments:
        path (str): path to file to read

    Returns:
        text (str): content of file
    """
    with open(path, 'r') as f:
        try:
            text = ''.join(f.readlines())
        except UnicodeError:
            text = ''
            print(f'Unicode error in file {path}')
    return text

def extract_ids(folder: str, filename: str) -> list:
    """Read questionnaire identifiers from 'models' section in JSON specification.

    Arguments:
        folder   (str): path to folder that contains JSON file
        filename (str): name of JSON file

    Returns:
        ids (list): list of questionnaire identifiersNico
    """
    json_name = splitext(filename)[0]
    json_content = read_file(join(folder, filename))
    try:
        ds = json.loads(json_content)
    except json.decoder.JSONDecodeError:
        print(f"{json_name}: invalid JSON\n{json_content}")
        return []
    except UnicodeDecodeError:
        print(f"{json_name}: Unicode error\n{json_content}")
        return []
    if 'models' not in ds:
        return []
    for model in [m for m in ds['models'] if m['model'] == 'Questionnaire']:
        if 'filters' not in model:
            return []
        for fltr in model['filters']:
            if fltr['field'] == 'identifier_value':
                if 'Gemstracker' in fltr['values']:
                    continue
                if fltr['operator'] == '=':
                    return [fltr['values'].strip("'")]
                elif fltr['operator'] == 'IN':
                    # 'values' is in SQL notation, not JSON notation!
                    values = fltr['values'].lower()
                    if 'select' in values:
                        split_values = values.split(' in ')[1].strip()
                        if ' and ' in split_values:
                            split_values = split_values.split(' and ')[0].strip()
                    else:
                        split_values = values
                    ids = [elt.strip().strip("'") for elt in split_values[1:-1].split(',')]
                    for elt in ids:
                        if len(elt) != 10:
                            print(f"{json_name}: unexpected value |{elt}| in\n{values}")
                    return ids
                else:
                    print(f"{json_name}: unexpected operator {fltr['operator']} in\n{fltr}")
                    return []

if __name__ == '__main__':
    identifiers = {}
    for (folder, _, filenames) in os.walk(f"{os.environ['HOME']}/project/dm/dataplatform-publications"):
        for filename in filenames:
            if splitext(filename)[1] == '.json':
                ids = extract_ids(folder, filename)
                if ids is None or ids == []:
                    continue
                for elt in ids:
                    identifiers[elt] = 1
    for elt in identifiers.keys():
        print(elt)
