#coding: utf-8
from os import system,popen,getcwd,path
import argparse
import platform
import sys

from tasks.users import Users
from tasks.libs.config import Config
import subprocess

_WINDOWS = 'Windows'
_LINUX = 'Linux'
_UBUNTU = 'Ubuntu'

def start_tasks():
	tasks_path = path.exists('./tasks')
	if tasks_path:
		if path.exists('./supervisord.conf'):
			system('supervisord -c supervisord.conf')
		else:
			print('error: supervisord.conf is not exists,please excute -i(--install)!')
	else:
		print('error: tasks directory is not exists')


def stop_tasks():
	# system("sudo pkill -9 -f 'celery'")
	if path.exists('./supervisord.conf'):
		system('supervisorctl -c supervisord.conf shutdown')
	else:
		print('error: supervisord.conf is not exists,please excute -i(--install)!')
	# print(popen("ps auxww | grep 'celery' | awk '{print $2}' | xargs kill -9"))


def reload_tasks():
	if path.exists('./supervisord.conf'):
		system('supervisorctl -c supervisord.conf reload')
	else:
		print('error: supervisord.conf is not exists,please excute -i(--install)!')


def list_tasks():
	system("ps auxw | grep 'celery'")


def check_version():
	return True if sys.version_info.major==2 and sys.version_info.minor==7 else False


def get_platform():
	uname = platform.uname()
	if sys.version_info.major==2:
		if uname[0] == _WINDOWS:
			return 'Windows_'+uname[3]
		elif uname[0] == _LINUX:
			if _UBUNTU in  uname[3]:
				return uname[3].split(' ')[0]
	else:
		if uname.system == _WINDOWS:
			return 'Windows_'+uname.version
			pass
		elif uname.system == _LINUX:
			pass


def install_redis():
	platform = get_platform()
	if _UBUNTU in platform:
		cmd = "which redis-cli"
		pi = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		result = pi.stdout.read()
		if len(result) == 0:
			system("sudo apt-get install redis-server")


def install_mysqldb():
	platform = get_platform()
	if _UBUNTU in platform:
		system('sudo apt-get install libmysqlclient-dev')
		cmd = 'which wget'
		pi = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
		result = pi.stdout.read()
		if 'wget' in result:
			system('wget http://sourceforge.net/projects/mysql-python/files/mysql-python/1.2.3/MySQL-python-1.2.3.tar.gz')
			system('tar -zxvf MySQL-python-1.2.3.tar.gz && cd MySQL-python-1.2.3')
			system('python setup.py build && python setup.py install')


def install_supervisor():
	cmd = "pip list | grep supervisor | awk '{print $1}'"
	pi = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	result = pi.stdout.read().replace('\n','')
	if result != 'supervisor':
		system('pip install supervisor')
	system('echo_supervisord_conf > supervisord.conf')
	with open('supervisord.conf','a+') as f:
		f.write("[program:celery.worker]\n")
		f.write("directory={0}\n".format(getcwd()))
		f.write("command=celery -A tasks worker -B -l info --logfile celery_worker.log \n")
		f.write("numprocs=1\n")
		f.write("autostart=true\n")
		f.write("autorestart=true\n")
		f.write("stopsignal=INT\n")


def create_db_datas():
	cmd = "pip list | grep MySQL | awk '{print $1}'"
	pi = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
	result = pi.stdout.read()
	if 'MySQL' in result:
	    config = Config(getcwd()+'/tasks/app.config')
	    result = config.get_section_options_value('mysql')
	    users = Users(result['host'],int(result['port']),result['username'],result['password'],result['dbname'])
	    start = int(config.get_config_value('datas','start'))
	    end = int(config.get_config_value('datas','end'))
	    users.create(start,end)


if __name__=='__main__':
	parser = argparse.ArgumentParser(description='task start or stop service.')
	parser.add_argument('-s','--start',action='store_true',help='if task not start,so start tasks')
	parser.add_argument('-p','--stop',action='store_true',help='if task start,so stop tasks')
	parser.add_argument('-r','--reload',action='store_true',help='reload tasks')
	parser.add_argument('-i','--install',action='store_true',help='install supervisor、MySQLdb、redis')
	parser.add_argument('-l','--list',action='store_true',help='show celery tasks,if tasks is running')
	parser.add_argument('-d','--mysql_datas',action='store_true',help='insert user account to mysql database')
	args = parser.parse_args()
	if args.start:
		start_tasks()
	elif args.stop:
		stop_tasks()
	elif args.reload:
		reload_tasks()
	elif args.install:
		install_supervisor()
		install_mysqldb()
		install_redis()
	elif args.list:
		list_tasks()
	elif args.mysql_datas:
		create_db_datas()
