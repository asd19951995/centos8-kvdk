# -*- coding: utf-8 -*-
'''
该脚本是对 kvdk build 生成的 build/tests/dbstress_test 脚本文件执行操作
'''

import os
import time
path1 = os.path.split(os.path.abspath(__file__))[0]  # 获取当前的工作目录
# print(path1)
# 删除 pmem 目录下的数据
results_files = os.listdir('/mnt/pmem0')

if results_files:
    for pmem_file in results_files:
        os.system('rm -rf /mnt/pmem0/' + pmem_file)
else:
    pass
time.sleep(100)
try:
    if 'tests' in os.listdir(path1):
        if 'dbstress_test' in os.listdir(path1 + '/tests'):
                cmd = path1 + '/tests/dbstress_test'
                # cmd = 'ls'
                os.system(cmd)
                print('Successful')
        else:
            print('Fial')
    else:
        print('Fail')

except Exception as err:
    print('Fial')