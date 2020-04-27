import pandas as pd
import requests
import plotly.graph_objs as go

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
    indicator = ['EN.ATM.CO2E.GF.KT', 'AG.LND.FRST.K2']
    
    all_data = []
    
    for i in indicator:
        url = 'https://api.worldbank.org/v2/countries/us;cn/indicators/{}'.format(i)
        
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
    df_one = pd.DataFrame(all_data[0])
    
    countries_one = df_one.country.unique().tolist()
    
    for country in countries_one:
        x_vals = df_one[df_one['country'] == country].date.tolist()
        y_vals = df_one[df_one['country'] == country].value.tolist()
        
        graph_one.append(
          go.Scatter(
          x = x_vals,
          y = y_vals,
          mode = 'lines',
          name = country
          )
        )

    layout_one = dict(title = 'CO2 Emissions from 1970-2011',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'CO2 Emissions (kt)'),
                )

# second chart plots forest area from US and China from 1990-2011    
    graph_two = []
    df_two = pd.DataFrame(all_data[1])
    df_two = df_two[df_two['date'] >= '1990']
    
    countries_two = df_two.country.unique().tolist()
    
    for country in countries_two:
        x_vals = df_two[df_two['country'] == country].date.tolist()
        y_vals = df_two[df_two['country'] == country].value.tolist()
        
        graph_two.append(
          go.Scatter(
          x = x_vals,
          y = y_vals,
          mode = 'lines',
          name = country
          )
        )

    layout_two = dict(title = 'Forest Area from 1970-2011',
                xaxis = dict(title = 'Year',),
                yaxis = dict(title = 'Forest Area (sq. km)'),
                )

    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))


    return figures