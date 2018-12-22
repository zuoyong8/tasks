from celery import Celery

app = Celery('tasks')
app.config_from_object('tasks.celeryconfig')

#
####--run--
#     celery -A tasks worker -B -l info

####--show tasks running--
#     celery -A tasks inspect registered

####--flower manage tasks--
#     celery flower --broker=redis://127.0.0.1:6379

####--close worker
#	 pkill -9 -f 'celery worker'
#    ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9

####--rabbitmq
#    rabbitmq-plugins enable rabbitmq_management
#    sudo rabbitmqctl add_user chain chain123
#    sudo rabbitmqctl set_user_tags chain  administrators
#	 sudo rabbitmqctl set_permissions -p / chain ".*" ".*" ".*"