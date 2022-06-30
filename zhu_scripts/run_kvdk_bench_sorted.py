# -*- coding: utf-8 -*-
"""
该脚本功能是对：
        run_kvdk_benchmake.sh 脚本执行完成后生成的 sorted.log文件进行数据收集、
"""
import os
import re

ops_old_path = '/home/jenkins/zhu/results'
path = os.path.split(os.path.realpath(__file__))[0]
# print(path)
for result_file in (os.listdir(path)):
    if 'results' in result_file:
        break
result_kvdk = []
if result_file == "results":
    for results_log_file in (os.listdir(path + '/' + result_file)):
        # print('------------------------------------------------------------------------------------------------------------------------------->')
        # print(results_log_file)
        logs = os.listdir(path + '/' + result_file + '/' + results_log_file)
        # print(logs)
        for log_file in logs:
            if "sorted" in log_file:
                sorted_list = []
                try:
                    if '.log' in log_file:
                        data_title = log_file.split('_')
                        sorted_list.append(data_title[0])
                        sorted_list.append(data_title[2])

                        if data_title[3] == 'range':
                            sorted_list.append('scan')
                        elif data_title[3] == 'read' and data_title[4] == 'random':
                            sorted_list.append('point-read')
                        elif data_title[3] == 'read-write':
                            sorted_list.append('9R:1W')
                        else:
                            sorted_list.append(data_title[3])

                        sorted_list.append(re.findall(r'\d+', data_title[-1])[0])
                        # 根据当前读取的log文件名称，读取上次执行results文件夹下的log 里面的 Average Ops 数据 
                        with open(ops_old_path  + '/' + results_log_file + '/' + log_file, 'r') as old_log_data:
                            old_log_true = []
                            for old_line in old_log_data.readlines():
                                if 'Average' in old_line:
                                    old_Ops = re.findall(r'\d+', old_line)
                                    sorted_list.append(format(int(old_Ops[0]), ','))
                                    sorted_list.append(format(int(old_Ops[1]), ','))
                                    old_log_true.append('True')

                            # 判断读取上一次的log文件是否存在Average 数据，如果不存在，那么会填充N/A值作为数据 
                            if 'True' in old_log_true:
                                pass
                            else:
                                old_Ops = ['N/A', 'N/A']
                                sorted_list.append('N/A')
                                sorted_list.append('N/A')
                        with open(path + '/' + result_file + '/' + results_log_file + '/' + log_file, 'r') as log_data:
                            log_true = []
                            for line in log_data.readlines():
                                if 'Average' in line:
                                    # print(line)
                                    Ops = re.findall(r'\d+', line)
                                    sorted_list.append(format(int(Ops[0]), ','))
                                    sorted_list.append(format(int(Ops[1]), ','))
                                    
                                    if old_Ops[0] != '0':
                                        if int(Ops[0]) != int(old_Ops[0]):
                                            Read_ops = (int(Ops[0]) - int(old_Ops[0])) / int(old_Ops[0]) * 100
                                            # 判断增幅 正负
                                            if Read_ops <= 0 :
                                                sorted_list.append(str(round(Read_ops, 2)) + '%')
                                                if round(Read_ops, 2) <= -5:
                                                    sorted_list.append('Fail')
                                                else:
                                                    sorted_list.append('Successful')
                                            elif Read_ops > 0 :
                                                sorted_list.append('+' + str(round(Read_ops, 2)) + '%')
                                                if round(Read_ops, 2) >= 5:
                                                    sorted_list.append('Fail')                                         
                                                else:
                                                    sorted_list.append('Successful')
                                        else:
                                            sorted_list.append('0%')
                                            sorted_list.append('Successful')
                                    else:
                                        sorted_list.append('0%')
                                        sorted_list.append('Successful')
                                    if old_Ops[1] != '0':
                                        if int(Ops[1]) != int(old_Ops[1]):
                                            Write_ops = (int(Ops[1]) - int(old_Ops[1])) / int(old_Ops[1]) * 100
                                            if Write_ops <= 0 :
                                                sorted_list.append(str(round(Write_ops, 2)) + '%')
                                                if round(Write_ops, 2) <= -5:
                                                    sorted_list.append('Fail')
                                                else:
                                                    sorted_list.append('Successful')
                                            else:
                                                sorted_list.append('+' + str(round(Write_ops, 2)) + '%')
                                                if round(Write_ops, 2) >= 5:
                                                    sorted_list.append('Fail')
                                                else:
                                                    sorted_list.append('Successful')
                                        else:
                                            sorted_list.append('0%')
                                            sorted_list.append('Successful')
                                        
                                    else:
                                        sorted_list.append('0%')
                                        sorted_list.append('Successful')
                                    log_true.append('True')
                            # 判断读取当前的log文件是否存在Average 数据，如果不存在，那么会填充N/A值作为数据 
                            if 'True' in log_true:
                                pass
                            else:
                                sorted_list.append('N/A')
                                sorted_list.append('N/A')
                                sorted_list.append('N/A')
                                sorted_list.append('N/A')
                                sorted_list.append('Successful')
                except Exception as err:
                    if len(sorted_list) < 10:
                        num = 10
                    for l in range(num - len(sorted_list)):
                        sorted_list.append('N/A')
                    sorted_list.append('Successful')
                result_kvdk.append(sorted_list)
                
# #######################################################################################################################################################################################
if 0 < len(result_kvdk) < 5:
    existence_mode = []
    for result_k in result_kvdk:
        existence_mode.append(result_k[2])
    if 'batch' not in existence_mode:
        result_kvdk.append([result_k[0], result_k[1], 'scan', result_k[3], 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'Fail'])
    elif 'insert' not in existence_mode:
        result_kvdk.append([result_k[0], result_k[1], 'insert', result_k[3], 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'Fail'])
    elif 'read' not in existence_mode:
        result_kvdk.append([result_k[0], result_k[1], 'point-read', result_k[3], 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'Fail'])
    elif 'read-write' not in existence_mode:
        result_kvdk.append([result_k[0], result_k[1], '9R:1W', result_k[3], 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'Fail'])
    elif 'update' not in existence_mode:
        result_kvdk.append([result_k[0], result_k[1], 'update', result_k[3], 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'Fail'])

elif 0 == len(result_kvdk) :
    result_kvdk.append(['sorted', 'N/A', 'point-read', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'Fail'])
    result_kvdk.append(['sorted', 'N/A', 'update', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'Fail'])
    result_kvdk.append(['sorted', 'N/A', 'insert', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'Fail'])
    result_kvdk.append(['sorted', 'N/A', 'scan', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'Fail'])
    result_kvdk.append(['sorted', 'N/A', '9R:1W', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'Fail'])

# 排序
all_result = []

for li in range(len(result_kvdk)):
    if result_kvdk[li][2] == 'point-read':
        all_result.append(result_kvdk[li])
        break
    else:
        continue
for la in range(len(result_kvdk)):
    if result_kvdk[la][2] == 'update':
        all_result.append(result_kvdk[la])
        break
    else:
        continue
for lb in range(len(result_kvdk)):
    if result_kvdk[lb][2] == 'insert':
        all_result.append(result_kvdk[lb])
        break
    else:
        continue
for lc in range(len(result_kvdk)):
    if result_kvdk[lc][2] == 'scan':
        all_result.append(result_kvdk[lc])
        break
    else:
        continue
for ld in range(len(result_kvdk)):
    if result_kvdk[ld][2] == '9R:1W':
        all_result.append(result_kvdk[ld])
        break
    else:
        continue

for result_data in all_result:
    for data in result_data:
        print(data)
##########################################################################################################################################################################
            
def delete_result_log():
    os.system('rm -rf ' + ops_old_path + '/*')
    os.system('cp -r ' + str(path) + '/results/* ' + ops_old_path)
try:
    delete_result_log()
except Exception as err:
    pass