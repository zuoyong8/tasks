# encoding=utf-8
import MySQLdb
from datetime import datetime

from tasks import app
from basetask import BaseTask


@app.task
def create_users():
    conn = MySQLdb.connect(host="xx.xx.xx.xx",port=3306,user="root",passwd="12345",db="gdae2_market",charset="utf8")
    curson = conn.cursor()
    i = 1
    t1 = datetime.strftime("%Y-%m-%d %H:%M:%S")
    # the number of creating users
    for k in xrange(1,1000):
        try:
            result=curson.execute("INSERT INTO gdae2_market.user (uid, invite_uid, broker_id, nickname, mobile, email, login_salt, login_password, pay_salt, pay_password, lock_num, role, fullname, create_date, createip, update_date, updateip, auth_level) VALUES (%s, 0, 10003, null, null, 'test%s@test.com', 'bPRUnp5CH7TO0qPk64rMrcMhQi97F4UqMdhiqkWFOAo=', 'ALQfNh69Br1GG4i6g+h6josFI+pGHc1B1bnLCthrkqCGlWU8a2T3pdT5sMeyxlhTC2XUYH45YYkzQCdkFrqhgBw=', 'ph+GXve0Dhc8hq+M3Gq7BPKqJ/RBBQe5uwqqKtIl6HI=', 'ADU+fge56/AhV4zRgMJ+fM5unYrQXVb4KZ/s12SRg8Qh0Q0uBYdfbgU3jGcqRzyU2pB+H48OMONdAnL1pmOc0U8=', 0, 'user', '223  432', '2018-04-17 15:50:30', '192.168.45.112', '2018-04-17 16:36:03', '0.0.0.0', 'LEVEL0')"%(i,str(i)))
            result1=curson.execute("INSERT INTO gdae2_market.finance (uid, broker_id, account_no, account_kind, asset_code, amount_available, amount_lock, amount_loan, update_date, version) VALUES (%s, 10003, '%sbtc', 'MASTER', 'BTC', 10000.0000000000000000000, 0.000000000000000000, 0.00000000000000000000,t1, 0)"%(i,str(i)))
            result2=curson.execute("INSERT INTO gdae2_market.finance (uid, broker_id, account_no, account_kind, asset_code, amount_available, amount_lock, amount_loan, update_date, version) VALUES (%s, 10003, '%seth', 'MASTER', 'ETH', 100000.00000000000000000000, 0.00000000000000000000, 0.00000000000000000000,t1, 0)"%(i,str(i)))
            result3=curson.execute("INSERT INTO gdae2_market.user_pay_password (uid, lock_num, create_date) VALUES (%s, 0,t1)"%(i))
            conn.commit()
           # print "result:",i,result3,result1,result2,result
            i += 1
        except Exception:
            #print e
            conn.rollback()
    curson.close()
    conn.close()


@app.task(base=BaseTask)
def set_tokens():
    dicts = set_tokens.config.get_section_options_value('users')

    for k,v in dicts.items():
        token = set_tokens.user_token_data.get_usertoken(k,v)
        set_tokens.redis.set(k,token)
