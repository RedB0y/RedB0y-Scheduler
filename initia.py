import SubClass 
import pickle
import json


with open("config.json")as js:
       store=json.load(js)
ObjL=[]
ObjTemp=[None]*len(store["SubNames"])
FileName="ObjectPickle.pick"
def initia():
              PickleW=open(FileName,"wb")
              SubNames=store["SubNames"]
              SubPrio=store["SubPrio"]
              SubColor=store["SubColor"]
              SubColorF=store["SubColorF"]
              for i in range(len(SubNames)):
                            ObjL.append(SubClass.Sub(SubNames[i],SubPrio[i],SubColor[i],SubColorF[i]))
                            pickle.dump(ObjL[i],PickleW)
              PickleW.close()
          
              
              
              
              

