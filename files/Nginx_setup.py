# -*- coding: UTF-8 -*-
import re
import json
import sys
import os

# main process

args = sys.argv
if (len(args) < 4):
    sys.exit(1)
fileName = args[1]
tmpPath = args[2]
def getServerParam(serverList,serverBlockInhttp,filePath):
    serverInfo = {}
    for serverInHttp in serverBlockInhttp:
        if 'directive' in serverInHttp and 'server_name' == serverInHttp['directive']:
            serverInfo['location'] = []
            serverInfo['isDelete'] = False
            serverInfo['serverFilePath'] = ''
            serverInfo['serverFilePath'] =  serverInfo['serverFilePath'] + ' '+ filePath.split(tmpPath, 1)[1]
            if 'args' in serverInHttp and serverInHttp['args'] is not None:
                serverInfo['server_name'] = ''
                for serverName in serverInHttp['args']:
                    serverInfo['server_name'] = serverInfo['server_name'] + ' ' + serverName
        if 'directive' in serverInHttp and 'listen' == serverInHttp['directive']:
            if 'args' in serverInHttp and serverInHttp['args'] is not None:
                serverInfo['listen'] = ''
                for listen in serverInHttp['args']:
                    serverInfo['listen'] = serverInfo['listen'] + ' ' + listen
        if 'directive' in serverInHttp and 'root' == serverInHttp['directive']:
            if 'args' in serverInHttp and serverInHttp['args'] is not None:
                serverInfo['root'] = serverInHttp['args'][0]
        if 'directive' in serverInHttp and 'location' == serverInHttp['directive']:
            locationInfo = {}
            locationInfo['isDelete'] = False
            if 'args' in serverInHttp and serverInHttp['args'] is not None:
                locationInfo['name'] = ''
                for locationname in serverInHttp['args']:
                    locationInfo['name'] = locationInfo['name'] + ' ' + locationname
            locationInfo['option'] = []
            if 'block' in serverInHttp and serverInHttp['block'] is not None:
                locationBlock = serverInHttp['block']
                for locationblock in locationBlock:
                    if 'directive' in locationblock:
                        if 'args' in locationblock and locationblock['args'] is not None:
                            optionStr = locationblock['directive']
                            for argsInlocation in locationblock['args']:
                                optionStr = optionStr + ' ' + argsInlocation
                            locationInfo['option'].append(optionStr)
            serverInfo['location'].append(locationInfo)
    if len(serverInfo) > 0:
        serverList.append(serverInfo)
    return serverList

result = {}
VAR_Nginx_server = []
if os.path.isfile(fileName):
    fp = open(fileName)
    pythonData = json.load(fp)
    # get path and httpBlock of nginx.conf in config
    nginxInConfig = pythonData['config'][0]['parsed']
    nginxFilePath = pythonData['config'][0]['file']
    httpInConfigParsed = {}
    httpBlock = []
    for parsed in nginxInConfig:
        if 'directive' in parsed and 'http' == parsed['directive']:
            httpInConfigParsed = parsed
            break
    httpBlock = httpInConfigParsed['block']
    # serverBlock of nginx.conf data to param VAR_Nginx_server
    for httpblock in httpBlock:
        if 'directive' in httpblock and 'server' == httpblock['directive']:
            if 'block' in httpblock and httpblock['block'] is not None:
                VAR_Nginx_server = getServerParam(VAR_Nginx_server, httpblock['block'], nginxFilePath)
    # get serverBlock of sub.conf
    serverBlockInSub = []
    indexInConfig = 1
    while indexInConfig < len(pythonData['config']):
        subConfig = pythonData['config'][indexInConfig]
        subFilePath = subConfig['file']
        '''
        if subFilePath.endswith('.conf'):
            indexInConfig = indexInConfig + 1
            continue
        '''
        if subFilePath.startswith('/') == False:
            subFilePath = nginxFilePath.split('/nginx.conf')[0] + '/' + subFilePath
        if 'parsed' in subConfig and subConfig['parsed'] is not None:
            subConfParsed = subConfig['parsed']
            for subConfparsed in subConfParsed:
                if 'directive' in subConfparsed and subConfparsed['directive'] == 'server':
                    if 'block' in subConfparsed and subConfparsed['block'] is not None:
                        VAR_Nginx_server = getServerParam(VAR_Nginx_server, subConfparsed['block'], subFilePath)
        indexInConfig = indexInConfig + 1
    if len(VAR_Nginx_server) > 0:
        result['VAR_Nginx_server'] = VAR_Nginx_server
    fp.close()
print(json.dumps(result))