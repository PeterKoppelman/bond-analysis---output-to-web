"""Update of final for Intermediate Python using Dash
by plotly instead of openpyxl to distribute the data.
Peter Koppelman"""

import auth_token as at
import pandas as pd
import quandl
import datetime
import pickle
import os, os.path
import time

from pandas.tseries.offsets import BQuarterEnd
from pathlib import Path

from datetime import datetime
from datetime import timedelta
from dateutil.easter import *

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol

from dash.dependencies import Input, Output

app = dash.Dash(__name__)
# server = app.server

def main_program():

    def get_data():
        # Get treasury yield data from Quandl
        df_treasury = quandl.get("USTREASURY/YIELD", authtoken=at.auth_key)

        # Get Freddie, conforming and Jumbo 30 yr mortgage data from Quandl
        # Get Freddie Mac Data
        df_freddie_mac = quandl.get("FMAC/30US", authtoken=at.auth_key)

        # Get Wells Fargo conforming data
        df_wfc_conf_30 = quandl.get("WFC/PR_CON_30YFIXED_IR",
                                 authtoken=at.auth_key)

        # Get Wells Fargo Jumbo data
        df_wfc_jumbo_30 = quandl.get("WFC/PR_JUMBO_30YFIXED_IR",
                                  authtoken=at.auth_key)

        # pickle the files 
        pickle.dump(df_treasury, open('treasury.pickle', 'wb'))
        pickle.dump(df_freddie_mac, open('freddie_mac.pickle', 'wb'))
        pickle.dump(df_wfc_conf_30, open('conf.pickle', 'wb'))
        pickle.dump(df_wfc_jumbo_30, open('jumbo.pickle', 'wb'))
        return df_treasury, df_freddie_mac, df_wfc_conf_30, df_wfc_jumbo_30

    def pickle_out():
        df_treasury = pickle.load(open('treasury.pickle', 'rb'))
        df_freddie_mac = pickle.load(open('freddie_mac.pickle', 'rb'))
        df_wfc_conf_30 = pickle.load(open('conf.pickle', 'rb'))
        df_wfc_jumbo_30 = pickle.load(open('jumbo.pickle', 'rb'))
        return df_treasury, df_freddie_mac, df_wfc_conf_30, df_wfc_jumbo_30


    def manipulate_mortgage_data(df_freddie_mac, df_wfc_conf_30, df_wfc_jumbo_30):
        # Rename columns
        df_freddie_mac.columns = ['Freddie Mac']
        df_wfc_conf_30.columns = ['WFC Conf Int Rate']
        df_wfc_jumbo_30.columns = ['WFC Jumbo Int Rate']

        # Merge freddie mac, Wells Fargo conforming and Wells Fargo jumbo datafrmes
        df_mortgage = pd.merge(df_freddie_mac, df_wfc_jumbo_30, 
            left_index = True, right_index = True)
        df_mortgage = pd.merge(df_mortgage, df_wfc_conf_30, 
            left_index = True, right_index = True)
        
        # Get differences in rates. Add them to the dataframe
        df_mortgage['Conf minus Freddie'] = (df_mortgage['WFC Conf Int Rate'] - \
        df_mortgage['Freddie Mac']).round(3)
        df_mortgage['Jumbo minus Freddie'] = (df_mortgage['WFC Jumbo Int Rate'] - \
        df_mortgage['Freddie Mac']).round(3)

        df_mortgage.reset_index(inplace=True)
        df_mortgage = df_mortgage.sort_values(by=['Date'], ascending=False)
        return df_mortgage


    def manipulate_yield_data(df_treasury):
        # Take out 2 month yield and only use 24 months of data
        df_treasury = df_treasury.drop(['2 MO'], axis=1).last('24M')
        df_treasury.reset_index(inplace=True)

        # Get the data for the last day of each business quarter for the 
        # last 24 months.
        df_us_treasury = df_treasury.loc[df_treasury.Date.isin(df_treasury.Date + BQuarterEnd())]

        # Once every 5 or 6 years the end of the first business
        # quarter is Good Friday. The financial markets in the US 
        # are closed on Good Friday. When this occurs we have to get
        # data from the day before Good Friday.

        # Create a list of the years that are in the df_treasury dataframe 
        df_dates = pd.to_datetime(df_treasury['Date']).dt.year.unique()

        for date in df_dates:
            # Calculate Good Friday. It's two days before Easter Sunday
            goodfriday = easter(date) + timedelta(days = -2)
            # Calculate the end of the business quarter for the quarter that 
            # Good Friday is in.
            Bqtr_end_date = (pd.to_datetime(goodfriday) + BQuarterEnd(0)).date()

            # check to see if Good Friday is the last day of the business quarter
            if goodfriday == Bqtr_end_date:

                # Subtract one day from Good Friday to get financial end of qtr
                end_of_qtr = pd.to_datetime(goodfriday + timedelta(days = -1))
                # Get the row in df_treasury with the information that we need
                df_temp = df_treasury[df_treasury.Date == end_of_qtr]
                # Add the dataframe with the one record that we need to the 
                # dataframe with the business quarter end data
                df_us_treasury = pd.concat([df_us_treasury, df_temp])

        # Add data from most recent date in df_treasury to df_us_treasury
        df_us_treasury = df_us_treasury.append(df_treasury.iloc[-1])
        # Update the index so that the data prints out correctly
        df_us_treasury = df_us_treasury.sort_values(by=['Date'], ascending=False)
        df_treasury = df_treasury.sort_values(by=['Date'], ascending=False)
        df_us_treasury['Date'] = pd.to_datetime(df_us_treasury['Date'], format = '%Y-%m-%d').dt.date
        return df_us_treasury, df_treasury

    def dash_create_charts(df_mortgage, df_us_treasury, df_treasury):
        tabs_styles = {
            'height': '44px',
            'textAlign' : 'center'
        }
        tab_style = {
            'borderBottom': '2px solid #d6d6d6',
            'padding': '12px',
            'fontWeight': 'bold'
        }

        tab_selected_style = {
            'borderTop': '1px solid #d6d6d6',
            'backgroundColor': '#119DFF',
            'color': 'white',
            'padding': '12px'
        }

        app.layout = html.Div([
            html.H1(
                'Interest Rate Information', 
                style = {'textAlign' : 'center'}
            ), 
            dcc.Tabs(
                id= 'interest-rates', 
                value='mortgage-rates', 
                children=[
                    dcc.Tab(
                        label='Mortgage Rates', 
                        value='mortgage-rates', 
                        style=tab_style, 
                        selected_style=tab_selected_style
                    ),
                    dcc.Tab(
                        label='Mortgage Spreads', 
                        value='mortgage-deltas', 
                        style=tab_style, 
                        selected_style=tab_selected_style
                    ),
                    dcc.Tab(
                        label='Yield Curve', 
                        value='yield-curve', 
                        style=tab_style, 
                        selected_style=tab_selected_style
                    ),
                ], style = tabs_styles
            ),
            html.Div(id='interest-rates-content')
        ])

        @app.callback(Output('interest-rates-content', 'children'),
            [Input('interest-rates', 'value')])
        def render_content(tab):

            if tab == 'mortgage-rates':
                return (html.Div([
                    dash_table.DataTable(
                        id='datatable-int-rates',
                        data = df_mortgage.to_dict('records'),
                        columns = [
                            {
                            'id' : 'Date', 
                            'name': 'Date', 
                            'editable': False
                            },
                            {
                            'id' : 'Freddie Mac', 
                            'name': 'Freddie Mac', 
                            'editable': True
                            },
                            {
                            'id' : 'WFC Conf Int Rate', 
                            'name': 'Wells Fargo Conforming Rates', 
                            'editable': True
                            },
                            {
                            'id' : 'WFC Jumbo Int Rate', 
                            'name': 'Wells Fargo Jumbo Rates', 
                            'editable': True
                            },
                        ],
                        virtualization = True,
                        fixed_rows = {
                            'headers' : True, 
                            'data' : 0
                        },
                        style_cell = {
                            'textAlign' : 'center'
                        },
                        style_table = {
                            'maxHeight': '300px', 
                            'overflowY' : 'scroll'
                        },
                        style_header = {
                            'backgroundColor': 'rgb(230,230,230)', 
                            'fontWeight' : 'bold'
                        },
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                        ],
                    ),
                    html.Div(id = 'mortgage_graph')
                ]),

                html.Div(
                    [
                    dcc.Graph(
                        id='fixed interest rates',
                        figure={
                            'data': [
                                {
                                'x': df_mortgage['Date'],
                                'y': df_mortgage['Freddie Mac'], 
                                'type': 'line',
                                'name': 'Freddie Mac Interest Rates'
                                },
                                {
                                'x': df_mortgage['Date'],
                                'y': df_mortgage['WFC Conf Int Rate'], 
                                'type': 'line',
                                'name': 'Wells Fargo Conforming Rates'
                                },
                                {
                                'x': df_mortgage['Date'],
                                'y': df_mortgage['WFC Jumbo Int Rate'], 
                                'type': 'line',
                                'name': 'Wells Fargo Jumbo Rates'
                                },
                            ],
                            'layout' : {
                                'title' : '<b>30 Year Fixed Rate Mortgages <br> Freddie Mac Vs. Wells Fargo<b>',
                                'xaxis' : {
                                    'title' : '<b>Date<b>'
                                },
                                'yaxis' : {
                                    'title' : '<b>Interest Rate<b>'
                                },
                                'height' : 500,
                                'margin' : {
                                    "t": 80, 
                                    "l": 70, 
                                    "r": 20
                                }, 
                                'hovermode': 'closest',
                                },
                            }
                        )
                    ]
                )
            )

            elif tab == 'mortgage-deltas':
                return (html.Div([
                    dash_table.DataTable(
                        id='datatable-deltas',
                        data = df_mortgage.to_dict('rows'),
                        columns = [
                            {
                            'id' : 'Date', 
                            'name': 'Date',
                            'editable': False
                            }, 
                            {
                            'id' : 'Conf minus Freddie', 
                            'name': 'Wells Fargo Conforming Rates minus Freddie',
                            'editable': True, 
                            'type' : 'numeric',
                            'format' : Format(
                                precision = 3,
                                scheme = Scheme.fixed,
                                sign = Sign.parantheses),
                            }, 
                            {
                            'id' : 'Jumbo minus Freddie', 
                            'name': 'Wells Fargo Jumbo Rates minus Freddie',
                            'editable': True, 
                            'type' : 'numeric',
                            'format' : Format(
                                precision = 3,
                                scheme = Scheme.fixed,
                                sign = Sign.parantheses),
                            },
                        ],
                        virtualization = True,
                        fixed_rows = {
                            'headers' : True, 
                            'data' : 0
                        },
                        style_cell = {
                            'textAlign' : 'center'
                        },
                        style_header = {
                            'fontWeight' : 'bold',
                            'backgroundColor': 'rgb(230,230,230)', 
                        },
                        style_table = {
                            'maxHeight': '300px', 
                            'overflowY' : 'scroll'
                        },
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'}, 
                            'backgroundColor': 'rgb(248, 248, 248)'},
                        ],
                    ),                   
                    html.Div(id = 'delta_graph')
                ]),
                html.Div(
                    [
                    dcc.Graph(
                        id='fixed interest rates',
                        figure={
                            'data': [
                                {
                                'x': df_mortgage['Date'],
                                'y': df_mortgage['Conf minus Freddie'], 
                                'type': 'line',
                                'name': 'Wells Fargo Conforming <br> Rates minus Freddie'
                                },
                                {
                                'x': df_mortgage['Date'],
                                'y': df_mortgage['Jumbo minus Freddie'], 
                                'type': 'line',
                                'name': 'Wells Fargo Jumbo <br> Rates minus Freddie'
                                },
                            ],
                            'layout' : {
                                'title' : '<b>Spreads in Mortgage Interest Rates<br>30 Year Fixed Rate Mortgage<b>',
                                'xaxis' : {'title' : '<b>Date<b>'},
                                'yaxis' : {'title' : '<b>Interest Rate<b>'},
                                'height' : 500,
                                'margin' : {
                                    "t": 80, 
                                    "l": 70, 
                                    "r": 20
                                }, 
                                'hovermode': 'closest',
                                },
                            }
                        )
                    ]
                )
            )

            # elif tab == 'yield-curve':
            else:           
                return (html.Div([
                    dash_table.DataTable(
                        id='fixed interest rates',
                        data = df_treasury.to_dict('rows'),
                        columns=[{"name": i, "id": i} for i in df_treasury.columns],
                        virtualization = True,
                        page_action = 'none',
                        editable = False,
                        fixed_rows = {
                            'headers' : True, 'data' : 0
                        },
                        style_cell = {
                            'textAlign' : 'center'
                        },
                        style_header = {
                            'backgroundColor': 'rgb(230,230,230)', 
                            'fontWeight' : 'bold'
                        },
                        style_table = {
                            'maxHeight': '300px',
                            'overflowY' : 'scroll'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'}, 
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                        ],
                        style_cell_conditional = [
                            {
                                'if': {'column_id' : key}, 'width' : value
                            }   for key, value in at.col_dict.items()
                        ],
                    ),
                    html.Div(id = 'yield_curve_data')
                ]),
                html.Div(
                    [
                    dcc.Graph(
                        id='yield-curve-graph',
                        figure={
                            'data': [
                                {'x': df_us_treasury.iloc[i][0],
                                'y': df_us_treasury.iloc[i],
                                'type': 'line',
                                'name' : df_us_treasury.iloc[i][0],
                                } for i in range(len(df_us_treasury))

                            ],
                            'layout' : {
                                'title' : '<b>Yield Curve End of Quarter - Eight Quarters Running<b>',
                                'xaxis' : {
                                    'title' : '<b>Tenor<b>', 
                                    'tickmode' : 'array',
                                    'tickvals' : [i for i in range(1, len(df_us_treasury.columns))],
                                    'ticktext' : 
                                        [i for i in df_us_treasury.columns.tolist() if i != 'Date'],
                                        'range' : ['1', len(df_us_treasury.columns)-1]
                                    },
                                'yaxis' : {
                                    'title' : '<b>Interest Rate<b>'
                                },
                                'height' : 500,
                                'margin' : {
                                    "t": 80, 
                                    "l": 70, 
                                    "r": 20
                                }, 
                                'hovermode': 'closest',
                                },
                            }
                        )
                    ]
                )
            )

  
    ## Run the Code. ##
    # Get the data from Quandl or from pickle file

    # # does the pickle file exist
    # if os.path.exists(at.last_pickle_file):
    #     print('the file exists')
    #     # if the file exists get the last date that the file was run
    #     pickle_date = time.strftime("%Y-%m-%d", time.localtime(os.stat(at.last_pickle_file)[8]))

    #     # if the pickle date is less than today
    #     if pickle_date < datetime.today().strftime('%Y-%m-%d'):
    #         print('pickle date is not today')

    #         # if the pickle was not run on a Friday
    #         if datetime.strptime(pickle_date, '%Y-%m-%d').weekday() != 3:
    #             print('pickle date is not equal to today and its day is not Friday')
    #             # get updated data
    #             df_treasury, df_freddie_mac, df_wfc_conf_30, df_wfc_jumbo_30 = get_data()
    #         else:
    #             # pickle was run on a Friday and we are ok
    #             print('the pickle day of the week is Friday')
    #             df_treasury, df_freddie_mac, df_wfc_conf_30, df_wfc_jumbo_30 = pickle_out()
    # else:

        # if the pickle file does not exist, get the data from quandl and create the pickle files.
    df_treasury, df_freddie_mac, df_wfc_conf_30, df_wfc_jumbo_30 = get_data()


    # df_treasury, df_freddie_mac, df_wfc_conf_30, df_wfc_jumbo_30 = get_data()
    # df_treasury, df_freddie_mac, df_wfc_conf_30, df_wfc_jumbo_30 = pickle_out()

    # Manipulate data for use in dash
    df_mortgage = manipulate_mortgage_data(df_freddie_mac, df_wfc_conf_30, df_wfc_jumbo_30)
    df_mortgage.Date = pd.DatetimeIndex(df_mortgage.Date).strftime("%Y-%m-%d")

    df_us_treasury, df_treasury = manipulate_yield_data(df_treasury)
    df_us_treasury.Date = pd.DatetimeIndex(df_us_treasury.Date).strftime("%Y-%m-%d")
    df_treasury.Date = pd.DatetimeIndex(df_treasury.Date).strftime("%Y-%m-%d")

    # Create datatables and graphs
    dash_create_charts(df_mortgage, df_us_treasury, df_treasury)
    print('Complete main program')
    app.run_server(debug=True)
   

if __name__ == '__main__':
    print('Starting main program')
    main_program()
