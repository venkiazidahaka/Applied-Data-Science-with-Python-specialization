
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]
    
    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[9]:

import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker

import pandas as pd
import numpy as np

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df1 = df

df1['Date'] = pd.to_datetime(df1['Date'])
df1['Y'] = df1['Date'].dt.year
df1['M_D'] = df1['Date'].dt.strftime('%m-%d')

df1 = df1[df1['M_D']!='02-29']

df1['Data_Value'] = df1['Data_Value']*0.1

TMX = df1[(df1.Y >= 2005) & (df1.Y <= 2014) & (df1['Element'] == 'TMAX')].groupby(['M_D'])['Data_Value'].max()
TMN = df1[(df1.Y >= 2005) & (df1.Y <= 2014) & (df1['Element'] == 'TMIN')].groupby(['M_D'])['Data_Value'].min()

df1 = df1.merge(TMX.reset_index(drop=False).rename(columns={'Data_Value':'max_temp'}), on='M_D', how='left')
df1 = df1.merge(TMN.reset_index(drop=False).rename(columns={'Data_Value':'min_temp'}), on='M_D', how='left')

HIGHEST_TMX = df1[(df1.Y==2015)&(df1.Data_Value > df1.max_temp)]
LOWEST_TMN = df1[(df1.Y==2015)&(df1.Data_Value < df1.min_temp)]

dates1 = np.arange('2015-01-01','2016-01-01', dtype='datetime64[D]')

plt.figure()

plt.plot(dates1,TMX,color='crimson', linewidth=1) 
plt.plot(dates1,TMN,color='skyblue', linewidth=1)

plt.scatter(HIGHEST_TMX.Date.values, HIGHEST_TMX.Data_Value.values, color='purple', s=8)
plt.scatter(LOWEST_TMN.Date.values, LOWEST_TMN.Data_Value.values, color='green', s=8)

x_axis = plt.gca()
x_axis.axis(['2015/01/01','2015/12/31',-60,60])

plt.xlabel('Date', fontsize=10)
plt.ylabel('degree Celsius', fontsize=10)
plt.title('Temperature in Ann Arbour, Michigan, United States (2005-2015)', fontsize=12)

plt.legend(['Record high (2005-2014)','Record low (2005-2014)','Record broken high in 2015','Record broken low in 2015'],loc=0,frameon=False)

x_axis.fill_between(dates1, TMX, TMN, facecolor='grey', alpha=0.25)
x_axis.xaxis.set_major_locator(dates.MonthLocator())
x_axis.xaxis.set_minor_locator(dates.MonthLocator(bymonthday=15)) 
x_axis.xaxis.set_major_formatter(ticker.NullFormatter())
x_axis.xaxis.set_minor_formatter(dates.DateFormatter('%b'))

for tick in x_axis.xaxis.get_minor_ticks():
    tick.tick1line.set_markersize(0) 
    tick.label1.set_horizontalalignment('center')
    
plt.show()    
plt.savefig('Assignment_2.png')


# In[ ]:




# In[ ]:



