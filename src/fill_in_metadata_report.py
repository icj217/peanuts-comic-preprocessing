import sys
import csv
import json
import re

report_file_name = sys.argv[1]

report_updated_file_name = report_file_name.split('.')[0] + '_updated.' + report_file_name.split('.')[1]

with open(report_file_name, newline='') as report, open(report_updated_file_name, mode='w+', newline='') as output:
    rows = csv.reader(report, delimiter='\t', quotechar='"')
    writer = csv.writer(output)

    keep_going = True
    previous_row = None

    year_idx = 4
    month_idx = 3

    while keep_going:
        try:
            this_row = next(rows)
            print("previous_row: ", previous_row)
            print("this_row: ", this_row)
            if previous_row is None:
                print("This is the first row. We're gonna move to next one so we have a previous row to work with")
                writer.writerow(this_row)
            else:
                if this_row[year_idx] == 'None' and previous_row[year_idx] != 'None':
                    this_row[year_idx] = previous_row[year_idx]
                if this_row[month_idx] == 'None' and previous_row[month_idx] != 'None':
                    months = re.findall(r"'(.*?)'", str(previous_row[month_idx])) or []
                    this_row[month_idx] = [months[1]] if len(months) > 1 else months
                writer.writerow(this_row)
            # When done with this row
            previous_row = this_row
        except StopIteration:
            keep_going = False
            print('DONE')