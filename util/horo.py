#!/usr/bin/env python
'''
A simple script to read your horoscrop from command line.
'''

import datetime
import urllib
import requests
import sys

from HTMLParser import HTMLParser
link = 'http://www.elle.com/horoscopes/daily/a100/%s-daily-horoscope/'
f = requests.get(link)
x = datetime.date.today()
today_date = "%s %s, %s" % (x.strftime("%B"), x.strftime("%d"), x.strftime("%Y"))

# print f.text
class MyHTMLParser(HTMLParser):
    data_flag = False

    def handle_data(self, data):
        try:
            data.strip()

            if self.data_flag:
                print data
                self.data_flag = False

            if data == today_date:
                self.data_flag = True
        except Exception as err:
            pass

if __name__ == '__main__':
    try:
        sign = sys.argv[1]
    except Exception as err:
        sign = "cancer"

    link = link % sign
    parser = MyHTMLParser()
    parser.feed(f.text)

