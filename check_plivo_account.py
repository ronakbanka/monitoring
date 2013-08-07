#!/usr/bin/env python
import sys
import httplib2
import argparse

# Exit statuses recognized by Nagios
OK = 0
WARNING = 1
CRITICAL = 2

# Initializing parser
parser = argparse.ArgumentParser(description='Check Plivo Account services')
parser.add_argument('--auth_id', metavar='id', type=str,
                    required=True)
parser.add_argument('--auth_token', metavar='token', type=str,
                    required=True)
args = parser.parse_args()

UserName=args.auth_id
Password=args.auth_token

url = "https://api.plivo.com/v1/Account/{0}".format(UserName) 
headers = {"Content-Type":"application/json"}

http = httplib2.Http()
http.add_credentials(UserName,Password)
response,content = http.request(url, "GET", headers=headers)

start=content.find("name")+8
end=content.find("resource")-6
user = content[start:end]

status = response.status

if status == 200:
   print "OK:Plivo Account verified for %s" %user
   sys.exit(0)
elif status == 401:
   print "CRITICAL: Authentication Failed"
   sys.exit(2)
elif status == 404:
   print "CRITICAL: Resource not found"
   sys.exit(2) 
