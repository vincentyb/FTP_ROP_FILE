#! /bin/env python

import json
import datetime
import ftplib
import os
import threading




def load_config():
        config_file = open('./config_json', 'r')
        config = json.load(config_file)
        config_file.close()
        sessions = {}
        i = 0
        for session in config['session']:
                sessions[i] = {}
                sessions[i]['Host'] = session['Host']
                sessions[i]['User'] = session['User']
                sessions[i]['Pass'] = session['Pass']
                sessions[i]['Data_dir'] = '/'.join(' '.join(session['Data_dir']).split(' '))
                sessions[i]['RE'] = session['RE']
                sessions[i]['Data_local'] = session['Data_local']
                sessions[i]['Hour'] = session['Hour']
                sessions[i]['Hostname'] = session['Hostname']
                i += 1
        return sessions

def check_local_dir(dir):
        if os.path.exists(dir):
                return dir
        else:
                os.makedirs(dir)
                return dir

def get_file(Host,User,Pass,Dir_local,File_list,Received_file_list):
        Received_file_list = []
        session = ftplib.FTP(Host)
        session.login(User,Pass)
        for item in File_list:
                Path = '/'.join(item.split('/')[:-1])
                File = item.split('/')[-1]
                session.cwd(Path)
                File_local = Dir_local + File
                fp = open(File_local, 'wb')
                session.retrbinary('retr %s' %File,fp.write,1024)
                Received_file_list.append(File_local)
                fp.close()
        session.quit()

def get_file_list(Host,User,Pass,Path):
        session = ftplib.FTP(Host)
        session.login(User,Pass)
        L = session.nlst(Path)
        session.quit()
        return L

def list_to_file(File, List):
        fp = open(File, 'w')
        for item in List:
                fp.write(item + '\n')
        fp.close()
        

sessions = load_config()
Time_start = datetime.datetime.now()
for key in sessions:
        Host = sessions[key]['Host']
        Head = (datetime.datetime.now() + datetime.timedelta(hours = -sessions[key]['Hour'])).strftime(sessions[key]['RE'])
        Path_RE = sessions[key]['Data_dir'] + '/' + Head 
        User = sessions[key]['User']
        Pass = sessions[key]['Pass']
        Data_local = sessions[key]['Data_local']
        Dir_RE = (datetime.datetime.now() + datetime.timedelta(hours = -sessions[key]['Hour'])).strftime(Data_local)
        Dir_local = '/'.join(Dir_RE.split('/')[:-1]) + '/' + sessions[key]['Hostname'] + '/' + Dir_RE.split('/')[-1] + '/'
        Dir_local_log_base = '/'.join(Dir_RE.split('/')[:-1]) + '/log/'
        Dir_local = check_local_dir(Dir_local)
        Dir_local_log_base = check_local_dir(Dir_local_log_base)
        log_remote_file = Dir_local_log_base + sessions[key]['Hostname'] + '_' + Head[:-1] + '_remote.log'
        log_received_file = Dir_local_log_base + sessions[key]['Hostname'] + '_' + Head[:-1] + '_received.log'
        Received_file_list = []
        File_list = get_file_list(Host,User,Pass,Path_RE)
        list_to_file(log_remote_file, File_list)
        get_file(Host,User,Pass,Dir_local,File_list,Received_file_list)
        list_to_file(log_received_file, Received_file_list)
'''
        session = ftplib.FTP(Host)
        session.login(User,Pass)
        for item in File_list:
                Path = '/'.join(item.split('/')[:-1])
                File = item.split('/')[-1]
                print Path
                print File
                session.cwd(Path)
                File_local = Dir_local + File
                print File_local
                fp = open(File_local, 'wb')
                session.retrbinary('retr %s' %File,fp.write,1024)
                fp.close()
        session.quit()
'''

Time_end = datetime.datetime.now()
print Time_start
print Time_end
