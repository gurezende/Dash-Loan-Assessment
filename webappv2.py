# In this script I will create a simple page where we will enter a few numbers
# and use it as input for a Machine Learning model to give us output either if
# the credit should be approved or not.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
import pickle


# Instantiating the app
app = dash.Dash()

# Title in the app browser tab
app.title = 'Loan Pre-appoval Assessment'

# Bootstrap css
app.css.append_css({"external_url":"https://codepen.io/amyoshino/pen/jzXypZ.css"})

# Creating the app layout

# Title
app.layout = html.Div([
        html.Div([
            html.H1('Credit Auto-Assessment'),
            html.H6('by Gustavo Santos')], style = {'font-family':'Tahoma', 'background-color':'rgb(150,230,255)', 'font-color':'rgb(0,0,0)'}, className='row'),

# Here is the block for Amount requested
        html.Div([
        html.Div([
            html.Div(['How much do you want to loan:',
            dcc.RadioItems(id='amount',
            options=[{'label': '1k USD', 'value':1000},
                     {'label': '2k USD', 'value':2000},
                     {'label': '3k USD', 'value':3000}], value=1000)])
                     ], style = {'font-family':'Tahoma', 'background-color':'rgb(150,230,255)', 'width': '40%', 'height':'10%', 'margin':10}, className='four.columns'),

# Here is the block for requestor's age
        html.Div([
            html.Div(['What is your age:',
            dcc.Input(id='age',
                placeholder='Enter your age...',
                type = 'number',
                value = '')],
                style={'font-family':'Tahoma', 'background-color':'rgb(150,230,255)', 'width': '40%', 'height':'10%', 'margin':10}, className='six.columns')
                ])
                ], className='ten columns'),

# Here is the block for requested Loan Duration
        html.Div([
            html.Div(['What is the Loan Length:',
            dcc.RadioItems(id='duration',
            options=[{'label': '12 months', 'value':12},
                     {'label': '24 months', 'value':24},
                     {'label': '36 months', 'value':36}], value=12)],
                     style={'font-family':'Tahoma', 'background-color':'rgb(150,230,255)', 'width': '40%', 'height':'10%', 'margin':10})
                ], className='four columns'),

# Here is the block for requestor's years at the same residence
        html.Div([
            html.Div(['How long have you been living in your current address:',
            dcc.Input(id='house',
                placeholder='Years...',
                type = 'number',
                value = '')],
                style={'font-family':'Tahoma', 'background-color':'rgb(150,230,255)', 'width': '40%', 'height':'10%', 'margin':10})
                ], className='four columns'),


# How much do you have in your checking account
        html.Div([
            html.Div(['How much do you have in your checking account:',
            dcc.RadioItems(id='checking',
            options=[{'label': 'negative', 'value':'< 0 DM'},
                     {'label': '1 - 200', 'value':'1 - 200 DM'},
                     {'label': '> 200', 'value':'> 200 DM'},
                     {'label': 'Prefer not to declare', 'value':'unknown'}], value='1 - 200 DM')],
                     style={'font-family':'Tahoma', 'background-color':'rgb(150,230,255)', 'width': '40%', 'height':'10%', 'margin':10})
                ], className='four columns'),

#Submit Button
html.Button(id='submit', n_clicks=0, children='Process Request', style={'fontsize':25}),

# See what were the choices
html.H1(id='out')
],className= 'ten columns offset-by-one')



# Starting the Callbacks to get the inputs and format them to serve as input for
# the ML model
@app.callback(
    Output('out','children'),
    [Input('submit','n_clicks')],
    [State('amount', 'value'),
     State('age','value'),
     State('duration','value'),
     State('house','value'),
     State('checking','value')])

# Function to determine what the callback will do
def gather_inputs(n_clicks,amount, age, duration, house, checking):
    if checking == '< 0 DM':
        df = pd.DataFrame([[amount, age, duration, house, 1,0,0]], columns=['amount', 'age', 'months_loan_duration','years_at_residence', 'checking_balance_< 0 DM','checking_balance_> 200 DM','checking_balance_unknown'])
    elif checking == '> 200 DM':
        df = pd.DataFrame([[amount, age, duration, house, 0,1,0]], columns=['amount', 'age', 'months_loan_duration','years_at_residence', 'checking_balance_< 0 DM','checking_balance_> 200 DM','checking_balance_unknown'])
    elif checking == 'unknown':
        df = pd.DataFrame([[amount, age, duration, house, 0,0,1]], columns=['amount', 'age', 'months_loan_duration','years_at_residence', 'checking_balance_< 0 DM','checking_balance_> 200 DM','checking_balance_unknown'])
    else:
        df = pd.DataFrame([[amount, age, duration, house, 0,0,0]], columns=['amount', 'age', 'months_loan_duration','years_at_residence', 'checking_balance_< 0 DM','checking_balance_> 200 DM','checking_balance_unknown'])

    #Load saved model from disk
    model = pickle.load(open('DTClass_model.sav', 'rb'))
    result = model.predict(df)

    #Message to pop in the screen
    if result == 0:
        return 'Based on your input, your credit is pre-approved. Please talk to your account manager. Thanks!'
    else:
        return 'Based on your input, your credit was NOT approved. Thanks!'




if __name__ == '__main__':
    app.run_server()
