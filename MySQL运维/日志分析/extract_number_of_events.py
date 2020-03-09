"""
Script which creates a list of tables sorted by number of events.
Just run it with --start_datetime and --stop_datetime args, and it goes through
all the MySQL binlog files in the current directory, and then writes a result
to a text file.
"""

import argparse
from collections import defaultdict
import os
import operator
import subprocess
import tempfile
import time

CMD = "mysqlbinlog --base64-output=decode-rows  \
    --start-datetime='{start_datetime}'  \
    --stop-datetime='{stop_datetime}' \
    -vv {filename} \
    | grep -e 'UPDATE' -e 'INSERT' -e 'DELETE FROM' \
    | awk '{{print $NF}}' \
    | sed -e 's/\`//g' \
    | sort \
    | uniq -c \
    | sort -k 1 -r \
    | awk '{{t = $1; $1 = $2; $2 = t; print;}}'"


def main():
    """Main function."""
    start = time.time()

    parser = argparse.ArgumentParser(
        description='Extract number of events from MySQL binlogs')
    parser.add_argument(
        '--start_datetime',
        help='Start timestamp in YYYY-MM-DD HH:MM:SS')
    parser.add_argument(
        '--stop_datetime',
        help='Stop timestamp in YYYY-MM-DD HH:MM:SS')
    args = parser.parse_args()

    print('\nExtraction process started...')

    tables = defaultdict(int)

    with tempfile.TemporaryFile(mode='a+t') as tmp_file:
        filenames = [
            file for file in list(
                os.walk(os.getcwd()))[0][2] if 'mysql' in file]
        for filename in filenames:
            cmd_to_execute = CMD.format(
                start_datetime=args.start_datetime,
                stop_datetime=args.stop_datetime,
                filename=filename)
            subprocess.check_call(cmd_to_execute, shell=True, stdout=tmp_file)
            print('\n{filename} was processed'.format(filename=filename))

        tmp_file.seek(0)
        for line in tmp_file.readlines():
            table, number_of_events = line.split()
            tables[table] += int(number_of_events)

    sorted_tables = sorted(
        tables.items(), key=operator.itemgetter(1), reverse=True)

    start_cleaned = args.start_datetime.replace(' ', 'T').replace(':', '-')
    stop_cleaned = args.stop_datetime.replace(' ', 'T').replace(':', '-')
    filename_all = '{start_cleaned}_{stop_cleaned}.txt'.format(
        start_cleaned=start_cleaned, stop_cleaned=stop_cleaned)

    with open(filename_all, mode='w+t') as fa:
        for table in sorted_tables:
            fa.write(' '.join((table[0], str(table[1]))) + '\n')

    end = time.time()
    elapsed_time = int(str(end - start).split('.')[0])
    mins, secs = divmod(elapsed_time, 60)

    print('\nEvents were extracted, the whole process took {mins} mins {secs} '
          'seconds.\nThe result was written to {filename} in the current '
          'directory'.format(mins=mins, secs=secs, filename=filename_all))

if __name__ == '__main__':
    main()
