import plotly.express as px
import plotly.graph_objects as go
import numpy as np

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


def county_drought(df, name):
    d = df.loc[(df['County'] == name)]
    d['any_drought'] = d[['D1','D2','D3','D4', 'County']].sum(axis=1)
    return d


def plot_any_drought(df):
    fig = (px.line(df, x=df.index, y='any_drought', 
               labels={'any_drought' :'Percent of Land in D1-D4'}, title=f'Percent of {df.County[1]} with Drought (Any Severity)',
              range_x=['2000-01-01','2020-01-01'])
      )
    return fig

def mean_drought_time(df, time_scale):
    #given a dataframe indexed by a datetime object, returns a df of average drought levels for given time scale
    return df.groupby(time_scale)[['None', 'D0', 'D1', 'D2', 'D3', 'D4']].mean()

def plot_dry_levels(df, name, time_scale):
    # credit to https://plotly.com/python/line-charts/ for example code
    
    fig = go.Figure()
    #fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Create and style traces
    fig.add_trace(go.Scatter(x=df.index, y=df['None'], name='Normal',
                             line=dict(color='firebrick', width=4)))
    fig.add_trace(go.Scatter(x=df.index, y=df['D0'], name = 'Dryness',
                             line=dict(color='royalblue', width=4)))
    fig.add_trace(go.Scatter(x=df.index, y=df['D1'], name='D1',
                             line=dict(color='firebrick', width=4,
                                  dash='dash') # dash options include 'dash', 'dot', and 'dashdot'
    ))
    fig.add_trace(go.Scatter(x=df.index, y=df['D2'], name = 'D2',
                             line = dict(color='royalblue', width=4, dash='dash')))
    fig.add_trace(go.Scatter(x=df.index, y=df['D3'], name = 'D3',
                             line = dict(color='firebrick', width=4, dash='dot')))
    fig.add_trace(go.Scatter(x=df.index, y=df['D4'], name = 'D4',
                             line=dict(color='royalblue', width=4, dash='dot')))

    # Edit the layout
    fig.update_layout(title=f'{name} County Average Dryness Per {time_scale}',
                       xaxis_title=f'{time_scale}',
                       yaxis_title='Dryness Level')
    return fig

