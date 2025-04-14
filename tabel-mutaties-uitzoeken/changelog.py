#!/usr/bin/env python3

import sys
import argparse
from csv import DictReader
from collections import defaultdict
from datetime import datetime, MAXYEAR, timedelta
from tabulate import tabulate

# DDR_Q
#table_name = 'questionnaire'
#partition_column = 'parent_identifier_value'
#key_column = 'identifier_value'
#descr_column = 'item_text'

# Agenda
table_name = 'agenda_afspcode'
partition_column = ''
key_column = 'CODE|AGENDA|SUBAGENDA'
descr_column = 'OMSCHR'

def delta(x, y, ignore=None):
    result = []
    ignore_keys = [] if ignore is None else ignore
    for key in x.keys():
        if key in ignore_keys:
            continue
        if '_UTC_x' not in key and x[key] != y[key]:
            result.append([key, x[key] if x[key] else 'NULL', y[key] if y[key] else 'NULL'])
    return result

def inactive(record):
    if 'Vervallen' in record:
        return record['Vervallen'] == '1'
    elif 'item_status' in record:
        return record['item_status'] == 'inactive'
    else:
        return False

def process_file(filename, begin, end):
    infile = open(filename, 'r', encoding='utf-8-sig')
    window_left, window_right = begin, end

    # Pass 1: read CSV file with and store as 2-level hash table 'change_table'
    if '|' in key_column:
        keys = key_column.split('|')
        key_function = lambda x: '|'.join(x[key] for key in keys)
    else:
        key_function = lambda x: x[key_column]
    reader = DictReader(infile, delimiter=';')
    # change_table is a 2-d matrix of changes:
    # - coordinate 1 is the primary key of a record in the database table
    # - coordinate 2 is the datetime of a change
    change_table = {}
    included, excluded = 0, 0
    encountered = open('encountered', 'w')
    for k, row in enumerate(reader):
        if partition_column in row: # DDR
            if 'Gemstracker' in row['identifier_system'] or 'PEM' in row['identifier_system']:
                excluded += 1
                continue # skip this row
            quest_id = row[partition_column].lower()
            print(quest_id, file=encountered)
            if quest_id in include_ids:
                included += 1
            else:
                excluded += 1
                continue # skip this row
        else:
            included += 1
        # Python raises exception when the seconds component has >3 decimal places
        valid_from = datetime.fromisoformat(row['ValidFrom_UTC_x'].split('.')[0])
        valid_to = datetime.fromisoformat(row['ValidTo_UTC_x'].split('.')[0])
        key = key_function(row)
        if key not in change_table:
            change_table[key] = {}
        change_table[key][valid_from] = row
        if valid_to.year == MAXYEAR:
            change_table[key][valid_to] = row
    # if partition_column:
    #     print(f"included: {included}, excluded: {excluded}")

    # Pass 2: partition change_table on value of 'partition_column'
    change_groups = {}
    if partition_column:
        for key, changes in change_table.items():
            head = changes[list(changes.keys())[0]]
            partition_name = head[partition_column]
            if partition_name not in change_groups:
                change_groups[partition_name] = {}
            change_groups[partition_name][key] = changes
    else:
        change_groups[table_name] = change_table

    # Pass 3: for all partitioned change sets, print delta for all points in the timeline
    # that are in the given time window
    for partition_name in change_groups.keys():
        changes = defaultdict(list)
        # change_table is a 2-d matrix of changes
        # (for one database table, or for one questionnaire in the case of DDR)
        # - coordinate 1 is the primary key of a record in the database table
        # - coordinate 2 is the datetime of a change
        change_table = change_groups[partition_name]
        for key in sorted(change_table.keys()):
            timeline = sorted(change_table[key].keys())
            first, last = timeline[0], timeline[-1]
            if window_left <= first <= window_right:
                record = change_table[key][first]
                status = 'I' if inactive(record) else 'A'
                changes[first].append(f"+{status} {key}|{record[descr_column]}")
            if window_left <= last <= window_right:
                record = change_table[key][last]
                status = 'I' if inactive(record) else 'A'
                changes[last].append(f"-{status} {key}|{record[descr_column]}")
            n = len(timeline)
            for k in range(n-1):
                past, present = timeline[k], timeline[k+1]
                if present < window_left or present > window_right:
                    continue # change outside time window
                past_record, present_record = change_table[key][past], change_table[key][present]
                past_status = 'I' if inactive(past_record) else 'A'
                present_status = 'I' if inactive(present_record) else 'A'
                if past_status == present_status == 'I':
                    continue # question was inactive before and after the change
                difference = delta(past_record, present_record,
                                   ignore=['item_sequence', 'REMINDER', 'GEENDBC', 'ZONDERPAT', 'ISSFBMEETING'])
                if difference:
                    changes[present].append(f" {past_status} {key}|{past_record[descr_column]}")
                    for line in tabulate(difference, headers=['field', 'old', 'new']).splitlines():
                        changes[present].append(f"   {line}")
                    changes[present].append(' ')

        # print results, sorted on time and then on sequence number
        report = []
        for point in sorted(changes.keys()):
            changes_for_point = changes[point]
            n = len(changes_for_point)
            if n > 0:
                report.append(f"Wijzigingen op {point}")
                for change in changes_for_point:
                    report.append(change)
                report.append("\n")
        if report:
            if partition_column:
                lid = partition_name
                label = f"{quest_name[lid]} ({quest_cat[lid]}, {lid})"
            else:
                label = partition_name
            print(f"Wijzigingen in {label}\n==============================")
            print('\n'.join(report))

if __name__ == '__main__':
    # determine default begin and end dates
    today = datetime.now()
    before = today - timedelta(days=30)
    day_to, month_to, year_to = today.day, today.month, today.year
    begin_default = f"{before.year:4}-{before.month:02}-{before.day:02}"
    end_default = f"{today.year:4}-{today.month:02}-{today.day:02}"
    day_from, month_from, year_from = before.day , before.month, before.year
    # process command line
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',      help='input file')
    parser.add_argument('-b', '--begin', help='begin (datetime)', default=begin_default)
    parser.add_argument('-e', '--end',   help='end (datetime)',   default=end_default)
    args = parser.parse_args()
    # extra steps for Questionnaire
    quest_name, quest_cat = {}, {}
    if partition_column:
        # read names/categories
        infile = open('lstdef.csv', 'r')
        reader = DictReader(infile, delimiter=',')
        for row in reader:
            lid = row['LIJSTID']
            quest_name[lid] = row['LIJSTNAAM']
            quest_cat[lid] = row['CATEGORIE']
        # read include file
        with open('include.srt', 'r') as f:
            include_ids = [line.strip() for line in f.readlines()]
    else:
        include_ids = []
    # proces input file
    process_file(args.filename, begin=datetime.fromisoformat(args.begin), end=datetime.fromisoformat(args.end))

