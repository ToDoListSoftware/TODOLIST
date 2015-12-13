#coding:utf-8

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from func.operatedb import *
from func.code import *
from tasklist.views import *
from func.logintest import *
from func.sendemail import *
# Create your views here.
def testemail(str):
    l=len(str)
    for i in range (0,l):
        if str[i] == '@':
            return True
    return False


def registerpre(request):
    return render(request,'register.html')

def register(request):
    if request.method == "POST":

        if GetUserIDMax()[0]:
            id = GetUserIDMax()[0]+1
        else:
            id = 1
        name = request.POST.get('name')
        email = request.POST.get('email')
        gender = ''
        password = request.POST.get('password')
        fpassword = encode(password)
        description = ''
        date = '1000-01-01'
        if name.isalnum():
            if testemail(email):
                if len(password)>=6:
                    if SearchUserByName(name):
                        flag = 0
                        return render_to_response('register.html', {'flag':flag}, context_instance=RequestContext(request))#用户名已存在
                    elif SearchUserByEmail(email):
                        flag = 1
                        return render_to_response('register.html', {'flag':flag}, context_instance=RequestContext(request)) #邮箱存在
                    else:
                        flag = 2

                        WriteUser(id,name,email,gender,fpassword,description,date)
                        newlogin(id)
                        return render_to_response('loginjump.html', {'uid':id}, context_instance=RequestContext(request))#注册成功
                else:
                    flag=3
                    return render_to_response('register.html', {'flag':flag}, context_instance=RequestContext(request)) #密码过短
            else:
                flag=4
                return render_to_response('register.html', {'flag':flag}, context_instance=RequestContext(request)) #邮箱格式不对
        else:
            flag=5
            return render_to_response('register.html', {'flag':flag}, context_instance=RequestContext(request)) #用户名中存在特殊字符
    else:
        return render(request,'register.html')

def login(request):
    if request.method == "POST":
        str=request.POST.get('name')
        if testemail(str):
            if SearchUserByEmail(str):
                info=SearchUserByEmail(str)
            else:
                flag = 0
                return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request)) #邮箱不存在
        else:
            if SearchUserByName(str):
                info=SearchUserByName(str)
            else:
                flag = 0
                return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request)) #用户名不存在
        password=decode(info[4])
        enterpassword=request.POST.get('password')
        if enterpassword==password :
            flag = 1
            uid = info[0]
            newlogin(uid)
            return render_to_response('loginjump.html', {'uid':uid}, context_instance=RequestContext(request))#登陆成功
        else:
            flag = 0
            return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
    else:
        return render(request,'login.html')

def logout(request,uid):
    if timetest(uid):
        DeleteUserLogin(uid)
        return HttpResponseRedirect('/login')
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))

def ForgetPwd(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        if SearchUserByEmail(email):
            info=SearchUserByEmail(email)
            uid=info[0]
            skey=createskey()
            url="127.0.0.1:8000/ResetPwd/uid"+str(uid)+"skey"+skey
            if GetresetpwdMax()[0]==None:
                id =1
            else:
                id=GetresetpwdMax()[0]+1
            Writeresetpwd(id,uid,skey)
            if sendemail(email,url):
                flag = 1
                return render_to_response('forgetpwd.html', {'flag':flag}, context_instance=RequestContext(request))#邮件发送成功
            else:
                flag = 2
                return render_to_response('forgetpwd.html', {'flag':flag}, context_instance=RequestContext(request))#邮件发送失败
        else:
            flag = 0
            return render_to_response('forgetpwd.html', {'flag':flag}, context_instance=RequestContext(request))#邮箱不存在
    else:
        return render_to_response('forgetpwd.html',context_instance=RequestContext(request))
def ResetPwdpre(request,uid,skey):
    if Searchresetpwd(int(uid)):
        info=Searchresetpwd(int(uid))
        if info[2]==skey:
            Deleteresetpwd(uid)
            info=SearchUserByID(uid)
            name=info[1]
            email=info[2]
            return render_to_response ('resetpwd.html',{'uid':uid,'email':email,'name':name},context_instance=RequestContext(request))
        else:
            return render_to_response('resetpwderror.html')
    else:
        return render_to_response('resetpwderror.html')

def ResetPwd(request):
    uid= request.POST.get('uid')
    pwd= request.POST.get('pwd')
    info = SearchUserByID(int(uid))
    DeleteUser(int(uid))
    if WriteUser(info[0],info[1],info[2],info[3],encode(pwd),info[5],info[6]):
        flag = 3
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
    else:
        flag = 4
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))#失败
def UserDetail(request,uid):
    uid=int(uid)
    if timetest(uid):
        updatelogindate(uid)
        info=SearchUserByID(uid)
        uname=info[1]
        email=info[2]
        gender=info[3]
        if gender == '':
            gender='未填写'
        des=info[5]
        if des=='':
            des='未填写'
        birth=info[6]
        if birth == datetime.date(1000,01,01):
            birth='未填写'

        l=len(SearchTaskByDate(1,uid,str(datetime.date.today())))
        print uname
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
        return render_to_response('personinfo.html', {'uid':uid,'len':l,'result2':result2,'flag1':flag1,'uname':uname,'email':email,'gender':gender,'des':des,'birth':birth}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def UserUpdatepre(request,uid):
    uid=int(uid)
    if timetest(uid):
        updatelogindate(uid)
        info=SearchUserByID(uid)
        uname=info[1]
        email=info[2]
        gender=info[3]
        if gender == '':
            gender=u'未填写'
        des=info[5]
        if des=='':
            des=u'未填写'
        birth=info[6]
        if birth == datetime.date(1000,01,01):
            birth=u'未填写'
        else:
            birth=birth.strftime('%Y-%m-%d')

        l=len(SearchTaskByDate(1,uid,str(datetime.date.today())))
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
        return render_to_response('userupdate.html', {'uid':uid,'len':l,'result2':result2,'flag1':flag1,'uname':uname,'email':email,'gender':gender,'des':des,'birth':birth}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))
def UserUpdate(request):
    uid=int(request.POST.get('uid'))
    if timetest(uid):
        updatelogindate(uid)
        info=SearchUserByID(uid)

        gender=request.POST.get('gender')
        des=request.POST.get('des')
        birth=request.POST.get('birth')
        if birth==u'未填写':
            birth="1000-01-01"

        DeleteUser(uid)
        WriteUser(uid,info[1],info[2],gender,info[4],des,birth)
        uname=info[1]
        l=len(SearchTaskByDate(1,uid,str(datetime.date.today())))
        email=info[2]

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
        return render_to_response('personinfo.html', {'uid':uid,'len':l,'result2':result2,'flag1':flag1,'uname':uname,'email':email,'gender':gender,'des':des,'birth':birth}, context_instance=RequestContext(request))
    else:
        flag = 2
        return render_to_response('login.html', {'flag':flag}, context_instance=RequestContext(request))



