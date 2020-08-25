Canadian Royal Bank Exercise

I.Problem: Create a web application that can read data from an excel spreadsheet, then create a graph based on the information provided. The graph should be able to be generated based on either Management Owners or Source System. Then if the user clicks on a bar, it should open a new tab of a spreadsheet with the information of that bar.

II. Instructions
To run the project go to the file directory and first set the flask file to FLASK_APP, and then run.
WINDOWS
set FLASK_APP=flaskFile.py
flask run

LINUX/MAC
export FLASK_APP=flaskFile.py
flask run

III.Files: flaskFile.py, main.js,  about.html, home.html

A. flaskFile.py
This file is the backend of the application, it handles the routing and sending data to the front end. The file uses the Flask framework and is written in python. Pandas and Numpy have been imported for creating a dataframe of the excel data. 
	
1)countData(df,params)
	This function calculates how many time each value appears in a given 
parameter. For example, if Source System is provided, it will calculate how many times, “ABC System”, “BCD System”, “DEF System”, etc. appear in the dataframe.
	
2)sortData(df,params)
	This function filters the dataframe to see which rows contain the parameters 
Specified. For example if the parameters ask for “Source System: ABC”, it will 
return all rows where the Source System is ABC System.
	
3)Other details
	There is a customJSON encoder since the dates were not serializable for json 
export. Some columns needed to be renamed because they conflicted with 
UI-grid.

B. main.js
This file is for the frontend javascript, it uses Angularjs. It imports ui.grid and uses 
high-charts to make the graphs on home.html.
	
1)homeCtrl
	 In the home controller the select box is defaulted to Source System, and it 
generates a graph from the data collected from the sort(choice,category) function. When the user selects an option in the select box, it will call the sort function and redraw the graph. When a user clicks on a bar on the graph, it will open a new tab sending the user’s choice in the url.

2)focusCtrl
Here the URL is parsed and the parameters are sent to the backend and a sorted JSON object is returned. This JSON is sent to the ui-grid, to draw a table of the data provided.
	
C.about.html
	Here a grid is drawn by the information provided from the GET request. The table can be 
organized by any of the columns in either descending or ascending order.

D.home.html
Here a graph is drawn from the information provided in the homeCtrl.
