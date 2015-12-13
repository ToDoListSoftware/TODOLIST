#-*- coding: utf-8 -*-
from __future__ import division
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from func.operatedb import *
from func.logintest import *
from datetime import *
import time
import calendar

def Calendar(request,uid,year=None,month=None,change=None):
    uid= int(uid)
    if year==None and month ==None:
        year=datetime.now().year
        month=datetime.now().month
    year=int(year)
    month=int(month)
    if timetest(uid):
        todaytasks=SearchTaskByDate(1,uid,str(datetime.now()))
        l=len(todaytasks)
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

        year,month = int(year),int(month)
        if change in ("next","prev"):
            now,mdelta=date(year,month,15),timedelta(days=31)
            if change=="next": mod = mdelta
            elif change == "prev" : mod = -mdelta

            year,month = (now+mod).timetuple()[:2]
        cal= calendar.Calendar()
        month_days=cal.itermonthdays(year,month)
        nyear,nmonth,nday=time.localtime()[:3]
        lst=[[]]
        week=0
        for day in month_days:
            entries = current = False
            if day:
                entries=[]
                result=SearchTaskByDate(1,uid,datetime(year,month,day).strftime("%Y-%m-%d"))
                for row in result:
                    entries.append({'id':row[0],'title':row[3],'pri':row[5]})
                if day == nday and year==nyear and month==nmonth:
                    current = True
            lst[week].append((day,entries,current))
            if len(lst[week])==7:
                lst.append([])
                week+=1
        print lst
        return render_to_response('calendar.html',{'month_days':lst,'month':month,'year':year,'flag1':flag1, 'uname':uname,'uid':uid, 'len':l,'result2':result2}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
