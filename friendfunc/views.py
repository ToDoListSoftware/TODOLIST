#-*- coding: utf-8 -*-
from __future__ import division
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from func.operatedb import *
from func.logintest import *
from datetime import *
def SearchUserpre(request,uid):
    uid =int(uid)
    if timetest(uid):
        l=len(SearchTaskByDate(1,uid,str(datetime.today().strftime("%Y-%m-%d"))))
        updatelogindate(uid)
        uname=SearchUserByID(uid)[1]
        result2=[]
        info=SearchSituation(uid)
        if len(info)==0:
            result2=[]
        else:
            for i in info:
                sid = i[0]
                stitle=i[2]
                newnode={'sid':sid,'stitle':stitle}
                result2.append(newnode)
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1
        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)
        return render_to_response('searchuser.html',{'len1':l1,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def SearchUser(request):
    uid=request.POST.get('uid')
    keyword=request.POST.get('keyword')
    uid = int(uid)
    if timetest(uid):
        l=len(SearchTaskByDate(1,uid,str(datetime.today().strftime("%Y-%m-%d"))))
        updatelogindate(uid)
        uname=SearchUserByID(uid)[1]
        result2=[]
        info=SearchSituation(uid)
        if len(info)==0:
            result2=[]
        else:
            for i in info:
                sid = i[0]
                stitle=i[2]
                newnode={'sid':sid,'stitle':stitle}
                result2.append(newnode)
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1

        userresult=SearchUserByKW(keyword)
        fuserlist=[]
        aflist=SearchRelationshipByMuid(uid)
        flist=[]

        if len(aflist) !=0:
            for j in aflist:
                flist.append(j[2])
        for row in userresult:
            if row[0] != uid and row[0] not in flist:#不是自己好友
                fuserlist.append({'fuid':row[0],'funame':row[1],'gender':row[3],'ftag':0})
            elif row[0] != uid and row[0] in flist:#是自己好友
                fuserlist.append({'fuid':row[0],'funame':row[1],'gender':row[3],'ftag':1})
        usernum = len(fuserlist)
        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)
        return render_to_response('searchuserresult.html',{'len1':l1,'usernum':usernum,'keyword':keyword,'fuserlist':fuserlist,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def ShowUserDetail(request,fuid,uid):
    fuid=int(fuid)
    uid = int(uid)
    if timetest(uid):
        l=len(SearchTaskByDate(1,uid,str(datetime.today().strftime("%Y-%m-%d"))))
        updatelogindate(uid)
        uname=SearchUserByID(uid)[1]
        result2=[]
        info=SearchSituation(uid)
        if len(info)==0:
            result2=[]
        else:
            for i in info:
                sid = i[0]
                stitle=i[2]
                newnode={'sid':sid,'stitle':stitle}
                result2.append(newnode)
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1

        row=SearchUserByID(fuid)
        if row[6]==date(1000,01,01):
            birth=u"未填写"
        else:
            birth=row[6].strftime("%Y-%m-%d")
        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)
        fuserdict={"uname":row[1],"gender":row[3],"des":row[5],"birth":birth,"location":row[7],"school":row[8],"company":row[9],"job":row[10]}
        return render_to_response('fuserinfo.html',{'len1':l1,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2,"fuserdict":fuserdict}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
# Create your views here.
def AddFriend(request):
    uid=int(request.POST.get('uid'))
    fuid=int(request.POST.get('fuid'))
    desc=request.POST.get('desc')
    keyword=request.POST.get('keyword')
    if desc==None or desc=='':
        desc = '未填写'
    if timetest(uid):
        l=len(SearchTaskByDate(1,uid,str(datetime.today().strftime("%Y-%m-%d"))))
        updatelogindate(uid)
        uname=SearchUserByID(uid)[1]
        result2=[]
        info=SearchSituation(uid)
        if len(info)==0:
            result2=[]
        else:
            for i in info:
                sid = i[0]
                stitle=i[2]
                newnode={'sid':sid,'stitle':stitle}
                result2.append(newnode)
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1

        userresult=SearchUserByKW(keyword)
        fuserlist=[]
        aflist=SearchRelationshipByMuid(uid)
        flist=[]
        if len(aflist) !=0:
            for j in aflist:
                flist.append(j[2])
        for row in userresult:
            if row[0] != uid and row[0] not in flist:#不是自己好友
                fuserlist.append({'fuid':row[0],'funame':row[1],'gender':row[3],'ftag':0})
            elif row[0] != uid and row[0] in flist:#是自己好友
                fuserlist.append({'fuid':row[0],'funame':row[1],'gender':row[3],'ftag':1})
        usernum = len(fuserlist)

        afuid=fuserlist[fuid-1].get('fuid')
        oid=GetFReqIDMax()
        if oid[0]==None:
            nid=1
        else:
            nid=oid[0]+1
        WriteFriendRequest(nid,uid,afuid,desc,datetime.now().strftime("%Y-%m-%d"),0)
        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)
        return render_to_response('searchuserresult.html',{'len1':l1,'usernum':usernum,'keyword':keyword,'fuserlist':fuserlist,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def ShowMessagepre(request,uid):
    uid = int(uid)
    if timetest(uid):
        l=len(SearchTaskByDate(1,uid,str(datetime.today().strftime("%Y-%m-%d"))))
        updatelogindate(uid)
        uname=SearchUserByID(uid)[1]
        result2=[]
        info=SearchSituation(uid)
        if len(info)==0:
            result2=[]
        else:
            for i in info:
                sid = i[0]
                stitle=i[2]
                newnode={'sid':sid,'stitle':stitle}
                result2.append(newnode)
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1

        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)

        msg=[]
        for row in tmsg0:
            funame = SearchUserByID(row[1])[1]
            node={'id':row[0],'fuid':row[1],'funame':funame,'desc':row[3],'sdate':row[4].strftime("%Y-%m-%d"),'ttag':0}

            msg.append(node)
        for row in tmsg1:
            funame = SearchUserByID(row[2])[1]
            node={'id':row[0],'fuid':row[2],'funame':funame,'desc':row[3],'sdate':row[4].strftime("%Y-%m-%d"),'tag':row[5],'ttag':1}
            msg.append(node)

        for row in tmsg2:
            funame = SearchUserByID(row[1])[1]
            node={'id':row[0],'fuid':row[1],'funame':funame,'desc':row[3],'sdate':row[4].strftime("%Y-%m-%d"),'odate':row[5].strftime("%Y-%m-%d"),'period':row[6],'ttag':2}
            msg.append(node)

        for row in tmsg3:
            funame = SearchUserByID(row[2])[1]
            node={'id':row[0],'fuid':row[2],'funame':funame,'sdate':row[4].strftime("%Y-%m-%d"),'odate':row[5].strftime("%Y-%m-%d"),'period':row[6],'tag':row[7],'ttag':3}
            msg.append(node)

        msg = sorted(msg, key=operator.itemgetter('sdate'))

        return render_to_response('message.html',{'len1':l1,'messages':msg,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def DealMsg(request,option,mid,uid,ttag,fuid):
    uid = int(uid)
    mid=int(mid)
    option=int(option)
    ttag=int(ttag)
    if timetest(uid):
        updatelogindate(uid)
        if ttag==0 or ttag==1:
            if option==3:
                DeleteFReqByid(mid)
                othermsg=SearchFReqBysuidmuid(uid,fuid)
                for row in othermsg:
                    if row[0]!=mid:
                        DeleteFReqByid(row[0])
            elif option==1:#同意好友请求
                UpdateFReqTag(mid,datetime.now().strftime("%Y-%m-%d"),1)
                rid=GetRelationshipIDMax()
                if rid[0]==''or rid[0] == None:
                    rid=1
                else:
                    rid=rid[0]+1
                WriteRelationship(rid,uid,fuid)
                othermsg=SearchFReqBysuidmuid(fuid,uid)
                for row in othermsg:
                    if row[0]!=mid:
                        DeleteFReqByid(row[0])
            elif option==2:
                UpdateFReqTag(mid,datetime.now().strftime("%Y-%m-%d"),2)
                othermsg=SearchFReqBysuidmuid(fuid,uid)
                for row in othermsg:
                    if row[0]!=mid:
                        DeleteFReqByid(row[0])
        elif ttag==3 or ttag==2:
            if option==3:#忽略
                DeleteOReqByid(mid)
            elif option == 1:#同意
                UpdateOReqTag(mid,datetime.now().strftime("%Y-%m-%d"),1)
                id = GetTaskIDMax()
                if id[0]==''or id[0] == None:
                    id=1
                else:
                    id=id[0]+1

                tid = GetTaskTIDMax()
                if tid[0]==''or tid[0] == None:
                    tid=1
                else:
                    tid=tid[0]+1
                msg=SearchOReqByid(mid)
                uid1=msg[1]
                uid2=msg[2]
                WriteTask(id,tid,uid1,msg[8],msg[5],2,msg[9],msg[3],0,None,1,uid2,msg[6])
                WriteTask(id+1,tid,uid2,msg[8],msg[5],2,msg[9],msg[3],0,None,1,uid1,msg[6])
            elif option==2:
                UpdateOReqTag(mid,datetime.now().strftime("%Y-%m-%d"),2)

        return HttpResponseRedirect('/ShowMessage/'+str(uid))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def ShowFriend(request,uid):
    uid=int(uid)
    if timetest(uid):
        l=len(SearchTaskByDate(1,uid,str(datetime.today().strftime("%Y-%m-%d"))))
        updatelogindate(uid)
        uname=SearchUserByID(uid)[1]
        result2=[]
        info=SearchSituation(uid)
        if len(info)==0:
            result2=[]
        else:
            for i in info:
                sid = i[0]
                stitle=i[2]
                newnode={'sid':sid,'stitle':stitle}
                result2.append(newnode)
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1

        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)

        friendlist=SearchRelationshipByMuid(uid)
        fresult=[]
        for row in friendlist:
            node={'fuid':row[2],'funame':SearchUserByID(row[2])[1],'gender':SearchUserByID(row[2])[3]}
            fresult.append(node)
        friendnum = len(fresult)
        fresult=sorted(fresult,key=operator.itemgetter('funame'))
        return render_to_response('myfriend.html',{'friendnum':friendnum,'friendlist':fresult,'len1':l1,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def SearchFriend(request):
    keyword=request.POST.get('keyword')
    uid=request.POST.get('uid')
    uid=int(uid)
    if timetest(uid):
        l=len(SearchTaskByDate(1,uid,str(datetime.today().strftime("%Y-%m-%d"))))
        updatelogindate(uid)
        uname=SearchUserByID(uid)[1]
        result2=[]
        info=SearchSituation(uid)
        if len(info)==0:
            result2=[]
        else:
            for i in info:
                sid = i[0]
                stitle=i[2]
                newnode={'sid':sid,'stitle':stitle}
                result2.append(newnode)
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1

        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)

        result=SearchRelationshipByMuid(uid)
        fresult=[]
        for row in result:
            if keyword in SearchUserByID(row[2])[1]:
                node={'fuid':row[2],'funame':SearchUserByID(row[2])[1],'gender':SearchUserByID(row[2])[3]}
                fresult.append(node)
        friendnum=len(fresult)
        return render_to_response('myfriend.html',{'keyword':keyword,'flag2':1,'friendnum':friendnum,'friendlist':fresult,'len1':l1,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def DeleteFriend(request,uid,fuid,option,keyword=None):
    uid=int(uid)
    fuid=int(fuid)
    option=int(option)
    if timetest(uid):
        l=len(SearchTaskByDate(1,uid,str(datetime.today().strftime("%Y-%m-%d"))))
        updatelogindate(uid)
        uname=SearchUserByID(uid)[1]
        result2=[]
        info=SearchSituation(uid)
        if len(info)==0:
            result2=[]
        else:
            for i in info:
                sid = i[0]
                stitle=i[2]
                newnode={'sid':sid,'stitle':stitle}
                result2.append(newnode)
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1

        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)

        DeleteRelationship(SearchOneRelationship(uid,fuid)[0])
        DeleteRelationship(SearchOneRelationship(fuid,uid)[0])

        if keyword and option==3:#查询好友
            result=SearchRelationshipByMuid(uid)
            fresult=[]
            for row in result:
                if keyword in SearchUserByID(row[2])[1]:
                    node={'fuid':row[2],'funame':SearchUserByID(row[2])[1],'gender':SearchUserByID(row[2])[3]}
                    fresult.append(node)
            friendnum=len(fresult)
            return render_to_response('myfriend.html',{'keyword':keyword,'flag2':1,'friendnum':friendnum,'friendlist':fresult,'len1':l1,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
        else:
            if option==0:#查看好友
                return HttpResponseRedirect('/MyFriendPre/'+str(uid))
            elif option==1:#查询用户界面
                if keyword == None:
                    keyword=''
                userresult=SearchUserByKW(keyword)
                fuserlist=[]
                aflist=SearchRelationshipByMuid(uid)
                flist=[]
                if len(aflist) !=0:
                    for j in aflist:
                        flist.append(j[2])
                for row in userresult:
                    if row[0] != uid and row[0] not in flist:#不是自己好友
                        fuserlist.append({'fuid':row[0],'funame':row[1],'gender':row[3],'ftag':0})
                    elif row[0] != uid and row[0] in flist:#是自己好友
                        fuserlist.append({'fuid':row[0],'funame':row[1],'gender':row[3],'ftag':1})
                usernum = len(fuserlist)
                return render_to_response('searchuserresult.html',{'len1':l1,'usernum':usernum,'keyword':keyword,'fuserlist':fuserlist,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
