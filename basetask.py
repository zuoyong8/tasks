from redis import Redis
from os import getcwd
from celery import Task

from libs.config import Config
from libs.datas import Datas

class BaseTask(Task):
    _redis = None
    _config = None
    _match_order_data = None
    _user_token_data = None

    @property
    def redis(self):
        if self._redis is None:
            self._redis = Redis(host='localhost',port=6379,db=1)
        return self._redis


    @property
    def config(self):
        if self._config is None:
            self._config = Config(getcwd()+'/tasks/app.config')
        return self._config


    @property
    def user_token_data(self):
        if self._user_token_data is None:
            if self._config is not None:
                user_token_url = self._config.get_config_value('urls','URL_USER_LOGIN')
                self._user_token_data = Datas(user_token_url)
        return self._user_token_data


    @property
    def match_order_data(self):
        if self._match_order_data is None:
            if self._config is not None:
                match_order_url = self._config.get_config_value('urls','URL_MATCH_ORDER')
                self._match_order_data = Datas(match_order_url)
        return self._match_order_data
