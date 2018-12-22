# coding:utf-8

from datetime import datetime,timedelta
from celery.schedules import crontab
from libs.datas import OrderFuncType

BROKER_URL = 'redis://127.0.0.1:6379'
BROKER_END = 'redis://127.0.0.1:6379'  #结果保存
CELERY_TIMEZONE = 'Asia/Shanghai'
# CELERY_CONCURRENCY = 4  			   #任务并发数
# CELERY_TASK_SOFT_TIME_LIMIT = 300    #任务超时时间
# CELERY_DISABLE_RATE_LIMITS = Ture    #任务频率限制开关
CELERY_IMPORTS = (
	'tasks.orders',
	'tasks.users'
	)

CELERYBEAT_SCHEDULE = {
	#生成机器人买订单
	'orders-machine-buy':{
		'task': 'tasks.orders.create_orders',
		'schedule': timedelta(seconds=1),
		#options: {}
		'args': (OrderFuncType.MACHINE,'BUY','ETH_MFT')
	},
	#生成机器人卖订单
	'orders-machine-sell':{
		'task': 'tasks.orders.create_orders',
		'schedule': timedelta(seconds=1),
		'args': (OrderFuncType.MACHINE,'SELL','ETH_MFT')
	},
	#生成深度买订单
	'orders-dept-buy':{
		'task':'tasks.orders.create_orders',
		'schedule': timedelta(seconds=2),
		'args': (OrderFuncType.DEPTH,'BUY','ETH_MFT')
	},
	#生成深度卖订单
	'orders-dept-sell':{
		'task':'tasks.orders.create_orders',
		'schedule': timedelta(seconds=2),
		'args': (OrderFuncType.DEPTH,'SELL','ETH_MFT')
	},
	'users-set-tokens':{
		'task': 'tasks.users.set_tokens',
		'schedule': timedelta(minutes=30),
		'args': ''
	},
}