# -*- coding: UTF-8 -*-
import re
import json
import sys
import os

# main process

args = sys.argv
if (len(args) < 3):
    sys.exit(1)
fileName = args[1]
result = {}
result['VAR_Nginx_status'] = 'start'
result['VAR_Nginx_auto'] = True

if os.path.isfile(fileName):
    fp = open(fileName)
    readStr = fp.read()
    nginxAuto = re.match('\s*nginx.service\s*(.*)\s*', readStr)
    if nginxAuto is not None:
        if nginxAuto.group(1).strip() == 'disabled':
            result['VAR_Nginx_auto'] = False
    fp.close()
print(json.dumps(result))