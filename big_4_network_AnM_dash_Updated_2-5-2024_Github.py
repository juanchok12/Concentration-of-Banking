import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import networkx as nx
import pandas as pd
import dash_daq as daq
import gunicorn


app = dash.Dash(__name__, external_stylesheets=['dark_theme.css'])
server=app.server
#========================Loading the dataframes=================================
path_to_tables = r"C:\Users\16193\My Drive\Back Up\The Internationalist Group\Political Economy\Lenin's Imperialism\Concentration of banking\Phylogeny tree\Tables"

#Dataframe for Chase
trans_chase_df=pd.read_csv('https://raw.githubusercontent.com/juanchok12/Concentration-of-Banking/main/transformations_big_4/trans_chase_df.csv')

#Dataframe for Bank of America
trans_boa_df=pd.read_csv('https://raw.githubusercontent.com/juanchok12/Concentration-of-Banking/main/transformations_big_4/trans_boa_df.csv')

#Dataframe for Wells Fargo
trans_wf_df=pd.read_csv('https://raw.githubusercontent.com/juanchok12/Concentration-of-Banking/main/transformations_big_4/trans_wf_df.csv')  

#Dataframe for Citibank
trans_cb_df=pd.read_csv('https://raw.githubusercontent.com/juanchok12/Concentration-of-Banking/main/transformations_big_4/trans_cb_df.csv')


#============================= Initialize your Dash app==============================================

# App layout
app.layout = html.Div([
    html.H1('The Big Four Banks-Network of Acquisitions and Mergers',
            style={'textAlign': 'center'},),
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
                'backgroundColor':'#121212',
                'color':'#FFFFFF',
                'border':'1px solid #FFFFFF',
                'width':'400px',
                'textAlign':'center',
                'margin':'auto',
                
                
            }
        )
    ], style={'padding': '20px'}),

    html.Div([
        daq.BooleanSwitch(
            id='branch-consolidation-toggle',
            label='Include branch consolidation',
            color='#4146cc',
            vertical=False,
            on=False

        )
    ], style={'padding': '5px',
              'color':'#FFFFFF',
              #'float':'left'              
              }),

    html.Div([
        html.H3('Filter by Accounting Method:', style={'textAlign': 'center'}),
        dcc.Checklist(
            id='acct-method-checklist',
            options=[
                {'label': 'Not applicable', 'value': 'Not Applicable'},
                {'label': 'Merger', 'value': 'Merger'},
                {'label': 'Purchase/acquisition', 'value': 'Purchase/acquisition'}
            ],
            value=['Not Applicable', 'Merger', 'Purchase/acquisition'],  # Default selected values
            inline=True,
            style={'marginLeft': '40%', 'marginRight': '25%','width': '50%'}
        ),
    ]),
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
            inline=True,
            style={'marginLeft': '35%', 'marginRight': '25%','width': '50%'}
        ),
    ]),
    dcc.Graph(id='network-graph',
              style={'width': '50%', 'margin': 'auto'},
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

    <u>Data source:</u> "Relationships.csv". National Information Center. Federal Financial Instututions Examination Council. Feb. 5, 2024. [Link](https://www.ffiec.gov/npw/FinancialReport/DataDownload).

    <u>Data dictionary:</u> "Bulk Data Download Data Dictionary and References Guide." Version 2.0. National Information Center. Federal Financial Instututions Examination Council. Sept., 2023. [Link](https://www.ffiec.gov/npw/StaticData/DataDownload/NPW%20Data%20Dictionary.pdf).

    <u>Limitations</u>: The data does not exclude subsidiary consolidations.

       
    ''', 
     dangerously_allow_html=True, 
     style={'padding': '1px', 
             'margin-top':'1px', # Add margin to the top
             'backgroundColor':'#121212',
             'color':'white', # Change the font color to white
             'marginLeft': '25%', 'marginRight': '25%'
             }
                 )
])

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
