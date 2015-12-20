#-*- coding: utf-8 -*-
from __future__ import division
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from func.operatedb import *
from func.logintest import *
import time
import datetime
def strtodatetime(datestr,format):
    return datetime.datetime.strptime(datestr,format)
def datediff(beginDate,endDate):
    format="%Y-%m-%d"
    bd=strtodatetime(beginDate,format)
    ed=strtodatetime(endDate,format)
    oneday=datetime.timedelta(days=1)
    count=0
    while bd!=ed:
        ed=ed-oneday
        count+=1
    return count
def TodayTask(request,uid):
    if timetest(uid):
        updatelogindate(uid)
        tasks=SearchTaskByDate(1,uid,str(datetime.date.today()))
        result=[]
        l=len(tasks)
        uname=SearchUserByID(uid)[1]
        for row in tasks:
            id = row[0]
            title = row[3]
            date =  row[4]
            pri=row[5]
            newnode = {'id1':id, 'title1':title, 'date1':date, 'pri1':pri}
            result.append(newnode)
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
        return render_to_response('index.html',{'len1':l1,'flag1':flag1,'result':result,'result2':result2,'uname':uname,'uid':uid, 'len':l}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))


def TaskFinish(request):
    uid = int(request.POST.get('uid'))
    id = int(request.POST.get('id'))
    if timetest(uid):
        updatelogindate(uid)
        UpdateTagById(1,id)
        uid = request.POST.get('uid')
        return  HttpResponseRedirect('/TodayTask/'+str(uid))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def FinishedTask(request,uid):
    if timetest(uid):
        todaytasks=SearchTaskByDate(1,uid,str(datetime.date.today()))
        l=len(todaytasks)
        updatelogindate(uid)
        tasks=SearchTaskByDate(4,uid,str(datetime.date.today()))
        result=[]
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
        for row in tasks:
            id = row[0]
            title = row[3]
            date =  row[4]
            if date==datetime.date(3000, 1, 1):
                tag= 1
            else:
                tag=0
            pri=row[5]
            newnode = {'id1':id, 'title1':title, 'date1':date, 'pri1':pri,"tag1":tag}
            result.append(newnode)
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1
        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)
        return render_to_response('finished.html',{'len1':l1,'flag1':flag1,'result':result, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def TaskUnfinish(request):
    uid = int(request.POST.get('uid'))
    id = int(request.POST.get('id'))
    if timetest(uid):
        updatelogindate(uid)
        UpdateTagById(0,id)
        uid = request.POST.get('uid')
        return  HttpResponseRedirect('/finished/'+str(uid))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def CollectedTask(request,uid):
    if timetest(uid):
        todaytasks=SearchTaskByDate(1,uid,str(datetime.date.today()))
        l=len(todaytasks)
        updatelogindate(uid)
        tasks=SearchTaskByDate(2,uid,str(datetime.date.today()))
        result=[]
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
        for row in tasks:
            id = row[0]
            title = row[3]
            date =  row[4]
            pri=row[5]
            newnode = {'id1':id, 'title1':title, 'date1':date, 'pri1':pri}
            result.append(newnode)
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1
        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)
        return render_to_response('collect.html',{'len1':l1,'flag1':flag1,'result':result, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def TaskFinishInCollect(request):
    uid = int(request.POST.get('uid'))
    id = int(request.POST.get('id'))
    print id
    if timetest(uid):
        updatelogindate(uid)
        UpdateTagById(1,id)
        uid = request.POST.get('uid')
        return  HttpResponseRedirect('/CollectedTask/'+str(uid))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def TaskFinishInMaybe(request):
    uid = int(request.POST.get('uid'))
    id = int(request.POST.get('id'))
    print id
    if timetest(uid):
        updatelogindate(uid)
        UpdateTagById(1,id)
        uid = request.POST.get('uid')
        return  HttpResponseRedirect('/maybe/'+str(uid))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def TaskDelete(request):
    uid = int(request.POST.get('uid'))
    id = int(request.POST.get('id'))
    print id
    if timetest(uid):
        updatelogindate(uid)
        UpdateTagById(2,id)
        uid = request.POST.get('uid')
        return  HttpResponseRedirect('/TodayTask/'+str(uid))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def TaskDeleteInCollect(request):
    uid = int(request.POST.get('uid'))
    id = int(request.POST.get('id'))
    print id
    if timetest(uid):
        updatelogindate(uid)
        UpdateTagById(2,id)
        uid = request.POST.get('uid')
        return  HttpResponseRedirect('/CollectedTask/'+str(uid))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def TaskDeleteInMaybe(request):
    uid = int(request.POST.get('uid'))
    id = int(request.POST.get('id'))
    print id
    if timetest(uid):
        updatelogindate(uid)
        UpdateTagById(2,id)
        uid = request.POST.get('uid')
        return  HttpResponseRedirect('/maybe/'+str(uid))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def TaskDeleteInFinish(request):
    uid = int(request.POST.get('uid'))
    id = int(request.POST.get('id'))
    print id
    if timetest(uid):
        updatelogindate(uid)
        UpdateTagById(2,id)
        uid = request.POST.get('uid')
        return  HttpResponseRedirect('/finished/'+str(uid))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def TaskDeleteInSitu(request):
    uid = int(request.POST.get('uid'))
    id = int(request.POST.get('id'))
    sid = request.POST.get('sid')
    print id
    if timetest(uid):
        updatelogindate(uid)
        UpdateTagById(2,id)
        uid = request.POST.get('uid')
        return  HttpResponseRedirect('/SituationTask/uid'+str(uid)+'sid'+str(sid)+'/')
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def TaskUndelete(request):
    uid = int(request.POST.get('uid'))
    id = int(request.POST.get('id'))
    if timetest(uid):
        updatelogindate(uid)
        UpdateTagById(0,id)
        uid = request.POST.get('uid')
        return  HttpResponseRedirect('/deleted/'+str(uid))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def DeletedTask(request,uid):
    if timetest(uid):
        todaytasks=SearchTaskByDate(1,uid,str(datetime.date.today()))
        l=len(todaytasks)
        updatelogindate(uid)
        tasks=SearchTaskByDate(5,uid,str(datetime.date.today()))
        result=[]
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
        for row in tasks:
            id = row[0]
            title = row[3]
            date =  row[4]
            print date
            if date==datetime.date(3000, 1, 1):
                tag= 1
            else:
                tag=0
            pri=row[5]
            newnode = {'id1':id, 'title1':title, 'date1':date, 'pri1':pri,'tag1':tag}
            result.append(newnode)
            print newnode
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1
        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)
        return render_to_response('deleted.html',{'len1':l1,'flag1':flag1,'result':result, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def FutureTask(request,uid):
    if timetest(uid):
        todaytasks=SearchTaskByDate(1,uid,str(datetime.date.today()))
        l=len(todaytasks)
        updatelogindate(uid)
        tasks=SearchTaskByDate(3,uid,str(datetime.date.today()))
        result=[]
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

        for row in tasks:
            id = row[0]
            title = row[3]
            pri=row[5]
            newnode = {'id1':id, 'title1':title, 'pri1':pri}
            result.append(newnode)
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1
        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)
        return render_to_response('maybe.html',{'len1':l1,'flag1':flag1,'result':result, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def AddTaskpre(request,uid,option):
    if timetest(uid):
        updatelogindate(uid)
        todaytasks=SearchTaskByDate(1,uid,str(datetime.date.today()))
        l=len(todaytasks)
        uname=SearchUserByID(uid)[1]
        info=SearchSituation(uid)
        result2=[]
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
        return render_to_response('addtask.html',{'len1':l1,'flag1':flag1,'uname':uname,'uid':uid,'option':option,'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def AddTask(request):
    uid=request.POST.get('uid')
    option=int(request.POST.get('option'))
    if timetest(uid):
        title = request.POST.get('title')
        sdate = request.POST.get('sdate')
        edate = request.POST.get('edate')
        priority = request.POST.get('priority')
        location = request.POST.get('location')
        if location== None or location=='':
            location='无'
        situation = request.POST.get('situation')
        des = request.POST.get('des')
        if des== None or des=='':
            des='无'
        ordertag=0
        couid=0
        period=0
        if request.POST.get('situation')=='':
            situation=None
        else:
            situation=int(request.POST.get('situation'))

        updatelogindate(uid)
        if GetTaskIDMax()[0]==None:
            id=1
        else:
            id=GetTaskIDMax()[0]+1
        if GetTaskTIDMax()[0]==None:
            tid=1
        else:
            tid=GetTaskTIDMax()[0]+1
        if sdate ==u'无' :
            WriteTask(int(id),int(tid),int(uid),title,"3000-01-01",int(priority),location,des,0,situation,ordertag,couid,period)
        elif edate ==u'无':
            WriteTask(int(id),int(tid),int(uid),title,sdate,int(priority),location,des,0,situation,ordertag,couid,period)
        elif edate==sdate:
            WriteTask(int(id),int(tid),int(uid),title,sdate,int(priority),location,des,0,situation,ordertag,couid,period)
        elif edate!=sdate:
            days=datediff(sdate,edate)
            date1=strtodatetime(sdate,"%Y-%m-%d")
            for i in range(0,days+1):
                tdate=date1+datetime.timedelta(days=i)
                if GetTaskIDMax()[0]== None:
                    id=1
                else:
                    id=GetTaskIDMax()[0]+1
                WriteTask(id,tid,uid,title,tdate,priority,location,des,0,situation,ordertag,couid,period)
        if option==0:
            return HttpResponseRedirect('/CollectedTask/'+str(uid))
        elif option == 1:
            return HttpResponseRedirect('/TodayTask/'+str(uid))
        elif option == 2:
            return HttpResponseRedirect('/maybe/'+str(uid))
        elif option ==3:
            return HttpResponseRedirect('/finished/'+str(uid))
        elif option ==4:
            return HttpResponseRedirect('/DeletedTask/'+str(uid))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def AddSituationpre(request,uid):
    if timetest(uid):
        updatelogindate(uid)
        todaytasks=SearchTaskByDate(1,uid,str(datetime.date.today()))
        l=len(todaytasks)
        uname=SearchUserByID(uid)[1]
        info=SearchSituation(int(uid))
        result2=[]
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
        return render_to_response('addsituation.html',{'len1':l1,'flag1':flag1,'uname':uname,'result2':result2,'uid':uid,'len':l}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def AddSituation(request):
    uid = int(request.POST.get('uid'))
    title=request.POST.get('title')
    if timetest(uid):
        updatelogindate(uid)
        todaytasks=SearchTaskByDate(1,uid,str(datetime.date.today()))
        l=len(todaytasks)
        if GetSituationIDMax()[0]==None:
            id=1
        else:
            id=GetSituationIDMax()[0]+1
        WriteSituation(id,uid,title)
        return HttpResponseRedirect('/TodayTask/'+str(uid))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def SituationTask(request,uid,sid):
    if timetest(uid):
        sid1=int(sid)
        updatelogindate(uid)
        tasks=SearchTaskBySituation(sid,uid)
        result=[]
        l=len(SearchTaskByDate(1,uid,str(datetime.date.today())))
        uname=SearchUserByID(uid)[1]
        for row in tasks:
            id = row[0]
            title = row[3]
            date =  row[4]
            if date==datetime.date(3000, 1, 1):
                tag= 1
            else:
                tag=0
            pri=row[5]
            newnode = {'id1':id, 'title1':title, 'date1':date, 'pri1':pri,'tag1':tag}
            result.append(newnode)
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
        return render_to_response('situationtask.html',{'len1':l1,'flag1':flag1,'result':result,'result2':result2,'uname':uname,'uid':uid, 'len':l,'sid':sid1}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def searchtask(request):
    uid=int(request.POST.get('uid'))
    string=request.POST.get('word')
    r1=SearchTaskLike('title',string,uid)
    r2=SearchTaskLike('location',string,uid)
    r3=SearchTaskLike('description',string,uid)
    result=[]
    if r1:
        result.extend(r1)
    if r2:
        result.extend(r2)
    if r3:
        result.extend(r3)
    tasks=sorted(set(result),key=operator.itemgetter(4))
    if timetest(uid):
        updatelogindate(uid)
        result=[]
        l=len(SearchTaskByDate(1,uid,str(datetime.date.today())))
        uname=SearchUserByID(uid)[1]
        tag=0
        for row in tasks:
            tag=0
            id = row[0]
            title = row[3]
            date =  row[4]
            if date==datetime.date(3000, 1, 1):
                tag= 1
            else:
                tag=0
            pri=row[5]
            newnode = {'id1':id, 'title1':title, 'date1':date, 'pri1':pri,"tag1":tag}
            result.append(newnode)
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
        if result == []:
            flag2 = 0
        else:
            flag2 = 1
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1
        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)
        return render_to_response('searchresult.html',{'len1':l1,'tag':tag,'flag1':flag1,'result':result,'result2':result2,'uname':uname,'uid':uid, 'len':l,'string':string,'flag2':flag2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def TaskDetail(request,id,uid):
    uid =int(uid)
    if timetest(uid):
        name=SearchUserByID(int(uid))[1]
        num=0
        sum=1
        l=len(SearchTaskByDate(1,uid,str(datetime.date.today())))
        info = SearchTaskByID(id)
        tid = info[1]
        title=info[3]
        date=info[4]
        if date == datetime.date(3000, 1, 1):
            tag1=1#将来
        else:
            tag1=0
        priority=info[5]
        location=info[6]
        desc=info[7]
        tag=info[8]
        ordertag=info[10]
        if ordertag==1:
            couname=SearchUserByID(info[11])[1]
            period=info[12]
            if period == 1:
                period="6:00~9:00"
            elif period == 2:
                period="9:00~12:00"
            elif period == 3:
                period="12:00~15:00"
            elif period == 4:
                period="15:00~18:00"
            elif period == 5:
                period="18:00~21:00"
            elif period == 6:
                period="21:00~24:00"

        else:
            couname=0
            period=0
        if tag==1:
            num+=1

        if SearchOneSituation(int(uid),info[9]):
            situation=SearchOneSituation(int(uid),info[9])[2]
        else:
            situation='无'
        result=[]
        tasks=SearchTaskByTID(uid,tid)
        for i in tasks:
            id1=i[0]
            if id1==int(id):
                continue
            title1=i[3]
            date1=i[4]
            pri=i[5]
            desc1=i[7]
            if i[8]==1:
                num+=1
            newnode={'id1':id1,'title1':title1,'date1':date1,'pri':pri,'desc1':desc1}
            result.append(newnode)
            sum+=1
        if len(result)==0:
            tag2=1#为空
        else:
            tag2=0



        result2=[]
        info1=SearchSituation(uid)
        if len(info1)==0:
            result2=[]
        else:
            for i in info1:
                sid = i[0]
                stitle=i[2]
                newnode={'sid':sid,'stitle':stitle}
                result2.append(newnode)
        if result2==[]:
            flag1 = 0
        else:
            flag1 = 1
        per=round(float(num/sum),2)*100
        tmsg0=SearchFReqByTag(uid,2)#ttag=0
        tmsg1=SearchFReqByTag(uid,1)#ttag=1
        tmsg2=SearchOReqByTag(uid,2)#ttag=2
        tmsg3=SearchOReqByTag(uid,1)#ttag=3
        l1=len(tmsg0)+len(tmsg1)+len(tmsg2)+len(tmsg3)
        return render_to_response("taskdetail.html",{'ordertag':ordertag,'couname':couname,'period':period,'len1':l1,'result2':result2,'flag1':flag1,'l':l,'uname':name,'id':id,'uid':uid,'title':title,'sdate':date,'tag1':tag1,'tag':tag,'priority':priority,'location':location,\
                                                     'des':desc,'situation':situation,'tag2':tag2,'result':result,'per':per}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def ChangeTaskpre(request):
    uid=request.POST.get("uid")
    id=request.POST.get("id")
    name=SearchUserByID(int(uid))[1]
    if timetest(uid):
        info=SearchTaskByID(id)
        tid=info[1]
        title=info[3]
        date=info[4].strftime('%Y-%m-%d')
        if date=="3000-01-01":
            date=u"无"
        priority=info[5]
        location=info[6]
        desc=info[7]
        tag=info[8]
        sid=info[9]
        ordertag=info[10]
        if ordertag==1:
            couname=SearchUserByID(info[11])[1]
            period=info[12]
            if period == 1:
                period="6:00~9:00"
            elif period == 2:
                period="9:00~12:00"
            elif period == 3:
                period="12:00~15:00"
            elif period == 4:
                period="15:00~18:00"
            elif period == 5:
                period="18:00~21:00"
            elif period == 6:
                period="21:00~24:00"
        else:
            couname=0
            period=0
        if sid==None:
            situ=u'无'
        else:
            situ=SearchOneSituation(int(uid),sid)[2]
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
        return render_to_response("updatetask.html",{'ordertag':ordertag,'couname':couname,'period':period,"situ1":situ,"uid":int(uid),'tid':tid,'uname':name,"id":int(id),"title":title,"date":date,"pri":priority,"location":location,"des":desc,"tag":tag,"result2":result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def ChangeTask(request):
    uid=request.POST.get("uid")
    id=request.POST.get("id")
    tid=request.POST.get("tid")
    title=request.POST.get("title")
    sdate=request.POST.get("sdate")
    if timetest(uid):
        info=SearchTaskByID(id)
        if sdate==u"无":
            sdate="3000-01-01"
        priority=request.POST.get("pri")
        location=request.POST.get("location")
        des=request.POST.get("des")
        tag=request.POST.get("tag")
        situation=request.POST.get("situation")
        if situation=='':
            situ=None
        else:
            situ=int(situation)
        if timetest(int(uid)):
            DeleteTask(int(id))
            if info[10]==0:
                WriteTask(int(id),int(tid),int(uid),title,sdate,priority,location,des,tag,situ,info[10],info[11],info[12])
            elif info[10]==1:
                WriteTask(int(id),int(tid),int(uid),title,info[4],priority,location,des,tag,situ,info[10],info[11],info[12])
            return HttpResponseRedirect('/TaskDetail/id'+id+'uid'+uid+'/')
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def DeleteSituation(request,sid,uid):
    uid = int(uid)
    sid = int(sid)
    if timetest(uid):
        info=SearchTaskByID(uid)
        DeleteOneSituation(uid,sid)
        return HttpResponseRedirect('/UserDetail/'+str(uid)+'/')
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def DeleteAllTask(request,option,uid):
    uid = int(uid)
    option = int (option)
    if timetest(uid):
        if option==1:
            DeleteDoneTask(uid)
            return HttpResponseRedirect('/finished/'+str(uid)+'/')
        elif option==2:
            DeleteDeleteTask(uid)
            return HttpResponseRedirect('/deleted/'+str(uid)+'/')

    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

