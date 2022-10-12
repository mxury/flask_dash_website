from dash import Dash, dcc, html, Input, Output
import pandas as pd
from application.dash.utility_funs import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import dash_bootstrap_components as dbc


def create_dashboard(server):
    slider_dict = {**{k: f'{k}am - {k + 1}am' for k in range(1, 11, 3)},
                   **{k + 12: f'{k}pm - {k + 1}pm' for k in range(1, 11, 3)}}

    journey_data = pd.read_pickle('./data/journey_data.pkl')

    first_date = journey_data['StartDate'].min()
    last_date = journey_data['EndDate'].max()
    last_7days = last_date - pd.Timedelta('7d')

    if last_7days < first_date:
        last_7days = first_date

    first_date = first_date.strftime('%Y-%m-%d')
    last_date = last_date.strftime('%Y-%m-%d')
    last_7days = last_7days.strftime('%Y-%m-%d')

    bootstrap_css = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css"

    dash_app = Dash(server=server,
                    routes_pathname_prefix='/dash/',
                    external_stylesheets=[bootstrap_css, './application/assets/temp.css'],
                    title='Boris Bike Journeys',
                    )

    with open('./application/templates/dash_layout.html', 'r') as fp:
        index_layout = fp.read()

    dash_app.index_string = index_layout

    tab_station = dbc.Tab(label='Explore journeys by station',
                          id='tab-stations',
                          children=[
                              dbc.Row(
                                  className="d-flex justify-content-center py-3",
                                  children=
                                  [
                                      dbc.Col(
                                          className="col-8 text-center color-primary",
                                          children=
                                          [
                                              html.P(
                                                  """
                                                  While there are over 300 Santander bike stations in London, a 
                                                  few of them dwarf the others when it comes to how many people use
                                                   them. In this tab we can explore the most popular start and end 
                                                   stations. First choose the dates you would like to explore and 
                                                   then choose the granularity of the data you want to consider. 
                                                   Have fun!
                                                  """
                                              )
                                          ]
                                      )
                                  ]
                              ),
                              html.Br(),
                              dbc.Row(
                                  className="d-flex justify-content-evenly",
                                  children=
                                  [
                                      dbc.Col(
                                          className="col-3",
                                          children=
                                          [
                                              dbc.Card(
                                                  className="",
                                                  children=
                                                  [
                                                      dbc.CardHeader('Date range', className="text-center"),
                                                      dbc.CardBody(
                                                          dcc.DatePickerRange(
                                                              id='date-picker-range',
                                                              min_date_allowed=first_date,
                                                              max_date_allowed=last_date,
                                                              start_date=last_7days,
                                                              end_date=last_date,
                                                              minimum_nights=0,
                                                              display_format="DD/MM/YY"),
                                                          className="text-center"
                                                      ),
                                                  ]
                                              ),
                                          ]
                                      ),
                                      dbc.Col(
                                          className="col-5 d-flex justify-content-center",
                                          children=
                                          [
                                              dbc.Card(
                                                  [
                                                      dbc.CardHeader('''Explore station data by choosing the 
                                                                      granularity of it'''),
                                                      dbc.CardBody(
                                                          dcc.Dropdown(
                                                              ['Include all journeys',
                                                               'Filter by hour of the day',
                                                               'Weekdays',
                                                               'Weekends'],
                                                              'Include all journeys',
                                                              id='station-granularity-dropdown',
                                                              clearable=False,
                                                          ),
                                                          className="text-center",
                                                      )
                                                  ]
                                              ),
                                          ],
                                      ),
                                  ]
                              ),
                              html.Br(),
                              dbc.Row(
                                  [
                                      dbc.Col(
                                          width=12, lg=6,
                                          children= dcc.Graph(id="start_graph"),
                                      ),
                                      dbc.Col(
                                          width=12, lg=6,
                                          children=dcc.Graph(id='end_graph'),
                                      ),
                                  ]
                              ),
                              dbc.Row(
                                  dbc.Col(
                                      html.P('Choose hour of the journeys'),
                                      width={'size': 6, 'offset': 5},
                                  ),
                                  id='slider-row-text'
                              ),
                              dbc.Row(
                                  dbc.Col(
                                      dcc.Slider(0, 24, 1,
                                                 value=12,
                                                 id='my_slider',
                                                 marks=slider_dict,
                                                 included=False,
                                                 tooltip={"placement": "top",
                                                          "always_visible": True}
                                                 ),
                                      width={'size': 8, 'offset': 2},
                                  ),
                                  id='slider-row',
                              ),
                          ]
                          )

    tab_journeys = dbc.Tab(label='Explore time series of journeys',
                           id='journeys-trend',
                           children=[
                               dbc.Row(
                                   className="d-flex justify-content-center p-lg-3",
                                   children=
                                   [
                                       dbc.Col(
                                           className="col-lg-8 col-xs-12 text-center",
                                           children=
                                           [
                                               html.P(
                                                   """In this tab we can explore larger cycling trends in London. There
                                                   are two graphs provided allowing for comparison between different 
                                                   dates, and a choice of granularity of which the data is averaged. 
                                                   Have fun!"""
                                               )
                                           ]
                                       )
                                   ]
                               ),
                               dbc.Row(
                                   className="p-lg-3 d-flex justify-content-md-center",
                                   children=
                                   [
                                       dbc.Col(
                                           className="col-3",
                                           children=
                                           [
                                               dbc.Card(
                                                   className="",
                                                   children=
                                                   [
                                                       dbc.CardHeader('Explore', className="text-center"),
                                                       dbc.CardBody(
                                                           className="text-center",
                                                           children=
                                                           [
                                                               dcc.Dropdown(['Total Journeys', 'Weekly Time Series',
                                                                             'Average over x-Days'],
                                                                            'Total Journeys',
                                                                            id='time-series-options',
                                                                            clearable=False,
                                                                            ),
                                                           ]
                                                       )
                                                   ]
                                               ),
                                           ]
                                       ),
                                   ],
                               ),
                               dbc.Row(html.Br()),
                               dbc.Row(
                                   className="d-flex justify-content-center",
                                   id='x-Days-row',
                                   children=
                                   [
                                       dbc.Col(
                                           className="col-2 text-right",
                                           id='x-Days-col1',
                                           children=
                                           [
                                               html.P('For a weekly frequency type in "7" etc.')
                                           ]
                                       ),
                                       dbc.Col(
                                           className="col-2",
                                           id='x-Days-col2',
                                           children=
                                           [
                                               dcc.Input(
                                                   id='x-Days-input',
                                                   type='number',
                                                   placeholder='Number of days',
                                                   min=1, value=2,
                                                   debounce=True,
                                               ),
                                           ]
                                       ),
                                   ],
                               ),
                               dbc.Row(
                                   [
                                       dbc.Col(
                                           [
                                               dbc.Row(dbc.Col(
                                                   dcc.DatePickerRange(
                                                       id='date-picker-time-series1',
                                                       min_date_allowed=first_date,
                                                       max_date_allowed=last_date,
                                                       start_date=last_7days,
                                                       end_date=last_date,
                                                       minimum_nights=0,
                                                       display_format="DD/MM/YY",
                                                   ),
                                                   width={'size': 5, 'offset': 3},
                                               )),
                                               dbc.Row(dbc.Col(id='time-series-graph-1')),
                                           ],
                                           width=12,
                                           lg=6,
                                       ),
                                       dbc.Col(
                                           [
                                               dbc.Row(
                                                   [
                                                       dbc.Col(
                                                           dcc.DatePickerRange(
                                                               id='date-picker-time-series2',
                                                               min_date_allowed=first_date,
                                                               max_date_allowed=last_date,
                                                               start_date=last_7days,
                                                               end_date=last_date,
                                                               minimum_nights=0,
                                                               display_format="DD/MM/YY",
                                                           ),
                                                           width={'size': 5, 'offset': 3},
                                                       ),
                                                   ]
                                               ),
                                               dbc.Row(dbc.Col(id='time-series-graph-2')),
                                           ],
                                           width=12,
                                           lg=6,
                                       ),
                                   ]
                               ),
                           ]
                           )

    dash_app.layout = dbc.Container(
        [
            html.Section(className="pt-5 text-center container",
                         children=
                         [
                             dbc.Row(class_name="pt-lg-2",
                                     children=dbc.Col(class_name="col-lg-8 col-md-8 mx-auto", children=[
                                         html.H1('Visualising Boris Bike Journeys', className="fw-light"),
                                         html.P(className="text-muted", children=
                                         """Santander (Boris) bikes are a major part of the Transport for 
                                                       London network. This dashboard made with Dash and 
                                                       dash-bootstrap-components provides a visualisation of the larger
                                                       trends in journeys across time and stations.  
                                                       """)]
                                                      ))
                         ]
                         ),
            html.Section(className="", children=
            [
                dbc.Row(dbc.Col(
                    class_name="col-12",
                    children=dbc.Tabs(
                        [tab_station, tab_journeys],
                        id='journey-tabs',
                        class_name='nav nav-tab justify-content-center',
                    )
                ),
                    class_name="d-flex justify-content-center"
                ),
                # storing the journey data frame in the user's browser session to save computation time when the user changes
                # granularity and other further options
                # maybe just maybe not really needed, given it's just filtering the data
                dcc.Store(id='date-filter-store'),
                html.P('Powered by TfL Open Data.'),
                html.P('Contains: OS data (c) Crown copyright and database rights 2016, and Geomni UK '
                       'Map data (c) and database rights [2019].'),
            ],
                         style={'margin': 100},
                         )
        ],
        fluid=True,
    )

    init_callbacks(dash_app)
    return dash_app.server


def init_callbacks(dash_app):
    """Initiaties callbacks"""

    journey_data = pd.read_pickle('./data/journey_data.pkl')

    @dash_app.callback(
        Output('slider-row', 'style'),
        Output('slider-row-text', 'style'),
        Input('station-granularity-dropdown', 'value')
    )
    def render_hr_granularity_statin(option):
        if option == 'Filter by hour of the day':
            return {'display': 'block'}, {'display': 'block'}
        else:
            return {'display': 'none'}, {'display': 'none'}

    # @dash_app.callback(
    # Output('date-filter-store', 'data'),
    #     Input('date-picker-range', 'start_date'),
    #     Input('date-picker-range', 'end_date'),
    # )
    # def select_date(start_date, end_date):
    #     filtered_df = journey_data[(journey_data['StartDate'] >= pd.Timestamp(start_date))
    #                                & (journey_data['EndDate'] <= pd.Timestamp(end_date))]
    #     return filtered_df.to_json(orient='split')

    @dash_app.callback(
        Output("start_graph", "figure"),
        Output("end_graph", "figure"),
        Input("my_slider", "value"),
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('station-granularity-dropdown', 'value'),
    )
    def render_station_maps(hours, start_date, end_date, option):
        if option == 'Filter by hour of the day':
            apply_columns = {'BikeId': 'count', 'Duration': 'mean'}
            # these have to be functions so that I can get the hour of the day functionality
            # as I am unable to see how I can get it by using pd.Grouper which only allows for frequencies, i.e.
            # would only give me the hour of that particular day
            start_cols = lambda x: [x['StartStationId'], x['StartDate'].dt.hour]
            end_cols = lambda x: [x['EndStationId'], x['EndDate'].dt.hour]

            df_start = filter_journey_data(journey_data, start_date, end_date, start_cols, apply_columns, hours)
            df_end = filter_journey_data(journey_data, start_date, end_date, end_cols, apply_columns, hours)
            return create_journey_maps(df_start, df_end)

        elif option == 'Include all journeys':
            apply_columns = {'BikeId': 'count', 'Duration': 'mean'}
            start_cols = lambda x: [x['StartStationId']]
            end_cols = lambda x: [x['EndStationId']]

            df_start = filter_journey_data(journey_data, start_date, end_date, start_cols, apply_columns)
            df_end = filter_journey_data(journey_data, start_date, end_date, end_cols, apply_columns)
            return create_journey_maps(df_start, df_end)

        elif option == 'Weekends':
            apply_columns = {'BikeId': 'count', 'Duration': 'mean'}
            start_cols = lambda x: [x['StartStationId']]
            end_cols = lambda x: [x['EndStationId']]

            journey_weekday_start = journey_data[(journey_data['StartDate'].dt.weekday == 5) |
                                                 (journey_data['StartDate'].dt.weekday == 6)]
            journey_weekday_end = journey_data[(journey_data['EndDate'].dt.weekday == 5) |
                                               (journey_data['EndDate'].dt.weekday == 6)]

            df_start = filter_journey_data(journey_weekday_start, start_date, end_date, start_cols, apply_columns)
            df_end = filter_journey_data(journey_weekday_end, start_date, end_date, end_cols, apply_columns)

            return create_journey_maps(df_start, df_end)

        elif option == 'Weekdays':
            apply_columns = {'BikeId': 'count', 'Duration': 'mean'}
            start_cols = lambda x: [x['StartStationId']]
            end_cols = lambda x: [x['EndStationId']]

            journey_weekday_start = journey_data[(journey_data['StartDate'].dt.weekday < 5)]
            journey_weekday_end = journey_data[(journey_data['EndDate'].dt.weekday < 5)]

            df_start = filter_journey_data(journey_weekday_start, start_date, end_date, start_cols, apply_columns)
            df_end = filter_journey_data(journey_weekday_end, start_date, end_date, end_cols, apply_columns)

            return create_journey_maps(df_start, df_end)

    @dash_app.callback(
        Output('x-Days-col1', 'style'),
        Output('x-Days-col2', 'style'),
        Input('time-series-options', 'value')
    )
    def toggle_xdays_input(option):
        if option == 'Average over x-Days':
            return {'display': 'block'}, {'display': 'block'}
        else:
            return {'display': 'none'}, {'display': 'none'},

    def render_time_series_results(option, start_date, end_date, days):
        if start_date == end_date:
            return html.H1('Please select at least two days in order to view the trend!')

        if option == 'Total Journeys':
            apply_columns = {'BikeId': 'count', 'Duration': 'mean'}
            grouped_cols = lambda x: [pd.Grouper(key='StartDate', freq='1D')]
            filtered_df = filter_journey_data(journey_data, start_date, end_date, grouped_cols, apply_columns)
            fig = create_line_graphs(filtered_df)
            return dcc.Graph(figure=fig)

        elif option == 'Weekly Time Series':
            apply_columns = {'BikeId': 'count', 'Duration': 'mean'}
            grouped_cols = lambda x: [x['StartDate'].dt.dayofweek]
            filtered_df = filter_journey_data(journey_data, start_date, end_date, grouped_cols, apply_columns)
            daysofweek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            fig = create_line_graphs(filtered_df, daysofweek)
            return dcc.Graph(figure=fig)

        elif option == 'Average over x-Days':
            apply_columns = {'BikeId': 'count', 'Duration': 'mean'}
            grouped_cols = lambda x: [pd.Grouper(key='StartDate', freq=f'{days}D')]
            filtered_df = filter_journey_data(journey_data, start_date, end_date, grouped_cols, apply_columns)
            fig = create_line_graphs(filtered_df)
            return dcc.Graph(figure=fig)

    @dash_app.callback(
        Output('time-series-graph-1', 'children'),
        Input('time-series-options', 'value'),
        Input('date-picker-time-series1', 'start_date'),
        Input('date-picker-time-series1', 'end_date'),
        Input('x-Days-input', 'value'),
    )
    def time_series_graph1(option, start_date, end_date, days):
        return render_time_series_results(option, start_date, end_date, days)

    @dash_app.callback(
        Output('time-series-graph-2', 'children'),
        Input('time-series-options', 'value'),
        Input('date-picker-time-series2', 'start_date'),
        Input('date-picker-time-series2', 'end_date'),
        Input('x-Days-input', 'value'),
    )
    def time_series_graph2(option, start_date, end_date, days):
        return render_time_series_results(option, start_date, end_date, days)

# if __name__ == "__main__":
#     app.run_server(debug=True)
