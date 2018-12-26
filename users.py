# encoding=utf-8
import MySQLdb
from datetime import datetime
import random

from tasks import app
from basetask import BaseTask


class Users(object):
    def __init__(self,host,port,user,passwd,dbname):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = dbname


    def create(self,start,end):
        conn = MySQLdb.connect(host=self.host,port=self.port,user=self.user,passwd=self.passwd,db=self.dbname,charset="utf8")
        curson = conn.cursor()
        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # the number of creating users
        for k in xrange(start,end):
            try:
                email = 'test{0}@test.com'.format(k)
                count = curson.execute("INSERT INTO %s.user (invite_uid, broker_id, nickname, mobile, email, login_salt, login_password, pay_salt, pay_password, lock_num, role, fullname, create_date, createip, update_date, updateip, auth_level) VALUES (0, 10003, null, null, '%s', 'bPRUnp5CH7TO0qPk64rMrcMhQi97F4UqMdhiqkWFOAo=', 'ALQfNh69Br1GG4i6g+h6josFI+pGHc1B1bnLCthrkqCGlWU8a2T3pdT5sMeyxlhTC2XUYH45YYkzQCdkFrqhgBw=', 'ph+GXve0Dhc8hq+M3Gq7BPKqJ/RBBQe5uwqqKtIl6HI=', 'ADU+fge56/AhV4zRgMJ+fM5unYrQXVb4KZ/s12SRg8Qh0Q0uBYdfbgU3jGcqRzyU2pB+H48OMONdAnL1pmOc0U8=', 0, 'user', '223  432', '%s', '192.168.45.112', '%s', '0.0.0.0', 'LEVEL0')"%(self.dbname,email,curr_time,curr_time))
                conn.commit()

                count = curson.execute("SELECT uid FROM %s.user where email='%s'"%(self.dbname,email))
                user_uid = curson.fetchone()[0]

                account_no = str(random.randint(1000000000000000000,1999999999999999999))
                count = curson.execute("INSERT INTO %s.finance (uid,broker_id, account_no, account_kind, asset_code, amount_available, amount_lock, amount_loan, update_date, version) VALUES ('%d',10003, '%s', 'MASTER', 'BTC', 10000.0000000000000000000, 0.000000000000000000, 0.00000000000000000000,'%s', 0)"%(self.dbname,user_uid,account_no,curr_time))
                account_no = str(random.randint(1000000000000000000,1999999999999999999))
                count = curson.execute("INSERT INTO %s.finance (uid,broker_id, account_no, account_kind, asset_code, amount_available, amount_lock, amount_loan, update_date, version) VALUES ('%s', 10003, '%s', 'MASTER', 'ETH', 100000.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000,'%s', 0)"%(self.dbname,user_uid,account_no,curr_time))
                count = curson.execute("INSERT INTO %s.user_pay_password (uid,lock_num, create_date) VALUES ('%s', 0,'%s')"%(self.dbname,user_uid,curr_time)) 
                
                conn.commit()
                print k,user_uid
            except Exception,e:
                print e
                conn.rollback()
        curson.close()
        conn.close()


@app.task(base=BaseTask)
def set_tokens():
    dicts = set_tokens.config.get_section_options_value('users')

    for k,v in dicts.items():
        token = set_tokens.user_token_data.get_usertoken(k,v)
        set_tokens.redis.set(k,token)
