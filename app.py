import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go


######################################################Data##############################################################
df = pd.read_csv('data/export_dataframe.csv')

indicator_names = ["Government expenditure on education, total (% of GDP)",
                   "Labor force, female (% of total labor force)",
                   "Literacy rate, adult female (% of females ages 15 and above)",
                   "Unemployment, total (% of total labor force)",
                   "Literacy rate, adult male (% of males ages 15 and above)",
                   "GDP per capita (current US$)"]
######################################################Interactive Components############################################
country_options = [dict(label=country, value=country) for country in df['Country Name'].unique()]

continent_options = [dict(label=continent, value=continent) for continent in df['Continent'].unique()]

indicator_options= [dict(label=indicator, value=indicator) for indicator in indicator_names]

####################################################APP#################################################################
app = dash.Dash(__name__)
server = app.server
##################################################CALLBACKS#############################################################

app.layout = html.Div([
    html.Div([
        html.H1(['Education as an Economy and Gender Equality Metric'])
    ]),

    html.Div([
            html.Label('Indicator Choice'),
                dcc.Dropdown(
                    id='indicator_options',
                    options=indicator_options,
                    value="Government expenditure on education, total (% of GDP)",
                    style={'backgroundColor': '#fffb77'}),
    ]),

    html.Div([
            html.Div([
                html.Div([

                    html.Article(['TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n' +
                                  'TESTETESTETESTETESTETESTETESTETESTETESTETESTETESS' + '\n']),

                html.Br(),

                html.Label('Year Slider'),

                html.Br(),
                html.Br(),

                dcc.Slider(
                    id='year_slider',
                    min=df['Time'].min(),
                    max=df['Time'].max(),
                    marks={str(i): '{}'.format(str(i)) for i in [1995, 2000, 2005, 2010, 2015, 2019]},
                    value=df['Time'].min(),
                    step=1
                ),

                html.Br(),
                html.Br(),

                html.Label('Projection'),

                html.Br(),
                html.Br(),

                dcc.RadioItems(
                    id='projection',
                    options=[dict(label='Orthographic', value=0), dict(label='Equirectangular', value=1)],
                    value=0
            ),

                    ], className='container'),

            ],className='column col1'),


            html.Div([
                dcc.Graph(id='choropleth_graph')
            ],className=' container cont2 column col2')

            ], className='row'),

            html.Label('Continent Choice'),

            html.Br(),

            dcc.Dropdown(
                id='continent_options',
                options=continent_options,
                value=['Europe'],
                multi=True,
                style={'backgroundColor': '#fffb77'},
            ),

            html.Div([

                html.Div([
                    dcc.Graph(id='bar1_graph')
                ], className='container cont1 column col3'),

                html.Div([
                    dcc.Graph(id='bar2_graph')
                ], className='container cont1 column col4'),

            ], className='row'),

            html.Div([

                html.Div([

                    html.Label('Country Choice'),

                    html.Br(),

                    dcc.Dropdown(
                        id='country_drop',
                        options=country_options,
                        value=['Portugal'],
                        multi=True,
                        style={'backgroundColor': '#fffb77'},
                    ),

                    html.Br(),

                    dcc.Graph(id='line_graph')
                ],className='container cont1 column col5'),

                html.Div([
                    dcc.Graph(id='matrix_graph'),html.Br(),

                    html.Article('Ind.1 = Government expenditure on education, total (% of GDP) '
                                 'Ind.2 = Labor force, female (% of total labor force) '
                                'Ind.3 = Literacy rate, adult female (% of females ages 15 and above) '
                                'Ind.4 = Unemployment, total (% of total labor force) '
                                'Ind.5 = Literacy rate, adult male (% of males ages 15 and above) '
                                'Ind.6 = GDP per capita (current US$)')
                ], className='container cont1 column col6')

            ], className='row')

],className='body')

@app.callback(
    [
        Output("bar1_graph", "figure"),
        Output("choropleth_graph", "figure"),
        Output("bar2_graph", 'figure'),
        Output('line_graph', 'figure'),
        Output('matrix_graph', 'figure')
    ],
    [
        Input("year_slider", "value"),
        Input("country_drop", "value"),
        Input("indicator_options", "value"),
        Input("projection", "value"),
        Input('continent_options','value')
    ]
)

def plots(year, countries, indicator, projection, continents):
    ############################################First Bar Plot##########################################################
    data_bar1 = []
    df_temp = df.fillna(0.0)
    df_temp = df_temp.replace(0.0,np.nan)


    for continent in continents:
        df_temp = df_temp.loc[(df_temp['Time'] == year)]
        df_temp = df_temp.loc[(df_temp['Continent']==continent)]
        df_temp = df_temp.nlargest(5,[indicator])
        x_bar = df_temp['Country Name']
        y_bar = df_temp[indicator]

        data_bar1.append(dict(type='bar', x=x_bar, y=y_bar,name=str(continent)))

    layout_bar1 = dict(title=dict(text='Values'),
                  yaxis=dict(title='Value',type='linear'),
                  paper_bgcolor='#f9f9f9'
                  )

    ############################################Second Bar Plot##########################################################
    data_bar2 = []
    df_temp = df.fillna(0.0)
    df_temp = df_temp.replace(0.0, np.nan)

    for continent in continents:
        df_temp = df_temp.loc[(df_temp['Time'] == year)]
        df_temp = df_temp.loc[(df_temp['Continent'] == continent)]
        df_temp = df_temp.nsmallest(5, [indicator])
        x_bar = df_temp['Country Name']
        y_bar = df_temp[indicator]

        data_bar2.append(dict(type='bar', x=x_bar, y=y_bar, name=str(continent)))

    layout_bar2 = dict(title=dict(text='Values'),
                      yaxis=dict(title='Value', type='linear'),
                      paper_bgcolor='#f9f9f9'
                      )

    #############################################Second Choropleth######################################################

    df_emission_0 = df.loc[df['Time'] == year]

    z = (df_emission_0[indicator])

    data_choropleth = dict(type='choropleth',
                           locations=df_emission_0['Country Name'],
                           # There are three ways to 'merge' your data with the data pre embedded in the map
                           locationmode='country names',
                           z=z,
                           text=df_emission_0['Country Name'],
                           colorscale='Viridis',
                           colorbar=dict(title='Scale'),

                           hovertemplate='Country: %{text} <br>' + str(indicator) + ': %{z}',
                           name=''
                           )

    layout_choropleth = dict(geo=dict(scope='world',  # default
                                      projection=dict(type=['orthographic', 'equirectangular'][projection]),
                                      # showland=True,   # default = True
                                      landcolor='black',
                                      lakecolor='white',
                                      showocean=True,  # default = False
                                      oceancolor='azure',
                                      bgcolor='#f9f9f9'
                                      ),

                             title=dict(text='World ' + str(indicator) + '<br>Choropleth Map on the year ' + str(year),

                                        x=.01,  # Title relative position according to the xaxis, range (0,1)
                                        xanchor='auto'
                                        ),
                             paper_bgcolor='#f9f9f9'
                             )

    ############################################## Line Graph ##########################################################
    data_line = []
    for country in countries:
        df_line=df.loc[(df['Country Name'] == country)]
        x_line = df_line['Time']
        y_line = df_line[indicator]

        data_line.append(dict(type='scatter', x=x_line, y=y_line, name=country, connectgaps = True))

    layout_line = dict(title=dict(text='Cona'),
                  yaxis=dict(title=indicator, type='linear'),
                  paper_bgcolor='#f9f9f9'
                  )

    ############################################### Matrix #############################################################

    df_matrix = df
    index_vals = df['Continent'].astype('category').cat.codes

    data_matrix=go.Splom(
                dimensions = [dict(label='Ind.1', values=df['Government expenditure on education, total (% of GDP)']),
                              dict(label='Ind.2', values=df['Labor force, female (% of total labor force)']),
                              dict(label='Ind.3',values=df['Literacy rate, adult female (% of females ages 15 and above)']),
                              dict(label='Ind.4',values=df['Unemployment, total (% of total labor force)']),
                              dict(label='Ind.5',values=df['Literacy rate, adult male (% of males ages 15 and above)']),
                              dict(label='Ind.6',values=df['GDP per capita (current US$)'])],
                text = df['Continent'],
                marker = dict(color = index_vals,
                              size=5,
                              line=dict(width=0.5,
                                        color='rgb(230,230,230)')
                              )
    )

    layout_matrix = dict(title=dict(text='Correlation between indicators'))

    ################################################ Return ############################################################

    return go.Figure(data=data_bar1, layout=layout_bar1), \
           go.Figure(data=data_choropleth, layout=layout_choropleth), \
           go.Figure(data=data_bar2, layout=layout_bar2), \
           go.Figure(data=data_line, layout=layout_line), \
           go.Figure(data=data_matrix, layout=layout_matrix)

######################################################Run the app#######################################################
if __name__ == '__main__':
    app.run_server(debug=True)

