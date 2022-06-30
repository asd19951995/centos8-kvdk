# -*- coding: utf-8 -*-
'''
该脚本是对git log > commit.txt
文件内的最新版本号、上次版本号、指定版本号信息进行数据提取
'''
import os
import json
version_logname = "commint.txt"
path = os.path.split(os.path.realpath(__file__))[0]
# print(path)
# if os.path.isdir(path):
#     file_list = os.listdir(path)
#     for file_name in file_list:
#         # print(file_name)
#         if version_logname == file_name:
#             os.remove(path + '/' + file_name)
#         os.system(path + '/kvdk_commit.sh')

# else:
#     os.system(path + '/kvdk_commit.sh')

# 读取指定版本文件编号
with open(path + '/specified_version.txt', 'r') as specified:
    specified_version = (specified.readlines()[0])
    # print(specified_version)

# 获取最新本吧与上一次版本编号
with open(path + '/commit.txt', 'r') as commits:
    commit_list = []
    Author_list = []
    Date_list = []
    time_num = []
    num = 0
    for commit in commits.readlines():
        num = num +1
        if 'commit' in commit:
            if commit.replace('\n', '').split(' ')[0] == 'commit':
                commit_list.append(commit.replace('\n', '').split(' ')[1])
        elif 'Author' in commit:
            Author_list.append(''.join(commit.replace('\n', '').split(' ')[1:-1]) + ':' + commit.replace('\n', '').split(' ')[-1])
        elif 'Date' in commit:
            Date_list.append(('-'.join(commit.replace('\n', '').split(' ')[1:-2]) + '-' + commit.replace('\n', '').split(' ')[-2])[2:])
        time_num.append(str(num))
        if len(commit_list) == 2 and len(Author_list) == 2 and len(Date_list) == 2:
            break
    # print(commit_list)
    # print(Author_list)
    # print(Date_list)
with open(path + '/commit.txt', 'r') as commits1:
    for commit1 in commits1.readlines():
        if specified_version in commit1:
            commit_list.append(commit1.replace('\n', '').split(' ')[1])
        if len(commit_list) == 3 and 'Author' in commit1:
            Author_list.append(''.join(commit1.replace('\n', '').split(' ')[1:-1]) + ':' + commit1.replace('\n', '').split(' ')[-1])
        elif len(commit_list) == 3 and 'Date' in commit1:
            Date_list.append(('-'.join(commit1.replace('\n', '').split(' ')[1:-2]) + '-' + commit1.replace('\n', '').split(' ')[-2])[2:])
        time_num.append('3')
        if len(commit_list) == 3 and len(Author_list) == 3 and len(Date_list) == 3 and len(time_num) == 3:
            break
    # print(commit_list)
    # print(Author_list)
    # print(Date_list)

pr_dict_list = {}
for i in range(len(commit_list)):
    pr_dict = {}
    if i == 0:
        commit_version = "current_commit"
    elif i == 1:
        commit_version = "previous_commit"
    elif i == 2:
        commit_version = "baseline_commit"
    
    pr_dict['commit'] = commit_list[i]
    pr_dict['Author'] = Author_list[i]
    pr_dict['Date'] = Date_list[i]
    pr_dict['time_num'] = time_num[i]
    pr_dict_list[commit_version] = pr_dict

print(json.dumps(pr_dict_list))
