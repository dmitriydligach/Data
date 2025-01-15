#! /usr/bin/env python3
import pandas, string, os

NOTES_CSV = 'MimicIII/Source/NOTEEVENTS.csv'
OUT_DIR = 'Notes'
BATCH_SIZE = 25000

def notes_to_flat_files():
  """Split input into files grouped in several directories"""

  notes_csv = os.path.join(base_path, NOTES_CSV)
  out_dir = os.path.join(OUT_DIR)

  df = pandas.read_csv(notes_csv, dtype='str')

  # fields in NOTEEVENT.csv:
  # "ROW_ID","SUBJECT_ID","HADM_ID","CHARTDATE","CHARTTIME",
  # "STORETIME","CATEGORY","DESCRIPTION","CGID","ISERROR","TEXT"

  for row, adm, cat, desc, cgid, text in \
    zip(df.ROW_ID, df.HADM_ID, df.CATEGORY, df.DESCRIPTION, df.CGID, df.TEXT):

    # get something like note type to include in file name
    note_type = desc.replace('/', '_').replace(' ', '_').lower()

    # does adm+note_type uniquely identify a file?
    # out_path = f'{out_dir}/{int(row) // BATCH_SIZE}/{row}-{note_type}.txt'
    out_path = f'{out_dir}/{int(row) // BATCH_SIZE}/{adm}-{note_type}.txt'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    outfile = open(out_path, 'w')

    printable = ''.join(c for c in text if c in string.printable)

    outfile.write(printable)

if __name__ == "__main__":

  base_path = os.environ['DATA_ROOT']
  notes_to_flat_files()
