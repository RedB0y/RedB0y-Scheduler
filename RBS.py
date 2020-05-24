import gspread
import random
from gspread_formatting import *
from google.oauth2.service_account import Credentials
import pickle
import initia
import json
import SubClass
import datetime
import argparse
scopes = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
credentials=Credentials.from_service_account_file('scheduler-v-1-0-f224b62b5208.json',scopes=scopes)
gc=gspread.authorize(credentials)
sht=gc.open('TEST')
wks=sht.get_worksheet(1)

parser=argparse.ArgumentParser()
parser.add_argument("-hour",type=int,help="Specific Hour when you want to start the scheduler at,(24 hrs Format)")
parser.add_argument("--minutes",type=int,default=0,help="Specific minute when you want to start the scheduler at")
args=parser.parse_args()

Hrs=args.hour
mins=args.minutes
dt_now=datetime.datetime.now()
schd_time=datetime.datetime(dt_now.year,dt_now.month,dt_now.day,Hrs,mins)
time_delta=datetime.timedelta(hours=2)

def DumpXL(row,col,obj):
              global schd_time
              format_cell_range(wks,str(col)+str(row),obj.MFmt)
              format_cell_range(wks,str(col)+str(row-1),obj.FFmt)
              wks.update(str(col)+str(row),obj.SName)
              temp=schd_time+time_delta
              wks.update(str(col)+str(row-1),schd_time.strftime("%I:%M%p - ")+temp.strftime("%I:%M%p"))
              schd_time=temp

def DumpBreak(row,col):
              global schd_time
              format_cell_range(wks,str(col)+str(row),SubClass.BMFmt)
              format_cell_range(wks,str(col)+str(row-1),SubClass.BFFmt)
              wks.update(str(col)+str(row),"BREAK")
              temp=schd_time+time_delta
              wks.update(str(col)+str(row-1),schd_time.strftime("%I:%M%p - ")+temp.strftime("%I:%M%p"))
              schd_time=temp


def DumpTimeBegin(row):
              format_cell_range(wks,'B'+str(row),SubClass.DMFmt)
              format_cell_range(wks,'B'+str(row-1),SubClass.DFFmt)
              wks.update('B'+str(row-1),dt_now.strftime("%I:%M%p - ")+schd_time.strftime("%I:%M%p"))
              wks.update('B'+str(row),'SESH_BEGIN')

def DumpDate(row):
              format_cell_range(wks,'A'+str(row),SubClass.DMFmt)
              format_cell_range(wks,'A'+str(row-1),SubClass.DFFmt)
              wks.update('A'+str(row),dt_now.strftime("%d/%m/%Y-%a"))
              wks.update('A'+str(row-1),"DATE")
              
#def DumpSesh(row,col,timeB,timeE)
FileName=initia.FileName
ObjL=[]
j=0
SumOfSubHours=0
CounterFlag=False
with open("config.json") as js:
              store=json.load(js)
              
TempObjL=[None]*store["NoOfTasks"]
Col_D=['B','H']
Col_B=['D','F']
Col_S=['C','E','G']
row=store["RowCounter"]






if store["PC"] == 0:
              store["PC"]+=1 
              initia.initia()
              print("InPC")

elif store["WeekCounter"] == 0:
              print("InWC",end=' ')
              print(store["WeekCounter"])
              store["WeekCounter"]=7
              print("$$")
              initia.initia()

#Reading From the pickled File
PickleR = open(FileName,"rb")
while True:
              try:
                            
                            temp=pickle.load(PickleR)
                            
                            if temp.SubHours>0 :
                                          ObjL.append(temp)
                            SumOfSubHours+=temp.SubHours
                            
              except:
                            PickleR.close()
                            break


while j < 3:
              #print(j)
              RObj=random.choice(ObjL)
              if SumOfSubHours==0:
                            break
              elif RObj.IsVisited == False:
                            
                            RObj.SubVisit()
                            TempObjL[j]=RObj
                            
              elif RObj.IsVisited==True:
                            
                            if len(ObjL)<3:
                                          RObj.SubVisit()
                                          TempObjL[j]=RObj              
                            else:
                                          continue
              j+=1
DumpDate(row)
DumpTimeBegin(row)
for i in range(3):
              
              if i<2:
                         DumpXL(row,Col_S[i],TempObjL[i])
                         DumpBreak(row,Col_B[i])
                         print(TempObjL[i].SName, end=' ')
                         TempObjL[i].IsVisited=False
              else:
                         DumpXL(row,Col_S[i],TempObjL[i])
                         print(TempObjL[i].SName, end=' ')
                         TempObjL[i].IsVisited=False

store["WeekCounter"]-=1
store["RowCounter"]+=2
with open("config.json","w") as js:
              json.dump(store,js,indent=2)              
print("")
for obj in ObjL:
              
              print(obj.SubHours,end=" ")

print(store["WeekCounter"])
PickleW=open(FileName,"wb")
for obj in ObjL:
              pickle.dump(obj,PickleW)
PickleW.close()              
