# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 17:14:34 2018

@author: John
"""

import dash
import dash_core_components as dcc
import dash_html_components as html


import pandas as pd
import numpy as np


def getTreeHealth(boroname):
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
    return df3

def getStewardVsTreeHealth(boroname):
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
    
    return df3
    

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
        
    
 html.Div([
    html.Label('Boro'),
    
    dcc.Dropdown(
        id='boro_type',    
        options=[
            {'label': 'Manhattan', 'value': 'Manhattan'},
            {'label': 'Bronx', 'value': 'Bronx'},
            {'label': 'Queens', 'value': 'Queens'},
            {'label': 'Brooklyn', 'value': 'Brooklyn'},
            {'label': 'Stand Island', 'value': 'stand%20Island'}

        ],
        value='Manhattan'
    ),

    
    dcc.Graph(id='tree-health-proportion-by-boro'),
    dcc.Graph(id='steward-tree-health-by-boro')
    


    ])
    
  
])

@app.callback(
    dash.dependencies.Output('tree-health-proportion-by-boro', 'figure'),
    [dash.dependencies.Input('boro_type', 'value')
     ])
def update_graph_tree_proportion(boro_type):
    x = getTreeHealth(boro_type)
    return {
            'data': [
                {'x': x.index, 'y': x['goodPct'] , 'type': 'bar', 'name': 'Good'},
                {'x': x.index, 'y': x['fairPct'], 'type': 'bar', 'name': 'Fair'},
                {'x': x.index, 'y': x['poorPct'], 'type': 'bar', 'name': 'Poor'},
                
                ],
            'layout': {
                'title': 'Q1: Tree Health Proportion ' + boro_type
            }
      
            
            
            
            
            
            
        }


@app.callback(
    dash.dependencies.Output('steward-tree-health-by-boro', 'figure'),
    [dash.dependencies.Input('boro_type', 'value')
     ])
def update_graph_steward(boro_type):
    x = getStewardVsTreeHealth(boro_type)
    return {
            'data': [
                {'x': x.index, 'y': x['goodPct'] , 'type': 'bar', 'name': 'Good'},
                {'x': x.index, 'y': x['fairPct'], 'type': 'bar', 'name': 'Fair'},
                {'x': x.index, 'y': x['poorPct'], 'type': 'bar', 'name': 'Poor'},
                
                ],
            'layout': {
                'title': 'Q2: Steward vs Tree Health in ' + boro_type
            }
      
            
            
            
            
            
            
        }



    
    
    
if __name__ == '__main__':
    app.run_server(debug=True)