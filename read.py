from flask import Flask, render_template
import openpyxl 
import json
#file for testing xlsx calls

#location of data
path = ("./data/GRM_IssueDB_Dummy.xlsx") 
#create an object of the excel sheet
wb_obj = openpyxl.load_workbook(path)
#read the second sheet
sheet_obj = wb_obj.worksheets[1]
#read the data from the specified column
def generateKey(sheet_obj,row):
    keyList=[]
    for r in sheet_obj[row]:
        keyList.append(str(r.value))
    return keyList
def readData(sheet_obj,key,row):
    data={}
    dataList=[]
    for r in sheet_obj[row]:
         dataList.append(str(r.value))
    for i in range(len(key)):
        data[key[i]] = dataList[i]
    return data
def sortData(xlData,params):
    key=[]
    for i in xlData:
        dataFilter=0
        for x,y in params.items():
            a=i.get(x)
            if y in a:
                dataFilter +=1
            if len(params) == dataFilter:    
                key.append(i)
    return key

key = generateKey(sheet_obj,1)
xlsxData=[]
for i in range(2, 226):
    xlsxData.append(readData(sheet_obj,key,i))
params={"Source_System":"ABC","asofdate":"2019-02-28"}
x=sortData(xlsxData,params)
xlsxData=tuple(xlsxData)
args = "ABC"
# for i in key:
#             if i in args:
#                 xlsxData.keys(i)      
print(x)
