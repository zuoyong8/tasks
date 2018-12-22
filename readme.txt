
// python: 2.7.5

//安装MySQLdb
1、 yum install mysql-devel libmysqlclient-dev (centos or debian)
   apt-get install libmysqlclient-dev  (ubuntu)

   //下载MySQL-python
   wget http://sourceforge.net/projects/mysql-python/files/mysql-python/1.2.3/MySQL-python-1.2.3.tar.gz 
    
   //编译并安装  
   python setup.py build
   python setup.py install

//安装redis
2、 安装redis

　　apt-get install redis-server (ubuntu)

//安装依赖包
3、  pip install requirements.txt