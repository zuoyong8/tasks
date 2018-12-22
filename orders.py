# encoding=utf-8
from __future__ import print_function

from libs.datas import OrderFuncType
from tasks import app
from basetask import BaseTask


@app.task(base=BaseTask)
def create_orders(func_type,order_type,symbol):
    dicts = create_orders.config.get_section_options_value('users')
    for k,_ in dicts.items():
        token = create_orders.redis.get(k)
        o_type = 'machine' if func_type==OrderFuncType.MACHINE else 'dept'
        print("func_type="+o_type+"   order_type="+order_type+"   token="+token)
        print(create_orders.match_order_data.create_order(func_type,token,'coins123',order_type,symbol))
        # self.data.create_order(func_type,token,'coins123',order_type,symbol)
	# dicts = create_orders.config.get_section_options_value('symbols')
	# for k,v in dicts.items():
	# 	print('symbol:'+k+'-----'+v)