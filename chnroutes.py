#-*- coding: UTF-8 -*-
#python2.7
import argparse
import math
import os
import re
import subprocess
import sys
import urllib2

def generate_linux(metric):
###########################################
#
###########################################
    pass


def generate_mac(_):
    results = fetch_ip_data()

    upscript_header = """\
#!/bin/sh
#export PATH="/bin:/sbin:/usr/sbin:/usr/bin"

TEMP=`netstat -nr | grep '^default' | grep -v 'utun' | sed 's/default *\([0-9\.]*\) .*/\1/'`
echo "${TEMP}" > /tmp/temp.txt
OLDGW=`head -1 /tmp/temp.txt`

dscacheutil -flushcache


"""

    downscript_header = """\
#!/bin/sh
export PATH="/bin:/sbin:/usr/sbin:/usr/bin"

if [ ! -e /tmp/temp.txt ]; then
        exit 0
fi

OLDGW=`head -1 /tmp/temp.txt`
"""

    upfile = open('./macOS/addRoute.sh', 'w')
    downfile = open('./macOS/deleteRoute.sh', 'w')

    upfile.write(upscript_header)
    downfile.write(downscript_header)

    for ip, _, mask in results:
        upfile.write('route add %s/%s "${OLDGW}"\n' % (ip, mask))
        downfile.write('route delete %s/%s ${OLDGW}\n' % (ip, mask))


    upfile.close()
    downfile.close()

    os.chmod('addRoute.sh', 00755)
    os.chmod('deleteRoute.sh', 00755)


def generate_win(metric):
    results = fetch_ip_data()

    upscript_header = """\

:start

for /F %%i in ('ping www.baidu.com -n 1') do (set com=%%i)
echo %com%
if "%com%"=="Ping" (
echo Disconnect...
timeout /T 10
goto start
) else (
echo Connected!
timeout /T 3
)

for /F "tokens=3" %%* in ('route print ^| findstr "\<0.0.0.0\>"') do set "gw=%%*"
ipconfig /flushdns

"""

    upscript_tail = """\

echo Complete!
timeout /T 5
"""
    upfile = open('./Windows/Refresh.bat','w')
    upfile.write('@echo off')
    upfile.write(upscript_header)
    for ip, mask, _ in results:
        upfile.write('route add %s mask %s %s metric %d\n' %
                     (ip, mask, "%gw%", metric))

    upfile.write(upscript_tail)
    upfile.close()


def fetch_ip_data():
    url = 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
    try:
        data = subprocess.check_output(['wget', url, '-O-'])
    except (OSError, AttributeError):
        print >> sys.stderr, "Fetching data from apnic.net, "\
                             "it might take a few minutes, please wait..."
        data = urllib2.urlopen(url).read()

    cnregex = re.compile(r'^apnic\|cn\|ipv4\|[\d\.]+\|\d+\|\d+\|a\w*$',
                         re.I | re.M)
    cndata = cnregex.findall(data)

    results = []

    for item in cndata:
        unit_items = item.split('|')
        starting_ip = unit_items[3]
        num_ip = int(unit_items[4])

        imask = 0xffffffff ^ (num_ip - 1)
        imask = hex(imask)[2:]

        mask = [imask[i:i + 2] for i in xrange(0, 8, 2)]
        mask = '.'.join([str(int(i, 16)) for i in mask])

        cidr = 32 - int(math.log(num_ip, 2))

        results.append((starting_ip, mask, cidr))

    return results

def main():
    parser = argparse.ArgumentParser(
                 description="Generate routing rules for VPN users in China.")
    parser.add_argument('-p',
                        dest='platform',
                        default='mac',
                        nargs='?',
                        choices=['mac', 'linux', 'win'],
                        help="target platform")

    parser.add_argument('-m',
                        dest='metric',
                        default=5,
                        nargs='?',
                        type=int,
                        help="metric")

    args = parser.parse_args()
    if args.platform.lower() == 'linux':
        generate_linux(args.metric)
    elif args.platform.lower() == 'mac':
        generate_mac(args.metric)
    elif args.platform.lower() == 'win':
        generate_win(args.metric)
    else:
        exit(1)

if __name__ == '__main__':
    main()
