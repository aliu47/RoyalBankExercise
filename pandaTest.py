import numpy 
import pandas
from pandas import DataFrame,Series

path = ("./data/GRM_IssueDB_Dummy.xlsx") 
df = pandas.read_excel(path,sheet_name="GRM_Issue_Repository",)
df=df.rename(columns = {'Notes(Status Update)':'Notes_Status_Update'})
df=df.rename(columns = {'CCAR_v.non-CCAR':'CCAR_v_non-CCAR'})
# df = df.replace({pandas.np.nan: None})

def sortData(df,params):
    sort = df
    for x,y in params.items():
        if(df[x].dtypes == "datetime64[ns]"):
            date=pandas.to_datetime(y, format='%Y-%m-%d %H:%M:%S')
            sort = sort[sort[x]==date]
        elif(df[x].dtypes == "object"):
            sort = sort[sort[x].str.contains(y)]
        else:
            sort = sort[sort[x]==y]
    print("data: "+str(sort["asofdate"].dtypes))
    sort = sort.to_dict('records')
    return sort   
    
def dataParams(params):
    path = ("./data/GRM_IssueDB_Dummy.xlsx") 
    df = pandas.read_excel(path,sheet_name="GRM_Issue_Repository")
    df=df.rename(columns = {'Notes(Status Update)':'Notes_Status_Update'})
    key=[]
    for x,y in params.items():
        key.append(x)
    print(key)
    df=DataFrame(df,columns=key)    
    a=df.groupby(key).size().reset_index(name='counts')
    # a= a.to_frame
    a=a.to_dict('records')
    return a
params={
    "Source_System": "ABC",
        "asofdate": "2019-02-28"
}
a=sortData(df,params)
print(a)