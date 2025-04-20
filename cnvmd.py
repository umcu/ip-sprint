#!/usr/bin/python3

import sys, glob, os, argparse

def convert_mdfile(filename):
    with open(filename, 'r') as readfile:
        lines = readfile.readlines()
    os.rename(filename, filename+'-')
    with open(filename, 'w') as writefile:
        tbody_seen = False
        for line in lines:
            l = line.strip()
            if l in ['</tbody>', '</table>']:
                continue  # skip two closing tags
            if l == '<tbody>':
                if tbody_seen:
                    continue  # keep only first tbody
                else:
                    print(l, file=writefile)
                    tbody_seen = True
            elif l in ['<table>', '<thead>', '</thead>', '<tbody>']:
                if tbody_seen:
                    continue  # keep only first occurrence
                else:
                    print(l, file=writefile)
            elif l.startswith('<tr><th>'):  # add class
                print(l.replace('<tr>', '<tr class="thead-bg">'), file=writefile)
            else:
                print(l, file=writefile)
        print('</tbody>\n</table>', file=writefile)

def restore_mdfile(filename):
    os.remove(filename)
    os.rename(filename+'-', filename)

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--convert', help='convert .md files', action='store_true')
parser.add_argument('-u', '--undo',    help='undo conversion',   action='store_true')
args = parser.parse_args()
if args.convert:
    for filename in glob.glob("*.md"):
        convert_mdfile(filename)
elif args.undo:
    for filename in glob.glob("*.md"):
        restore_mdfile(filename)
else:
    print("Available options: --convert, --undo")
