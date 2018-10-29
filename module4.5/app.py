from flask import Flask, render_template, request, url_for


import pandas as pd
import numpy as np



app = Flask(__name__)

@app.route("/")
def hello():
    #default page
    return render_template('main.html')



####Controllers ####
@app.route("/TreeHealth",methods=['GET','POST'])
def getTreeHealth():

    #boroname = request.form['boroname']
    boroname = request.args.get('boroname')

    groupByHealth = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$select=spc_common,health,count(spc_common)&$where=boroname=\''+ str(boroname) +'\'&$group=spc_common,health' )

    df = pd.read_json(groupByHealth)

    #using pivot table for calculating percetage.
    #lambda expression and merging is not working with properly

    df2=df.pivot_table(values='count_spc_common', index='spc_common', columns='health')
    #get total with spc_common
    df2['total']=df2.sum(axis=1)
    df2.fillna(0, inplace=True)
    #calculating pct
    df2['fairPct']=df2['Fair']/df2['total']
    df2['goodPct']=df2['Good']/df2['total']
    df2['poorPct']=df2['Poor']/df2['total']
    #merge
    df3=df2[['fairPct','goodPct','poorPct']]
    df3.reset_index()
    return df3.to_json(orient='index')

@app.route("/StewardVSTreeHealth",methods=['GET','POST'])
def getStewardVsTreeHealth():

    #boroname = request.form['boroname']
    boroname = request.args.get('boroname')

    steward = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$select=steward,health,count(health)&$where=boroname=\''+ str(boroname) +'\'&$group=steward,health')

    df = pd.read_json(steward)

    df2=df.pivot_table(values='count_health', index='steward', columns='health')
    #get total with spc_common
    df2['total']=df2.sum(axis=1)
    df2.fillna(0, inplace=True)
    #calculating pct
    df2['fairPct']=df2['Fair']/df2['total']
    df2['goodPct']=df2['Good']/df2['total']
    df2['poorPct']=df2['Poor']/df2['total']
    #merge
    df3=df2[['fairPct','goodPct','poorPct']]
    df3.reset_index()

    return df3.to_json(orient='index')






if __name__ == "__main__":
    app.run()
