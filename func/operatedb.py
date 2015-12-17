#-*- coding: utf-8 -*-
_author_='shishuangwei'
import operator
import MySQLdb
#import sae.const
"""
HOST = 'localhost'
PORT = 3306
USER = 'root'
PASSWORD = '1234'
DBNAME = 'todolist'
CHARSET = 'utf8'
"""
import sae.const
HOST = sae.const.MYSQL_HOST
PORT = int(sae.const.MYSQL_PORT)
USER = sae.const.MYSQL_USER
PASSWORD = sae.const.MYSQL_PASS
DBNAME = sae.const.MYSQL_DB
CHARSET = 'utf8'

def Init():
    try:
        conn = MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, charset = CHARSET )
        cur = conn.cursor()
        cur.execute('create database if not exists '+ DBNAME )
        conn.select_db(DBNAME)
        cur.execute('create table usertable (userid INT NOT NULL ,\
                                        username VARCHAR(100) UNIQUE ,\
                                        email VARCHAR(100) UNIQUE ,\
                                        gender VARCHAR (20),\
                                        password VARCHAR(100),\
                                        description VARCHAR(200),\
                                        brithday DATE,\
                                        location varchar(100),\
                                        school varchar(100),\
                                        company varchar(100),\
                                        job varchar(100),\
                                        PRIMARY KEY (userid))DEFAULT CHARSET=utf8;')
        cur.execute('create table situation(id INT NOT NULL,\
                                            userid int not null,\
                                          title varchar(100) not null,\
                                          PRIMARY KEY(id)\
                                          )CHARSET=utf8;' )
        cur.execute('create table tasklist(id INT NOT NULL,\
                                          tid INT NOT NULL,\
                                          userid INT NOT NULL,\
                                          title VARCHAR (100),\
                                          sdate DATE,\
                                          priority INT,\
                                          location VARCHAR(100),\
                                          description VARCHAR(200),\
                                          tag INT NOT NULL,\
                                          situation int ,\
                                          ordertag int,\
                                          couid int,\
                                          period int,\
                                          PRIMARY KEY(id)\
                                          )CHARSET=utf8;' )
        cur.execute('create table loginsuccess(id INT NOT NULL,\
                                          userid int not null,\
                                          sdate datetime ,\
                                          PRIMARY KEY(id)\
                                          )CHARSET=utf8;' )
        cur.execute('create table resetpwd(id INT NOT NULL,\
                                          userid int not null,\
                                          skey varchar(100),\
                                          PRIMARY KEY(id))CHARSET=utf8;' )
        cur.execute('create table relationship(id INT PRIMARY key,\
                                          muid int,\
                                          suid int,\
                                          FOREIGN KEY(muid) REFERENCES usertable(userid),\
                                          FOREIGN KEY (suid) REFERENCES usertable(userid))DEFAULT CHARSET=utf8;' )
        cur.execute('create table friendrequest(id int PRIMARY KEY NOT NULL ,\
                                            muid int,\
                                            suid int,\
                                            description varchar(200),\
                                            sdate date,\
                                            tag int,\
                                            FOREIGN KEY (muid) REFERENCES usertable(userid),\
                                            FOREIGN KEY (suid) REFERENCES usertable(userid))DEFAULT CHARSET=utf8;' )
        cur.execute('create table orderrequest(id int PRIMARY KEY NOT NULL ,\
                                              muid int,\
                                              suid int,\
                                              description varchar(200),\
                                              sdate date,\
                                              odate date,\
                                              period int,\
                                              tag int,\
                                              title varchar(100),\
                                              location varchar(100),\
                                              FOREIGN KEY (muid) REFERENCES usertable(userid),\
                                              FOREIGN KEY (suid) REFERENCES usertable(userid))DEFAULT CHARSET=utf8;')


        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def DropDB():
    try:
        conn=MySQLdb.connect(host=HOST,user=USER,passwd=PASSWORD,port=PORT,db=DBNAME,charset=CHARSET)
        cur=conn.cursor()
        cur.execute('drop database '+DBNAME)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False

###################user#########################
def WriteUser(id,username,email,gender,password,description,brithday,location,school,company,job):
    try:
        value= (id,username,email,gender,password,description,brithday,location,school,company,job)
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("insert into usertable values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",value)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def ReadUser():
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from usertable")
        info=cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def DeleteUser(id):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("delete from usertable where userid = %s ", id)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchUserByName(name):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from usertable where username = "+"'"+name+"'")
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchUserByEmail(email):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from usertable where email = " + "'"+ email +"'")
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchUserByID(id):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from usertable where userid = " + "'"+ str(id) +"'")
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def GetUserIDMax():
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select max(userid) as LargestOrderPrice from usertable")
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchUserByKW(kw):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from usertable where username like '%"+kw+"%'")
        info=cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
###################用户登录检测#######################
def WriteLogin(id,uid,date):
    try:
        value= (id,uid,date)
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("insert into loginsuccess values (%s,%s,%s)",value)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchUserLogin(uid):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from loginsuccess where userid = %s", uid)
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def DeleteUserLogin(uid):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("delete from loginsuccess where userid = %s", uid)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def GetLoginMax():
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select max(id) as LargestOrderPrice from loginsuccess")
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
###############tasklist########################
def ReadTask():
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from tasklist")
        info=cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def WriteTask(id,tid,userid,title,sdate,priority,location,description,tag,situation,ordertag,couid,period):
    try:
        value= (id,tid,userid,title,sdate,priority,location,description,tag,situation,ordertag,couid,period)
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("insert into tasklist values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",value)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def DeleteTask(id):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("delete from tasklist where id = %s", id)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchTaskByDate(option,userid,date):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        if option == 1:#今日待办
            cur.execute("select * from tasklist where tag = 0 and  sdate = "+"'"+date+"'"+" and userid = "+str(userid)+" order by sdate")
        elif option == 2: #收集箱
            cur.execute("select * from tasklist where tag = 0 and  sdate <> '3000-01-01' "+" and userid = "+str(userid)+" order by sdate")
        elif option ==3: #将来也许
            cur.execute("select * from tasklist where tag = 0 and  sdate = '3000-01-01' "+" and userid = "+str(userid)+" order by sdate")
        elif option == 4 :#已完成
            cur.execute("select * from tasklist where tag = 1 "+" and userid = "+str(userid)+" order by sdate")
        elif option == 5: #回收站
            cur.execute("select * from tasklist where tag = 2 "+" and userid = "+str(userid)+" order by sdate")
        info=cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def UpdateTagById(option,id):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("update tasklist set tag = %s where id = %s",(option,id))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def GetTaskIDMax():
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select max(id) as LargestOrderPrice from tasklist")
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def GetTaskTIDMax():
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select max(tid) as LargestOrderPrice from tasklist")
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchTaskByID(id):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from tasklist where id = %s ",id)
        info=cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchTaskByTID(tid):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from tasklist where tid = %s ",tid)
        info=cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchTaskBySituation(sid,uid):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from tasklist where situation = %s and userid = %s and tag = 0 order by sdate",(sid,uid))
        info=cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchTaskLike(option,str,uid):
    try:
        str="%%"+str+"%%"
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from tasklist where "+option+" like "+'"'+str+'"'+" and userid = %s order by sdate",uid)
        info=cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
################情景####################
def WriteSituation(id,uid,title):
    try:
        value= (id,uid,title)
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("insert into situation values (%s,%s,%s)",value)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False

def ReadSituation():
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from situation")
        info=cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchSituation(uid):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from situation where userid = %s",uid)
        info=cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchOneSituation(uid,id):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from situation where userid = %s and id= %s",(uid,id))
        info=cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def DeleteOneSituation(uid,id):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("delete from situation where userid = %s and id = %s", (uid,id))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def GetSituationIDMax():
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select max(id) as LargestOrderPrice from situation")
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False


######################重置密码######################
def Writeresetpwd(id,uid,skey):
    try:
        value= (id,uid,skey)
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("insert into resetpwd values (%s,%s,%s)",value)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False

def Searchresetpwd(uid):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from resetpwd where userid = %s", uid)
        info = cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def Deleteresetpwd(id):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("delete from resetpwd where id = %s", id)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def GetresetpwdMax():
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select max(id) as LargestOrderPrice from resetpwd")
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
###############friendreaqest###################
def WriteFriendRequest(id,muid,suid,desc,sdate,tag):
    try:
        value= (id,muid,suid,desc,sdate,tag)
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("insert into friendrequest values (%s,%s,%s,%s,%s,%s)",value)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def UpdateFReqTag(frid,ndate,option):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("update friendrequest set tag = %s  where id = %s",(option,frid))
        conn.commit()
        cur.execute("update friendrequest set sdate= %s where id = %s",(ndate,frid))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchFReqBymuid(muid):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from friendrequest where muid = %s", muid)
        info = cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchFReqBysuid(suid):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from friendrequest where suid = %s", suid)
        info = cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchFReqBysuidmuid(muid,suid):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from friendrequest where suid = %s and muid = %s", (suid,muid))
        info = cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def DeleteFReqByid(id):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("delete from friendrequest where id = %s", id)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def GetFReqIDMax():
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select max(id) as LargestOrderPrice from friendrequest")
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchFReqByTag(uid,option):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        if option == 1:#自己为消息发送方,查看对方处理意见
            cur.execute("select * from friendrequest where (tag = 1 or tag = 2) and  muid = "+str(uid)+"  order by sdate")
        elif option == 2: #自己为消息接收方,查看未处理的消息
            cur.execute("select * from friendrequest where tag = 0  and suid = "+str(uid)+" order by sdate")
        info=cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
#################relationship######################
def WriteRelationship(id,uid1,uid2):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("insert into relationship values (%s,%s,%s)",(id,uid1,uid2))
        cur.execute("insert into relationship values (%s,%s,%s)",(id+1,uid2,uid1))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchRelationshipByMuid(muid):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from relationship where  muid = "+str(muid)+"")
        info=cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchOneRelationship(muid,suid):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from relationship where  muid = "+str(muid)+" and suid = "+str(suid)+"")
        info=cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def GetRelationshipIDMax():
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select max(id) as LargestOrderPrice from relationship")
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def DeleteRelationship(id):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("delete from relationship where id = %s", id)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
###############orderrequest####################
def WriteOReq(id,muid,suid,desc,sdate,odate,period,tag,title,location):
    try:
        value= (id,muid,suid,desc,sdate,odate,period,tag,title,location)
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("insert into orderrequest values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",value)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def UpdateOReqTag(orid,ndate,option):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("update orderrequest set tag = %s  where id = %s",(option,orid))
        conn.commit()
        cur.execute("update orderrequest set sdate= %s where id = %s",(ndate,orid))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchOReqBymuid(muid):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from orderrequest where muid = %s", muid)
        info = cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchOReqBysuid(suid):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from orderrequest where suid = %s", suid)
        info = cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def DeleteOReqByid(id):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("delete from orderrequest where id = %s", id)
        conn.commit()
        cur.close()
        conn.close()
        return True
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def GetOReqIDMax():
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select max(id) as LargestOrderPrice from orderrequest")
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchOReqByTag(uid,option):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        if option == 1:#自己为消息发送方,查看对方处理意见
            cur.execute("select * from orderrequest where (tag = 1 or tag = 2) and  muid = "+str(uid)+"  order by sdate")
        elif option == 2: #自己为消息接收方,查看未处理的消息
            cur.execute("select * from orderrequest where tag = 0  and suid = "+str(uid)+" order by sdate")
        info=cur.fetchall()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False
def SearchOReqByid(id):
    try:
        conn=MySQLdb.connect(host = HOST,user = USER, passwd = PASSWORD, port = PORT, db=DBNAME , charset = CHARSET )
        cur=conn.cursor()
        cur.execute("select * from orderrequest where id = %s ",id)
        info = cur.fetchone()
        cur.close()
        conn.close()
        return info
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False

