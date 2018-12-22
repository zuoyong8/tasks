from os import system,popen,getcwd,path
import argparse
import platform
import sys


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
		if uname[0] == 'Windows':
			return 'Windows_'+uname[3]
		elif uname[0] == 'Linux':
			if 'Ubuntu' in  uname[3]:
				return uname[3].split(' ')[0]
	else:
		if uname.system == 'Windows':
			return 'Windows_'+uname.version
			pass
		elif uname.system == 'Linux':
			pass


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


if __name__=='__main__':
	parser = argparse.ArgumentParser(description='task start or stop service.')
	parser.add_argument('-s','--start',action='store_true',help='if task not start,so start tasks')
	parser.add_argument('-p','--stop',action='store_true',help='if task start,so stop tasks')
	parser.add_argument('-r','--reload',action='store_true',help='reload tasks')
	parser.add_argument('-i','--install',action='store_true',help='install supervisor')
	parser.add_argument('-l','--list',action='store_true',help='show celery tasks,if tasks is running')
	args = parser.parse_args()
	if args.start:
		start_tasks()
	elif args.stop:
		stop_tasks()
	elif args.reload:
		reload_tasks()
	elif args.install:
		install_supervisor()
	elif args.list:
		list_tasks()