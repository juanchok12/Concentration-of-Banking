import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import dash_daq as daq
import gunicorn
from dash import Dash, html
import dash_mantine_components as dmc
from dash import dash_table
import yfinance as yf
import plotly.graph_objects as go 


# Create a Dash app
app = dash.Dash(__name__) # Add external CSS
server=app.server # Add server
#========================Loading the dataframes=================================

#---------------------------Dataframe for the network plots of the Big Four Banks---------------------
#Dataframe for Chase (mergers and acquisitions)
trans_chase_df=pd.read_csv('https://raw.githubusercontent.com/juanchok12/Concentration-of-Banking/main/transformations_big_4/trans_chase_df.csv')

#Dataframe for Bank of America (mergers and acquisitions)
trans_boa_df=pd.read_csv('https://raw.githubusercontent.com/juanchok12/Concentration-of-Banking/main/transformations_big_4/trans_boa_df.csv')

#Dataframe for Wells Fargo (mergers and acquisitions)
trans_wf_df=pd.read_csv('https://raw.githubusercontent.com/juanchok12/Concentration-of-Banking/main/transformations_big_4/trans_wf_df.csv')  

#Dataframe for Citibank (mergers and acquisitions)
trans_cb_df=pd.read_csv('https://raw.githubusercontent.com/juanchok12/Concentration-of-Banking/main/transformations_big_4/trans_cb_df.csv')  

#Dataframe for the Giga Banks ownership of the Big Four Banks
giga_ownership_df=pd.read_csv('https://raw.githubusercontent.com/juanchok12/Concentration-of-Banking/main/transformations_big_4/giga_banks/giga_banks.csv')

#----------------------------Dataframe for the consolidated assets of the Big Four Banks-----------------


#==========================Stylying the Giga Banks ownership table==========================================

# #Adding title row to DataFrame
# title_row = pd.DataFrame([['Percentage of Ownership by the Giga Banks'] + [''] * (len(giga_ownership_df.columns) - 1)], columns=giga_ownership_df.columns)
# giga_ownership_df = pd.concat([title_row, giga_ownership_df]).reset_index(drop=True)


#Creates a styled 'DataTable' component from using Dash
def create_data_table_from_df(giga_ownership_df):
    #Instatiates a DataTable component that will display data from the DataFrame
    return dash_table.DataTable(
        id='table', #Unique indentifier for the DataTable component
        #List dictionary for each column in the DataFrame. 
        columns=[{"name": i, "id": i} for i in giga_ownership_df.columns],
        data=giga_ownership_df.to_dict('records'), #Converts the DataFrame to a list of dictionaries, where each dictionary represent a row in the DataFrame
        style_table={'heigth': '300px',  #Sets the height of the table
                     'overflow': 'auto'}, #Sets the overflow property of the table which is used when the content is too big to fit into the specified area
        style_cell={
            'textAlign': 'center', #Sets the text alignment of the cells to center
            'padding': '10px', #Sets the padding of the cells
            'backgroundColor': '#121212', #Sets the background color of the cells
            'color':'white', #Sets the font color of the cells to white



        },
        style_data_conditional=[
            {  'if': {'state': 'selected'}, #Sets the style of the cells when they are active
                'backgroundColor': '#4f6475', #Sets the background color of the cells when the mouse hovers over them
                'border': '1px solid #FFFFFF', #Sets the border of the cells when the mouse hovers over them
                'cursor': 'crosshair', #Sets the cursor to a pointer when the mouse hovers over the cells
            },
            {
                'if': {
                    'row_index': len(giga_ownership_df) -1 #Sets the style of the last row in the table
                },
                'fontStyle': 'italic', #Sets the font style of the last row to italic
                'fontWeight': 'bold', #Sets the font weight of the last row to bold
                }
            
        ],



        #Sets the style of the header of the table
        style_header={
            'backgroundColor':'#333333', #Sets the background color of the header
            'fontWeight': 'bold', #Sets the font weight of the header to bold
            'color':'white' #Sets the font color of the header to white

        }
    )
#Create the DataTable from the DataFrame
data_table = create_data_table_from_df(giga_ownership_df)


#========================Logo styles for the Big Four Banks======================================================

color_discrete_map={'Chase': '#0D5EAF',  # Blue
                                            'Bank of America': '#CB0D1F',  # Red
                                            'Citigroup': '#1598C3',  # Blue-ish
                                            'Wells Fargo': '#FFD408',  # Yellow
}

#==========================Historical Stock Prices for the Big Four Banks=======================================


#-------------------------Historical stock price plot for Chase-----------------------------------
#Line plot for stock price of Chase

#Ticker module to access the JPM stock data
jpm=yf.Ticker('JPM')
jpm_stock_data=jpm.history(period='max')
jpm_stock_data.reset_index(inplace=True) #inpleace=True to modify the original dataframe to have the date as a column

def plot_stock_price_chase(stock_data, stock_name):
    
    #Parameters:
    stock_name='Chase' #Representing the name of the stock
    stock_data=jpm_stock_data # DataFrame containing the stock data

    #Ensure that date is in datetime format
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])

    #Get today's date in the format YYYY-MM-DD
    today_date=pd.to_datetime('today').strftime('%Y-%m-%d')

    #Creating the line plot
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=stock_data['Date'], 
                                y=stock_data['Close'], 
                                mode='lines', 
                                name='Share Price',
                                line=dict(color=color_discrete_map[stock_name])))

    #Update the layout
    fig.update_layout(
        title=f'{stock_name} Historical Share Price',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        height=600,
        xaxis=dict(
            range=["1990-01-01", today_date],  # Directly set the initial view range of the plot
            rangeslider=dict(visible=True),
            rangeselector=dict(
                font=dict(color="black", size=12),  # Customize font color and size
                buttons=list([
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(count=5, label="5Y", step="year", stepmode="backward"),
                    dict(count=10, label="10Y", step="year", stepmode="backward"),
                    dict(step="all")
                ]),
                bgcolor="white"  # Optional: Change background color of the selector
            )

        )
    )

    #Show the plot
    return fig

chase_stock_line=plot_stock_price_chase(jpm_stock_data, 'Chase')

#-------------------------Historical stock price plot for Bank of America-----------------------------------

#Line plot for stock price of Bank of America

#Ticker module to access the JPM stock data
bac=yf.Ticker('BAC')
bac_stock_data=bac.history(period='max')
bac_stock_data.reset_index(inplace=True) #inpleace=True to modify the original dataframe to have the date as a column
bac_stock_data


def plot_stock_price_boa(stock_data, stock_name):
    
    #Parameters:
    stock_name='Bank of America' #Representing the name of the stock
    stock_data=bac_stock_data # DataFrame containing the stock data

    #Ensure that date is in datetime format
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])

    #Get today's date in the format YYYY-MM-DD
    today_date=pd.to_datetime('today').strftime('%Y-%m-%d')

    #Creating the line plot
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=stock_data['Date'], 
                                y=stock_data['Close'], 
                                mode='lines', 
                                name='Share Price',
                                line=dict(color=color_discrete_map[stock_name])))

    #Update the layout
    fig.update_layout(
        title=f'{stock_name} Historical Share Price',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        height=600,
        xaxis=dict(
            range=["1990-01-01", today_date],  # Directly set the initial view range of the plot
            rangeslider=dict(visible=True),
            rangeselector=dict(
                font=dict(color="black", size=12),  # Customize font color and size
                buttons=list([
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(count=5, label="5Y", step="year", stepmode="backward"),
                    dict(count=10, label="10Y", step="year", stepmode="backward"),
                    dict(step="all")
                ]),
                bgcolor="white"  # Optional: Change background color of the selector
            )

        )
    )

    #Show the plot
    return fig

boa_stock_line=plot_stock_price_boa(bac_stock_data, 'Bank of America')

#-------------------------Historical stock price plot for Wells Fargo-----------------------------------

#Ticker module to access the JPM stock data
wfc=yf.Ticker('WFC')
wfc_stock_data=wfc.history(period='max')
wfc_stock_data.reset_index(inplace=True) #inpleace=True to modify the original dataframe to have the date as a column


def plot_stock_price_wfc(stock_data, stock_name):
    
    #Parameters:
    stock_name='Wells Fargo' #Representing the name of the stock
    stock_data=wfc_stock_data # DataFrame containing the stock data

    #Ensure that date is in datetime format
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])

    #Get today's date in the format YYYY-MM-DD
    today_date=pd.to_datetime('today').strftime('%Y-%m-%d')

    #Creating the line plot
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=stock_data['Date'], 
                                y=stock_data['Close'], 
                                mode='lines', 
                                name='Share Price',
                                line=dict(color=color_discrete_map[stock_name])))

    #Update the layout
    fig.update_layout(
        title=f'{stock_name} Historical Share Price',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        height=600,
        xaxis=dict(
            range=["1990-01-01", today_date],  # Directly set the initial view range of the plot
            rangeslider=dict(visible=True),
            rangeselector=dict(
                font=dict(color="black", size=12),  # Customize font color and size
                buttons=list([
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(count=5, label="5Y", step="year", stepmode="backward"),
                    dict(count=10, label="10Y", step="year", stepmode="backward"),
                    dict(step="all")
                ]),
                bgcolor="white"  # Optional: Change background color of the selector
            )

        )
    )

    #Show the plot
    return fig
wf_stock_line=plot_stock_price_wfc(wfc_stock_data, 'Wells Fargo')

#-------------------------Historical stock price plot for Citibank-----------------------------------



#Ticker module to access the JPM stock data
c=yf.Ticker('C')
c_stock_data=c.history(period='max')
c_stock_data.reset_index(inplace=True) #inpleace=True to modify the original dataframe to have the date as a column


def plot_stock_price_c(stock_data, stock_name):
    
    #Parameters:
    stock_name='Citigroup' #Representing the name of the stock
    stock_data=c_stock_data # DataFrame containing the stock data

    #Ensure that date is in datetime format
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])

    #Get today's date in the format YYYY-MM-DD
    today_date=pd.to_datetime('today').strftime('%Y-%m-%d')

    #Creating the line plot
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=stock_data['Date'], 
                                y=stock_data['Close'], 
                                mode='lines', 
                                name='Share Price',
                                line=dict(color=color_discrete_map[stock_name])))

    #Update the layout
    fig.update_layout(
        title=f'{stock_name} Historical Share Price',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark',
        height=600,
        xaxis=dict(
            range=["1990-01-01", today_date],  # Directly set the initial view range of the plot
            rangeslider=dict(visible=True),
            rangeselector=dict(
                font=dict(color="black", size=12),  # Customize font color and size
                buttons=list([
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(count=5, label="5Y", step="year", stepmode="backward"),
                    dict(count=10, label="10Y", step="year", stepmode="backward"),
                    dict(step="all")
                ]),
                bgcolor="white"  # Optional: Change background color of the selector
            )

        )
    )

    #Show the plot
    return fig

cg_stock_line=plot_stock_price_c(c_stock_data, 'Citigroup')


#=============================  Dash app Layout==============================================

# App layout
app.layout = html.Div([
         dcc.Interval( #Updates the stock data for the Big Four Banks every 24 hours
        id='interval-component',
        interval=24*60*60*1000, # updates every 24 hours
        n_intervals=0 #
        ),
        dcc.Tabs(id="tabs",
                 #selected_style={'backgroundColor': '#4146cc', 'color': '#FFFFFF'},
                 children=[
        dcc.Tab(label='Mergers and Acquisitions', 
                style={'backgroundColor': '#121212', 'color': '#FFFFFF','height': '40px'},
                selected_style={'height': '35px'},
                children=[
            html.Div([
                    html.H1('The Big Four Banks-Network of Acquisitions and Mergers',
            style={'textAlign': 'center'}),
# Row for Dropdown and Toggle================================================
    html.Div([
        # Column for Dropdown
        html.Div([
            html.H3('Select a Bank:', style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='bank-dropdown',
                options=[
                    {'label': 'Bank of America', 'value': 'Bank of America'},
                    {'label': 'Wells Fargo', 'value': 'Wells Fargo'},
                    {'label': 'Citibank', 'value': 'Citibank'},
                    {'label': 'Chase', 'value': 'Chase'}
                    # Add more banks here
                ],
                value='Chase',  # Default bank selection
                style={
                    'backgroundColor': '#121212',
                    'color': '#FFFFFF',
                    'border': '1px solid #FFFFFF',
                    'width': '100%',  # Adjusted for responsiveness within the column
                    'textAlign': 'center',
                    'margin': 'auto',
                }
            )
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '0 20px 20px 0'}),  # Adjust width for side-by-side arrangement

        # Column for BooleanSwitch--------------------------------------------
        html.Div([
            html.H3('Include branch consolidation',style={'textAlign': 'center'}),
            daq.BooleanSwitch(
                id='branch-consolidation-toggle',
                color='#4146cc',
                on=False
            )
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ], style={'width': '100%', 'display': 'flex', 'flexWrap': 'wrap'}), #Style for the row

    # Row for Checklists of Accounting Method and Transformation Code==============
    html.Div([
        # Column for Accounting Method Checklist
        html.Div([
            html.H3('Filter by Accounting Method:', style={'textAlign': 'center'}),
            dcc.Checklist(
                id='acct-method-checklist',
                options=[
                    {'label': 'Not applicable', 'value': 'Not Applicable'},
                    {'label': 'Merger', 'value': 'Merger'},
                    {'label': 'Purchase/Acquisition', 'value': 'Purchase/Acquisition'}
                ],
                value=['Not Applicable', 'Merger', 'Purchase/Acquisition'],  # Default selected values
                inline=True
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '0 20px 20px 0','textAlign': 'center'}),

        # Column for Transformation Code Checklist---------------------------------
        html.Div([
            html.H3('Filter by Transformation Code:', style={'textAlign': 'center'}),
            dcc.Checklist(
                id='trsfm-code-checklist',
                options=[
                    {'label': 'Charter Discontinued', 'value': 'Charter Discontinued'},
                    {'label': 'Split', 'value': 'Split'},
                    {'label': 'Sale of Assets', 'value': 'Sale of Assets'},
                    {'label': 'Charter Retained', 'value': 'Charter Retained'},
                    {'label': 'Failure', 'value': 'Failure'}
                ],
                value=['Charter Discontinued', 'Split', 'Sale of Assets', 'Charter Retained', 'Failure'],  # Default selected values
                inline=True
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top','textAlign': 'center'}),
    ], style={'width': '100%', 'display': 'flex', 'flexWrap': 'wrap'}), #Style for the row

    # Row for Network Graph=======================================
    dcc.Graph(id='network-graph',
              style={'margin': 'auto'},
              ),
    dcc.Markdown(
    '''
    ### Notes Section

    <u>Accounting Method</u>: 
    indicates the accounting method used in resolving a non-failure transformation.
     * Not Applicable: The accounting method is not applicable.
     * Merger: the merger method occurs when  the assets, liabilities, and capital of the merging entitites are added together, and their expenses and income are combined.
     * Purhchase/acqusition: The purchase method occurs when one entity purchases some or all
     of the assets, and assumes some or all of the liabilities of another entity.

    <u>Transformation Code</u>: describes the nature of the transformation.
     * Charter Discontinued: Predecessor transfers its assets to one or more Successors. Predecessor ceases to exist.
     * Split: Predecessor transfers between 40 and 94 percent of its assets to one or more newly
          formed Successors. Predecessor and Successor continue to exist.
     * Sale of Assets: Predecessor transfers between 40 and 94 percent of its assets to one or
         more existing Successors. Predecessor and Successor continue to exist.
     * Charter Retained: Predecessor transfers 95 percent
         or more of its assets to one or more Successors. The charter that had been associated with
         Predecessor continues to exist.
     * Failure: Government assistance provided. Predecessor fails and ceases to exist. Assets
         may be distributed to other entities as well as the regulatory agency.    

    <u>Data source:</u> "Relationships.csv". National Information Center. Federal Financial Institutions Examination Council. Feb. 5, 2024. [Link](https://www.ffiec.gov/npw/FinancialReport/DataDownload).

    <u>Data dictionary:</u> "Bulk Data Download Data Dictionary and References Guide." Version 2.0. National Information Center. Federal Financial Institutions Examination Council. Sept., 2023. [Link](https://www.ffiec.gov/npw/StaticData/DataDownload/NPW%20Data%20Dictionary.pdf).

    <u>Limitations</u>: The data does not exclude subsidiary consolidations.

       
    ''', 
     dangerously_allow_html=True, 
     style={'padding': '1px', 
             'margin-top':'1px', # Add margin to the top
             'backgroundColor':'#121212',
             'color':'white', # Change the font color to white
             'marginLeft': '25%', 'marginRight': '25%'
             }
                 )# Place your network plot and its filtering capabilities here
            ])
        ]),
            dcc.Tab(
                label='Consolidated Assets',
                style={'backgroundColor': '#121212', 'color': '#FFFFFF', 'height': '30px', 'display': 'block'},
                selected_style={'height': '40px'},
                children=[
                    dmc.Grid(
                        gutter="xs",  # Adjust space between plots
                        children=[
                            dmc.Col(html.Iframe(id='lin-reg-plot', src="//plotly.com/~juanchojuaninski/60.embed", style={'width': '100%', 'height': '400px'}), md=6, sm=12),
                            dmc.Col(html.Iframe(id='treemap-plot', src="//plotly.com/~juanchojuaninski/48.embed", style={'width': '100%', 'height': '400px'}), md=6, sm=12),
                            dmc.Col(html.Iframe(id='animated-pie-chart', src="https://drive.google.com/file/d/1V9ediUsIoGrvC6Ngsh6ha0HosYxdDslL/preview", style={'width': '100%', 'height': '400px'}), md=6, sm=12),
                            dmc.Col(html.Iframe(id='line-plot', src="//plotly.com/~juanchojuaninski/44.embed", style={'width': '100%', 'height': '400px'}), md=6, sm=12),
                        ] 
                    ),
                    dcc.Markdown(
                        "Data source: Large Commercial Banks. Board of Governors of the Federal Reserve System. [Link](https://www.federalreserve.gov/releases/lbr/).",
                        dangerously_allow_html=True, 
                        style={'padding': '1px', 
                                'margin-top':'1px', # Add margin to the top
                                'backgroundColor':'#121212',
                                'color':'white', # Change the font color to white
                                'marginLeft': '25%', 'marginRight': '25%'
                                }
                    )
                ]
        
            ),
            dcc.Tab(label='Phylogenetic Tree',
                style={'backgroundColor': '#121212', 'color': '#FFFFFF', 'height': '30px', 'display': 'block'},
                selected_style={'height': '40px'},
                children=[
                    dmc.Grid(
                        gutter="xs",  # Adjust space between plots
                        children=[
                            dmc.Col([
                                dcc.Markdown(f"# Giga Banks Ownership on the Big Four", style={'text-align': 'center'}), #Add title to the table.
                                data_table, # Add the DataTable
                                dcc.Graph(id='chase-stock-price', figure=chase_stock_line, style={'width': '100%', 'height': '400px'}), # Add the Chase historical stock data plot
                                dcc.Graph(id='boa-stock-price', figure=boa_stock_line, style={'width': '100%', 'height': '400px'}), # Add the Bank of America historical stock data plot
                                dcc.Graph(id='wf-stock-price', figure=wf_stock_line, style={'width': '100%', 'height': '400px'}), # Add the Wells Fargo historical stock data plot
                                dcc.Graph(id='c-stock-price', figure=cg_stock_line, style={'width': '100%', 'height': '400px'}), # Add the Bank of America historical stock data plot
                                dcc.Markdown(
                                    "Data source: Yahoo! Finace. yfiance API. [Link](https://finance.yahoo.com/).",
                                    dangerously_allow_html=True, 
                                    style={'padding': '1px', 
                                    'margin-top':'1px', # Add margin to the top
                                    'backgroundColor':'#121212',
                                    'color':'white', # Change the font color to white
                                    'marginLeft': '25%', 'marginRight': '25%'
                                    }
                    )
                                     ],style={'overflow':'auto', 'height':'950px'}
                                    ,md=6, sm=12), # Add the DataTable 
                                
                                dmc.Col(html.Iframe(id='phylogenetic_tree', src="//jsfiddle.net/juancho12k/8foahbuz/54/embedded/result/dark/", style={'width': '100%', 'height': '950px'}), md=6, sm=12),
                        ]
                    )
                ]



            )
        ])])
    
#==========Callback function to update the stock data plots of the Big Four banks every 24 horus=============================

@app.callback(
        [Output('chase-stock-price','figure'),
         Output('boa-stock-price','figure'),
        Output('wf-stock-price','figure'),
        Output('c-stock-price','figure')],
        [Input('interval-component', 'n_intervals')]
        )
def update_stock_data(n):
    #Fetch new data from Yahoo Finance for Chase
    jmp=yf.Ticker('JPM')
    jpm_stock_data=jmp.history(period='1d')
    chase_figure=plot_stock_price_chase(jpm_stock_data, 'Chase')

    #Fetch new data from Yahoo Finance for Bank of America
    bac=yf.Ticker('BAC')
    bac_stock_data=bac.history(period='1d')
    boa_figure=plot_stock_price_boa(bac_stock_data, 'Bank of America')

    #Fetch new data from Yahoo Finance for Wells Fargo
    wfc=yf.Ticker('WFC')
    wfc_stock_data=wfc.history(period='1d')
    wf_figure=plot_stock_price_wfc(wfc_stock_data, 'Wells Fargo')

    #Fetch new data from Yahoo Finance for Citigroup
    c=yf.Ticker('C')
    c_stock_data=c.history(period='1d')
    c_figure=plot_stock_price_c(c_stock_data, 'Citigroup')

    return chase_figure, boa_figure, wf_figure, c_figure

#========================control browser caching behavior ===================================    
@app.server.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response



#========================Callback to update the network graph based on selected filters==============================
# Callback to update the network graph based on selected filters
@app.callback(
    Output('network-graph', 'figure'),
    [Input('bank-dropdown', 'value'),
     Input('acct-method-checklist', 'value'),
     Input('trsfm-code-checklist', 'value'),
     Input('branch-consolidation-toggle', 'on')
     ]
)


def update_graph(selected_bank, selected_acct_methods, selected_trsfm_codes, branch_consolidation):
    # Define a dictionary to map bank names to their corresponding DataFrames and plot functions
    bank_data = {
        'Chase': {
            'df': trans_chase_df,
            'plot_func': generate_chase_network_plot
        },
        'Bank of America': {
            'df': trans_boa_df,
            'plot_func': generate_boa_network_plot
        },
        'Wells Fargo': {
            'df': trans_wf_df,
            'plot_func': generate_wf_network_plot 
        },
        'Citibank': {
            'df': trans_cb_df,
            'plot_func': generate_cb_network_plot  
        }
    }

    #Initially assign the DataFrame for the selected bank
    df=bank_data[selected_bank]['df']



    #Continue with your filtering logic as before
    if not branch_consolidation:
        #Use 'selected_bank' to get the list of branches for the selected bank
        branch_list_var=bank_to_branch_list[selected_bank]
        df=df[~df['Predecessor_Name'].isin(branch_list_var)]

    # Plot function for the selected bank
    plot_func = bank_data[selected_bank]['plot_func']

    # Filter the DataFrame based on selected accounting methods and transformation codes
    filtered_df = df[
        (df['Accounting Method'].isin(selected_acct_methods)) &
        (df['Transformation Code'].isin(selected_trsfm_codes))
    ]

    # Generate the network plot based on the filtered DataFrame
    fig = plot_func(filtered_df)
    return fig

#========Function to generate network plot for Chase===============================
def generate_chase_network_plot(filtered_df):
    G = nx.DiGraph()

    # Define node positions based on the 'Year'
    pos = {}
    year_min = filtered_df['Year'].min()
    year_max = filtered_df['Year'].max()
    y_pos = 0

    for _, row in filtered_df.iterrows():
        G.add_node(row['Predecessor_Name'], 
                year=row['Year'], 
                trsfm_cd=row['Transformation Code'], 
                acct_method=row['Accounting Method'])
        pos[row['Predecessor_Name']] = (row['Year'], y_pos)
        y_pos += 1

    G.add_node('Chase')
    pos['Chase'] = (year_max + 1, y_pos / 2)  # Position Chase at the end

    # Add edges from predecessors to 'Chase'
    for _, row in filtered_df.iterrows():
        G.add_edge(row['Predecessor_Name'], row['Successor_Name'])

    # Create edge trace for plotly
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create node trace
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_text = []
    for node in G.nodes():
        year = G.nodes[node].get('year', 'N/A')
        trsfm_cd = G.nodes[node].get('trsfm_cd', 'N/A')
        acct_method = G.nodes[node].get('acct_method', 'N/A')
        node_info = f'{node}<br>Year: {year}<br>Transformation Code: {trsfm_cd}<br>Accounting Method: {acct_method}'
        node_text.append(node_info)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            size=10,
            line_width=2,color='#0D5EAF'))

    # Create the figure for plotting
    fig_chase = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Network of Chase Acquisitions and Mergers',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='y unified',
                    xaxis=dict(title='Year of Transformation'),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    margin=dict(b=20,l=5,r=5,t=40)) # Set margins to add a title and adjust the plot size. 'b' is the bottom margin, 'l' is the left margin, 'r' is the right margin, and 't' is the top margin.
                    )

    #Add dark theme
    fig_chase.update_layout(template='plotly_dark')
    fig = go.Figure()
    # Your code to generate the plot goes here
    
    return fig_chase

#========Function to generate network plot for Bank of America===============================

def generate_boa_network_plot(filtered_df):
# Create a directed graph
    G = nx.DiGraph()

    # Define node positions based on the 'Year'
    pos = {}
    year_min = filtered_df['Year'].min()
    year_max = filtered_df['Year'].max()
    y_pos = 0

    for _, row in filtered_df.iterrows():
        G.add_node(row['Predecessor_Name'], 
                year=row['Year'], 
                trsfm_cd=row['Transformation Code'], 
                acct_method=row['Accounting Method'])
        pos[row['Predecessor_Name']] = (row['Year'], y_pos)
        y_pos += 1

    G.add_node('Bank of America')
    pos['Bank of America'] = (year_max + 1, y_pos / 2)  # Position BoA at the end

    # Add edges from predecessors to 'BoA'
    for _, row in filtered_df.iterrows():
        G.add_edge(row['Predecessor_Name'], row['Successor_Name'])

    # Create edge trace for plotly
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create node trace
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_text = []
    for node in G.nodes():
        year = G.nodes[node].get('year', 'N/A')
        trsfm_cd = G.nodes[node].get('trsfm_cd', 'N/A')
        acct_method = G.nodes[node].get('acct_method', 'N/A')
        node_info = f'{node}<br>Year: {year}<br>Transformation Code: {trsfm_cd}<br>Accounting Method: {acct_method}'
        node_text.append(node_info)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            size=10,
            line_width=2,color='#CB0D1F'))

    # Create the figure for plotting
    fig_boa = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Network of Bank of America Acquisitions and Mergers',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='y unified',
                    xaxis=dict(title='Year of Transformation'),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    margin=dict(b=20,l=5,r=5,t=40)) # Set margins to add a title and adjust the plot size. 'b' is the bottom margin, 'l' is the left margin, 'r' is the right margin, and 't' is the top margin.
                    )

    #Add dark theme
    fig_boa.update_layout(template='plotly_dark')

    return fig_boa


#========Function to generate network plot for Well Fargo===============================
def generate_wf_network_plot(filtered_df):
# Create a directed graph
    G = nx.DiGraph()

    # Define node positions based on the 'Year'
    pos = {}
    year_min = filtered_df['Year'].min()
    year_max = filtered_df['Year'].max()
    y_pos = 0

    for _, row in filtered_df.iterrows():
        G.add_node(row['Predecessor_Name'], 
                year=row['Year'], 
                trsfm_cd=row['Transformation Code'], 
                acct_method=row['Accounting Method'])
        pos[row['Predecessor_Name']] = (row['Year'], y_pos)
        y_pos += 1

    G.add_node('Wells Fargo')
    pos['Wells Fargo'] = (year_max + 1, y_pos / 2)  # Position BoA at the end

    # Add edges from predecessors to 'Wells Fargo'
    for _, row in filtered_df.iterrows():
        G.add_edge(row['Predecessor_Name'], row['Successor_Name'])

    # Create edge trace for plotly
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create node trace
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_text = []
    for node in G.nodes():
        year = G.nodes[node].get('year', 'N/A')
        trsfm_cd = G.nodes[node].get('trsfm_cd', 'N/A')
        acct_method = G.nodes[node].get('acct_method', 'N/A')
        node_info = f'{node}<br>Year: {year}<br>Transformation Code: {trsfm_cd}<br>Accounting Method: {acct_method}'
        node_text.append(node_info)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            size=10,
            line_width=2,color='#FFD408'))

    # Create the figure for plotting
    fig_wf = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Network of Wells Fargo Acquisitions and Mergers',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='y unified',
                    xaxis=dict(title='Year of Transformation'),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    margin=dict(b=20,l=5,r=5,t=40)) # Set margins to add a title and adjust the plot size. 'b' is the bottom margin, 'l' is the left margin, 'r' is the right margin, and 't' is the top margin.
                    )

    #Add dark theme
    fig_wf.update_layout(template='plotly_dark')

    return fig_wf


#========Function to generate network plot for Citibank===============================
def generate_cb_network_plot(filtered_df):
    # Create a directed graph
    G = nx.DiGraph()

    # Define node positions based on the 'Year'
    pos = {}
    year_min = filtered_df['Year'].min()
    year_max = filtered_df['Year'].max()
    y_pos = 0

    for _, row in filtered_df.iterrows():
        G.add_node(row['Predecessor_Name'], 
                year=row['Year'], 
                trsfm_cd=row['Transformation Code'], 
                acct_method=row['Accounting Method'])
        pos[row['Predecessor_Name']] = (row['Year'], y_pos)
        y_pos += 1

    G.add_node('Citibank')
    pos['Citibank'] = (year_max + 1, y_pos / 2)  # Position BoA at the end

    # Add edges from predecessors to 'Citibank'
    for _, row in filtered_df.iterrows():
        G.add_edge(row['Predecessor_Name'], row['Successor_Name'])

    # Create edge trace for plotly
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Create node trace
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_text = []
    for node in G.nodes():
        year = G.nodes[node].get('year', 'N/A')
        trsfm_cd = G.nodes[node].get('trsfm_cd', 'N/A')
        acct_method = G.nodes[node].get('acct_method', 'N/A')
        node_info = f'{node}<br>Year: {year}<br>Transformation Code: {trsfm_cd}<br>Accounting Method: {acct_method}'
        node_text.append(node_info)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_text,
        marker=dict(
            size=10,
            line_width=2,color='#1598C3'))

    # Create the figure for plotting
    fig_cb = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Network of Citigroup Acquisitions and Mergers',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='y unified',
                    xaxis=dict(title='Year of Transformation'),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    margin=dict(b=20,l=5,r=5,t=40)) # Set margins to add a title and adjust the plot size. 'b' is the bottom margin, 'l' is the left margin, 'r' is the right margin, and 't' is the top margin.
                    )
        #Add dark theme
    fig_cb.update_layout(template='plotly_dark')

    return fig_cb

#===========================List of branches=======================================================
# Define the list of branch consolidation entities for the switch filter for Chase
    
chase_branch_list=[
 'BINGHAMTON BRANCH [CHASE MANHATTAN BANK, THE]',
 'GREENWICH OFFICE [GLENS FALLS NATIONAL BANK AND TRUST COMPANY]',
 'HILTON BRANCH [MANUFACTURERS AND TRADERS TRUST COMPANY]',
 '225 SOUTH STREET BRANCH [JPMORGAN CHASE BANK, NATIONAL ASSOCIATION]',
 'HEMPSTEAD BRANCH [JPMORGAN CHASE BANK]',
 'BROAD STREET DOWNTOWN [JPMORGAN CHASE BANK, NATIONAL ASSOCIATION]',
 'NYACK BRANCH [MANUFACTURERS AND TRADERS TRUST COMPANY]',
 'CHICAGO MAIN [JPMORGAN CHASE BANK, NATIONAL ASSOCIATION]',
 '60 WALL STREET BRANCH [JPMORGAN CHASE BANK, NATIONAL ASSOCIATION]',
 'PLUM STREET BRANCH [CHASE MANHATTAN BANK, THE]',
 'SMITHTOWN BRANCH [JPMORGAN CHASE BANK, NATIONAL ASSOCIATION]',
 'KIMBALL JUNCTION BRANCH [JPMORGAN CHASE BANK, NATIONAL ASSOCIATION]',
 'CHASE PLAZA [JPMORGAN CHASE BANK, NATIONAL ASSOCIATION]',
 'HOUSTON MAIN BRANCH [JPMORGAN CHASE BANK, NATIONAL ASSOCIATION]',
 '277 PARK AVENUE BRANCH [CHEMICAL BANK]',
 'BUFFALO BRANCH [MANUFACTURERS AND TRADERS TRUST COMPANY]'
]

# Define the list of branch consolidation entities for the switch filter for Bank of America
boa_branch_list = [
 'COLUMBIA DOWNTOWN BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'FORT DODGE BRANCH [NORTHWEST BANK]',
 'DOWNTOWN JACKSONVILLE BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'ASHEVILLE BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'NEW YORK BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'QUINCY BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'PINE BLUFF MAIN BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'NORTH AKARD STREET BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'SANIBEL BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'CAMDEN BRANCH [FARMERS BANK & TRUST COMPANY]',
 'HOME OFFICE [RBC CENTURA BANK]',
 'BATESVILLE MAIN BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'HILLSBORO MAIN BRANCH [FIRST COMMUNITY BANK OF HILLSBORO]',
 'FAYETTEVILLE EAST CENTER BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'JACKSONVILLE BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'MOUNT VERNON MAIN BRANCH [FIRST FINANCIAL BANK, NATIONAL ASSOCIATION]',
 'BANK OF AMERICA CENTER TULSA BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'RICHMOND CENTER BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'LINCOLNTON BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'FIELD BUILDING BRANCH, THE [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'MARSHALL MAIN BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'BENTON BRANCH PUBLIC SQUARE [FIRST FINANCIAL BANK, NATIONAL ASSOCIATION]',
 'SOUTHWEST MISSOURI BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 '114 WEST 47TH STREET BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'SKYWALK BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'PWM LITTLE ROCK BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'ROCK HILL BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'ROSWELL MAIN [WASHINGTON FEDERAL, NATIONAL ASSOCIATION]',
 'RICHLAND BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'HOT SPRINGS MAIN BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'WEST PLAINS MAIN BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'PWM LASALLE MIDWEST BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'DELAWARE AVENUE BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'RATON BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'TAPO CANYON BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'LAS CRUCES BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'FARMINGTON BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'GLOUCESTER STREET BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'RIO ARRIBA MAIN BRANCH [WASHINGTON FEDERAL BANK]',
 'SILVER CITY MAIN BRANCH [WASHINGTON FEDERAL BANK]',
 'ONE KANSAS CITY PLACE BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'SANTA TERESA NM BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'CALIFORNIA STREET BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'NEWARK FRONT STREET BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'ALBUQUERQUE BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'SPENCER BRANCH [NORTHWEST BANK]',
 'BOATMENS VANDALIA BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'SOUTHERN MISSOURI BR [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'CHERRY CREEK BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'LEBANON BRANCH [ARVEST BANK]',
 'ATLANTA BANK OF AMERICA PLAZA BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'SANTA FE BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'BOONVILLE BRANCH [FIRST STATE COMMUNITY BANK]',
 'RUSSELLVILLE MAIN BRANCH [ARVEST BANK]',
 'JONESBORO MAIN BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'BULL SHOALS MAIN BRANCH [FIRST SECURITY BANK]',
 'HARKRIDER NORTH BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'WILLIAM STREET BRANCH [FIRST STATE COMMUNITY BANK]',
 'MASON CITY BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'MIDTOWN BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'RIVER VALLEY BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'SAINT LOUIS MAIN BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'GALLUP BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'KENNEDY PLAZA [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'NEW BERN OFFICE [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'HOBBS MAIN BRANCH [WASHINGTON FEDERAL BANK]',
 'BANK OF AMERICA PLAZA BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'TROY BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'HIGHLANDS BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'PLAZA SAN JACINTO BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'COLES COUNTY BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'HENDERSON OFFICE [NATIONSBANK OF NORTH CAROLINA, NATIONAL ASSOCIATION]',
 'CLOVIS BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'KENNETT BRANCH [FIRST STATE COMMUNITY BANK]',
 'OSAGE BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'ROLLA MAIN BRANCH [FIRST STATE COMMUNITY BANK]',
 'NASHVILLE MAIN BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'SALT LAKE CITY BRANCH [BANK OF AMERICA, NATIONAL ASSOCIATION]',
 'MOUNT AIRY OFFICE [FIRST COMMUNITY BANK]']

# Define the list of branch consolidation entities for the switch filter for Wells Fargo
wf_branch_list = [
 'PAJARO VALLEY BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'BOISE MAIN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'FARGO MAIN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'BARRANCA TOWERS BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'SEATTLE MAIN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'SOLANA BEACH BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'BEVERLY HILLS BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'DOWNTOWN MB BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'MID-PENINSULA BANK MAIN, COWPER BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'DRIGGS BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'PINEDALE BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'SHERIDAN MAIN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'WELLS FARGO BANK SAN FRANCISCO OFFICE [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'DENVER MAIN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 '5TH & JEFFERSON BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'WELLS FARGO FINANCIAL BANK BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'CANON MAIN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'NORTHERN LIGHTS & C STREET BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'MESA MALL BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'ANAHEIM BRANCH #3 [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'VENTURA OFFICE [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'GLENDALE BRAND OFFICE [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'PHOENIX MAIN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'SANTA MARIA BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'TOWER BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'GATEWAY BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'DIXIE FARM ROAD STORE BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'VAN WERT BRANCH [FLAGSTAR BANK, NATIONAL ASSOCIATION]',
 'NAPA DOWNTOWN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'TENTH & SHIPLEY BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'CASPER DOWNTOWN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'JACKSON TOWN SQUARE BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'OMAHA MAIN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'FELICITA VILLAGE BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'SANTA CRUZ BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'CENTRAL & WASHINGTON BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'LAS VEGAS TOWER BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'WELLS FARGO CENTER SKYWAY BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'HARBOR BOULEVARD BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'MARQUETTE DOWNTOWN BRANCH [FLAGSTAR BANK, NATIONAL ASSOCIATION]',
 'CODY MAIN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'BILLINGS DOWNTOWN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'ROGERS SOUTH BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'ORANGE PLAZA BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'SANTA FE MAIN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'BUENA PARK BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'SAN FRANCISCO MAIN OFFICE [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'INDIANA CENTER BRANCH [FLAGSTAR BANK, NATIONAL ASSOCIATION]',
 'DOWNTOWN AUBURN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'HOLTVILLE BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'MARKET FINANCIAL BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'MARYSVILLE BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'AZUSA BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'RICHMOND ROAD BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'JACKSON BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'SAN FRANCISCO MAIN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'COLORADO-ORANGE GROVE BLVD BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'MILWAUKEE MAIN BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'NORTH LAS VEGAS BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'THOUSAND OAKS BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'LOMAS BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'PUEBLO MESSENGER SERVICE BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'SAN LUIS OBISPO BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'GALESBURG BRANCH [WELLS FARGO BANK, NATIONAL ASSOCIATION]',
 'PARADISE OFFICE [WELLS FARGO BANK, NATIONAL ASSOCIATION]'
]


# Define the list of branch consolidation entities for the switch filter for Citibank
cb_branch_list = [
 'RESTON BRANCH [CITIBANK, N.A.]',
 'PORT RICHMOND BR [CITIBANK, N.A.]',
 'NEW CASTLE BRANCH [CITIBANK, N.A.]',
 'LA MAIN BRANCH [CITIBANK, N.A.]',
 'CENTRAL VALLEY BRANCH [HUDSON UNITED BANK]',
 '120 BROADWAY BRANCH [CITIBANK, N.A.]',
 'LINCOLN PARK BRANCH [CITIBANK, N.A.]',
 '99 GARNSEY BRANCH [CITIBANK, N.A.]',
 'BAY SHORE BRANCH [CITIBANK, N.A.]',
 'SAN FRANCISCO BRANCH [CITIBANK, N.A.]'
]


# Map 'selected_bank' values to corresponding branch lists
bank_to_branch_list = {
    'Chase': chase_branch_list,
    'Bank of America': boa_branch_list,
    'Wells Fargo': wf_branch_list,
    'Citibank': cb_branch_list}




#==============================Theme=================================================
# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
