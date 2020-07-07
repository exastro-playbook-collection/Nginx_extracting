# -*- coding: UTF-8 -*-
import json
result = {}
result['VAR_Nginx_yumInstall'] = False
result['VAR_Nginx_package_dst'] = '/tmp'
result['VAR_Nginx_rpmList'] = []
result['VAR_Nginx_rpmList'].append('pcre-devel-8.32-17.el7.x86_64.rpm')
result['VAR_Nginx_pkgList'] = []
result['VAR_Nginx_pkgList'].append('zlib-1.2.11.tar.gz')
result['VAR_Nginx_nginxPkg'] = 'nginx-1.16.1.tar.gz'
print(json.dumps(result))