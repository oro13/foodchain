# data wrangling helper functions

import numpy as np
import pandas as pd
#import src.plot_help
pd.options.mode.chained_assignment = None #Supress false positive warning when declaring the county dataframes

#import all county drought data and clean
wa_county_tot_dry = pd.read_csv('data/drought_wa_county_cat_per.csv')
wa_county_tot_dry['MapDate'] = pd.to_datetime(wa_county_tot_dry['MapDate'], format='%Y%m%d')
wa_county_tot_dry.set_index('MapDate', inplace=True)

# creates any_drought column, a sum of all drought percentages
def county_drought(df, name):
    d = df.loc[(df['County'] == name)]
    d['any_drought'] = d[['D1','D2','D3','D4', 'County']].sum(axis=1)
    return d

# split into groups by county
#top 5 agrarian counties in WA, according to 2017 USDA Census of Agriculture State Profile for WA
yakima_drought = county_drought(wa_county_tot_dry, 'Yakima County') #1.8 mil acres of farmland
whitman_drought = county_drought(wa_county_tot_dry, 'Whitman County') #1.3 mil acres of farmland
okanogan_drought = county_drought(wa_county_tot_dry, 'Okanogan County') #1.23 mil acres of farmland
lincoln_drought = county_drought(wa_county_tot_dry, 'Lincoln County') #1.2 mil acres of farmland
grant_drought = county_drought(wa_county_tot_dry, 'Grant County') #1 mil acres of farmland

d1 = pd.read_csv('data/wa_4_week_d1.csv')
d2 = pd.read_csv('data/wa_4_week_d2.csv')
d3 = pd.read_csv('data/wa_4_week_d3.csv')

wheat_yield = pd.read_csv('data/wheat_yield.csv')
wheat_yield_not_irr = pd.read_csv('data/wheat_yield_not_irr.csv')
wheat_yield_irr = pd.read_csv('data/wheat_yield_irr.csv')


def year_drought_describe(county_drought):
    df = county_drought.copy()
    df.reset_index(inplace=True)
    df['Year'] = pd.DatetimeIndex(df['MapDate']).year
    df = df.groupby(['Year']).mean()
    df.reset_index(inplace=True)
    return df[['D0', 'D1', 'D2', 'D3', 'D4']].describe()
    
def wheat_describe(name):
    return wheat_yield.loc[wheat_yield['County'] == name]['Value'].describe()


# # groups county df by year and sums drought percentages
# def group_year_plot(df, plot=False):
#     d = df.groupby('Year')['Value'].sum()
#     d = d[1:]

#     if plot == True:
#         d.plot(figsize=(15,15))

#     return d

# # sums value for crop data
# def strip_clean(df, overwrite=False, file_path=''):
#     #df_new = df.loc[(df['State'] == 'WASHINGTON')]
#     df_new = clean_val_col(df)
#     if overwrite == True:
#         df.to_csv(file_path)
#     return df_new

# # cleans colum for crop data
# def clean_val_col(df):
    
#     df_new = df.replace(np.NaN, 0)
#     df_new['Value'] = df_new['Value'].str.replace([',','(', ')'], '')
#     #df['Value'] = df['Value'].str.replace('(', '')
#     #df['Value'] = df['Value'].str.replace(')', '')
#     df_new['Value'] = df_new['Value'].str.replace('D', '')
#     df_new['Value'] = df_new['Value'].str.replace('Z', '')
#     df_new['Value'] = df_new['Value'].str.replace(' ', '')
#     df_new.loc[(df_new['Value'] == '')] = 0
#     df_new['Value'] = df_new['Value'].astype(int)
#     return df_new


# finds the mean drought per month of given county
def mean_drought_time(df, time_scale):
    #given a dataframe indexed by a datetime object, returns a df of average drought levels for given time scale
    return df.groupby(time_scale)[['None', 'D0', 'D1', 'D2', 'D3', 'D4']].mean()



