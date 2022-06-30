# -*- coding: utf-8 -*-
'''
该脚本是对 kvdk result log 所有的数据获取 并进行对比处理
'''
from lib2to3.pgen2.token import OP
import os, json, re
path = os.path.split(os.path.realpath(__file__))[0]
file_name = "result_log.txt" 
# BASELINE PREVIOUS CURRENT

log_list = []
with open(path + '/' + file_name, 'r') as file_datas:
    for kvdk_log in file_datas.readlines():
        log_list.append(json.loads(kvdk_log))
    
all_json = {}
######################################################################### BASELINE OPS数据 #############################################################################################
string = {}
string_pointread = {}
string_update = {}
string_batch = {}
string_insert = {}
string_RW = {}

if log_list[0]['string']['point-read']['ops'] != "None":
    string_pointread['baseline_ops'] = (format(int(log_list[0]['string']['point-read']['ops']), ','))
else:
    string_pointread['baseline_ops'] = log_list[0]['string']['point-read']['ops']

if log_list[0]['string']['update']['ops'] != "None":
    string_update['baseline_ops'] = (format(int(log_list[0]['string']['update']['ops']), ','))
else:
    string_update['baseline_ops'] = log_list[0]['string']['update']['ops']

if log_list[0]['string']['batch']['ops'] != "None":
    string_batch['baseline_ops'] = (format(int(log_list[0]['string']['batch']['ops']), ','))
else:
    string_batch['baseline_ops'] = log_list[0]['string']['batch']['ops']

if log_list[0]['string']['insert']['ops'] != "None":
    string_insert['baseline_ops'] = (format(int(log_list[0]['string']['insert']['ops']), ','))
else:
    string_insert['baseline_ops'] = log_list[0]['string']['insert']['ops']

if log_list[0]['string']['9R:1W']['ops'].split('/')[0] != "None" and log_list[0]['string']['9R:1W']['ops'].split('/')[0] != "None":
    string_RW['baseline_ops'] = (format(int(re.findall(r'\d+', log_list[0]['string']['9R:1W']['ops'])[0]), ',')) + '/' + (format(int(re.findall(r'\d+', log_list[0]['string']['9R:1W']['ops'])[1]), ','))
else:
    if log_list[0]['string']['9R:1W']['ops'].split('/')[0] == "None" and log_list[0]['string']['9R:1W']['ops'].split('/')[1] != "None":
        string_RW['baseline_ops'] = (log_list[0]['string']['9R:1W']['ops'].split('/')[0] + '/' + format(int(re.findall(r'\d+', log_list[0]['string']['9R:1W']['ops'])[1]), ','))
    
    elif log_list[0]['string']['9R:1W']['ops'].split('/')[0] != "None" and log_list[0]['string']['9R:1W']['ops'].split('/')[1] == "None":
        string_RW['baseline_ops'] = (format(int(re.findall(r'\d+', log_list[0]['string']['9R:1W']['ops'])[0]), ',') + '/' +  log_list[0]['string']['9R:1W']['ops'].split('/')[1])
    else:
        string_RW['baseline_ops'] = (log_list[0]['string']['9R:1W']['ops'].split('/')[0] + '/' +  log_list[0]['string']['9R:1W']['ops'].split('/')[1])
######################################################################### PREVIOUS OPS数据 #############################################################################################
if log_list[1]['string']['point-read']['ops'] != "None":
    string_pointread['previous_ops'] = (format(int(log_list[1]['string']['point-read']['ops']), ','))
else:
    string_pointread['previous_ops'] = log_list[1]['string']['point-read']['ops']

if log_list[1]['string']['update']['ops'] != "None":
    string_update['previous_ops'] = (format(int(log_list[1]['string']['update']['ops']), ','))
else:
    string_update['previous_ops'] = log_list[1]['string']['update']['ops']

if log_list[1]['string']['batch']['ops'] != "None":
    string_batch['previous_ops'] = (format(int(log_list[1]['string']['batch']['ops']), ','))
else:
    string_batch['previous_ops'] = log_list[1]['string']['batch']['ops']

if log_list[1]['string']['insert']['ops'] != "None":
    string_insert['previous_ops'] = (format(int(log_list[1]['string']['insert']['ops']), ','))
else:
    string_insert['previous_ops'] = log_list[1]['string']['insert']['ops']

if log_list[1]['string']['9R:1W']['ops'].split('/')[0] != "None" and log_list[1]['string']['9R:1W']['ops'].split('/')[0] != "None":
    string_RW['previous_ops'] = (format(int(re.findall(r'\d+', log_list[1]['string']['9R:1W']['ops'])[0]), ',')) + '/' + (format(int(re.findall(r'\d+', log_list[1]['string']['9R:1W']['ops'])[1]), ','))
else:
    if log_list[1]['string']['9R:1W']['ops'].split('/')[0] == "None" and log_list[1]['string']['9R:1W']['ops'].split('/')[1] != "None":
        string_RW['previous_ops'] = (log_list[1]['string']['9R:1W']['ops'])[0] + '/' + (format(int(re.findall(r'\d+', log_list[1]['string']['9R:1W']['ops'])[1]), ','))
    elif log_list[1]['string']['9R:1W']['ops'].split('/')[0] != "None" and log_list[1]['string']['9R:1W']['ops'].split('/')[1] == "None":
        string_RW['previous_ops'] = (format(int(re.findall(r'\d+', log_list[1]['string']['9R:1W']['ops'])[0]), ',')) + '/' +  log_list[1]['string']['9R:1W']['ops'][1]
    else:
        string_RW['previous_ops'] = (log_list[1]['string']['9R:1W']['ops'].split('/')[0] + '/' + log_list[1]['string']['9R:1W']['ops'].split('/')[1])
######################################################################### CURRENT OPS数据 #############################################################################################
if log_list[2]['string']['point-read']['ops'] != "None":
    string_pointread['current_ops'] = (format(int(log_list[2]['string']['point-read']['ops']), ','))
else:
    string_pointread['current_ops'] = log_list[2]['string']['point-read']['ops']

if log_list[2]['string']['update']['ops'] != "None":
    string_update['current_ops'] = (format(int(log_list[2]['string']['update']['ops']), ','))
else:
    string_update['current_ops'] = log_list[2]['string']['update']['ops']

if log_list[2]['string']['batch']['ops'] != "None":
    string_batch['current_ops'] = (format(int(log_list[2]['string']['batch']['ops']), ','))
else:
    string_batch['current_ops'] = log_list[2]['string']['batch']['ops']

if log_list[2]['string']['insert']['ops'] != "None":
    string_insert['current_ops'] = (format(int(log_list[2]['string']['insert']['ops']), ','))
else:
    string_insert['current_ops'] = log_list[2]['string']['insert']['ops']

if log_list[2]['string']['9R:1W']['ops'].split('/')[0] != "None" and log_list[2]['string']['9R:1W']['ops'].split('/')[0] != "None":
    string_RW['current_ops'] = (format(int(re.findall(r'\d+', log_list[2]['string']['9R:1W']['ops'])[0]), ',')) + '/' + (format(int(re.findall(r'\d+', log_list[2]['string']['9R:1W']['ops'])[1]), ','))
else:
    if log_list[2]['string']['9R:1W']['ops'].split('/')[0] == "None" and log_list[2]['string']['9R:1W']['ops'].split('/')[1] != "None":
        string_RW['current_ops'] = (log_list[2]['string']['9R:1W']['ops'])[0] + '/' + (format(int(re.findall(r'\d+', log_list[2]['string']['9R:1W']['ops'])[1]), ','))
    elif log_list[2]['string']['9R:1W']['ops'].split('/')[0] != "None" and log_list[2]['string']['9R:1W']['ops'].split('/')[1] == "None":
        string_RW['current_ops'] = (format(int(re.findall(r'\d+', log_list[2]['string']['9R:1W']['ops'])[0]), ',')) + '/' +  log_list[2]['string']['9R:1W']['ops'][1]
    else:
        string_RW['current_ops'] = (log_list[2]['string']['9R:1W']['ops'].split('/')[0] + '/' + log_list[2]['string']['9R:1W']['ops'].split('/')[1])

string['point-read'] = string_pointread
string['update'] = string_update
string['batch'] = string_batch 
string['insert'] = string_insert 
string['9R:1W'] = string_RW 
all_json['string'] = string
sorted = {}

sorted_pointread = {}
sorted_update = {}
sorted_range = {}
sorted_insert = {}
sorted_RW = {}
# re.sub(r"(?<=\d)(?=(?:\d\d\d)+$)", ",", subject)

######################################################################### BASELINE OPS数据 #############################################################################################
if log_list[0]['sorted']['point-read']['ops'] != "None":
    sorted_pointread['baseline_ops'] = (format(int(log_list[0]['sorted']['point-read']['ops']), ','))
else:
    sorted_pointread['baseline_ops'] = log_list[0]['sorted']['point-read']['ops']
if log_list[0]['sorted']['update']['ops'] != "None":
    sorted_update['baseline_ops'] = (format(int(log_list[0]['sorted']['update']['ops']), ','))
else:
    sorted_update['baseline_ops'] = log_list[0]['sorted']['update']['ops']
if log_list[0]['sorted']['range']['ops'] != "None":
    sorted_range['baseline_ops'] = (format(int(log_list[0]['sorted']['range']['ops']), ','))
else:
    sorted_range['baseline_ops'] = log_list[0]['sorted']['range']['ops']
if log_list[0]['sorted']['insert']['ops'] != "None":
    sorted_insert['baseline_ops'] = (format(int(log_list[0]['sorted']['insert']['ops']), ','))
else:
    sorted_insert['baseline_ops'] = log_list[0]['sorted']['insert']['ops']
    
if log_list[0]['sorted']['9R:1W']['ops'].split('/')[0] != "None" and log_list[0]['sorted']['9R:1W']['ops'].split('/')[0] != "None":
    sorted_RW['baseline_ops'] = (format(int(re.findall(r'\d+', log_list[0]['sorted']['9R:1W']['ops'])[0]), ',')) + '/' + (format(int(re.findall(r'\d+', log_list[0]['sorted']['9R:1W']['ops'])[1]), ','))
else:
    if log_list[0]['sorted']['9R:1W']['ops'].split('/')[0] == "None" and log_list[0]['sorted']['9R:1W']['ops'].split('/')[1] != "None":
        sorted_RW['baseline_ops'] = (log_list[0]['sorted']['9R:1W']['ops'])[0] + '/' + (format(int(re.findall(r'\d+', log_list[0]['sorted']['9R:1W']['ops'])[1]), ','))
    elif log_list[0]['sorted']['9R:1W']['ops'].split('/')[0] != "None" and log_list[0]['sorted']['9R:1W']['ops'].split('/')[1] == "None":
        sorted_RW['baseline_ops'] = (format(int(re.findall(r'\d+', log_list[0]['sorted']['9R:1W']['ops'])[0]), ',')) + '/' +  log_list[0]['sorted']['9R:1W']['ops'][1]
    else:
        sorted_RW['baseline_ops'] = (log_list[0]['sorted']['9R:1W']['ops'].split('/')[0] + '/' + log_list[0]['sorted']['9R:1W']['ops'].split('/')[1])
######################################################################### PREVIOUS OPS数据 #############################################################################################
if log_list[1]['sorted']['point-read']['ops'] != "None":
    sorted_pointread['previous_ops'] = (format(int(log_list[1]['sorted']['point-read']['ops']), ','))
else:
    sorted_pointread['previous_ops'] = log_list[1]['sorted']['point-read']['ops']

if log_list[1]['sorted']['update']['ops'] != "None":
    sorted_update['previous_ops'] = (format(int(log_list[1]['sorted']['update']['ops']), ','))
else:
    sorted_update['previous_ops'] = log_list[1]['sorted']['update']['ops']

if log_list[1]['sorted']['range']['ops'] != "None":
    sorted_range['previous_ops'] = (format(int(log_list[1]['sorted']['range']['ops']), ','))
else:
    sorted_range['previous_ops'] = log_list[1]['sorted']['range']['ops']

if log_list[1]['sorted']['insert']['ops'] != "None":
    sorted_insert['previous_ops'] = (format(int(log_list[1]['sorted']['insert']['ops']), ','))
else:
    sorted_insert['previous_ops'] = log_list[1]['sorted']['insert']['ops']

if log_list[1]['sorted']['9R:1W']['ops'].split('/')[0] != "None" and log_list[1]['sorted']['9R:1W']['ops'].split('/')[0] != "None":
    sorted_RW['previous_ops'] = (format(int(re.findall(r'\d+', log_list[1]['sorted']['9R:1W']['ops'])[0]), ',')) + '/' + (format(int(re.findall(r'\d+', log_list[1]['sorted']['9R:1W']['ops'])[1]), ','))
else:
    if log_list[1]['sorted']['9R:1W']['ops'].split('/')[0] == "None" and log_list[1]['sorted']['9R:1W']['ops'].split('/')[1] != "None":
        sorted_RW['previous_ops'] = (log_list[1]['sorted']['9R:1W']['ops'])[0] + '/' + (format(int(re.findall(r'\d+', log_list[1]['sorted']['9R:1W']['ops'])[1]), ','))
    elif log_list[1]['sorted']['9R:1W']['ops'].split('/')[0] != "None" and log_list[1]['sorted']['9R:1W']['ops'].split('/')[1] == "None":
        sorted_RW['previous_ops'] = (format(int(re.findall(r'\d+', log_list[1]['sorted']['9R:1W']['ops'])[0]), ',')) + '/' +  log_list[1]['sorted']['9R:1W']['ops'][1]
    else:
        sorted_RW['previous_ops'] = (log_list[1]['sorted']['9R:1W']['ops'].split('/')[0] + '/' + log_list[1]['sorted']['9R:1W']['ops'].split('/')[1])

######################################################################### CURRENT OPS数据 #############################################################################################
if log_list[2]['sorted']['point-read']['ops'] != "None":
    sorted_pointread['current_ops'] = (format(int(log_list[2]['sorted']['point-read']['ops']), ','))
else:
    sorted_pointread['current_ops'] = log_list[2]['sorted']['point-read']['ops']

if log_list[2]['sorted']['update']['ops'] != "None":
    sorted_update['current_ops'] = (format(int(log_list[2]['sorted']['update']['ops']), ','))
else:
    sorted_update['current_ops'] = log_list[2]['sorted']['update']['ops']

if log_list[2]['sorted']['range']['ops'] != "None":
    sorted_range['current_ops'] = (format(int(log_list[2]['sorted']['range']['ops']), ','))
else:
    sorted_range['current_ops'] = log_list[2]['sorted']['range']['ops']

if log_list[2]['sorted']['insert']['ops'] != "None":
    sorted_insert['current_ops'] = (format(int(log_list[2]['sorted']['insert']['ops']), ','))
else:
    sorted_insert['current_ops'] = log_list[2]['sorted']['insert']['ops']

if log_list[2]['sorted']['9R:1W']['ops'].split('/')[0] != "None" and log_list[2]['sorted']['9R:1W']['ops'].split('/')[0] != "None":
    sorted_RW['current_ops'] = (format(int(re.findall(r'\d+', log_list[2]['sorted']['9R:1W']['ops'])[0]), ',')) + '/' + (format(int(re.findall(r'\d+', log_list[2]['sorted']['9R:1W']['ops'])[1]), ','))
else:
    if log_list[2]['sorted']['9R:1W']['ops'].split('/')[0] == "None" and log_list[2]['sorted']['9R:1W']['ops'].split('/')[1] != "None":
        sorted_RW['current_ops'] = (log_list[2]['sorted']['9R:1W']['ops'])[0] + '/' + (format(int(re.findall(r'\d+', log_list[2]['sorted']['9R:1W']['ops'])[1]), ','))
    elif log_list[2]['sorted']['9R:1W']['ops'].split('/')[0] != "None" and log_list[2]['sorted']['9R:1W']['ops'].split('/')[1] == "None":
        sorted_RW['current_ops'] = (format(int(re.findall(r'\d+', log_list[2]['sorted']['9R:1W']['ops'])[0]), ',')) + '/' +  log_list[2]['sorted']['9R:1W']['ops'][1]
    else:
        sorted_RW['current_ops'] = (log_list[2]['sorted']['9R:1W']['ops'].split('/')[0] + '/' + log_list[2]['sorted']['9R:1W']['ops'].split('/')[1])

sorted['point-read'] = sorted_pointread
sorted['update'] = sorted_update
sorted['range'] = sorted_range 
sorted['insert'] = sorted_insert 
sorted['9R:1W'] = sorted_RW 
all_json['sorted'] = sorted

all_json['server_data'] = log_list[2]['cpu_data']
######################################################################### 测试参数  #############################################################################################

test = {}
test['size'] = log_list[2]['sorted']['point-read']['size']
test['thread'] = log_list[2]['sorted']['point-read']['thread']
all_json['testing'] = test

######################################################################### Rate  #############################################################################################

for string_type in all_json['string'].keys():
    if string_type != '9R:1W':
        if string_type == 'point-read':
            json_model = string_pointread
        elif string_type == 'update':
            json_model = string_update
        elif string_type == 'batch':
            json_model = string_batch
        elif string_type == 'insert':
            json_model = string_insert
        if all_json['string'][string_type]['current_ops'] != "None" and all_json['string'][string_type]['previous_ops'] != "None":
            string_pc_rate = (int(all_json['string'][string_type]['current_ops'].replace(',', '')) - int(all_json['string'][string_type]['previous_ops'].replace(',', ''))) / int(all_json['string'][string_type]['previous_ops'].replace(',', '')) * 100
            if string_pc_rate <= -5 or string_pc_rate >= 5:
                json_model['pc_rate'] = (str(round(string_pc_rate, 2)) + '%')
                json_model['pc_rate_color'] = "#CC0000"
            else:
                json_model['pc_rate'] = (str(round(string_pc_rate, 2)) + '%')
                json_model['pc_rate_color'] = "#6666FF"
        else:
            json_model['pc_rate'] = ('None%')
            json_model['pc_rate_color'] = "#6666FF"
        
        if all_json['string'][string_type]['current_ops'] != "None" and all_json['string'][string_type]['baseline_ops'] != "None":
            string_bc_rate = (int(all_json['string'][string_type]['current_ops'].replace(',', '')) - int(all_json['string'][string_type]['baseline_ops'].replace(',', ''))) / int(all_json['string'][string_type]['baseline_ops'].replace(',', '')) * 100
            if string_bc_rate <= -5 or string_bc_rate >= 5:
                json_model['bc_rate'] = (str(round(string_bc_rate, 2)) + '%')
                json_model['bc_rate_color'] = "#CC0000"
            else:
                json_model['bc_rate'] = (str(round(string_bc_rate, 2)) + '%')
                json_model['bc_rate_color'] = "#6666FF"
        else:
            json_model['bc_rate'] = ('None%')
            json_model['bc_rate_color'] = "#6666FF"
        


    else:
        baseline_ops_list = []
        previous_ops_list = []
        current_ops_list = []
        if all_json['string'][string_type]['baseline_ops'].split('/')[0] != "None":
            baseline_ops_list.append(''.join(re.findall(r'\d+', all_json['string'][string_type]['baseline_ops'].split('/')[0])))
        else:
            baseline_ops_list.append('None')
        
        if all_json['string'][string_type]['baseline_ops'].split('/')[1] != "None":
            baseline_ops_list.append(''.join(re.findall(r'\d+', all_json['string'][string_type]['baseline_ops'].split('/')[1])))
        else:
            baseline_ops_list.append('None')

        if all_json['string'][string_type]['previous_ops'].split('/')[0] != "None":
            previous_ops_list.append(''.join(re.findall(r'\d+', all_json['string'][string_type]['previous_ops'].split('/')[0])))
        else:
            previous_ops_list.append('None')
        
        if all_json['string'][string_type]['previous_ops'].split('/')[1] != "None":
            previous_ops_list.append(''.join(re.findall(r'\d+', all_json['string'][string_type]['previous_ops'].split('/')[1])))
        else:
            previous_ops_list.append('None')
        if all_json['string'][string_type]['current_ops'].split('/')[0] != "None":
            current_ops_list.append(''.join(re.findall(r'\d+', all_json['string'][string_type]['current_ops'].split('/')[0])))
        else:
            current_ops_list.append('None')
        if all_json['string'][string_type]['current_ops'].split('/')[1] != "None":
            current_ops_list.append(''.join(re.findall(r'\d+', all_json['string'][string_type]['current_ops'].split('/')[1])))
        else:
            current_ops_list.append('None')
        
        # string_RW
        if current_ops_list[0] != "None" and  previous_ops_list[0] != "None":
            string_pc_rate0 = (int(current_ops_list[0]) - (int(previous_ops_list[0]))) / (int(previous_ops_list[0])) * 100
            if string_pc_rate0 <= -5 or string_pc_rate0 >= 5:
                string_RW['pc_rate0'] = (str(round(string_pc_rate0, 2)) + '%') 
                string_RW['pc_rate_color0'] = "#CC0000"
            else:
                string_RW['pc_rate0'] = (str(round(string_pc_rate0, 2)) + '%')
                string_RW['pc_rate_color0'] = "#6666FF"
        else:
            string_RW['pc_rate0'] = ('None%')
            string_RW['pc_rate_color0'] = "#6666FF"
        if current_ops_list[1] != "None" and previous_ops_list[1] != "None":
            string_pc_rate1 = (int(current_ops_list[1]) - (int(previous_ops_list[1]))) / (int(previous_ops_list[1])) * 100
            if string_pc_rate1 <= -5 or string_pc_rate1 >= 5:
                string_RW['pc_rate1'] = (str(round(string_pc_rate1, 2)) + '%') 
                string_RW['pc_rate_color1'] = "#CC0000"
            else:
                string_RW['pc_rate1'] = (str(round(string_pc_rate1, 2)) + '%')
                string_RW['pc_rate_color1'] = "#6666FF"
        else:
            string_RW['pc_rate1'] = ('None%')
            string_RW['pc_rate_color1'] = "#6666FF"
        if current_ops_list[0] != "None" and baseline_ops_list[0] != "None":
            string_bc_rate0 = (int(current_ops_list[0]) - (int(baseline_ops_list[0]))) / (int(baseline_ops_list[0])) * 100
            if string_bc_rate0 <= -5 or string_bc_rate0 >= 5:
                string_RW['bc_rate0'] = (str(round(string_bc_rate0, 2)) + '%') 
                string_RW['bc_rate_color0'] = "#CC0000"
            else:
                string_RW['bc_rate0'] = (str(round(string_bc_rate0, 2)) + '%')
                string_RW['bc_rate_color0'] = "#6666FF"
        else:
            string_RW['bc_rate0'] = ('None%')
            string_RW['bc_rate_color0'] = "#6666FF"

        if current_ops_list[0] != "None" and baseline_ops_list[0] != "None":
            string_bc_rate1 = (int(current_ops_list[1]) - (int(baseline_ops_list[1]))) / (int(baseline_ops_list[1])) * 100
            if string_bc_rate1 <= -5 or string_bc_rate1 >= 5:
                string_RW['bc_rate1'] = (str(round(string_bc_rate1, 2)) + '%') 
                string_RW['bc_rate_color1'] = "#CC0000"
            else:
                string_RW['bc_rate1'] = (str(round(string_bc_rate1, 2)) + '%')
                string_RW['bc_rate_color1'] = "#6666FF"
        else:
            string_RW['bc_rate1'] = ('None%')
            string_RW['bc_rate_color1'] = "#6666FF"

for sorted_type in all_json['sorted'].keys():
    # print(all_json['sorted'])
    # print(sorted_type)
    if sorted_type == 'point-read':
        json_model = sorted_pointread
    elif sorted_type == 'update':
        json_model = sorted_update
    elif sorted_type == 'range':
        json_model = sorted_range
    elif sorted_type == 'insert':
        json_model = sorted_insert

    if sorted_type != '9R:1W':
        # 判断 ops 数据是否存在None 数据
        if all_json['sorted'][sorted_type]['current_ops'] != "None" and all_json['sorted'][sorted_type]['previous_ops'] != "None":
            sorted_pc_rate = (int(all_json['sorted'][sorted_type]['current_ops'].replace(',', '')) - int(all_json['sorted'][sorted_type]['previous_ops'].replace(',', ''))) / int(all_json['sorted'][sorted_type]['previous_ops'].replace(',', '')) * 100
            if sorted_pc_rate <= -5 or sorted_pc_rate >= 5:
                json_model['pc_rate'] = (str(round(sorted_pc_rate, 2)) + '%')
                json_model['pc_rate_color'] = "#CC0000"
            else:
                json_model['pc_rate'] = (str(round(sorted_pc_rate, 2)) + '%')
                json_model['pc_rate_color'] = "#6666FF"
        else:
            json_model['pc_rate'] = ('None%')
            json_model['pc_rate_color'] = "#6666FF"
        
        if all_json['sorted'][sorted_type]['current_ops'] != "None" and all_json['sorted'][sorted_type]['baseline_ops'] != "None":
            sorted_bc_rate = (int(all_json['sorted'][sorted_type]['current_ops'].replace(',', '')) - int(all_json['sorted'][sorted_type]['baseline_ops'].replace(',', ''))) / int(all_json['sorted'][sorted_type]['baseline_ops'].replace(',', '')) * 100
            if sorted_bc_rate <= -5 or sorted_bc_rate >= 5:
                json_model['bc_rate'] = (str(round(sorted_bc_rate, 2)) + '%')
                json_model['bc_rate_color'] = "#CC0000"
            else:
                json_model['bc_rate'] = (str(round(sorted_bc_rate, 2)) + '%')
                json_model['bc_rate_color'] = "#6666FF"
        else:
            json_model['bc_rate'] = ('None%')
            json_model['bc_rate_color'] = "#6666FF"
        
    else:
        baseline_ops_list_sorted = []
        previous_ops_list_sorted = []
        current_ops_list_sorted = []
        if all_json['sorted'][sorted_type]['baseline_ops'].split('/')[0] != "None":
            baseline_ops_list_sorted.append(''.join(re.findall(r'\d+', all_json['sorted'][sorted_type]['baseline_ops'].split('/')[0])))
        else:
            baseline_ops_list_sorted.append('None')

        if all_json['sorted'][sorted_type]['baseline_ops'].split('/')[1] != "None":
            baseline_ops_list_sorted.append(''.join(re.findall(r'\d+', all_json['sorted'][sorted_type]['baseline_ops'].split('/')[1])))
        else:
            baseline_ops_list_sorted.append('None')
        
        if all_json['sorted'][sorted_type]['previous_ops'].split('/')[0] != "None":
            previous_ops_list_sorted.append(''.join(re.findall(r'\d+', all_json['sorted'][sorted_type]['previous_ops'].split('/')[0])))
        else:
            previous_ops_list_sorted.append('None')

        if all_json['sorted'][sorted_type]['previous_ops'].split('/')[1] != "None":
            previous_ops_list_sorted.append(''.join(re.findall(r'\d+', all_json['sorted'][sorted_type]['previous_ops'].split('/')[1])))
        else:
            previous_ops_list_sorted.append('None')

        if all_json['sorted'][sorted_type]['current_ops'].split('/')[0] != "None":
            current_ops_list_sorted.append(''.join(re.findall(r'\d+', all_json['sorted'][sorted_type]['current_ops'].split('/')[0])))
        else:
            current_ops_list_sorted.append('None')

        if all_json['sorted'][sorted_type]['current_ops'].split('/')[1] != "None":
            current_ops_list_sorted.append(''.join(re.findall(r'\d+', all_json['sorted'][sorted_type]['current_ops'].split('/')[1])))
        else:
            current_ops_list_sorted.append('None')
        # string_RW
        # sorted_RW
        if current_ops_list_sorted[0] != "None" and previous_ops_list_sorted[0] != "None":
            sorted_pc_rate0 = (int(current_ops_list_sorted[0]) - int(previous_ops_list_sorted[0])) / (int(previous_ops_list_sorted[0])) * 100
            if sorted_pc_rate0 <= -5 or sorted_pc_rate0 >= 5:
                sorted_RW['pc_rate0'] = (str(round(sorted_pc_rate0, 2)) + '%') 
                sorted_RW['pc_rate_color0'] = "#CC0000"
            else:
                sorted_RW['pc_rate0'] = (str(round(sorted_pc_rate0, 2)) + '%')
                sorted_RW['pc_rate_color0'] = "#6666FF"
        else:
            sorted_RW['pc_rate0'] = ('None%')
            
            sorted_RW['pc_rate_color0'] = "#6666FF"
        if current_ops_list_sorted[1] != "None" and previous_ops_list_sorted[1] != "None":
            sorted_pc_rate1 = (int(current_ops_list_sorted[1]) - (int(previous_ops_list_sorted[1]))) / (int(previous_ops_list_sorted[1])) * 100
            if sorted_pc_rate1 <= -5 or sorted_pc_rate1 >= 5:
                sorted_RW['pc_rate1'] = (str(round(sorted_pc_rate1, 2)) + '%') 
                sorted_RW['pc_rate_color1'] = "#CC0000"
            else:
                sorted_RW['pc_rate1'] = (str(round(sorted_pc_rate1, 2)) + '%')
                sorted_RW['pc_rate_color1'] = "#6666FF"
        else:
            sorted_RW['pc_rate1'] = ('None%')
            sorted_RW['pc_rate_color1'] = "#6666FF"

        if current_ops_list_sorted[0] != "None" and baseline_ops_list_sorted[0] != "None":
            sorted_bc_rate0 = (int(current_ops_list_sorted[0]) - (int(baseline_ops_list_sorted[0]))) / (int(baseline_ops_list_sorted[0])) * 100
            if sorted_bc_rate0 <= -5 or sorted_bc_rate0 >= 5:
                sorted_RW['bc_ratea0'] = (str(round(sorted_bc_rate0, 2)) + '%') 
                sorted_RW['bc_rate_color0'] = "#CC0000"
            else:
                sorted_RW['bc_rate0'] = (str(round(sorted_bc_rate0, 2)) + '%')
                sorted_RW['bc_rate_color0'] = "#6666FF"
        else:
            sorted_RW['bc_rate0'] = ('None%')
            sorted_RW['bc_rate_color0'] = "#6666FF"

        if current_ops_list_sorted[1] != "None" and baseline_ops_list_sorted[1] != "Noen":
            sorted_bc_rate1 = (int(current_ops_list_sorted[1]) - (int(baseline_ops_list_sorted[1]))) / (int(baseline_ops_list_sorted[1])) * 100
            if sorted_bc_rate1 <= -5 or sorted_bc_rate1 >= 5:
                sorted_RW['bc_rate1'] = (str(round(sorted_bc_rate1, 2)) + '%') 
                sorted_RW['bc_rate_color1'] = "#CC0000"
            else:
                sorted_RW['bc_rate1'] = (str(round(sorted_bc_rate1, 2)) + '%')
                sorted_RW['bc_rate_color1'] = "#6666FF"
        else:
            sorted_RW['bc_rate1'] = ('None%')
            sorted_RW['bc_rate_color1'] = "#6666FF"
            
# 删除 pmem 目录下的数据
results_files = os.listdir('/mnt/pmem0')

if results_files:
    for pmem_file in results_files:
        os.system('rm -rf /mnt/pmem0/' + pmem_file)
else:
    pass

print(json.dumps(all_json))