import numpy 
import pandas
from pandas import DataFrame,Series

path = ("./data/GRM_IssueDB_Dummy.xlsx") 
df = pandas.read_excel(path,sheet_name="GRM_Issue_Repository",)
df=df.rename(columns = {'Notes(Status Update)':'Notes_Status_Update'})
def sortData(df,params):
    key=[]
    values=[]
    for x,y in params.items():
        key.append(x)
        values.append(y)
    print(key[0])
    print(values[0])
    sort = df[df[key[0]].str.contains(values[0])]
    sort = sort[sort[key[1]]==values[1]]
    sort=sort.to_dict('records')
    print(sort)
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
    "Source_System": "ABC System",
        "asofdate": "2-28-2019"
}
a=sortData(df,params)
print(a)