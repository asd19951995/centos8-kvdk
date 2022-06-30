# -*- coding: utf-8 -*-
'''
该脚本是KVDK scripts自带run_benmark.py脚本 执行指定的string、sorted 模式的random数据正常并提取

'''
import json
import os, re, shutil
import subprocess
from unittest import result

def run_kvdk_benchmark():
    # 获取kvdk下的scripts目录路径
    path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    scripts_path = ('/'.join(path.split('/')) + '/scripts')

    # 修改 benchmark_impl.py 文件 confirm(pmem_path) 函数
    file_data = ""
    with open(scripts_path + '/benchmark_impl.py', "r", encoding="utf-8") as f:
        for line in f:
            if "confirm(pmem_path)" in line:
                continue
            file_data += line
    with open(scripts_path + '/benchmark_impl.py',"w",encoding="utf-8") as f:
        f.write(file_data)

    # 修改 run_benchmark.py 文件 num_thread  参数 为 48
    file_run = ""
    with open(scripts_path + '/run_benchmark.py', "r", encoding="utf-8") as g:
        for lines in g:
            if "num_thread = 64" in lines:
                lines = 'num_thread = 48\n'
            file_run += lines
    with open(scripts_path + '/run_benchmark.py',"w",encoding="utf-8") as g:
        g.write(file_run)

    if (os.path.isdir(scripts_path)):
        for run_file in (os.listdir(scripts_path)):
            # print(run_file)
            if 'run_benchmark.py' in run_file:
                cmd_string = 'python3 run_benchmark.py {} {}'.format('string', 'random')
                cmd_sorted = 'python3 run_benchmark.py {} {}'.format('sorted', 'random')

                os.system('cd ' + str(scripts_path) + '/ && ' + cmd_string)
                os.system('cd ' + str(scripts_path) + '/ && ' + cmd_sorted)

    # 获取scripts目录下的results目录下的文件的log数据

    result_jsons = {}
    results_files = os.listdir(scripts_path)
    if "results" in results_files:
        results_data = (os.listdir(scripts_path + '/' + 'results'))        
        for file in results_data:
            results_data_type = (os.listdir(scripts_path + '/' + 'results' + '/' + file))
            for random in results_data_type:
                # print(random)
                # print('  ')
                # print('------------------------------------------------------------------------------------------------------------------------------------')
                if 'string' in random:
                    random_type = 'string'
                elif 'sorted' in random:
                    random_type = 'sorted'
                results_log_files = os.listdir(scripts_path + '/' + 'results' + '/' + file + '/' + random)
                vsize = results_log_files[0].split('-')[1]
                thread = results_log_files[0].split('-')[5]
                log_list = os.listdir(scripts_path + '/' + 'results' + '/' + file + '/' + random + '/' + results_log_files[0])

                # 根据当前读取的log文件名称，读取上次执行results文件夹下的log 里面的 Average Ops 数据 
                json_data_list = {}
                
                for log in log_list:
                    # print(log)
                    kvdk_type = {}
                    if 'random' in log or 'range' in log:
                        dic_name = ('-'.join(log.split('_')[:-1]))
                        if dic_name == "read":
                            read_write_type = "point-read"
                        elif dic_name == "read-write":
                            read_write_type = '9R:1W'
                        elif dic_name == "batch-insert":
                            read_write_type = 'batch'
                        else:
                            read_write_type = dic_name
                        if dic_name != "read-write":
                            kvdk_type['model'] = random_type
                            kvdk_type['size'] = vsize
                            kvdk_type['thread'] = thread
                            kvdk_type['type'] = read_write_type
                            with open(scripts_path + '/' + 'results' + '/' + file + '/' + random + '/' + results_log_files[0] + '/' + log, 'r') as old_log_data:
                                        old_log_true = []
                                        for old_line in old_log_data.readlines():
                                            if 'Average' in old_line:
                                                Ops = re.findall(r'\d+', old_line)
                                                for o in Ops:
                                                    if '0' != o:
                                                        kvdk_type['ops'] = o
                                                break
                                            else:
                                                kvdk_type['ops'] = "None"
                            json_data_list[read_write_type] = kvdk_type
                        else:
                            kvdk_type['model'] = random_type
                            kvdk_type['type'] = read_write_type
                            with open(scripts_path + '/' + 'results' + '/' + file + '/' + random + '/' + results_log_files[0] + '/' + log, 'r') as old_log_data:
                                        old_log_true = []
                                        for old_line in old_log_data.readlines():
                                            if 'Average' in old_line:
                                            
                                                Ops = re.findall(r'\d+', old_line)
                                            
                                                kvdk_type['ops'] = Ops[0] + '/' +  Ops[1]
                                                break
                                            else:
                                                kvdk_type['ops'] = "None" + '/' + "None"
                                               
                            json_data_list[read_write_type] = kvdk_type

                    else:
                        continue
                    
                result_jsons[random_type] = json_data_list
    # print(result_jsons)
    # 处理results log 出现异常，导致数据不完整情况   
    if 'string' in result_jsons.keys():
        if 'update' not in result_jsons['string'].keys():
            result_jsons['string']['update']  = {"model": "string", "size": "None", "thread": "None", "type": "update", "ops": "None"}
        if 'point-read' not in result_jsons['string'].keys():
            result_jsons['string']['point-read']  = {"model": "string", "size": "None", "thread": "None", "type": "point-read", "ops": "None"}
        if 'batch' not in result_jsons['string'].keys():
            result_jsons['string']['batch']  = {"model": "string", "size": "None", "thread": "None", "type": "batch", "ops": "None"}
        if 'insert' not in result_jsons['string'].keys():
            result_jsons['string']['insert']  = {"model": "string", "size": "None", "thread": "None", "type": "insert", "ops": "None"}
        if '9R:1W' not in result_jsons['string'].keys():
            result_jsons['string']['9R:1W']  = {"model": "string", "size": "None", "thread": "None", "type": "9R:1W", "ops": "None/None"}
    else:
        result_jsons['string'] = {
            "batch": {"model": "string", "size": "None", "thread": "None", "type": "batch", "ops": "None"}, 
            "insert": {"model": "string", "size": "None", "thread": "None", "type": "insert", "ops": "None"}, 
            "point-read": {"model": "string", "size": "None", "thread": "None", "type": "point-read", "ops": "None"}, 
            "9R:1W": {"model": "string", "size": "None", "thread": "None", "type": "9R:1W", "ops": "None/None"}, 
            "update": {"model": "string", "size": "None", "thread": "None", "type": "update", "ops": "None"}}
    if 'sorted' in result_jsons.keys():
        if 'update' not in result_jsons['sorted'].keys():
            result_jsons['sorted']['update']  = {"model": "sorted", "size": "None", "thread": "None", "type": "update", "ops": "None"}
        if 'point-read' not in result_jsons['sorted'].keys():
            result_jsons['sorted']['point-read']  = {"model": "sorted", "size": "None", "thread": "None", "type": "point-read", "ops": "None"}
        if 'range' not in result_jsons['sorted'].keys():
            result_jsons['sorted']['range']  = {"model": "sorted", "size": "None", "thread": "None", "type": "range", "ops": "None"}
        if 'batch' not in result_jsons['sorted'].keys():
            result_jsons['sorted']['batch']  = {"model": "sorted", "size": "None", "thread": "None", "type": "batch", "ops": "None"}
        if 'insert' not in result_jsons['sorted'].keys():
            result_jsons['sorted']['insert']  = {"model": "sorted", "size": "None", "thread": "None", "type": "insert", "ops": "None"}
        if '9R:1W' not in result_jsons['sorted'].keys():
            result_jsons['sorted']['9R:1W']  = {"model": "sorted", "size": "None", "thread": "None", "type": "9R:1W", "ops": "None/None"}
    else:
        result_jsons['sorted'] = {
            "batch": {"model": "sorted", "size": "None", "thread": "None", "type": "batch", "ops": "None"}, 
            "insert": {"model": "sorted", "size": "None", "thread": "None", "type": "insert", "ops": "None"},
            "range": {"model": "sorted", "size": "None", "thread": "None", "type": "range", "ops": "None"},  
            "point-read": {"model": "sorted", "size": "None", "thread": "None", "type": "point-read", "ops": "None"}, 
            "9R:1W": {"model": "sorted", "size": "None", "thread": "None", "type": "9R:1W", "ops": "None/None"}, 
            "update": {"model": "sorted", "size": "None", "thread": "None", "type": "update", "ops": "None"}}
    # 判断某个目录是否存在
    if os.path.exists(path + '/' + 'results'):
        result_logs = os.listdir(path + '/' + 'results')
        if len(result_logs) < 3:
            if results_data[0] not in result_logs:
                shutil.move(scripts_path + '/' + 'results/' + results_data[0], path + '/' + 'results')
            else:
                shutil.rmtree(path + '/' + 'results/' + results_data[0])   # 先删除存在的result 版本号文件夹
                shutil.move(scripts_path + '/' + 'results/' + results_data[0], path + '/' + 'results')
        else:
            shutil.rmtree(path + '/' + 'results/')   # 先删除存在的result文件夹
            os.mkdir(path + '/' + 'results')
            shutil.move(scripts_path + '/' + 'results/' + results_data[0], path + '/' + 'results')
    else:
        os.mkdir(path + '/' + 'results')
        shutil.move(scripts_path + '/' + 'results/' + results_data[0], path + '/' + 'results')
    shutil.rmtree(scripts_path + '/' + 'results')   # 删除指定目录的

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

    result_jsons['cpu_data'] = all_result
    print(json.dumps(result_jsons))

run_kvdk_benchmark()