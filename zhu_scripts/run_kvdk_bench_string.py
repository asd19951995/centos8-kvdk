# -*- coding: utf-8 -*-
"""
该脚本功能是对：
        run_kvdk_benchmake.sh 脚本执行完成后生成的log文件进行数据收集、
        获取当前从KVDK版本号、
        读取本脚本执行的设备环境指定参数、
"""
from lib2to3.pgen2.token import OP
import os, json
import re
import subprocess

# ops_old_path = '/home/jenkins/zhu/results'
path = os.path.split(os.path.realpath(__file__))[0]
# print(path)
# os.system('git rev-parse HEAD')
for result_file in (os.listdir(path)):
    if 'results' in result_file:
        break

result_kvdk_all = {}
if result_file == "results":
    num = 0
    num1 = 0
    result_kvdk_string = {}
    result_kvdk_sorted = {}
    for results_log_file in (os.listdir(path + '/' + result_file)):
        
        logs = os.listdir(path + '/' + result_file + '/' + results_log_file)
        if "string" in results_log_file:
            num += 1
            modoul = 'string' + str(num)
            for log_file in logs:
                result_kvdk = {}
                if '.log' in log_file:
                    data_title = log_file.split('_')
                    result_kvdk['model'] = data_title[0]
                    result_kvdk['size'] = data_title[2]
                    if data_title[3] == 'read' and data_title[4] == 'random':
                        read_write_type = 'point-read'
                    elif data_title[3] == 'read-write':
                        read_write_type = '9R:1W'
                    else:
                        read_write_type = data_title[3]
                    result_kvdk['thread'] = re.findall(r'\d+', data_title[-1])[0]
                    result_kvdk['type'] = read_write_type
                    # 根据当前读取的log文件名称，读取上次执行results文件夹下的log 里面的 Average Ops 数据
                    # kvdk_ops = {} 
                    with open(path + '/' + result_file + '/' + results_log_file + '/' + log_file, 'r') as log_data:
                        for line in log_data.readlines():
                            if 'Average' in line:
                                # print(line)
                                Ops = re.findall(r'\d+', line)
                                # for o in Ops:
                                if '0' != Ops[0] and '0' != Ops[1]:
                                    result_kvdk['ops'] = Ops[0] + '/' + Ops[1]
                                    
                                else:
                                    if '0' != Ops[0]:
                                        result_kvdk['ops'] = Ops[0]
                                    else:
                                        result_kvdk['ops'] = Ops[1]
                                # result_kvdk['ops' + str(num)] = kvdk_ops
            result_kvdk_string[read_write_type] = result_kvdk
            
                # result_kvdk_all[modoul] = result_kvdk
        else:
            num1 += 1
            for log_file in logs:
                result_kvdk_1 = {}
                if '.log' in log_file:
                    data_title = log_file.split('_')
                    result_kvdk_1['model'] = data_title[0]
                    result_kvdk_1['size'] = data_title[2]
                    if data_title[3] == 'read' and data_title[4] == 'random':
                        read_write_type = 'point-read'
                    elif data_title[3] == 'read-write':
                        read_write_type = '9R:1W'
                    else:
                        read_write_type = data_title[3]
                    result_kvdk_1['thread'] = re.findall(r'\d+', data_title[-1])[0]
                    result_kvdk_1['type'] = read_write_type
                    # 根据当前读取的log文件名称，读取上次执行results文件夹下的log 里面的 Average Ops 数据 
                    # kvdk_ops_1 = {} 
                    with open(path + '/' + result_file + '/' + results_log_file + '/' + log_file, 'r') as log_data:
                        for line in log_data.readlines():
                            if 'Average' in line:
                                # print(line)
                                Ops = re.findall(r'\d+', line)
                                if '0' != Ops[0] and '0' != Ops[1]:
                                    result_kvdk_1['ops'] = Ops[0] + '/' + Ops[1]

                                else:
                                    if '0' != Ops[0]:
                                        result_kvdk_1['ops'] = Ops[0]
                                    else:
                                        result_kvdk_1['ops'] = Ops[1]
                            # result_kvdk_1['ops' + str(num)] = kvdk_ops_1
                        
            result_kvdk_sorted[read_write_type] = result_kvdk_1
                 
result_kvdk_all['string'] = result_kvdk_string
result_kvdk_all['sorted'] = result_kvdk_sorted


##########################################################################################################################################################################
device_data = []
all_result = {}
# 获取CPU信息
p = subprocess.Popen('lscpu', shell=True, stdout=subprocess.PIPE)
p_out, err = p.communicate()
for line in p_out.splitlines():
    
    if 'Model name' in str(line) and 'BIOS' not in str(line):
        device_data.append(str(line).split('          ')[-1][:-1])
    elif 'Core(s) per socket' in str(line):
        device_data.append(re.findall(r'\d+', str(line))[0]) 
    elif 'Socket(s)' in str(line):
        device_data.append(re.findall(r'\d+', str(line))[0])

# 获取DRAM容量
dram = subprocess.Popen('dmidecode -t17 | grep Size', shell=True, stdout=subprocess.PIPE)
dram_out, err = dram.communicate()
for dram_line in dram_out.splitlines():
    # print(dram_line)
    DRAM = (int(re.findall(r'\d+', str(dram_line))[0]))
    break
device_data.append(str(DRAM) + 'GB')
    

# 获取DRAM信息及CPU位置
cpu_num = 11
command_c = []
DDR_list = []
for num in range(cpu_num):
    command_c.append('ipmctl show -topology | grep "DDR" | grep CPU' + str(num) + ' | wc -l')
for command in command_c:
    c = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    c_out, err = c.communicate()
    for c_line in c_out.splitlines():
        if re.findall(r'\d+', str(c_line))[0]  == '0':
            continue
        else:
            DDR_list.append(int(re.findall(r'\d+', str(c_line))[0]))
device_data.append(round(sum(DDR_list)/int(device_data[1])))

# 获取PMEM信息
p_command = []
PEME_list = []
for P_NUM in range(cpu_num):
    p_command.append('ipmctl show -topology | grep "Logical Non-Volatile Device" | grep CPU' + str(P_NUM) + ' | wc -l')

for pmem_command in p_command:
    P = subprocess.Popen(pmem_command, shell=True, stdout=subprocess.PIPE)
    P_out, err = P.communicate()
    for P_line in P_out.splitlines():
        if re.findall(r'\d+', str(P_line))[0]  == '0':
            continue
        else:
            # 获取CPU1 * XX CPU2 * XX
            # PEME_list.append('CPU' + re.findall(r'\d+', str(pmem_command))[0] + ':  ' + re.findall(r'\d+', str(P_line))[0])
            PEME_list.append(int(re.findall(r'\d+', str(P_line))[0]))
device_data.append(round(sum(PEME_list)/int(device_data[1])))


# 获取PMEM容量
PU_command = "ipmctl show -a -dimm | grep -w 'Capacity' | cut -d'=' -f 2 | awk '{ print $1}'"
P_U = subprocess.Popen(PU_command, shell=True, stdout=subprocess.PIPE)
P_U_out, P_U_err = P_U.communicate()
for P_U_line in P_U_out.splitlines():
    capacity = re.findall(r'\d+',str(P_U_line))
    device_data.append(str(capacity[0] + '.' + capacity[1]) + 'GB')
    break

uname = subprocess.Popen('uname -sr', shell=True, stdout=subprocess.PIPE)
uname_out, uname_err = uname.communicate()
# print(type(uname_out.decode('UTF-8')))
all_result['uname'] = uname_out.decode('UTF-8').replace('\n','')
# os.system('uname -sr')

# print(device_data)
all_result['core_socket'] = device_data[0]
all_result['socket'] = device_data[1]
all_result['model_name'] = device_data[2]
all_result['derm_per'] = device_data[3] + '*' + str(device_data[4])
all_result['peme_per'] = device_data[6] + '*' + str(device_data[5])

result_kvdk_all['cpu_data'] = all_result
print(json.dumps(result_kvdk_all))