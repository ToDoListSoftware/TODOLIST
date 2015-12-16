#-*- coding: utf-8 -*-
from __future__ import division
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from func.operatedb import *
from func.logintest import *
from datetime import *

def MainOrder(request,uid):
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

        return render_to_response('mainoder.html',{'friendnum':friendnum,'friendlist':fresult,'len1':l1,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def SendOrderpre(request,uid,fuid):
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
        funame=SearchUserByID(int(fuid))[1]
        gender=SearchUserByID(int(fuid))[3]
        return render_to_response('sendorder.html',{'funame':funame,'gender':gender,'fuid':fuid,'len1':l1,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def SendOrder(request):
    uid=request.POST.get('uid')
    fuid=int(request.POST.get('fuid'))
    desc=request.POST.get('reason')
    period=request.POST.getlist('period')
    day=request.POST.get('day')
    title= request.POST.get('title')
    location= request.POST.get('location')
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

        oid=GetOReqIDMax()
        if oid[0]== None:
            oid=1
        else:
            oid=oid[0]+1
        for pitem in period:
            WriteOReq(oid,uid,fuid,desc,datetime.now().strftime("%Y-%m-%d"),day,int(pitem),0,title,location)
            oid+=1
        return render_to_response('myorders.html',{'len1':l1,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))