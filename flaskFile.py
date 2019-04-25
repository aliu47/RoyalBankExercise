from flask import Flask, render_template, jsonify, request
from flask_restful import Resource, Api
import openpyxl 

#location of data
path = ("./data/GRM_IssueDB_Dummy.xlsx") 
#create an object of the excel sheet
wb_obj = openpyxl.load_workbook(path)
#read the second sheet
sheet_obj = wb_obj.worksheets[1]
#read the first row to get the column xlKeys
def generatexlKey(sheet_obj,row):
    xlKeyList=[]
    for r in sheet_obj[row]:
        xlKeyList.append(str(r.value))
    return xlKeyList

#read the row given
def readData(sheet_obj,xlKey,row):
    data={}
    dataList=[]
    for r in sheet_obj[row]:
         dataList.append(str(r.value))
    for i in range(len(xlKey)):
        data[xlKey[i]] = dataList[i]
    return data

#return data specified by parameters
def sortData(xlData,params):
    key=[]
    for i in xlData:
        dataFilter=0
        #checks to make sure the row passes multiple params
        for x,y in params.items():
            a=i.get(x)
            if y in a:
                dataFilter +=1
            if len(params) == dataFilter:    
                key.append(i)
    return key

#get the key of the xlsx based on the first row
xlKey = generatexlKey(sheet_obj,1)
xlsxData=[]
#collect data from the sheet
for i in range(2, len(sheet_obj['A'])):
    xlsxData.append(readData(sheet_obj,xlKey,i))
app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False
# Flask mishandles boolean as string
TRUTHY = ['true', 'True', 'yes']
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about/<variable>")
def about(variable):
        return render_template('about.html',para=variable)
  
class DataAPI(Resource):
    def get(self):
        params = request.args
        if params:
            sortedData=sortData(xlsxData,params)
            sortedData=tuple(sortedData)
            return jsonify({"data":sortedData})
        else:
            data=tuple(xlsxData)
            return jsonify({"data":data})
   
api.add_resource(DataAPI,"/data")

if __name__=='__main__':
    app.run(debug=True)