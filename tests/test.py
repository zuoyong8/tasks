# coding: utf-8
from __future__ import print_function
import pytest
from redis import Redis
from os import getcwd

from libs.config import Config
from libs.datas import Datas,OrderFuncType


def set_tokens():
    config = Config(getcwd()+'/tasks/app.config')
    dicts = config.get_section_options_value('users')
    user_token_url = config.get_config_value('urls','URL_USER_LOGIN')
    r = Redis(host='localhost',port=6379,db=1)
    d = Datas(user_token_url)

    for k,v in dicts.items():
	    token = d.get_usertoken(k,v)
	    r.set(k,token)


def test_config_value():
	c = Config('app.config')
	assert c.get_config_value('urls','URL_USER_LOGIN')


def  test_config_options():
    c = Config('app.config')
    return c.get_section_options_value('users')
	# print(user_token_url)
	# d = Datas(user_token_url)
	# token = d.get_usertoken('kily_dd@163.com','kily123')
	# print(token)

	# match_order_url = c.get_config_value('url','URL_MATCH_ORDER')
	# print(match_order_url)
	# d = Datas(match_order_url)
	# print(d.create_order(OrderFuncType.DEPTH,token,'coins123','BUY','ETH_MFT'))
