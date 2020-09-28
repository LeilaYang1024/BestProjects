# coding: utf-8

"""
Created on:
@brief:python SFTP连接及上传、下载文件（注：需要安装paramiko环境填坑）
@author: YangLei
@version: Python3
"""

import paramiko
import uuid


class SSHConnection(object):

    def __init__(self, host, port, username, pwd):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def upload(self, local_path, target_path):
        # 连接，上传
        # file_name = self.create_file()
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 上传至服务器 /tmp/test.py
        sftp.put(local_path, target_path)

    def download(self, remote_path, local_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path, local_path)

    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read()
        print(str(result, encoding='utf-8'))
        return result


if __name__=="__main__":
    ssh = SSHConnection(host='118.178.226.227',port=22,username='tangdou01',pwd='ti2SKH#WfT')
    ssh.connect()
    ssh.cmd("ls")
    ssh.close()