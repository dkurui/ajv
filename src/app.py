import dash                              # pip install dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
from dash_extensions import Lottie       # pip install dash-extensions
# pip install dash-bootstrap-components
import dash_bootstrap_components as dbc
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
from dash.dependencies import Input, Output, State
from dash import dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from geopy.geocoders import Nominatim


from datetime import date
import calendar
from wordcloud import WordCloud
from dash import dependencies
yes_url = 'https://assets7.lottiefiles.com/packages/lf20_oaw8d1yt.json'
no_url = 'https://assets7.lottiefiles.com/packages/lf20_g0rackmk.json'
options = dict(loop=True, autoplay=True, rendererSettings=dict(
    preserveAspectRatio='xMidYMid slice'))
# data = pd.read_excel('ajv.xlsx')
data_2 = pd.read_csv('ajv_v2.csv')
data_3 = pd.read_csv('ajv_v2.csv')
original_journals = list(data_2['Journal tittle'])
journals = sorted(map(str, original_journals), key=lambda x: x.lower())
cols = ['number', 'journal_title', 'platform', 'country', 'publishers_name',
        'language', 'thematic_area', 'african_index_medicus',
        'medline', 'google_scholar',
        'impact_factor', 'scopus', 'h-index', 'eigen_factor',
        'eigen_factor_metrix', 'snip',
        'snip_metrix', 'oaj',
        'doaj',
        'issn',
        'cope',
        'publisher_in_africa', 'inasp',
        'Column1']
languages = list(set(data_2['Language']))
thematic_areas = list(set(data_2['Thematic area']))
data_3.columns = cols
original_values = {'country': '', 'language': '', 'thematic_area': '', 'google_scholar': '',
                   'scopus': '', 'oaj': '', 'doaj': '', 'issn': '', 'publisher_in_africa': '', 'inasp': '', 'cope': ''}

countries = ['Algeria',
             'Angola',
             'Benin',
             'Botswana',
             'Burkina Faso',
             'Burundi',
             'Cameroon',
             'Cape Verde',
             'Central African Republic',
             'Chad',
             'Comoros',
             'Democratic Republic of the Congo',
             'Djibouti',
             'Egypt',
             'Equatorial Guinea',
             'Eritrea',
             'Eswatini',
             'Ethiopia',
             'Gabon',
             'Ghana',
             'Guinea',
             'Guinea-Bissau',
             'Ivory Coast',
             'Kenya',
             'Lesotho',
             'Liberia',
             'Libya',
             'Madagascar',
             'Malawi',
             'Mali',
             'Mauritania',
             'Mauritius',
             'Morocco',
             'Mozambique',
             'Namibia',
             'Niger',
             'Nigeria',
             'Republic of the Congo',
             'Rwanda',
             'Sao Tome and Pri­ncipe',
             'Senegal',
             'Seychelles',
             'Sierra Leone',
             'Somalia',
             'South Africa',
             'South Sudan',
             'Sudan',
             'Tanzania',
             'The Gambia',
             'Togo',
             'Tunisia',
             'Uganda',
             'Zambia',
             'Zimbabwe']
selection_options = ['Yes', 'No']
final_table = ''

data_frame = pd.DataFrame()
# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

app.layout = dbc.Container([

    html.H1('African Journal Visibility', style={
            'text-align': 'center', 'margin-top': '10px'}),
    html.P('Enhancing African Journal Visibility',
           style={'text-align': 'center'}),

    dbc.Row([

        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Journals', style={
                    'text-align': 'center'}),
                html.Div(id='gs_plats', style={
                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                    html.P('The total number of Journals considered is:',
                           style={'text-align': 'center'}),
                    html.P(
                        id='content-total', style={'color': '#FF7F00', 'font-weight': 'bold', 'font-size': '48px', 'text-align': 'center'}),
                ])
            ], style={'border': 'none'}),

        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Journals Description', style={
                    'text-align': 'center'}),
                html.Div(id='scopus_', style={
                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'justify'}),
                dbc.CardBody([
                    html.P('The Journals considered are african journals that we were able to get their details. There may be more journals not captured here, we are trying to capture as many journals as possible. Keep checking for more updates',
                           style={'text-align': 'justify'}),
                ])
            ], style={'border': 'none'}),

        ], width=6),
    ], className='mb-0, mt-0'),
    html.Hr(style={'border-color': '#FF7F00'}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('JOURNALS\' DETAILS',
                               style={'text-align': 'center'}),
                html.Div(id='language', style={
                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader('Select/Search the Journal from the dropdown below to view its details', style={
                                    'text-align': 'center'}),
                                html.Div(id='journals_details', style={
                                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                                dbc.CardBody([
                                    dcc.Dropdown(
                                        options=[{'label': journal, 'value': journal}
                                             for journal in journals],
                                        # value=data['Journal tittle'][0],  # Set the initial value based on your data
                                        value='ACCORD Occasional Paper',  # Set the initial value based on your data
                                        id='journal-dropdown'
                                    ), ], style={'padding': '0', 'margin-top': '10px', 'border-radius': '10px', 'text-align': 'center', 'font-size': '14px'})
                            ], style={'border': 'none'}),
                        ], width=6),

                        dbc.Col([

                            dbc.Card([
                                dbc.CardHeader('Selected Journal', style={
                                    'text-align': 'center'}),
                                html.Div(id='selected_journal', style={
                                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                                dbc.CardBody([
                                    html.P(id='selected-journal', style={
                                        'color': '#FF7F00', 'font-weight': 'bold', 'text-align': 'left'}),
                                ], style={'border': 'none'}),
                            ], style={'border': 'none'})

                        ], width=6),
                    ]),
                ], style={'padding': '0', 'margin-top': '10px', 'border-radius': '10px', 'text-align': 'center'})
            ], style={'border': 'none'}),
        ], width=12),

    ], className='mb-0, mt-0'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(id='selected-journal2',
                               style={'text-align': 'center'}),
                html.Div(id='journal-details', style={
                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.P('Platform: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-platform',
                                       style={'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),

                            html.Div([
                                html.P('Country: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-country',  style={
                                       'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),

                            html.Div([
                                html.P('Language: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-language',  style={
                                       'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),

                            html.Div([
                                html.P('Journal Thematic Area: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-thematic_area',  style={
                                       'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P('Indexed on Google Scholar: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-google-scholar',  style={
                                       'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P('Indexed on Scopus: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-scopus',  style={'color': 'rgb(83 96 197)',  'font-weight': 'bold',
                                       'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P('Journal h-index: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-h_index',  style={
                                       'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),

                            html.Div([
                                html.P('Jounal Publisher: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-publisher_name',  style={
                                       'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),

                            html.Div([
                                html.P('Indexed on African Index Medicus: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-africa_index_medicus',  style={
                                       'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),

                            html.Div([
                                html.P(
                                    'Indexed in Medline (Medicine and Health Journals): ', style={
                                        'font-size': '14px'}),
                                html.P(id='content-medline',  style={
                                       'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P('Journal Impact Factor: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-impact_factor', style={
                                    'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),

                        ], width=6),

                        dbc.Col([


                            html.Div([


                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P('Journal Eigen Factor: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-eigen_factor',  style={
                                       'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P('Journal Eigen Matrix: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-eigen_factor_metrix',  style={
                                       'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P(
                                    'Journal Source Normalized Impact per Paper (SNIP): ', style={
                                        'font-size': '14px'}),
                                html.P(id='content-snip',  style={'color': 'rgb(83 96 197)',  'font-weight': 'bold',
                                       'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P(
                                    'Journal Source Normalized Impact per Paper (SNIP) Metrix: ', style={
                                        'font-size': '14px'}),
                                html.P(id='content-snip_metrix',  style={
                                       'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P('Listed on Open Access Journal (OAJ): ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-oaj',  style={'color': 'rgb(83 96 197)',  'font-weight': 'bold',
                                       'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P('Listed on Directory od Opena Access Journal (DOAJ): ', style={
                                       'font-size': '14px'}
                                       ),
                                html.P(id='content-doaj',  style={'color': 'rgb(83 96 197)',  'font-weight': 'bold',
                                       'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P('Journal present on ISSN Portal: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-issn',  style={'color': 'rgb(83 96 197)',  'font-weight': 'bold',
                                       'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P(
                                    'Journal\'s publisher is a member of Committee on publication Ethics: ', style={
                                        'font-size': '14px'}),
                                html.P(id='content-cope',  style={'color': 'rgb(83 96 197)',  'font-weight': 'bold',
                                       'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P(
                                    'Journal\'s Online publisher based in Africa: ', style={
                                        'font-size': '14px'}),
                                html.P(id='content-based-in-africa',  style={
                                       'color': 'rgb(83 96 197)',  'font-weight': 'bold', 'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),
                            html.Br(),
                            html.Div([
                                html.P('Hosted on INASP\'s Journal online: ', style={
                                       'font-size': '14px'}),
                                html.P(id='content-inasp',  style={'color': 'rgb(83 96 197)',  'font-weight': 'bold',
                                       'font-size': '12px', 'margin-top': '3.5px', 'margin-left': '10px'}),
                            ], style={'display': 'inline-flex', 'vertical-align': 'middle', 'height': '20px', 'margin-top': '4px'}),


                        ], width=6)

                    ]),

                ])
            ], style={'border': 'none'}),
        ], width=12),

    ], className='mb-2, mt-2'),

    html.Hr(style={'border-color': '#FF7F00'}),



    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Card([
                    dbc.CardHeader('Journal Filtering',
                                   style={'text-align': 'center'}),
                    html.Div(id='filtering', style={
                        'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                    dbc.CardBody([
                        html.P('In this section, use the options presented to filter the journals based on your preferences. All Journals that shall meet your criteria shall be displayed on the right in a table'),
                    ], style={'border': 'none'}),
                ],  style={'border': 'none'}),
            ]),

            dbc.Row([
                # COUNTRY
                dbc.Col([
                    dbc.Card([

                        dbc.CardBody([
                            html.P('COUNTRY', style={
                                'font-family': 'Sans-serif', 'text-align': 'left', 'font-color': 'black', 'font-size': '10px'}),
                            html.H6(id='selected-country', style={
                                'color': 'red',  'font-weight': 'bold', 'font-size': '12px', 'font-family': 'sans-serif'}),
                            dcc.Dropdown(
                                options=[{'label': opt, 'value': opt}
                                         for opt in countries],
                                value='',  # Set the initial value based on your data
                                id='country-dropdown-id'
                            ),

                        ])
                    ], className='mb-0', style={'border': 'red', 'background-color': 'transparent', 'border-radius': '10px', 'height': '5rem'}),
                ], width=4, style={'height': '10rem'}),

                # LANGUAGE
                dbc.Col([
                    dbc.Card([

                        dbc.CardBody([
                            html.P('LANGUAGE', style={
                                'font-family': 'Sans-serif', 'text-align': 'left', 'font-color': 'black', 'font-size': '10px'}),
                            html.H6(id='selected-langauge', style={
                                'color': 'red',  'font-weight': 'bold', 'font-size': '12px', 'font-family': 'sans-serif'}),
                            dcc.Dropdown(
                                options=[{'label': opt, 'value': opt}
                                         for opt in languages],
                                value='',  # Set the initial value based on your data
                                id='language-dropdown-id'
                            ),

                        ])
                    ], className='mb-0', style={'border': 'red', 'background-color': 'transparent', 'border-radius': '10px', 'height': '5rem'}),
                ], width=4, style={'height': '10rem'}),
                # THEMATIC AREA
                dbc.Col([
                    dbc.Card([

                        dbc.CardBody([
                            html.P('THEMATIC AREA', style={
                                'font-family': 'Sans-serif', 'text-align': 'left', 'font-color': 'black', 'font-size': '10px'}),
                            html.H6(id='selected-thematic_area', style={
                                'color': 'red',  'font-weight': 'bold', 'font-size': '12px', 'font-family': 'sans-serif'}),
                            dcc.Dropdown(
                                options=[{'label': opt, 'value': opt}
                                         for opt in thematic_areas],
                                value='',  # Set the initial value based on your data
                                id='thematic_area-dropdown-id'
                            ),
                        ])
                    ], className='mb-0', style={'border': 'red', 'background-color': 'transparent', 'border-radius': '10px', 'height': '5rem'}),
                ], width=4, style={'height': '10rem'}),


            ], className='mb-0 mt-0', style={'background-color': '#EFF7FD', 'border-radius': '10px', 'height': '6.5rem'}),
            dbc.Row([

                dbc.Col([
                    dbc.Row([
                        # GOOGLE SCHOLAR INDEXED
                        dbc.Col([
                            dbc.Card([

                                dbc.CardBody([
                                    html.P('GOOGLE SCHOLAR INDEXED', style={
                                        'font-family': 'Sans-serif', 'text-align': 'left', 'font-color': 'black', 'font-size': '10px'}),

                                    html.H6(id='selected-google_scholar', style={
                                        'color': 'red',  'font-weight': 'bold', 'font-size': '12px', 'font-family': 'sans-serif'}),
                                    dcc.Dropdown(
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in selection_options],
                                        value='',  # Set the initial value based on your data
                                        id='google_scholar-dropdown-id'
                                    ),
                                ])
                            ], className='mb-0', style={'border': 'red', 'background-color': 'transparent', 'border-radius': '10px'}),
                        ]),
                        # SCOPUS INDEXED
                        dbc.Col([
                            dbc.Card([

                                dbc.CardBody([
                                    html.P('INDEXED ON SCOPUS', style={
                                        'font-family': 'Sans-serif', 'text-align': 'left', 'font-color': 'black', 'font-size': '10px'}),
                                    html.H6(id='selected-scopus', style={
                                        'color': 'red',  'font-weight': 'bold', 'font-size': '12px', 'font-family': 'sans-serif'}),
                                    dcc.Dropdown(
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in selection_options],
                                        value='',  # Set the initial value based on your data
                                        id='scopus-dropdown-id'
                                    ),
                                ])
                            ], className='mb-0', style={'border': 'red', 'background-color': 'transparent', 'border-radius': '10px'}),
                        ]),

                    ]),
                    dbc.Row([
                        dbc.Col([
                            # DIRECTORY OF OPEN ACCESS (DOAJ)
                            dbc.Card([

                                dbc.CardBody([
                                    html.P('DIRECTORY OF OPEN ACCESS (DOAJ)', style={
                                        'font-family': 'Sans-serif', 'text-align': 'left', 'font-color': 'black', 'font-size': '10px'}),
                                    html.H6(id='selected-doaj', style={
                                        'color': 'red',  'font-weight': 'bold', 'font-size': '12px', 'font-family': 'sans-serif'}),
                                    dcc.Dropdown(
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in selection_options],
                                        value='',  # Set the initial value based on your data
                                        id='doaj-dropdown-id'
                                    ),
                                ])
                            ], className='mb-0', style={'border': 'red', 'background-color': 'transparent', 'border-radius': '10px'}),
                        ]),


                        # OPEN ACCESS JOURNAL
                        dbc.Col([
                            dbc.Card([

                                dbc.CardBody([
                                    html.P('OPEN ACCESS JOURNAL', style={
                                        'font-family': 'Sans-serif', 'text-align': 'left', 'font-color': 'black', 'font-size': '10px'}),
                                    html.H6(id='selected-oaj', style={
                                        'color': 'red',  'font-weight': 'bold', 'font-size': '12px', 'font-family': 'sans-serif'}),
                                    dcc.Dropdown(
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in selection_options],
                                        value='',  # Set the initial value based on your data
                                        id='oaj-dropdown-id'
                                    ),
                                ])
                            ], className='mb-0', style={'border': 'red', 'background-color': 'transparent', 'border-radius': '10px', 'height': '5rem'}),
                        ]),
                    ]),
                    dbc.Row([

                        # Online publisher based in Africa
                        dbc.Col([
                            dbc.Card([

                                dbc.CardBody([
                                    html.P('ONLINE PUBLISHER BASED IN AFRICA', style={
                                        'font-family': 'Sans-serif', 'text-align': 'left', 'font-color': 'black', 'font-size': '10px'}),
                                    html.H6(id='selected-africa', style={
                                        'color': 'red',  'font-weight': 'bold', 'font-size': '12px', 'font-family': 'sans-serif'}),
                                    dcc.Dropdown(
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in selection_options],
                                        value='',  # Set the initial value based on your data
                                        id='africa-dropdown-id'
                                    ),
                                ])
                            ], className='mb-0', style={'border': 'red', 'background-color': 'transparent', 'border-radius': '10px'}),
                        ]),

                        # Hosted on INASP'S Journal online
                        dbc.Col([
                            dbc.Card([

                                dbc.CardBody([
                                    html.P('HOSTED ON INASP\'S JOURNAL ONLINE', style={
                                        'font-family': 'Sans-serif', 'text-align': 'left', 'font-color': 'black', 'font-size': '10px'}),
                                    html.H6(id='selected-inasp', style={
                                        'color': 'red',  'font-weight': 'bold', 'font-size': '12px', 'font-family': 'sans-serif'}),
                                    dcc.Dropdown(
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in selection_options],
                                        value='',  # Set the initial value based on your data
                                        id='inasp-dropdown-id'
                                    ),
                                ])
                            ], className='mb-0', style={'border': 'red', 'background-color': 'transparent', 'border-radius': '10px'}),
                        ]),
                    ]),
                    dbc.Row([

                        # The publisher is a member of Committee on publication Ethics (COPE)
                        dbc.Col([
                            dbc.Card([

                                dbc.CardBody([
                                    html.P('PUBLISHER IS A MEMBER OF COMMITTEE ON PUBLICATION ETHICS (COPE)', style={
                                        'font-family': 'Sans-serif', 'text-align': 'left', 'font-color': 'black', 'font-size': '10px'}),
                                    html.H6(id='selected-cope', style={
                                        'color': 'red',  'font-weight': 'bold', 'font-size': '12px', 'font-family': 'sans-serif'}),
                                    dcc.Dropdown(
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in selection_options],
                                        value='',  # Set the initial value based on your data
                                        id='cope-dropdown-id'
                                    ),
                                ])
                            ], className='mb-0', style={'border': 'red', 'background-color': 'transparent', 'border-radius': '10px'}),
                        ]),
                        dbc.Col([

                            # Present on International Standard Serial Number (ISSN) portal

                            dbc.Card([

                                dbc.CardBody([
                                    html.P('ON INTERNATIONAL STANDARD SERIAL NUMBER (ISSN) PORTAL', style={
                                     'font-family': 'Sans-serif', 'text-align': 'left', 'font-color': 'black', 'font-size': '10px'}),
                                    html.H6(id='selected-issn', style={
                                        'color': 'red',  'font-weight': 'bold', 'font-size': '12px', 'font-family': 'sans-serif'}),
                                    dcc.Dropdown(
                                        options=[{'label': opt, 'value': opt}
                                                 for opt in selection_options],
                                        value='',  # Set the initial value based on your data
                                        id='issn-dropdown-id'
                                    ),
                                ])
                            ], className='mb-0', style={'border': 'red', 'background-color': 'transparent', 'border-radius': '10px'}),

                        ]),
                    ]),

                    dbc.Row([

                        # The publisher is a member of Committee on publication Ethics (COPE)
                        dbc.Col([
                            dbc.Col([
                                dbc.Card([

                                    html.Div([
                                        html.Button('FILTER',
                                                    id='your-button-id', style={'background': '#00ec53', 'border-radius': '10px', 'margin-right': '1rem', 'width': '10rem', 'font-family': 'sans-serif'}),
                                        # Other layout components here
                                        dcc.Store(id='outputs')
                                    ]),
                                ], className='mb-0', style={'border': 'red', 'background-color': 'transparent', 'border-radius': '10px', 'height': '5rem'}),
                            ], style={'text-align': 'end'}),
                        ]),


                    ]),

                ], width=6, style={'height': '10rem'}),



                # OUTPUT
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(
                            'List of journals that met your criteria'),
                        dbc.CardBody(
                            html.Div(
                                id='output',
                                style={
                                    'height': '26rem',
                                    'overflowY': 'auto',
                                    'font-family': 'sans-serif',
                                    'font-size': '11px',
                                    'line-height': '1'
                                }
                            ),
                            style={'text-align': 'left', 'margin-top': '2', 'font-family': 'sans-serif',
                                   'box-shadow': 'rgba(0, 0, 0, 0.3) 0px 19px 38px, rgba(0, 0, 0, 0.22) 0px 15px 12px'}

                        )
                    ], className='mt-2')

                ], width=6, style={'height': '95%', 'border-radius': '10px', 'background': '#d7daff'}),





            ], className='mb-3 mt-0', style={'background-color': '#EFF7FD', 'border-radius': '10px', 'height': '34rem'}),
        ], width=12),

    ], className='mb-2, mt-2'),
    dcc.Store(id='saved-value-store', data={}),
    html.Hr(style={'border-color': 'blue'}),
    html.H2('VISUALIZATION', style={'text-align': 'center'}),

    html.Hr(style={'border-color': '#FF7F00'}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Number of Journals per Country',
                               style={'text-align': 'center'}),
                html.Div(id='countries', style={
                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                    dbc.Spinner(children=[
                             dcc.Graph(id='country-bubble-chart',
                                       style={'height': '70vh'}, config={'displayModeBar': False},
                                       figure={'layout': {'plot_bgcolor': 'lightgray'}})], size="lg", color="success", type="border", fullscreen=False, spinner_style={'width': '6rem', 'height': '6rem'}),
                ])
            ], style={'border': 'none'}),
        ], width=12),

    ], className='mb-2, mt-2'),


    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Number of Journals per Language',
                               style={'text-align': 'center'}),
                html.Div(id='languages', style={
                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                             dcc.Graph(id='languages-bar-chart', figure={}),
                             ])
            ], style={'border': 'none'}),
        ], width=12),

    ], className='mb-2, mt-2'),




    dbc.Row([

        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Journals Indexed on Google Scholar', style={
                               'text-align': 'center'}),
                html.Div(id='gs_plat', style={
                         'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                    dcc.Graph(id='gs-pie-chart', figure={}),
                ])
            ], style={'border': 'none'}),

        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Journals Indexed on Scopus', style={
                               'text-align': 'center'}),
                html.Div(id='scopus_plat', style={
                         'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                    dcc.Graph(id='scopus-pie-chart', figure={}),
                ])
            ], style={'border': 'none'}),

        ], width=6),
    ], className='mb-2, mt-3'),

    dbc.Row([

        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Journals  hosted on INASP\'S Journal Online', style={
                               'text-align': 'center'}),
                html.Div(id='cope_plat', style={
                         'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                    dcc.Graph(id='inasp-column-chart', figure={}),
                ])
            ], style={'border': 'none'}),

        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Journals on International Standard Serial Number (ISSN) Portal       ', style={
                               'text-align': 'center'}),
                html.Div(id='issn_plat', style={
                         'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                    dcc.Graph(id='issn-column-chart', figure={}),
                ])
            ], style={'border': 'none'}),

        ], width=6),
    ], className='mb-2, mt-3'),








    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Journals Listed on African Index Medicus',
                               style={'text-align': 'center'}),
                html.Div(id='medicus', style={
                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                             dcc.Graph(id='medicus-pie-chart', figure={}),
                             ])
            ], style={'border': 'none'}),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Journals Listed on Directory of Open Access Journal (DOAJ)',
                               style={'text-align': 'center'}),
                html.Div(id='doaj_plat', style={
                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                             dcc.Graph(id='doaj-donut-chart', figure={}),
                             ])
            ], style={'border': 'none'}),
        ], width=6),

    ], className='mb-2, mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Number of Journals per Thematic Areas',
                               style={'text-align': 'center'}),
                html.Div(id='thematics', style={
                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                             dcc.Graph(id='thematic-bar-chart', figure={}),
                             ])
            ], style={'border': 'none'}),
        ], width=12),

    ], className='mb-2, mt-2'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Journals Listed on Open Access Journal (OAJ)',
                               style={'text-align': 'center'}),
                html.Div(id='oaj', style={
                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                             dcc.Graph(id='oaj-donut-chart', figure={}),
                             ])
            ], style={'border': 'none'}),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Journals whose online publisher is based in Africa',
                               style={'text-align': 'center'}),
                html.Div(id='publisher_plat', style={
                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                             dcc.Graph(id='publisher-in-africa', figure={}),
                             ])
            ], style={'border': 'none'}),
        ], width=6),

    ], className='mb-2, mt-2'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Journals whose publishers are a members of Committee on Publication Ethics (CoPE)',
                               style={'text-align': 'center'}),
                html.Div(id='language', style={
                    'color': 'darkviolet', 'font-weight': 'bold', 'font-size': '10px', 'text-align': 'center'}),
                dbc.CardBody([
                             dcc.Graph(id='cope-column-chart', figure={}),
                             ])
            ], style={'border': 'none'}),
        ], width=12),

    ], className='mb-2, mt-2'),


], fluid=False)


# Updating selected Journal
@app.callback(
    Output('content-total', 'children'),
    Output('content-platform', 'children'),
    Output(component_id='content-country', component_property='children'),
    Output(component_id='content-publisher_name',
           component_property='children'),
    Output(component_id='content-language', component_property='children'),
    Output(component_id='content-thematic_area',
           component_property='children'),
    Output(component_id='content-africa_index_medicus',
           component_property='children'),
    Output(component_id='content-medline', component_property='children'),
    Output(component_id='content-google-scholar',
           component_property='children'),
    Output(component_id='content-impact_factor',
           component_property='children'),
    Output(component_id='content-scopus', component_property='children'),
    Output(component_id='content-h_index', component_property='children'),
    Output(component_id='content-eigen_factor', component_property='children'),
    Output(component_id='content-eigen_factor_metrix',
           component_property='children'),
    Output(component_id='content-snip', component_property='children'),
    Output(component_id='content-snip_metrix', component_property='children'),
    Output(component_id='content-oaj', component_property='children'),
    Output(component_id='content-doaj', component_property='children'),
    Output(component_id='content-issn', component_property='children'),
    Output(component_id='content-cope', component_property='children'),
    Output(component_id='content-based-in-africa',
           component_property='children'),
    Output(component_id='content-inasp', component_property='children'),
    Output(component_id='selected-journal', component_property='children'),
    Output(component_id='selected-journal2', component_property='children'),

    [Input(component_id='journal-dropdown', component_property='value')]
)
def update_output_div(journal):
    data_copy = data_2.copy()
    df = data_copy.loc[data_copy['Journal tittle'] == journal]
    total = len(data_copy)
    platform = df['Platform']
    country = df['Country']
    publisher_name = df['Publishers Name']
    language = df['Language']
    thematic_area = df['Thematic area']
    africa_index_medicus = df['African Index Medicus']
    medline = df['Medline (Medicine and Health Journals)']
    google_scholar = df['Indexed on Google Scholar']
    impact_factor = df['Impact Factor']
    scopus = df['Scopus']
    h_index = df['H-Index']
    eigen_factor = df['Eigenfactor']
    eigen_factor_metrix = df['Eigenfactor metrix']
    snip = df['Source Normalized Impact per Paper (SNIP)']
    snip_metrix = df['SNIP metrix']
    oaj = df['Open Access Journal']
    doaj = df['Journal listed in the Directory of Open Access (DOAJ)']
    issn = df['Present on International Standard Serial Number (ISSN) portal']
    cope = df['The publisher is a member of Committee on publication Ethics (COPE)']
    based_in_africa = df['Online publisher based in Africa']
    inasp = df['Hosted on INASP\'S Journal online']
    google_scholar = get_lottie(google_scholar)
    scopus = get_lottie(scopus)
    africa_index_medicus = get_lottie(africa_index_medicus)
    eigen_factor = get_lottie(eigen_factor)
    snip = get_lottie(snip)
    oaj = get_lottie(oaj)
    doaj = get_lottie(doaj)
    issn = get_lottie(issn)
    cope = get_lottie(cope)
    based_in_africa = get_lottie(based_in_africa)
    inasp = get_lottie(inasp)
    return total, platform, country, publisher_name, language, thematic_area, africa_index_medicus, medline, google_scholar, impact_factor, scopus, h_index, eigen_factor, eigen_factor_metrix, snip, snip_metrix, oaj, doaj, issn, cope, based_in_africa, inasp, journal, journal


def get_lottie(value):
    if int(value) == 0:

        return (
            Lottie(options=options, width="25px",
                   height="25px", url=no_url, style={'margin-top': '-8px'})
        )
    elif int(value) == 1:
        return (
            Lottie(options=options, width="25px",
                   height="25px", url=yes_url, style={'margin-top': '-8px'})
        )
    else:
        return ''  # Return an empty div if the value is not 0 or 1


# FLITER COUNTRY ------------------------------------------------------------------------------


@app.callback(
    Output('selected-country', 'children'),
    [Input(component_id='country-dropdown-id', component_property='value')],
)
def filter_counrty(value):
    if str(value) == 'None':
        original_values['country'] = ''
    else:
        original_values['country'] = value

    table = display_selected_values(original_values)

    return value

# FILTER LANGUAGE------------------------------------------------------------------------------


@app.callback(
    Output('selected-langauge', 'children'),
    [Input(component_id='language-dropdown-id', component_property='value')],
)
def filter_language(value):
    if str(value) == 'None':
        original_values['language'] = ''
    else:
        original_values['language'] = value

    display_selected_values(original_values)
    table = display_selected_values(original_values)

    return value


# FILTER THEMATIC AREA------------------------------------------------------------------------------


@app.callback(
    Output('selected-thematic_area', 'children'),
    [Input(component_id='thematic_area-dropdown-id', component_property='value')],
)
def filter_thematic_area(value):
    if str(value) == 'None':
        original_values['thematic_area'] = ''
    else:
        original_values['thematic_area'] = value

    display_selected_values(original_values)
    return value

# FILTER GOOGLE SCHOLAR------------------------------------------------------------------------------


@app.callback(
    Output('selected-google_scholar', 'children'),
    [Input(component_id='google_scholar-dropdown-id', component_property='value')],
)
def filter_google_scholar(value):
    if str(value) == 'None':
        original_values['google_scholar'] = ''
    elif value == 'Yes':
        original_values['google_scholar'] = 1
    elif value == 'No':
        original_values['google_scholar'] = 0
    display_selected_values(original_values)
    return value

# FILTER SCOPUS------------------------------------------------------------------------------


@app.callback(
    Output('selected-scopus', 'children'),
    [Input(component_id='scopus-dropdown-id', component_property='value')],
)
def filter_scopus(value):
    if str(value) == 'None':
        original_values['scopus'] = ''
    elif value == 'Yes':
        original_values['scopus'] = 1
    elif value == 'No':
        original_values['scopus'] = 0
    display_selected_values(original_values)
    return value

# FILTER OAJ------------------------------------------------------------------------------


@app.callback(
    Output('selected-oaj', 'children'),
    [Input(component_id='oaj-dropdown-id', component_property='value')],
)
def filter_oaj(value):
    if str(value) == 'None':
        original_values['oaj'] = ''
    elif value == 'Yes':
        original_values['oaj'] = 1
    elif value == 'No':
        original_values['oaj'] = 0
    display_selected_values(original_values)
    return value

# FILTER DOAJ------------------------------------------------------------------------------


@app.callback(
    Output('selected-doaj', 'children'),
    [Input(component_id='doaj-dropdown-id', component_property='value')],
)
def filter_doaj(value):
    if str(value) == 'None':
        original_values['doaj'] = ''
    elif value == 'Yes':
        original_values['doaj'] = 1
    elif value == 'No':
        original_values['doaj'] = 0
    display_selected_values(original_values)
    return value


# FILTER ISSN------------------------------------------------------------------------------


@app.callback(
    Output('selected-issn', 'children'),
    [Input(component_id='issn-dropdown-id', component_property='value')],
)
def filter_issn(value):
    if str(value) == 'None':
        original_values['issn'] = ''
    elif value == 'Yes':
        original_values['issn'] = 1
    elif value == 'No':
        original_values['issn'] = 0
    display_selected_values(original_values)
    return value

# FILTER PIBLISHER BASEED IN AFRICA------------------------------------------------------------------------------


@app.callback(
    Output('selected-africa', 'children'),
    [Input(component_id='africa-dropdown-id', component_property='value')],
)
def filter_publisher_in_africa(value):
    if str(value) == 'None':
        original_values['publisher_in_africa'] = ''
    elif value == 'Yes':
        original_values['publisher_in_africa'] = 1
    elif value == 'No':
        original_values['publisher_in_africa'] = 0
    display_selected_values(original_values)
    return value

# FILTER INASP------------------------------------------------------------------------------


@app.callback(
    Output('selected-inasp', 'children'),
    [Input(component_id='inasp-dropdown-id', component_property='value')],
)
def filter_inasp(value):
    if str(value) == 'None':
        original_values['inasp'] = ''
    elif value == 'Yes':
        original_values['inasp'] = 1
    elif value == 'No':
        original_values['inasp'] = 0
    display_selected_values(original_values)
    return value


# FILTER COPE------------------------------------------------------------------------------


@app.callback(
    Output('selected-cope', 'children'),
    [Input(component_id='cope-dropdown-id', component_property='value')],
)
def filter_cope(value):
    if str(value) == 'None':
        original_values['cope'] = ''
    elif value == 'Yes':
        original_values['cope'] = 1
    elif value == 'No':
        original_values['cope'] = 0
    display_selected_values(original_values)
    return value


def filter_data(platform, google_scholar, scopus, one_platform, oaj, doaj, issn, cope, based_in_africa, inasp):
    df = data.copy()
    final_df = df.loc[(df['Platform'] == platform) & (df['Indexed on Google Scholar'] == google_scholar) & (df['Indexed on Scopus'] == scopus) &
                      (df['Indexed on at least one platform'] == one_platform) & (df['Open Access Journal'] == oaj) &
                      (df['Journal listed in the Directory of Open Access (DOAJ)'] == doaj) & (df['Present on International Standard Serial Number (ISSN) portal'] == issn) &
                      (df['The publisher is a member of Committee on publication Ethics (COPE)'] == cope) & (df['Online publisher based in Africa'] == based_in_africa) &
                      (df['Hosted on INASP\'S Journal online'] == inasp)
                      ]
    return final_df['Journal tittle']


def fil(cols):
    dataf = data.copy()
    if len(cols) > 0:
        for i in cols:
            dataf = dataf.loc[dataf[i] == 1]
            fin_df = pd.DataFrame(dataf, columns=['Journal tittle'])
        return fin_df
    else:
        fin_df = pd.DataFrame(dataf, columns=['Journal tittle'])
        return fin_df


# GOOGLE SCHOLAR PIE CHART ***************************************************************
@app.callback(
    Output('gs-pie-chart', 'figure'),
    Input('selected-thematic_area', 'children'),
)
def google_scholar(ff):
    df = data_2.copy()
    g_yes = len(df[df['Indexed on Google Scholar'] == 1])

    g_no = len(df[df['Indexed on Google Scholar'] == 0])

    g_none = len(df) - g_no - g_yes
    if g_yes > 0:
        google_yes = round(g_yes / (len(df)) * 100, 2)
        google_no = round(g_no / (len(df)) * 100, 2)
        google_none = round(g_none / (len(df)) * 100, 2)
        labels = ['Yes: {} ({:.2f}%)'.format(g_yes, google_yes),
                  'No: {} ({:.2f}%)'.format(g_no, google_no), 'Unknown: {} ({:.2f}%)'.format(g_none, google_none)]
        values = [google_yes, google_no, google_none]
        colors = ['#0FA69E', '#9A1651', '#D1D0D1']

        fig_pie = go.Figure(
            data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
        # Set the desired font size here
        fig_pie.update_traces(textfont_size=20)
        fig_pie.update_layout(title="", template='seaborn',
                              margin=dict(l=20, r=20, t=30, b=20), height=400)
    else:

        # empty piechat
        fig_pie = go.Figure(
            data=[go.Pie(labels=[], values=[], marker=dict(colors=[]), hole=1)])
        fig_pie.update_layout(title="", template='seaborn',
                              margin=dict(l=20, r=20, t=30, b=20))

    return fig_pie


# COUNTRY BUBBLE SCATTER CHART ***************************************************************
@app.callback(
    Output('country-bubble-chart', 'figure'),
    Input('selected-thematic_area', 'children'),
)
def google_scholar(ff):
    df = data_2.copy()
    country_vals = {}
    for country in countries:
        count = len(df[df['Country'] == country])
        country_vals[country] = count
    geolocator = Nominatim(user_agent="my_geocoder")

    lon_list = []
    lat_list = []
    text_list = []
    size_list = []
    color_list = []

    max_value = max(country_vals.values())

    for country, value in country_vals.items():
        location = geolocator.geocode(country)
        if location:
            lon_list.append(location.longitude)
            lat_list.append(location.latitude)
            text_list.append(f"{country}: {value}")
            # Adjust the scaling factor as needed
            scaled_size = (value / max_value) * 200
            size_list.append(scaled_size)
            # size_list.append(value)
            color_list.append(value)

    print('_____________________________________')
    print(lon_list)
    print('*************************')
    print(lat_list)
    print('*************************')
    print(text_list)
    print('*************************')
    print(size_list)
    print('*************************')
    print(color_list)
    print('_____________________________________')

    bubble_map = go.Scattergeo(
        lon=lon_list,
        lat=lat_list,
        text=text_list,
        marker=dict(
            size=size_list,
            sizemode="diameter",
            opacity=0.7,
            colorscale="Viridis",  # Set the colorscale for the marker colors
            cmin=min(color_list),
            cmax=max(color_list),
            color=color_list,  # This should be a single value to map to the colorscale
            colorbar=dict(title="Values"),

        ),
    )

    layout = go.Layout(
        geo=dict(
            scope="africa",
            showland=True,
            # bgcolor='rgba(255, 255, 255, 0.0)',
            bgcolor='lightgray'
        ),
        # title="Bubble Map Example",
    )

    return {"data": [bubble_map], "layout": layout}


# SCOPUS PIE CHART ***************************************************************


@app.callback(
    Output('scopus-pie-chart', 'figure'),
    Input('selected-thematic_area', 'children'),
)
def google_scholar(ff):
    df = data_2.copy()
    g_yes = len(df[df['Scopus'] == 1])

    g_no = len(df[df['Scopus'] == 0])

    g_none = len(df) - g_no - g_yes
    if g_yes > 0:
        google_yes = round(g_yes / (len(df)) * 100, 2)
        google_no = round(g_no / (len(df)) * 100, 2)
        google_none = round(g_none / (len(df)) * 100, 2)
        labels = ['Yes: {} ({:.2f}%)'.format(g_yes, google_yes),
                  'No: {} ({:.2f}%)'.format(g_no, google_no), 'Unknown: {} ({:.2f}%)'.format(g_none, google_none)]
        values = [google_yes, google_no, google_none]
        colors = ['#0FA69E', '#9A1651', '#D1D0D1']

        fig_pie = go.Figure(
            data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
        # Set the desired font size here
        fig_pie.update_traces(textfont_size=20)
        fig_pie.update_layout(title="", template='seaborn',
                              margin=dict(l=20, r=20, t=30, b=20), height=400)
    else:

        # empty piechat
        fig_pie = go.Figure(
            data=[go.Pie(labels=[], values=[], marker=dict(colors=[]), hole=1)])
        fig_pie.update_layout(title="", template='seaborn',
                              margin=dict(l=20, r=20, t=30, b=20))

    return fig_pie


# AFRICAN MEDICUS PIE CHART ***************************************************************


@app.callback(
    Output('medicus-pie-chart', 'figure'),
    Input('selected-thematic_area', 'children'),
)
def google_scholar(ff):
    df = data_2.copy()
    g_yes = len(df[df['African Index Medicus'] == 1])

    g_no = len(df[df['African Index Medicus'] == 0])

    g_none = len(df) - g_no - g_yes
    if g_yes > 0:
        google_yes = round(g_yes / (len(df)) * 100, 2)
        google_no = round(g_no / (len(df)) * 100, 2)
        google_none = round(g_none / (len(df)) * 100, 2)
        labels = ['Yes: {} ({:.2f}%)'.format(g_yes, google_yes),
                  'No: {} ({:.2f}%)'.format(g_no, google_no), 'Unknown: {} ({:.2f}%)'.format(g_none, google_none)]
        values = [google_yes, google_no, google_none]
        colors = ['#019D19', '#D60001', '#D1D0D1']

        fig_pie = go.Figure(
            data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
        # Set the desired font size here
        fig_pie.update_traces(textfont_size=20)
        fig_pie.update_layout(title="", template='seaborn',
                              margin=dict(l=20, r=20, t=30, b=20), height=400)
    else:

        # empty piechat
        fig_pie = go.Figure(
            data=[go.Pie(labels=[], values=[], marker=dict(colors=[]), hole=1)])
        fig_pie.update_layout(title="", template='seaborn',
                              margin=dict(l=20, r=20, t=30, b=20))

    return fig_pie


# DOAJ DONUT GRAPH *****************************************************************


@app.callback(
    Output('doaj-donut-chart', 'figure'),
    Input('selected-thematic_area', 'children'),
)
def doaj(plats):
    df = data_2.copy()
    g_yes = len(
        df[df['Journal listed in the Directory of Open Access (DOAJ)'] == 1])

    g_no = len(
        df[df['Journal listed in the Directory of Open Access (DOAJ)'] == 0])

    g_none = len(df) - g_no - g_yes
    if g_yes > 0:
        google_yes = round(g_yes / (len(df)) * 100, 2)
        google_no = round(g_no / (len(df)) * 100, 2)
        google_none = round(g_none / (len(df)) * 100, 2)
        labels = ['Yes: {} ({:.2f}%)'.format(g_yes, google_yes),
                  'No: {} ({:.2f}%)'.format(g_no, google_no), 'Unknown: {} ({:.2f}%)'.format(g_none, google_none)]
        values = [google_yes, google_no, google_none]
        colors = ['#019D19', '#D60001', '#D1D0D1']

        fig_donut = go.Figure(data=[
            go.Pie(labels=labels, values=values,
                   marker=dict(colors=colors), hole=0.5)
        ])

        # Set the desired font size here
        fig_donut.update_traces(textfont_size=20)
        fig_donut.update_layout(title="", template='seaborn',
                                margin=dict(l=20, r=20, t=30, b=20), height=400)
    else:
        # empty donut chart
        fig_donut = go.Figure(data=[
            go.Pie(labels=[], values=[], marker=dict(colors=[]), hole=0.7)
        ])

        fig_donut.update_layout(title="Listed in the Directory of Open Access (DOAJ)", template='seaborn',
                                margin=dict(l=20, r=20, t=30, b=20))

    return fig_donut

# OAJ DONUT GRAPH *****************************************************************


@app.callback(
    Output('oaj-donut-chart', 'figure'),
    Input('selected-thematic_area', 'children'),
)
def doaj(plats):
    df = data_2.copy()
    g_yes = len(
        df[df['Open Access Journal'] == 1])

    g_no = len(
        df[df['Open Access Journal'] == 0])

    g_none = len(df) - g_no - g_yes
    if g_yes > 0:
        google_yes = round(g_yes / (len(df)) * 100, 2)
        google_no = round(g_no / (len(df)) * 100, 2)
        google_none = round(g_none / (len(df)) * 100, 2)
        labels = ['Yes: {} ({:.2f}%)'.format(g_yes, google_yes),
                  'No: {} ({:.2f}%)'.format(g_no, google_no), 'Unknown: {} ({:.2f}%)'.format(g_none, google_none)]
        values = [google_yes, google_no, google_none]
        colors = ['#372261', '#B35A97', '#D1D0D1']
        # colors = ['#019D19', '#D60001', '#D1D0D1']

        fig_donut = go.Figure(data=[
            go.Pie(labels=labels, values=values,
                   marker=dict(colors=colors), hole=0.5)
        ])

        # Set the desired font size here
        fig_donut.update_traces(textfont_size=20)
        fig_donut.update_layout(title="", template='seaborn',
                                margin=dict(l=20, r=20, t=30, b=20), height=400)
    else:
        # empty donut chart
        fig_donut = go.Figure(data=[
            go.Pie(labels=[], values=[], marker=dict(colors=[]), hole=0.7)
        ])

        fig_donut.update_layout(title="Listed in the Directory of Open Access (DOAJ)", template='seaborn',
                                margin=dict(l=20, r=20, t=30, b=20))

    return fig_donut


# ONLINE PUBLISHER IN AFRICA DONUT GRAPH *****************************************************************


@app.callback(
    Output('publisher-in-africa', 'figure'),
    Input('selected-thematic_area', 'children'),
)
def doaj(plats):
    df = data_2.copy()
    g_yes = len(
        df[df['Online publisher based in Africa'] == 1])

    g_no = len(
        df[df['Online publisher based in Africa'] == 0])

    g_none = len(df) - g_no - g_yes
    if g_yes > 0:
        google_yes = round(g_yes / (len(df)) * 100, 2)
        google_no = round(g_no / (len(df)) * 100, 2)
        google_none = round(g_none / (len(df)) * 100, 2)
        labels = ['Yes: {} ({:.2f}%)'.format(g_yes, google_yes),
                  'No: {} ({:.2f}%)'.format(g_no, google_no), 'Unknown: {} ({:.2f}%)'.format(g_none, google_none)]
        values = [google_yes, google_no, google_none]
        colors = ['#372261', '#B35A97', '#D1D0D1']
        # colors = ['#019D19', '#D60001', '#D1D0D1']

        fig_donut = go.Figure(data=[
            go.Pie(labels=labels, values=values,
                   marker=dict(colors=colors), hole=0.5)
        ])

        # Set the desired font size here
        fig_donut.update_traces(textfont_size=20)
        fig_donut.update_layout(title="", template='seaborn',
                                margin=dict(l=20, r=20, t=30, b=20), height=400)
    else:
        # empty donut chart
        fig_donut = go.Figure(data=[
            go.Pie(labels=[], values=[], marker=dict(colors=[]), hole=0.7)
        ])

        fig_donut.update_layout(title="Listed in the Directory of Open Access (DOAJ)", template='seaborn',
                                margin=dict(l=20, r=20, t=30, b=20))

    return fig_donut


# JOURNALS PER LANGUAGE BAR GRAPH ************************************************************
@app.callback(
    Output('languages-bar-chart', 'figure'),
    Input('selected-thematic_area', 'children'),
)
def platform_bar(plats):
    df = data_2.copy()
    langauges = list(set(df['Language']))
    dfs = []
    for item in languages:
        sub_df = len(df[df['Language'] == item])
        dfs.append(sub_df)
    dff = pd.DataFrame(data=[dfs], columns=langauges)
    # Calculate the total sum of values for percentage calculation
    total_sum = sum(dff.values[0])

    # Calculate the percentages for each value
    percentages = [(value / total_sum) * 100 for value in dff.values[0]]

    # ajol = len(
    #     df[df['Platform'] == 'African Journal Online (AJOL)'])
    # sabinet = len(
    #     df[df['Platform'] == 'SABINET Journal repository'])
    # dff = pd.DataFrame(data=[[ajol, sabinet]], columns=[
    #                    'African Journal Online (AJOL)', 'SABINET Journal repository'])
    colors = ['#0C4F67', '#DD3A9E']
    num_bars = len(dff.columns)
    # You can choose any color scale you prefer
    color_scale = px.colors.qualitative.Set1[:num_bars]

    fig_bar = make_subplots(rows=1, cols=1)
    fig_bar.add_trace(
        go.Bar(y=dff.columns, x=dff.values[0],        text=[f'{value:.0f} ({percentage:.2f}%)' for value, percentage in zip(dff.values[0], percentages)],

               textposition='auto', marker=dict(color=color_scale), orientation='h'),
        row=1, col=1
    )
    fig_bar.update_layout(
        template='seaborn',
        # title='Number of Journals per Platform',
        margin=dict(l=20, r=20, t=30, b=20),
        height=400
    )

    fig_bar.update_xaxes(title_text="Count")
    fig_bar.update_yaxes(title_text="Langauge")

    return fig_bar


# JOURNALS PER ThEMATIC AREA BAR GRAPH ************************************************************
@app.callback(
    Output('thematic-bar-chart', 'figure'),
    Input('selected-thematic_area', 'children'),
)
def platform_bar(plats):
    df = data_2.copy()
    thematic_areas = list(set(df['Thematic area']))
    dfs = []
    for item in thematic_areas:
        sub_df = len(df[df['Thematic area'] == item])
        dfs.append(sub_df)
    dff = pd.DataFrame(data=[dfs], columns=thematic_areas)
    # Calculate the total sum of values for percentage calculation
    total_sum = sum(dff.values[0])

    # Calculate the percentages for each value
    percentages = [(value / total_sum) * 100 for value in dff.values[0]]

    # ajol = len(
    #     df[df['Platform'] == 'African Journal Online (AJOL)'])
    # sabinet = len(
    #     df[df['Platform'] == 'SABINET Journal repository'])
    # dff = pd.DataFrame(data=[[ajol, sabinet]], columns=[
    #                    'African Journal Online (AJOL)', 'SABINET Journal repository'])
    colors = ['#0C4F67', '#DD3A9E']
    num_bars = len(dff.columns)
    # You can choose any color scale you prefer
    color_scale = px.colors.qualitative.Set1[:num_bars]

    fig_bar = make_subplots(rows=1, cols=1)
    fig_bar.add_trace(
        go.Bar(y=dff.columns, x=dff.values[0],        text=[f'{value:.0f} ({percentage:.2f}%)' for value, percentage in zip(dff.values[0], percentages)],

               textposition='auto', marker=dict(color=color_scale), orientation='h'),
        row=1, col=1
    )
    fig_bar.update_layout(
        template='seaborn',
        # title='Number of Journals per Platform',
        margin=dict(l=20, r=20, t=30, b=20),
        height=400
    )

    fig_bar.update_xaxes(title_text="Count")
    fig_bar.update_yaxes(title_text="Thematic Area")

    return fig_bar

# The publisher is a member of Committee on publication Ethics (COPE) *****************************************************************


@app.callback(
    Output('cope-column-chart', 'figure'),
    Input('selected-thematic_area', 'children'),
)
def cope(plats):
    df = data_2.copy()
    g_yes = len(
        df[df['The publisher is a member of Committee on publication Ethics (COPE)'] == 1])
    g_no = len(
        df[df['The publisher is a member of Committee on publication Ethics (COPE)'] == 0])
    g_none = len(df) - g_no - g_yes

    dff = pd.DataFrame(data=[[g_yes, g_no, g_none]],
                       columns=['YES', 'NO', 'Unknown'])

    if g_yes > 0:
        colors = ['#008001', '#AA2120', '#F2C603']

        fig_bar = make_subplots(rows=1, cols=1)

        fig_bar.add_trace(
            go.Bar(y=dff.columns, x=dff.values[0], marker=dict(
                color=colors), text=dff.values[0], textposition='auto', orientation='h'),
            row=1, col=1
        )

        fig_bar.update_layout(
            template='seaborn',
            title='',
            margin=dict(l=20, r=20, t=30, b=20),
            height=200
        )

        fig_bar.update_xaxes(title_text="Count")
        fig_bar.update_yaxes(title_text="")

    else:
        fig_bar = go.Figure()

    return fig_bar

# The Journal hosted on INASP Journal Online *****************************************************************


@app.callback(
    Output('inasp-column-chart', 'figure'),
    Input('selected-thematic_area', 'children'),
)
def cope(plats):
    df = data_2.copy()
    g_yes = len(
        df[df['Hosted on INASP\'S Journal online'] == 1])
    g_no = len(
        df[df['Hosted on INASP\'S Journal online'] == 0])
    g_none = len(df) - g_no - g_yes

    dff = pd.DataFrame(data=[[g_yes, g_no, g_none]],
                       columns=['YES', 'NO', 'Unknown'])

    if g_yes > 0:
        colors = ['#008001', '#AA2120', '#F2C603']

        fig_bar = make_subplots(rows=1, cols=1)

        fig_bar.add_trace(
            go.Bar(y=dff.columns, x=dff.values[0], marker=dict(
                color=colors), text=dff.values[0], textposition='auto', orientation='h'),
            row=1, col=1
        )

        fig_bar.update_layout(
            template='seaborn',
            title='',
            margin=dict(l=20, r=20, t=30, b=20),
            height=200
        )

        fig_bar.update_xaxes(title_text="Count")
        fig_bar.update_yaxes(title_text="")

    else:
        fig_bar = go.Figure()

    return fig_bar


# Present on International Standard Serial Number (ISSN) portal *****************************************************************


@app.callback(
    Output('issn-column-chart', 'figure'),
    Input('selected-thematic_area', 'children'),
)
def cope(plats):
    df = data_2.copy()
    g_yes = len(
        df[df['Present on International Standard Serial Number (ISSN) portal'] == 1])
    g_no = len(
        df[df['Present on International Standard Serial Number (ISSN) portal'] == 0])
    g_none = len(df) - g_no - g_yes

    dff = pd.DataFrame(data=[[g_yes, g_no, g_none]],
                       columns=['YES', 'NO', 'Unknown'])

    if g_yes > 0:
        colors = ['#008001', '#AA2120', '#F2C603']

        fig_bar = make_subplots(rows=1, cols=1)

        fig_bar.add_trace(
            go.Bar(y=dff.columns, x=dff.values[0], marker=dict(
                color=colors), text=dff.values[0], textposition='auto', orientation='h'),
            row=1, col=1
        )

        fig_bar.update_layout(
            template='seaborn',
            title='',
            margin=dict(l=20, r=20, t=30, b=20),
            height=200
        )

        fig_bar.update_xaxes(title_text="Count")
        fig_bar.update_yaxes(title_text="")

    else:
        fig_bar = go.Figure()

    return fig_bar


# DISPLAY OF JOURNALS ON A TABLE BASED ON THE CRITERIA SELETED *****************************************************************

def display_selected_values(values):
    filter_criteria = values
    filtered_data = data_3
    if (filter_criteria['country'] == ''):
        filtered_data = filtered_data
    else:
        filtered_data = filtered_data[(
            filtered_data['country'] == filter_criteria['country'])]

    if (filter_criteria['language'] == ''):
        filtered_data = filtered_data
    else:
        filtered_data = filtered_data[(
            filtered_data['language'] == filter_criteria['language'])]

    if (filter_criteria['thematic_area'] == ''):
        filtered_data = filtered_data
    else:
        filtered_data = filtered_data[(
            filtered_data['thematic_area'] == filter_criteria['thematic_area'])]

    if (filter_criteria['thematic_area'] == ''):
        filtered_data = filtered_data
    else:
        filtered_data = filtered_data[(
            filtered_data['thematic_area'] == filter_criteria['thematic_area'])]

    if (filter_criteria['google_scholar'] == ''):
        filtered_data = filtered_data
    else:
        filtered_data = filtered_data[(
            filtered_data['google_scholar'] == filter_criteria['google_scholar'])]

    if (filter_criteria['scopus'] == ''):
        filtered_data = filtered_data
    else:
        filtered_data = filtered_data[(
            filtered_data['scopus'] == filter_criteria['scopus'])]

    if (filter_criteria['oaj'] == ''):
        filtered_data = filtered_data
    else:
        filtered_data = filtered_data[(
            filtered_data['oaj'] == filter_criteria['oaj'])]

    if (filter_criteria['doaj'] == ''):
        filtered_data = filtered_data
    else:
        filtered_data = filtered_data[(
            filtered_data['doaj'] == filter_criteria['doaj'])]

    if (filter_criteria['issn'] == ''):
        filtered_data = filtered_data
    else:
        filtered_data = filtered_data[(
            filtered_data['issn'] == filter_criteria['issn'])]

    if (filter_criteria['publisher_in_africa'] == ''):
        filtered_data = filtered_data
    else:
        filtered_data = filtered_data[(
            filtered_data['publisher_in_africa'] == filter_criteria['publisher_in_africa'])]

    if (filter_criteria['inasp'] == ''):
        filtered_data = filtered_data
    else:
        filtered_data = filtered_data[(
            filtered_data['inasp'] == filter_criteria['inasp'])]

    if (filter_criteria['cope'] == ''):
        filtered_data = filtered_data
    else:
        filtered_data = filtered_data[(
            filtered_data['cope'] == filter_criteria['cope'])]

    filtered_data['Number'] = range(1, len(filtered_data) + 1)

    # Swap the columns in the DataFrame
    filtered_data = filtered_data[['Number'] +
                                  list(filtered_data.columns[:-1])]

    filtered_data = filtered_data[['Number', 'journal_title']]

    data_table = dash_table.DataTable(
        id='data-table',
        columns=[{"name": col, "id": col} for col in filtered_data.columns],
        data=filtered_data.to_dict('records'),
        style_table={'font-family': 'sans-serif'},
        style_cell_conditional=[
            {'if': {'column_id': 'Date'}, 'textAlign': 'left'},
            {'if': {'column_id': 'Region'}, 'textAlign': 'left'}
        ],
        style_data={
            'color': 'black',
            'backgroundColor': 'white',
            'textAlign': 'left',
            'font-family': 'sans-serif',
        },
        style_data_conditional=[
            {'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)'}
        ],
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold',
            'textAlign': 'left',
            'font-family': 'sans-serif',
        }
    )

    global final_table
    final_table = html.Div(data_table)

    return html.Div(data_table)


@app.callback(
    Output('output', 'children'),
    # Replace 'your-button-id' with the actual ID of your button
    Input('your-button-id', 'n_clicks')
)
def update_data_table(n_clicks):
    global final_table
    if n_clicks is None:
        return dash.no_update
    # Perform any desired updates to final_table here

    return final_table


if __name__ == '__main__':
    app.run_server(debug=False, port=8001)
