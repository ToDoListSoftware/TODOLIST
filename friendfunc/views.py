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
        return render_to_response('searchuser.html',{'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
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
        aflist=SearchFReqBymuid(uid)
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
        return render_to_response('searchuserresult.html',{'usernum':usernum,'keyword':keyword,'fuserlist':fuserlist,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
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
        fuserdict={"uname":row[1],"gender":row[3],"des":row[5],"birth":birth,"location":row[7],"school":row[8],"company":row[9],"job":row[10]}
        return render_to_response('fuserinfo.html',{'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2,"fuserdict":fuserdict}, context_instance=RequestContext(request))
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
        aflist=SearchFReqBymuid(uid)
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

        return render_to_response('searchuserresult.html',{'usernum':usernum,'keyword':keyword,'fuserlist':fuserlist,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))