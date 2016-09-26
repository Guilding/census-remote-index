import csv
import simplejson as json
from decimal import Decimal
from collections import OrderedDict
from itertools import groupby

column_descriptions = []

# Read the sequence/table lookup
with open('ACS_1yr_Seq_Table_Number_Lookup.txt', 'r', encoding='latin-1') as f:
    reader = csv.DictReader(f)
    for line in reader:
        if line['Subject Area']:
            table_id = line['Table ID']

            universe_line = next(reader)
            universe = universe_line['Table Title'].lstrip('Universe:  ')
            # print("{}: {}".format(line['Table ID'], universe))
        elif line['Line Number']:
            line_no = line['Line Number']
            if line_no.endswith('.5'):
                # Skip the aggregation columns for now
                continue
            line_no = int(line_no)

            column_descriptions.append((table_id, line_no, 'estimate'))
            column_descriptions.append((table_id, line_no, 'error'))

# Read the adjoined table
with open('adjoined.csv', 'r', encoding='latin-1') as f:
    reader = csv.reader(f)
    for line in reader:
        one_doc = OrderedDict()

        geoid = line[48]
        geom_name = line[49]
        one_doc['geography'] = OrderedDict([
            ('geoid', geoid),
            ('name', geom_name),
        ])

        tables = OrderedDict()
        for table_id, columns in groupby(zip(column_descriptions, line[53:]), lambda f: f[0][0]):
            table = OrderedDict([
                ('estimate', OrderedDict()),
                ('error', OrderedDict()),
            ])

            for (table_id, line_no, which), data in columns:
                column_id = "{}{:03d}".format(table_id, line_no)
                if data and data != '.':
                    table[which][column_id] = Decimal(data)
                else:
                    table[which][column_id] = None

            tables[table_id] = table
        one_doc['tables'] = tables

        with open('jsoned/{}.json'.format(geoid), 'w') as f:
            json.dump(one_doc, f, separators=(',',':'))
            print("Wrote out {}".format(f.name))
