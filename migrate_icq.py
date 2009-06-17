#!/usr/bin/env python

import os
import sys
import re
from datetime import datetime


def get_log(in_file):
    content = None

    with open(in_file) as f:
        content = f.readlines()

    if not content:
        print 'No text files with logs found'
        return None

    # find where actual log starts
    log_start_mark = '------------------------------------------------\r\n'
    log_start = content.index(log_start_mark) + 1

    return content[log_start:]


def parse_log(content):
    day_res = {}
    result = {}
    i  = 0
    
    last_msg = {}
    for line in content:
        line = line.replace('\r\n', '')
        if len(line) != 0:
            if line[0] != ' ':
                # Start of the message, lets read sender name, recepient name, date and time
                res = re.search('\d{1,2}\.\d{1,2}\.\d{4} \d{1,2}:\d{1,2}:\d{1,2}', line)
                if not res:
                    print """Line %s\n%s\nin in unknown format""" % (i, line.encode(ENCODING))
                    return line
                else:
                    if last_msg:
                        day_res[last_msg['date']] = last_msg['data']
                        
                    new_msg = {}
                    new_msg['date'] = datetime.strptime(line[res.start():res.end()], '%d.%m.%Y %H:%M:%S')
                    new_msg['data'] = {'nick': line[:res.start()], 'text' : line[res.end():]}

                    if last_msg:
                        last_day = last_msg['date'].date()
                        if last_day != new_msg['date'].date():
                            result[last_day] = day_res
                            day_res = {}

                    last_msg = new_msg

            else:
                line = line.strip()
                if line:
                    last = last_msg['data']
                    last['text'] = last['text'] + '\r\n' + line.strip()

                #print i, len(line.strip())

        i += 1

    return result

def write_to_files(days, dir):
    for day, data in days.items():
        time_keys = data.keys()
        time_keys.sort()

        with open('%s/%s+1000EST.txt' % 
                  (dir, time_keys[0].strftime('%Y-%m-%d.%H%M%S')), 'w') as f:

            f.write('Conversation with %s \n' % data[time_keys[0]]['nick'])
            for msg_time, msg_data in data.items():
                f.write('(%(time)s) %(nick)s: %(text)s \n' % {'time' : msg_time.strftime('%H:%M:%S'),
                                                           'nick' : msg_data['nick'].strip(),
                                                           'text' : msg_data['text'].strip()})

ENCODING = 'cp1251'

def main():
    if len(sys.argv) < 3:
        print """\n\tExport Miranda logs using Message Export plugin from http://sourceforge.net/projects/msg-export"""
        print """\tUse following format for file name in Message Export's 'Default' field: %UIN%\%year%-%month%-%day%.txt"""
        print '\n\tUsage: migrate_icq.py <root_dir_with_miranda_logs> <target_dir_with_pidgin_icq_logs> [encoding]\n'
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if len(sys.argv) == 4:
        ENCODING = sys.argv[3]

    for d, di, f in os.walk(input_dir):
        for f_name in f:
            if f_name.lower().endswith('.txt'):
                source_file = os.path.join(d, f_name)
                print 'Procesing %s' % source_file
                uin = re.findall('/([^/]+)?$', d)[0]
                out_uin = os.path.join(output_dir, uin)

                content = get_log(source_file)
                days = parse_log(content)
                print 'Writing to %s' % out_uin
                if not os.path.exists(out_uin):
                    os.mkdir(out_uin)
                write_to_files(days, out_uin)


if __name__ == "__main__":
    main()





