#-*- coding: utf-8 -*-
_author_='shishuangwei'
import random
lettertrans=['q','a','z','w','s','x','e','d','c','r','f','v','t','g','b','y','h','n','u','j','m','i','k','o','l','p']
numtrans=['3','7','4','5','1','8','2','9','0','6']
def encode(str):#加密密码
    l = len(str)
    result=''
    for i in range (0,l):
        asc=ord(str[i])
        if asc >= 48 and asc <= 57:
            index = asc-48
            result+=numtrans[index]
        elif asc >= 97 and asc <= 122:
            index = asc-97
            result+=lettertrans[index]
        elif asc >= 65 and asc <= 90:
            index = asc-65
            result+=lettertrans[index].upper()
        else:
            result+=str[i]
    return result
def decode(str):#解密
    l=len(str)
    result=''
    for i in range(0,l):
        asc=ord(str[i])
        if asc >= 48 and asc <= 57:
            index=numtrans.index(str[i])
            result+=chr(48+index)
        elif asc >= 97 and asc <= 122:
            index = lettertrans.index(str[i])
            result+=chr(97+index)
        elif asc >= 65 and asc <= 90:
            index = lettertrans.index(str[i].lower())
            result+=chr(65+index)
        else:
            result+=str[i]
    return result
def createskey():
    str=''
    for i in range(0,10):
        choice= random.randint(1,3)
        if choice==1:
            letter=chr(random.randint(48,57))
        elif choice==2:
            letter=chr(random.randint(97,122))
        elif choice ==3:
            letter=chr(random.randint(65,90))
        str+=letter
    return str
"""
str='abcdefghijklm12345@6#7%8^9*/0ABCDEFG'
print str
str1=encode(str)
print str1
str2=decode(str1)
print str2


str='abcdefghijklm1234567890ABCDEFG'
print str.isalnum()

import datetime
d1="2015-01-01"
d2="2015-02-02"

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
print datediff(d1,d2)
"""
