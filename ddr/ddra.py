#!/usr/bin/env python3

from csv import DictReader

def read_table(filename):
    with open(filename) as csvfile:
        reader = DictReader(csvfile, delimiter=',')
        result = []
        for row in reader:
            result.append(row)
        return result

ddra = read_table('ddr_a_type31.csv')
candidates = [row for row in ddra if 'antwoordenid' in row['ANTWOORD']]
row = candidates[0]
print(row['ANTWOORD'])
for elt in row['ANTWOORD'].split(','):
    print(elt)
