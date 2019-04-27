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
    key=[]
    values=[]
    for x,y in params.items():
        key.append(x)
        values.append(y)
    sort = df[df[key[0]].str.contains(values[0])]
    if(key[1]=='asofdate'):
        values[1]=pandas.to_datetime(values[1], format='%Y-%m-%d %H:%M:%S')
        sort = sort[sort[key[1]]==values[1]]
    sort=sort.to_dict('records')
    return sort
        

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
api = Api(app)
app.config['JSON_SORT_KEYS'] = False
# Flask mishandles boolean as string
TRUTHY = ['true', 'True', 'yes']
#get data
path = ("./data/GRM_IssueDB_Dummy.xlsx") 
df = pandas.read_excel(path,sheet_name="GRM_Issue_Repository")
df=df.rename(columns = {'Notes(Status Update)':'Notes_Status_Update'})
df=df.rename(columns = {'CCAR_v.non-CCAR':'CCAR_v_non-CCAR'})
df = df.replace({pandas.np.nan: None})
   
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/about/<variable>")
def about(variable):
        return render_template('about.html',para=variable)

class returnAll(Resource):
    def get(self):
        allData=df.to_dict('records') 
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