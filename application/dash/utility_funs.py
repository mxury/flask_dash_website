import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

station_data = pd.read_pickle('./data/station_data.pkl')


def merge_id_coord(df, stations_df):
    return df.merge(stations_df, how='inner', left_index=True, right_index=True)


def topNstations(df, n=25):
    column = df.columns[0]
    return df.nlargest(n, column)


def create_map(df, title):
    """
    Creates a mapbox plot given a dataframe and it's title.
    :param df: Pandas dataframe, must include longitude and latitude params.
    :param title: Title of the map figure
    :return: plotly express scatter mapbox object
    """
    if 'start' in title.lower():
        df.rename(columns={'BikeId': 'Number of bikes rented'}, inplace=True)
    # elif 'EndStationId' in df.index.names:
    elif 'end' in title.lower():
        df.rename(columns={'BikeId': '# of bikes docked'}, inplace=True)

    df['Mean duration [min]'] = df['Duration'] / 60
    token = open("./application/dash/keys/mapbox.key").read()
    px.set_mapbox_access_token(token)

    fig = px.scatter_mapbox(df, lat="lat", lon="lon", color=df.columns[0],
                            color_continuous_scale='bluered', size_max=20, zoom=10.9,
                            hover_name=df['Station Name'],
                            hover_data={
                                'lat': False,
                                'lon': False,
                                df.columns[0]: True,
                                'Mean duration [min]': ':.2f',
                            },
                            )

    fig.update_layout(title={'text': title,
                             'x': 0.4,
                             })
    fig.update_layout(
        margin=dict(l=30, r=30, t=40, b=20),
    )

    return fig


def create_journey_maps(df_start_grouped, df_end_grouped):
    df_start = topNstations(merge_id_coord(df_start_grouped, station_data))

    df_end = topNstations(merge_id_coord(df_end_grouped, station_data))

    fig_start = create_map(df_start, 'Most popular start stations')
    fig_start.update_layout(transition_duration=500)

    fig_end = create_map(df_end, 'Most popular end stations')
    fig_end.update_layout(transition_duration=500)

    return fig_start, fig_end

## not used at the moment
def select_hour_of_day(df, hr, station='StartStationId', point='StartDate'):
    filt_df = df.groupby([station, df[point].dt.hour])['Duration'].count().unstack().fillna(0).loc[:, [hr]]

    rental_action = {'StartStationId': 'rented', 'EndStationId': 'docked'}
    filt_df.columns = [f'Number of bikes {rental_action[station]}']

    return filt_df


def filter_journey_data(journey_df, start_date, end_date, grouped_cols_fun, apply_cols, granularity=slice(None)):
    # the end date from the Dash date picker gives the first minute of that day, i.e. for 15-04-2018 we'd have
    # end_date = '00:00 15-04-2018', in reality we want end_date = '23:59 15-04-2018' hence the need for the addition
    # pd.Timedelta('1D')
    df = journey_df[(journey_df['StartDate'] >= pd.Timestamp(start_date))
                      & (journey_df['EndDate'] < (pd.Timestamp(end_date) + pd.Timedelta('1D')))]
    grouped_cols = grouped_cols_fun(df)
    filtered_df = \
        df.groupby(grouped_cols).agg(apply_cols).fillna(0)
    if len(grouped_cols) > 1:
        return filtered_df.xs(granularity, level=1, drop_level=True)
    else:
        return filtered_df


def create_line_graphs(df, xaxis_markers=None):

    df['Duration'] = df['Duration'] / 60

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=df.index, y=df['BikeId'], name='Journeys',
                   hovertemplate='Number of rentals on %{x}: %{y}',
                   marker=dict(color='#1c452e')),
        secondary_y=False,
    )

    fig.update_yaxes(
        title='Number of journeys',
        titlefont=dict(
            color="#1c452e"
        ),
        secondary_y=False,
    )

    if len(df.columns) > 1:
        fig.add_trace(
            go.Scatter(x=df.index, y=df['Duration'],
                       marker=dict(color='#add6ab'),
                       # name='Cycle duration',
                       hovertemplate='Mean trip duration on %{x}: %{y:.2f}mins',
                       ),
            secondary_y=True,
        )
        fig.update_yaxes(
            title='Average duration of rental [min]',
            titlefont=dict(
                color='#add6ab'
            ),
            secondary_y=True,
        )

    if xaxis_markers is not None:
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(7)),
                ticktext=xaxis_markers,
            )
        )

    fig.update_layout(
        margin=dict(l=30, r=30, t=40, b=20),
    )

    fig.update_layout(
        xaxis_title='Date',
        showlegend=False,
    )

    return fig
