import pandas as pd
import requests
import plotly.graph_objs as go
from collections import defaultdict

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    
    # Get the data from the world bank api 
    payload = {'format': 'json', 'per_page': '1000', 'date': '1970:2012'}
    indicator = ['EN.ATM.CO2E.GF.KT', 'one other']
    
    all_data = []
    
    for i in indicator:
        url = 'https://api.worldbank.org/v2/countries/us;cn/indicators/{}'.format(indicator[i])
        
        try:
            r = requests.get(url, params = payload)
            data = r.json()[1]
        except:
            print('data not loaded correctly for indicator {}'.format(i))
            
        for i, val in enumerate(data):
            val['indicator'] = val['indicator']['value']
            val['country'] = val['country']['value']

        all_data.append(data)
    
    # first chart plots co2 emissions from US and China from 1970-2011 
    # as a line chart
    
    graph_one = []    
    graph_one.append(
      go.Scatter(
      x = [0, 1, 2, 3, 4, 5],
      y = [0, 2, 4, 6, 8, 10],
      mode = 'lines'
      )
    )

    layout_one = dict(title = 'Chart One',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )

# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []

    graph_two.append(
      go.Bar(
      x = ['a', 'b', 'c', 'd', 'e'],
      y = [12, 9, 7, 5, 1],
      )
    )

    layout_two = dict(title = 'Chart Two',
                xaxis = dict(title = 'x-axis label',),
                yaxis = dict(title = 'y-axis label'),
                )

    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))


    return figures