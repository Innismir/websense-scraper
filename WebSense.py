#!/usr/bin/env python
#
# WebSense.py - Python class to search WebSense for domains and IP addresses
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


import urllib, urllib2, cookielib, getpass, mechanize, time, logging, sys, re

class WebSenseTriton:
    def __init__(self, host, username, password):

        self.host = host

        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')]

        self.browser.open('https://' + self.host + '/triton/login/pages/loginPage.jsf')

        self.browser.select_form(name="loginForm")
        self.browser['loginForm:idUserName'] = username
        self.browser['loginForm:idPassword'] = password
        self.browser.submit('loginForm:idLoginButton')

        self.browser.open('https://' + self.host + '/triton/launcher/wsg')
        self.browser.select_form(name="loginRedirectForm")
        self.browser.submit('loginRedirectForm:okbutton')

    def hostname_search(self, hostname, start_date, end_date):
        url = 'https://' + self.host + '/explorer_wse/ws_irpt.exe?qcol=2&qtext=' + hostname + '&startDate=' + start_date + '&endDate=' + end_date
    
        result = self.browser.open(url)
        data = result.get_data()

        if data == '':
            raise Exception

        nonefound_check = re.search('No records found', str(data), re.IGNORECASE)

        if nonefound_check is None:
            return 1
        else:
            return 0

    def destinationip_search(self, ipaddress, start_date, end_date):
        url = 'https://' + self.host + '/explorer_wse/ws_irpt.exe?qcol=13&qtext=' + ipaddress + '&startDate=' + start_date + '&endDate=' + end_date

        result = self.browser.open(url)
        data = result.get_data()

        if data == '':
            raise Exception

        nonefound_check = re.search('No records found', str(data), re.IGNORECASE)

        if nonefound_check is None:
            return 1
        else:
            return 0


class WebSense:
    def  __init__(self, host, username, password):
        pass

