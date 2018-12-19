from flask import Flask, render_template, request, url_for


import pandas as pd
import numpy as np

from google.cloud import bigquery

app = Flask(__name__)

@app.route("/")
def defaultPage():
    #default page
    return render_template('main.html')



####Controllers ####
@app.route("/Top3",methods=['GET','POST'])
def getTop3():


    client = bigquery.Client.from_service_account_json('gcloudkeyfile.json')

    #boroname = request.form['boroname']
    DRG = request.args.get('DRG')

    QUERY = (
        'with MyRowSet '
        'As '
        '( '
        'select provider_state, provider_name,drg_definition, total_discharges, '
        'ROW_NUMBER() over (partition by provider_state order by total_discharges desc) as ROW_NUM '
        'FROM  `bigquery-public-data.cms_medicare.inpatient_charges_2015` '
        'where drg_definition like "%' + DRG + '%" '
        ') '

        'select provider_state, sum(total_discharges) as stateDischarge, STRING_AGG( provider_name, "|"  ORDER BY total_discharges desc) AS Name , STRING_AGG( cast(total_discharges as string) , "|"  ORDER BY total_discharges desc) AS Discharges '
        'from MyRowSet where ROW_NUM <= 3 group by provider_state '

        )

    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish


    cols = ['provider_state', 'stateDischarge', 'Name', 'Discharges']
    lst = []
    for row in rows:
        lst.append([row.provider_state , row.stateDischarge , row.Name , row.Discharges])

    df1 = pd.DataFrame(lst, columns=cols)

    outjson = df1.to_json(orient='records')

    return outjson






if __name__ == "__main__":
    app.run()
