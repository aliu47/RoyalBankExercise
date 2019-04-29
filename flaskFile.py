from flask import Flask, render_template, jsonify, request
from flask_restful import Resource, Api
import numpy 
import pandas
from pandas import DataFrame
from datetime import date
from flask.json import JSONEncoder

# Adjusts dates for exporting to JSON
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

def countData(df,params):
    key=[]
    for x,y in params.items():
        key.append(x)
    print(key)
    df=DataFrame(df,columns=key)
    a=df.groupby(key).size().reset_index(name='counts')
    a=a.to_dict('records')    
    return a

def sortData(df,params):
    sort = df
    for x,y in params.items():
        if(df[x].dtypes == "object"):
            sort = sort[sort[x].str.contains(y)]
        elif(df[x].dtypes == "datetime64[ns]"):
            date=pandas.to_datetime(y, format='%Y-%m-%d %H:%M:%S')
            sort = sort[sort[x]==date]
        else:
            sort = sort[sort[x]==y]
    print("date:"+str(sort["asofdate"].dtypes))
    sort = sort.replace({pandas.np.nan: None})
    sort = sort.to_dict('records')
    return sort  
  
app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
api = Api(app)
app.config['JSON_SORT_KEYS'] = False
# Flask mishandles boolean as string
TRUTHY = ['true', 'True', 'yes']
path = ("./data/GRM_IssueDB_Dummy.xlsx") 
df = pandas.read_excel(path,sheet_name="GRM_Issue_Repository")
df=df.rename(columns = {'Notes(Status Update)':'Notes_Status_Update'})
df=df.rename(columns = {'CCAR_v.non-CCAR':'CCAR_v_non-CCAR'})
dfAll=df.replace({pandas.np.nan: None})
       
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about/<variable>")
def about(variable):
        return render_template('about.html',para=variable)

class returnAll(Resource):
    def get(self):
        allData=dfAll.to_dict('records') 
        return jsonify({"data":allData})

class dataCount(Resource):
    def get(self):
        params = request.args
        count=countData(df,params)
        return jsonify({"data":count})

class dataSort(Resource):
    def get(self):
        params=request.args
        sort=sortData(df,params)
        return jsonify({"data":sort})

api.add_resource(dataCount,"/dataCount")
api.add_resource(returnAll,"/data")
api.add_resource(dataSort,"/dataSort")

if __name__=='__main__':
    app.run(debug=True)