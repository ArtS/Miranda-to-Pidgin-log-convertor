#!/usr/bin/env python

import os
import sys
import re
from datetime import datetime


def get_log():
    content = None

    print 'reading'
    for f_name in os.listdir('.'):
        if f_name.lower().endswith('.txt'):
            with open(f_name) as f:
                content = f.readlines()

    if not content:
        print 'No text files with logs found'
        return None

    # find where actual log starts

    tab_space = '                          '
    log_start_mark = '------------------------------------------------\r\n'

    print 'looking for start'
    log_start = content.index(log_start_mark) + 1

    return content[log_start:]

def parse_log(content):
    result = {}
    i  = 0

    last_msg = {}
    for line in content:
        line = unicode(line.replace('\r\n', '').decode('cp1251', 'replace'))
        if len(line) != 0:
            if line[0] != ' ':
                # Start of the message, lets read sender name, recepient name, date and time
                res = re.search('\d{1,2}\.\d{1,2}\.\d{4} \d{1,2}:\d{1,2}:\d{1,2}', line)
                if not res:
                    print """Line %s\n%s\nin in unknown format""" % (i, line.encode('cp1251'))
                    return line
                else:
                    if last_msg:
                        result[last_msg['date']] = last_msg['data']
                        
                    last_msg = {}
                    last_msg['date'] = datetime.strptime(line[res.start():res.end()], '%d.%m.%Y %H:%M:%S')
                    last_msg['data'] = {'nick': line[:res.start()], 'text' : line[res.end():]}
            else:
                line = line.strip()
                if line:
                    last = last_msg['data']
                    last['text'] = last['text'] + '\r\n' + line.strip()

                #print i, len(line.strip())

        i += 1

    return result

content = get_log()
parse_log(content)


