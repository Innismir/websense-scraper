#!/usr/bin/env python
#
# seach_websense.py - Script that uses the WebSense scraper class to search
# a WebSense Triton system for hosts listed in urls.txt
#
# USAGE: ./search_websense.py [-f <FILE>] [-u <URL>]
#
# All code Copyright (c) 2013, Ben Jackson and Mayhemic Labs -
# bbj@mayhemiclabs.com. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# * Neither the name of the author nor the names of contributors may be
# used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import getpass, sys, datetime, ipaddr, argparse, requests
from ConfigParser import SafeConfigParser
from WebSense import *

today = datetime.datetime.now()
DD = datetime.timedelta(days=90)
earlier = today - DD
start_date = earlier.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

print "Searching from " + start_date + " to " + end_date

#Read the configuration file
config = SafeConfigParser()
config.read('config.ini')

#Read the command line arguments
parser = argparse.ArgumentParser()

#The user needs to specify iether a URL or a filename
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-u', '--url', action='store')
group.add_argument('-f', '--file', action='store')

args = parser.parse_args()

if args.file is None:

    #If user has told us it's a URL download it

    print "Downloading " + args.url + "..."

    #Make the request

    sample_request = requests.get(args.url)

    if sample_request.status_code == 200:

        lines = sample_request.splitlines()

    else:

        #If it doesn't return a 200, abort....

        print args.url + " did not return HTTP 200..."
        sys.exit(1)

else:

    try:
        f = open(args.file)
        lines = f.read().splitlines()
        f.close()
    except:
        print "Unable to read file..."
        sys.exit(1)

password = getpass.getpass("WebSense Password: ")

websense = WebSenseTriton(config.get('websense', 'host') + ':' + config.get('websense', 'port'), config.get('websense', 'username'), password)

print "Searching..."

found_domains = []

for domain in lines:

    found = 0

    if domain == "":
        continue

    try:
        ipaddr.IPv4Address(domain)
        if websense.destinationip_search(domain, start_date, end_date):
            found = 1
    except:
        if websense.hostname_search(domain, start_date, end_date):
            found = 1

    if found == 1:
        sys.stdout.write('!')
        found_domains.append(domain)
    else:
        sys.stdout.write('.')

    sys.stdout.flush()

print "\n"

if len(found_domains) > 0:

    print "FOUND DOMAINS:"

    for domain in found_domains:
        print domain + " - Found"

    print "\n"

