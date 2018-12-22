# coding: utf-8
import requests
import json
import random
import time
from configparser import ConfigParser

class OrderFuncType:
	DEPTH,MACHINE = range(2)


class Datas(object):
	def __init__(self,url):
		self.url = url


	def get_usertoken(self,account_no,login_password):
		'''
		获取用户token

		account_no      -- 用户名
		login_password  -- 登陆密码
		'''
		headers = {'authorization':
	            'account-no={0},login-password={1}'.format(account_no,login_password)}
		try:
			resp = requests.get(self.url,headers = headers)
			if resp.status_code == 200:
				j = json.loads(resp.text)
				return j['data']['token']
		except Exception,e:
			raise Exception(e.message)

	
	def create_order(self,func_type,user_token,pay_pwd,order_type,symbol):
	    '''
		买卖订单

		func_type  -- 函数类型(DEPTH-深度,MACHINE-机器人)
		user_token -- 用户token
		pay_pwd    -- 用户支付密码
		order_type -- 订单类型(BUY/SELL)
		symbol     -- 交易对
	    '''
	    tx_no = str(random.randint(100000000000000,999999999999999))
	    uid = random.randint(1,1000)
	    if order_type == "BUY":
	    	if func_type == OrderFuncType.DEPTH:
	    		price = round(random.uniform(1,10),5)
	    	elif func_type == OrderFuncType.MACHINE:
		    	price = round(random.uniform(200,300),5)
	    else:
		    if func_type == OrderFuncType.DEPTH:
		        price = round(random.uniform(200,300),5)
		    elif func_type == OrderFuncType.MACHINE:
		    	price = round(random.uniform(1,10),5)
	    num = round(random.uniform(1,10),2)
	    headers = {'authorization':'token={0},pay-password={1}'.format(user_token,pay_pwd)}
	    params = {'outOrderNo': tx_no,
	                'symbol': symbol,
	                'tradeCoinFlag': 'FIXED',
	                'tradeCoinType': order_type,
	                'price': price,
	                'amount': num}
	    try:
	        resp = requests.get(self.url,params = params,headers = headers)
	        if resp.status_code == 200:
	            return resp.text
	    except Exception,e:
	        raise Exception(e.message)


	def generatesign(self,timestamp,noncestr,apisecret):
		# data = "<span id = \"data\">"+jsonData+"</span>"
	    # nonceStr = str(random.randint(10000000000000000000000000000000,99999999999999999999999999999999))
	    # timestamp = int(round(time.time()))

	    # signature = {
	    #     'businessNo':'',  #Api账号 
	    #     'nonceStr': nonceStr,  #32位随机数字
	    #     'timestamp': timestamp , #时间戳（秒数）
	    #     'data': data,  #
	    #     'sign':''   #签名
	    # }
		d = OrderedDict()
		d['nonceStr'] = noncestr
		d['timestamp'] = timestamp
		d['apiSecret'] = apisecret
		d = OrderedDict(sorted(d.items(), key=lambda k: k[0],reverse=True))
		result = ''
		for k,v in d.items():
		    result = '{0}={1}&'.format(k,v)+result
		result = result[0:len(result)-1]
		return md5(result).hexdigest().upper()
