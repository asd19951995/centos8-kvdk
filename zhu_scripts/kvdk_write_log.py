# -*- coding: utf-8 -*-
'''
该脚本是对 kvdk result log 数据 写入 指定result_log txt文件中 
'''
from lib2to3.pgen2.token import OP
import os, json
import subprocess
path = os.path.split(os.path.realpath(__file__))[0]
print(path)
file_name = "result_log.txt" 
# run_file_name = "run_kvdk_bench_string.py"  
run_file_name = "run_scripts_kvdk.py"
######################################################################### 获取result数据 #############################################################################################

c = subprocess.Popen('python3 -v ' + path + '/' + run_file_name, shell=True, stdout=subprocess.PIPE)
c_out, err = c.communicate()
# for kvdk_result_data in c_out.splitlines():
#     pass
kvdk_result_data = str(c_out.splitlines()[-1], 'UTF-8')

print('######################################################################### 写入result数据 #############################################################################################')
print(kvdk_result_data)


######################################################################### 写入result数据 #############################################################################################

# 获取当前目录下的result_log.txt 文件是否存在
build_files = os.listdir(path=path) 



# 当文件存在当前目录时
if file_name in build_files:

    """如果存在result_log.txt 
        那么就获取文件所以的数据，并判断是否存在 三列json数据.如果是空数据，那么直接写入、 
        如果存在1列、那么追加写入、如果存在2列 也追加写入、如果存在3列数据，那么清空文件数据，重新写入
    """
    print('存在文件')
    print(len(open(path + '/' + file_name , 'r').readlines()))
    if len(open(path + '/' + file_name, 'r').readlines()) < 3:
        with open(path + '/' + file_name, 'a') as file_txt:
            file_txt.write(kvdk_result_data + '\n')
    else:
        # 如果result_log.txt 大于 2列，那么先删除文件，再次创建新的result_log.txt
        os.remove(path + '/' + file_name)
        with open(path + '/' + file_name, 'w') as file_txt:
            file_txt.write(kvdk_result_data + '\n')

else:
    # 如果不存在时，那就新建result_log.txt
    with open(path + '/' + file_name, 'w') as file_txt:
        file_txt.write(kvdk_result_data + '\n')