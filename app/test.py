#!/usr/bin/python

import sys
import json
import cgi

fs = cgi.FieldStorage()

result = {}
result['success'] = True
result['message'] = "The command Completed Successfully"
result['keys'] = ",".join(fs.keys())

d = {}
for k in fs.keys():
    d[k] = fs.getvalue(k)

result['data'] = d
with open("temp.log",'w') as outfile:
    json.dump(result, outfile)
