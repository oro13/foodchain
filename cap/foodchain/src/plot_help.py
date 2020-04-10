import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from src.dw import *


def plot_any_drought(df):
    fig = (px.line(df, x=df.index, y='any_drought', 
               labels={'any_drought' :'Percent of Land in D1-D4'}, title=f'Percent of {df.County[1]} with Drought (Any Severity)',
              range_x=['2000-01-01','2020-01-01'])
      )
    return fig

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
    
    return fig
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

def county_crop_helper(df, df_county, county_name, title, y_label):
    df2 = df.loc[df['County'] == county_name]
    try:
        df['Value'] = df['Value'].str.replace('(|)|,|V| ', '').astype(int)
    except:
        pass

    fig = county_crop_plot(df_county, df2, title, y_label)
    
    return fig
    
def county_crop_plot(df1, df2, title, y_label):

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=df1.index, y=df1['D1'], name="D1", fill='tonexty'),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df1.index, y=df1['D2'], name="D2", fill='tonexty'),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=df1.index, y=df1['D3'], name="D3", fill='tonexty'),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=df1.index, y=df1['D4'], name="D4", fill='tonexty'),
        secondary_y=False,
    )

    # Add crop data
    fig.add_trace(
        go.Scatter(x=df2.Year, y=df2['Value'], name=f"{title}", 
                  line = dict(dash='dot')),
        secondary_y=True,
        )

    # Set x-axis title
    fig.update_xaxes(title_text="Year")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Percent Land in Drought</b>", secondary_y=False)
    fig.update_yaxes(title_text=f"<b>{y_label}</b>", secondary_y=True)
    
    fig.update_layout(xaxis_range=['2000-01-01','2007-01-01'],
                  title_text=f"{title} in {df1['County'][0]}"
                     )

    fig.update_xaxes(rangeslider_visible=True)
    
    return fig

# def county_2crop_plot(df1, df2, df3, title, y_label):

#     # Create figure with secondary y-axis
#     fig = make_subplots(specs=[[{"secondary_y": True}]])

#     # Add traces
#     fig.add_trace(
#         go.Scatter(x=df1.index, y=df1['D1'], name="D1", fill='tonexty'),
#         secondary_y=False,
#     )
#     fig.add_trace(
#         go.Scatter(x=df1.index, y=df1['D2'], name="D2", fill='tonexty'),
#         secondary_y=False,
#     )
#     fig.add_trace(
#         go.Scatter(x=df1.index, y=df1['D3'], name="D3", fill='tonexty'),
#         secondary_y=False,
#     )
    
#     fig.add_trace(
#         go.Scatter(x=df1.index, y=df1['D4'], name="D4", fill='tonexty'),
#         secondary_y=False,
#     )

#     # Add crop data
#     fig.add_trace(
#         go.Scatter(x=df2.Year, y=df2['Value'], name="Wheat Irr", 
#                   line = dict(dash='dot')),
#         secondary_y=True,
#         )
#         # Add crop data
#     fig.add_trace(
#         go.Scatter(x=df3.Year, y=df3['Value'], name="Wheat Not Irr", 
#                   line = dict(dash='dot')),
#         secondary_y=True,
#         )
    
                                                                                                              

#     # Set x-axis title
#     fig.update_xaxes(title_text="Year")

#     # Set y-axes titles
#     fig.update_yaxes(title_text="<b>Percent Land in Drought</b>", secondary_y=False)
#     fig.update_yaxes(title_text=f"<b>{y_label}</b>", secondary_y=True)
    
#     fig.update_layout(xaxis_range=['2000-01-01','2007-01-01'],
#                   title_text=f"{title} in {df1['County'][0]}"
#                      )

#     fig.update_xaxes(rangeslider_visible=True)
    
#     fig.show()

