import plotly.express as px
import plotly.graph_objects as go
import numpy as np

import pandas as pd


def county_drought(df, name):
    d = df.loc[(df['County'] == name)]
    d['any_drought'] = d[['D1','D2','D3','D4', 'County']].sum(axis=1)
    return d

wa_county_tot_dry = pd.read_csv('data/drought_wa_county_cat_per.csv')
wa_county_tot_dry['MapDate'] = pd.to_datetime(wa_county_tot_dry['MapDate'], format='%Y%m%d')
wa_county_tot_dry.set_index('MapDate', inplace=True)

#top 5 agrarian counties in WA, according to 2017 USDA Census of Agriculture State Profile for WA

yakima_drought = county_drought(wa_county_tot_dry, 'Yakima County') #1.8 mil acres of farmland
whitman_drought = county_drought(wa_county_tot_dry, 'Whitman County') #1.3 mil acres of farmland
okanogan_drought = county_drought(wa_county_tot_dry, 'Okanogan County') #1.23 mil acres of farmland
lincoln_drought = county_drought(wa_county_tot_dry, 'Lincoln County') #1.2 mil acres of farmland
grant_drought = county_drought(wa_county_tot_dry, 'Grant County') #1 mil acres of farmland


def group_year_plot(df, plot=False):
    d = df.groupby('Year')['Value'].sum()
    d = d[1:]

    if plot == True:
        d.plot(figsize=(15,15))
        #return d
    else:
        return d
    
def strip_clean(df, overwrite=False, file_path=''):
    df = df.loc[(df['State'] == 'WASHINGTON')]
    df = clean_val_col(df)
    if overwrite == True:
        df.to_csv(file_path)
    return df


def clean_val_col(df):
    
    df = df.replace(np.NaN, 0)
    df['Value'] = df['Value'].str.replace(',', '')
    df['Value'] = df['Value'].str.replace('(', '')
    df['Value'] = df['Value'].str.replace(')', '')
    df['Value'] = df['Value'].str.replace('D', '')
    df['Value'] = df['Value'].str.replace('Z', '')
    df['Value'] = df['Value'].str.replace(' ', '')
    df.loc[(df['Value'] == '')] = 0
    df['Value'] = df['Value'].astype(int)
    return df



def plot_any_drought(df):
    fig = (px.line(df, x=df.index, y='any_drought', 
               labels={'any_drought' :'Percent of Land in D1-D4'}, title=f'Percent of {df.County[1]} with Drought (Any Severity)',
              range_x=['2000-01-01','2020-01-01'])
      )
    return fig

def mean_drought_time(df, time_scale):
    #given a dataframe indexed by a datetime object, returns a df of average drought levels for given time scale
    return df.groupby(time_scale)[['None', 'D0', 'D1', 'D2', 'D3', 'D4']].mean()

def plot_dry_levels_month(df, name):
    # credit to https://plotly.com/python/line-charts/ for example code
    
    df_month = mean_drought_time(df, df.index.month)
    
    df_month.reset_index(inplace=True)
    
    df_month['MapDate'] = pd.to_datetime(df_month['MapDate'], format='%m').dt.month_name()
    
    fig = go.Figure()
    #fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Create and style traces
    
#     fig.add_trace(go.Scatter(x=df.index, y=df['None'], name='Normal',
#                              line=dict(
#                                  #color='firebrick', 
#                                  width=4), fill='tonexty'))
    fig.add_trace(go.Scatter(x=df_month['MapDate'], y=df['D0'], name = 'Dryness',
                             line=dict(
                                 #color='royalblue', 
                                 width=4), fill='tonexty'))
    fig.add_trace(go.Scatter(x=df_month['MapDate'], y=df['D1'], name='D1',
                             line=dict(
                                 #color='firebrick', 
                                 width=4), fill='tonexty')) # dash options include 'dash', 'dot', and 'dashdot'
    
    fig.add_trace(go.Scatter(x=df_month['MapDate'], y=df['D2'], name = 'D2',
                             line = dict(
                                 #color='royalblue', 
                                 width=4), fill='tonexty'))
    fig.add_trace(go.Scatter(x=df_month['MapDate'], y=df['D3'], name = 'D3',
                             line = dict(
                                 #color='firebrick', 
                                 width=4), fill='tonexty'))
    fig.add_trace(go.Scatter(x=df_month['MapDate'], y=df['D4'], name = 'D4',
                             line=dict(
                                 #color='royalblue', 
                                 width=4 
                                      ), fill='tonexty'))

    # Edit the layout
    fig.update_layout(title=f'{name} County: Average Dryness (2000-2020)',
                       xaxis_title=f'Month',
                       yaxis_title='Percent of Land')
    return fig


def trace(df, f):
    
    f.add_trace(
        go.Scatter(x=df.index, y=df['D1'], name="D1", fill='tonexty'),
        #secondary_y=False, 

    )

    f.add_trace(
        go.Scatter(x=df.index, y=df['D2'], name="D2", fill='tonexty'),
        #secondary_y=False
    )


    f.add_trace(
        go.Scatter(x=df.index, y=df['D3'], name="D3", fill='tonexty'),
        #secondary_y=False
    )

    f.add_trace(
        go.Scatter(x=df.index, y=df['D4'], name="D4", fill='tonexty'),
        #secondary_y=False
    )

#     f.add_trace(
#         go.Scatter(x=grant_drought.index, y=grant_drought[level], name="Grant", fill='tonexty'),
#         #secondary_y=False
#     )
    return f
    
def county_plot_year_mean(df, name):
    
    year_mean_df = mean_drought_time(df, df.index.year)
    
    fig = go.Figure()

    
    fig = trace(year_mean_df, fig)
#     fig = trace(df, fig, 'D2')
#     fig = trace(df, fig, 'D3')
#     fig = trace(df, fig, 'D4')
    
    
    
    fig.update_layout(
        title_text=f"{name} County: Year Average Drought"
    )

    fig.update_xaxes(title_text="Year")

    fig.update_yaxes(title_text="<b>Percent of Land</b>")
    #fig.update_yaxes(title_text="<b>Whitman</b> County", secondary_y=True)

    fig.update_traces(marker=dict(size=12,
                                  line=dict(width=2,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    
    
    # Add range slider

    fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
    )


    return fig
    

def county_plot_drought(level):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=yakima_drought.index, y=yakima_drought[level], name="Yakima", fill='tonexty'),
        #secondary_y=False, 

    )

    fig.add_trace(
        go.Scatter(x=whitman_drought.index, y=whitman_drought[level], name="Whitman", fill='tonexty'),
        #secondary_y=False
    )


    fig.add_trace(
        go.Scatter(x=okanogan_drought.index, y=okanogan_drought[level], name="Okanogan", fill='tonexty'),
        #secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=lincoln_drought.index, y=lincoln_drought[level], name="Lincoln", fill='tonexty'),
        #secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=grant_drought.index, y=grant_drought[level], name="Grant", fill='tonexty'),
        #secondary_y=False
    )
    lev_s = level
    if level == 'any_drought':
        lev_s = 'Any Drought'
    if level == 'None':
        lev_s = 'Normal Conditions'
    if level == 'D0':
        lev_s = 'Dry But No Drought'

    
    
    fig.update_layout(
        title_text=f"Yakima, Whitman, Okanogan, Lincoln, Grant: {lev_s}"
    )

    fig.update_xaxes(title_text="Year")

    fig.update_yaxes(title_text="<b>Percent of Land</b>")
    #fig.update_yaxes(title_text="<b>Whitman</b> County", secondary_y=True)

    fig.update_traces(marker=dict(size=12,
                                  line=dict(width=2,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    
    
    # Add range slider

    fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
    )


    return fig



