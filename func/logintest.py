from operatedb import *
import datetime

def timetest(uid):
    info=SearchUserLogin(uid)
    if info:
        sdate=info[2]
        sucdate=sdate+datetime.timedelta(hours=1)
        now=datetime.datetime.now()
        if now <= sucdate:
            return True
        else:
            return False
    else:
        return False

def updatelogindate(uid):
    info=SearchUserLogin(uid)
    id=info[0]
    DeleteUserLogin(uid)
    WriteLogin(id,uid,datetime.datetime.now())

def newlogin(uid):
    if GetLoginMax()[0]:
        lid=GetLoginMax()[0]+1
    else:
        lid=1
    if SearchUserLogin(uid):
        info=SearchUserByID(uid)
        lid=info[0]
        DeleteUserLogin(uid)
    WriteLogin(lid,uid,datetime.datetime.now())
