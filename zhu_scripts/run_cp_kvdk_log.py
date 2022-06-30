# -*- coding: utf-8 -*
from distutils import cmd
import os
import datetime
import paramiko
import sys
from stat import S_ISDIR as isdir

"""
通过paramiko从远处服务器下载文件资源到本地
"""
 
def down_from_remote(sftp_obj, remote_dir_name, local_dir_name):
    """远程下载文件"""
    remote_file = sftp_obj.stat(remote_dir_name)
    if isdir(remote_file.st_mode):
        # 文件夹，不能直接下载，需要继续循环
        check_local_dir(local_dir_name)
        print('开始下载文件夹：' + remote_dir_name)
        for remote_file_name in sftp.listdir(remote_dir_name):
            sub_remote = os.path.join(remote_dir_name, remote_file_name)
            sub_remote = sub_remote.replace('\\', '/')
            sub_local = os.path.join(local_dir_name, remote_file_name)
            sub_local = sub_local.replace('\\', '/')
            down_from_remote(sftp_obj, sub_remote, sub_local)
    else:
        # 文件，直接下载
        print('开始下载文件：' + remote_dir_name)
        sftp.get(remote_dir_name, local_dir_name)
 
 
def check_local_dir(local_dir_name):
    """本地文件夹是否存在，不存在则创建"""
    if not os.path.exists(local_dir_name):
        os.makedirs(local_dir_name)

def read_kvdk_log(local_dir, save_path):
    """在本地文件夹读取log日志内容"""
    with open(local_dir + '/log', 'r') as f:
        n = 0
        m = 0
        k = 0
        for read_log in f.readlines():
            n = n+1
            if '开始执行： dbstress test stage' in read_log:
                m = n
            elif '结束执行： dbstress test stage' in read_log:
                k = n
        f.close()

    with open(local_dir + '/log', 'r') as P:
        with open(save_path + '/dbstress.log', 'w') as F:
            l = 0
            for read_log in P.readlines():
                l = l+1
                if m <= l <= k:
                    F.writelines(str(read_log))
            F.close()
        P.close()
        
def move_results_log(current_path, dest_path):
    """修改results 并复制指定目录"""
    # 移动results 文件
    cmd = 'cp -r ' + current_path + '/results ' + dest_path + '/kvdk_logs/'
    os.system(cmd)
    # 修改名称
    os.system('mv ' + dest_path + '/kvdk_logs/results ' + dest_path + '/kvdk_logs/' + datetime.datetime.now().strftime("%Y年_%m月_%d日-%H时_%M分_%S秒"))
 
 
 
 
if __name__ == "__main__":
    path = os.path.split(os.path.realpath(__file__))[0]
    save_path = '/'.join(path.split('/')[:-1])
    
    """程序主入口"""
    """
    通过paramiko从远处服务器备执行命令
    """
    num = sys.argv[1]      # 参数 项目编号
    job_name = sys.argv[2] # 参数 项目名称

    docker_num = 'jenkins_kvdk'   # docker 容器 CONTAINER ID 
    # 允许连接不在know_hosts文件中的主机
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
    s.connect("10.112.227.43",22,"root", "intel123")
    execmd1 = 'docker cp ' + docker_num + ':/var/jenkins_home/jobs/' + job_name + '/builds/' + str(num) + '/ /home/chengxiang/kvdk-log/' #需要输入的命令
    stdin1, stdout1, stderr1 = s.exec_command (execmd1)
    s.close()
    # 服务器连接信息

    host_name = '10.112.227.43'
    user_name = 'root'
    password = 'intel123'
    port = 22
    obj_name = str(num)
    # 远程文件路径（需要绝对路径）
    remote_dir = '/home/chengxiang/kvdk-log/' + obj_name
    # # 本地文件存放路径（绝对路径或者相对路径都可以）
    local_dir = save_path  + '/' + obj_name
 
    # 连接远程服务器
    t = paramiko.Transport((host_name, port))
    t.connect(username=user_name, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
 
    # 远程文件开始下载
    down_from_remote(sftp, remote_dir, local_dir)
 
    # 关闭连接
    t.close()
    # 读取log
    read_kvdk_log(local_dir, save_path)
 
    # 修改当前resutls log目录
    move_results_log(save_path, '/'.join(save_path.split('/')[:-1]))