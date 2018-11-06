import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc4
import os
#from adcirc import adcirc
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.offline as po
import random
import plotly.graph_objs as go
from IPython.display import HTML
import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import folium
def libs():
    import numpy as np
    import matplotlib.pyplot as plt
    import netCDF4 as nc4
    import os
    from adcirc import adcirc
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    import plotly.offline as po
    import random
    import plotly.graph_objs as go
    from IPython.display import HTML
    import pandas as pd
    import plotly.graph_objs as go
    return np,plt,nc4,os,adcirc,download_plotlyjs, init_notebook_mode, plot, iplot,po,go,HTML,pd,go

def files(root,root2):
    stations = [{'Duck':'https://tidesandcurrents.noaa.gov/api/datagetter?product=hourly_height&application=NOS.COOPS.TAC.WL&begin_date=20030827&end_date=20030927&datum=MSL&station=8651370&time_zone=GMT&units=metric&format=csv','Duck2':'https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=20030828&end_date=20030927&datum=MSL&station=8651370&time_zone=GMT&units=metric&interval=h&format=csv',
             'Ocean City':'https://tidesandcurrents.noaa.gov/api/datagetter?product=hourly_height&application=NOS.COOPS.TAC.WL&begin_date=20030827&end_date=20030927&datum=MSL&station=8570283&time_zone=GMT&units=metric&format=csv','Ocean City2':'https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date=20030828&end_date=20030927&datum=MSL&station=8570283&time_zone=GMT&units=metric&interval=h&format=csv'
            }]
    file_t = os.path.join(root2,'true\\fort.63.nc')
    file4  = os.path.join(root2,'week4\\fort.63.nc')
    file3  = os.path.join(root2,'week3\\fort.63.nc')
    file2  = os.path.join(root2,'week2\\fort.63.nc')
    file1  = os.path.join(root2,'week1\\fort.63.nc')
    tidal4  = os.path.join(root,'tidal\\week4\\fort.63.nc')
    tidal3  = os.path.join(root,'tidal\\week3\\fort.63.nc')
    tidal2  = os.path.join(root,'tidal\\week2\\fort.63.nc')
    tidal1  = os.path.join(root,'tidal\\week1\\fort.63.nc')
    start4 = '20030827 00:00:00'
    start3 = '20030903 00:00:00'
    start2 = '20030910 00:00:00'
    start1 = '20030917 00:00:00'
    files = [file_t,file4,file3,file2,file1]
    tidal = [tidal4,tidal4,tidal3,tidal2,tidal1]
    start = [start4,start4,start3,start2,start1]
    nodes = [26642,26720] # duck, ocean city
    name = ['Control','Week 4','Week 3','week 2','week 1','Observation']
    return files,tidal,start,nodes,name,stations

def sub_tidal2surge(files,nodes,start,name,tidal):
    data = []
    for f in range(0,len(files)):
        wl  = nc4.Dataset(tidal[f])
        wl = wl['zeta'][:,nodes[0]]
        wl = pd.DataFrame(wl)
        tidal_dt=pd.date_range(start=start[f],periods=int(len(wl)),freq='1H')
        wl.insert(0,'Date Time',tidal_dt)
        wl=wl.rename(columns={0:' Water Level'})
        nc_file = nc4.Dataset(files[f])
        water_level = nc_file['zeta'][:,nodes]
        water_level = pd.DataFrame(water_level)
        date_time = pd.date_range(start=start[f],periods=int(len(water_level)),freq='1H')
        water_level.insert(0,'Date Time',date_time)
        water_level=water_level.rename(columns={0:' Water Level'})
        c_list = ['rgba(51, 204, 51)','rgba(0, 255, 204)',
                  'rgba(0, 204, 255)','rgba(102, 255, 255)',
                  'rgba(0, 102, 153)','rgba(0, 0, 255)',
                  'rgba(51, 51, 255)','rgba(102, 0, 255)',
                  'rgba(153, 153, 255)','rgba(204, 0, 255)',
                  'rgba(255, 51, 204)','rgba(204, 0, 0)',
                  'rgba(255, 153, 0)','rgba(204, 255, 51)',
                  'rgba(0, 153, 0)']
        for x in range(1):
                y=random.randint(1,14)
                color = c_list[y]
        surge = pd.DataFrame()
        surge.insert(0,'Date Time',date_time)
        surge.insert(1,' Water Level',np.zeros(len(water_level)))
        if len(wl)>len(water_level):
            for ii in range(len(water_level[' Water Level'])):
                if water_level['Date Time'][ii]==wl['Date Time'][ii]:
                    surge[' Water Level'][ii] = abs(water_level[' Water Level'][ii]) - abs(wl[' Water Level'][ii])
                if water_level[' Water Level'][ii]<0 or surge[' Water Level'][ii]<0:
                    surge[' Water Level'][ii] = 0
        else:
            for ii in range(len(wl[' Water Level'])):
                if water_level[' Water Level'][ii]<0 or surge[' Water Level'][ii]<0:
                    surge[' Water Level'][ii] = 0
                if water_level['Date Time'][ii]==wl['Date Time'][ii]:
                    surge[' Water Level'][ii] = abs(water_level[' Water Level'][ii]) - abs(wl[' Water Level'][ii])

        surge[' Water Level'].iloc[surge[' Water Level'].values<np.max(surge[' Water Level'].values)]=0

        trace = go.Scatter(x =surge['Date Time'],y =surge[' Water Level'],
                    name = name[f],mode = 'lines',
                    line = dict(
                        color = (color)))
        data.append(trace)
    return data




def surge(files,nodes,start,name):
    data = []
    for f in range(0,len(files)):
        nc_file = nc4.Dataset(files[f])
        water_level = nc_file['zeta'][:,nodes[0]]
        water_level = pd.DataFrame(water_level)
        date_time = pd.date_range(start=start[f],periods=int(len(water_level)),freq='1H')
        water_level.insert(0,'Date Time',date_time)
        water_level=water_level.rename(columns={0:' Water Level'})
        c_list = ['rgba(51, 204, 51)','rgba(0, 255, 204)',
                  'rgba(0, 204, 255)','rgba(102, 255, 255)',
                  'rgba(0, 102, 153)','rgba(0, 0, 255)',
                  'rgba(51, 51, 255)','rgba(102, 0, 255)',
                  'rgba(153, 153, 255)','rgba(204, 0, 255)',
                  'rgba(255, 51, 204)','rgba(204, 0, 0)',
                  'rgba(255, 153, 0)','rgba(204, 255, 51)',
                  'rgba(0, 153, 0)']
        for x in range(1):
                y=random.randint(1,14)
                color = c_list[y]
        trace = go.Scatter(x = water_level['Date Time'],y = water_level[' Water Level'],
                    name = name[f],mode = 'lines',
                    line = dict(
                        color = (color)))
        data.append(trace)
    return data
    

def timeseries(nc_data,start,noaa_start,freq,station,name):
    data = nc_data['zeta'][:,station]#106378]
    table = pd.DataFrame(data)
    date  = pd.date_range(start=start,periods=int(len(table)),freq=freq)
    table.insert(0,'Date Time',date)
    table = table.rename(columns={0:name})
    return table

def plot_timeseries(files,start,noaa_start,end,station,name,nodes):
    data = []
    pred = pd.read_csv('https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date='+noaa_start+'&end_date='+end+'&datum=MSL&station='+station+'&time_zone=GMT&units=metric&interval=h&format=csv')
    obs  = pd.read_csv('https://tidesandcurrents.noaa.gov/api/datagetter?product=hourly_height&application=NOS.COOPS.TAC.WL&begin_date='+noaa_start+'&end_date='+end+'&datum=MSL&station='+station+'&time_zone=GMT&units=metric&format=csv')
    for f in range(0,len(files)):
        nc_file = nc4.Dataset(files[f])
        water_level = nc_file['zeta'][:,nodes]
        water_level = pd.DataFrame(water_level)
        date_time = pd.date_range(start=start[f],periods=int(len(water_level)),freq='1H')
        water_level.insert(0,'Date Time',date_time)
        water_level=water_level.rename(columns={0:' Water Level'})
        
        c_list = ['rgba(51, 204, 51)','rgba(0, 255, 204)',
                  'rgba(0, 204, 255)','rgba(102, 255, 255)',
                  'rgba(0, 102, 153)','rgba(0, 0, 255)',
                  'rgba(51, 51, 255)','rgba(102, 0, 255)',
                  'rgba(153, 153, 255)','rgba(204, 0, 255)',
                  'rgba(255, 51, 204)','rgba(204, 0, 0)',
                  'rgba(255, 153, 0)','rgba(204, 255, 51)',
                  'rgba(0, 153, 0)']
        for x in range(1):
            y=random.randint(1,14)
            color = c_list[y]
        
        for i3 in range(0,len(water_level)):
            if  water_level[' Water Level'][i3]<0:
                water_level[' Water Level'][i3]=0
        water_level = water_level.set_index(pd.DatetimeIndex(water_level['Date Time']))
        trace = go.Scatter(x = water_level['Date Time']['2003-09-07 00:00:00':'2003-09-21 00:00:00'],y = water_level[' Water Level']['2003-09-07 00:00:00':'2003-09-21 00:00:00'],
                    name = name[f],mode = 'lines',
                    line = dict(
                        color = (color)))
        data.append(trace)
   # trace2 = go.Scatter(x = pred['Date Time'],y = pred[' Prediction'],
   #                 name = 'NOAA Prediction',mode = 'lines',
   #                 line = dict(
   #                     color = ('rgb(100, 100, 153)')))
    obs = obs.set_index(pd.DatetimeIndex(obs['Date Time']))
    pred = pred.set_index(pd.DatetimeIndex(pred['Date Time']))
    trace3 = go.Scatter(x = obs['Date Time']['2003-09-07 00:00:00':'2003-09-21 00:00:00'],y = obs[' Water Level']['2003-09-07 00:00:00':'2003-09-21 00:00:00']-pred[' Prediction']['2003-09-07 00:00:00':'2003-09-21 00:00:00'],
                    name = 'NOAA Observation',mode = 'lines',
                    line = dict(
                        color = ('rgb(100, 100, 53)')))
    data.append(trace3)
    return data

def layout(title,xaxis,yaxis):
    layout = go.Layout(dict(title=title),xaxis = dict(title = xaxis),
                   yaxis = dict(title = yaxis),legend= dict(orientation="h"),
                   font = dict(color = 'rgb(0,0,0)'),paper_bgcolor = 'rgb(255,255,255)',
                   plot_bgcolor = 'rgb(255,255,255)')
    return layout



def plot_timeseries2(files,start,name,nodes,noaa_start,end,station):
    data = []
    pred = pd.read_csv('https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date='+noaa_start+'&end_date='+end+'&datum=MSL&station='+station+'&time_zone=GMT&units=metric&interval=h&format=csv')
    obs  = pd.read_csv('https://tidesandcurrents.noaa.gov/api/datagetter?product=hourly_height&application=NOS.COOPS.TAC.WL&begin_date='+noaa_start+'&end_date='+end+'&datum=MSL&station='+station+'&time_zone=GMT&units=metric&format=csv')

    for f in range(0,len(files)):
        nc_file = nc4.Dataset(files[f])
        water_level = nc_file['zeta'][:,nodes]
        water_level = pd.DataFrame(water_level)
        date_time = pd.date_range(start=start[f],periods=int(len(water_level)),freq='1H')
        water_level.insert(0,'Date Time',date_time)
        water_level=water_level.rename(columns={0:' Water Level'})
        
        c_list = ['rgba(51, 204, 51)','rgba(0, 255, 204)',
                  'rgba(0, 204, 255)','rgba(102, 255, 255)',
                  'rgba(0, 102, 153)','rgba(0, 0, 255)',
                  'rgba(51, 51, 255)','rgba(102, 0, 255)',
                  'rgba(153, 153, 255)','rgba(204, 0, 255)',
                  'rgba(255, 51, 204)','rgba(204, 0, 0)',
                  'rgba(255, 153, 0)','rgba(204, 255, 51)',
                  'rgba(0, 153, 0)']
        for x in range(1):
            y=random.randint(1,14)
            color = c_list[y]
        
        for i3 in range(0,len(water_level)):
            if  water_level[' Water Level'][i3]<0:
                water_level[' Water Level'][i3]=0
        water_level = water_level.set_index(pd.DatetimeIndex(water_level['Date Time']))
        storm_begin = '2003-09-10 00:00:00'
        storm_end = '2003-09-24 00:00:00'
        trace = go.Scatter(x = water_level['Date Time'][storm_begin:storm_end],y = water_level[' Water Level'][storm_begin:storm_end],
                    name = name[f],mode = 'lines',
                    line = dict(
                        color = (color)))
        data.append(trace)
    #trace2 = go.Scatter(x = pred['Date Time'],y = pred[' Prediction'],name = 'NOAA Prediction',mode = 'lines',line = dict(color = ('rgb(100, 100, 153)')))
    obs = obs.set_index(pd.DatetimeIndex(obs['Date Time']))
    pred = pred.set_index(pd.DatetimeIndex(pred['Date Time']))
    trace3 = go.Scatter(x = obs['Date Time'][storm_begin:storm_end],y = obs[' Water Level'][storm_begin:storm_end]-pred[' Prediction'][storm_begin:storm_end],
                    name = 'NOAA Observation',mode = 'lines',
                    line = dict(
                        color = ('rgb(100, 100, 53)')))
    data.append(trace3)
    return data

def layout(title,xaxis,yaxis):
    layout = go.Layout(dict(title=title),xaxis = dict(title = xaxis),
                   yaxis = dict(title = yaxis),legend= dict(orientation="h"),
                   font = dict(color = 'rgb(0,0,0)'),paper_bgcolor = 'rgb(255,255,255)',
                   plot_bgcolor = 'rgb(255,255,255)')
    return layout

def metric(files,week,start,nodes):
    peak=[]
    for f in range(0,len(files)):
        true = nc4.Dataset(files[0])
        nc_file = nc4.Dataset(files[f])
        true_data = true['zeta'][:,nodes]
        water_level = nc_file['zeta'][:,nodes]
        true_data = pd.DataFrame(true_data)
        water_level = pd.DataFrame(water_level)
        date_time = pd.date_range(start=start[f],periods=int(len(water_level)),freq='1H')
        dt_true = pd.date_range(start=start[0],periods=int(len(true_data)),freq='1H')
        true_data.insert(0,'Date Time',dt_true)
        true_data=true_data.rename(columns={0:' Water Level'})
        water_level.insert(0,'Date Time',date_time)
        water_level=water_level.rename(columns={0:' Water Level'})

        c_list = ['rgba(51, 204, 51)','rgba(0, 255, 204)',
                  'rgba(0, 204, 255)','rgba(102, 255, 255)',
                  'rgba(0, 102, 153)','rgba(0, 0, 255)',
                  'rgba(51, 51, 255)','rgba(102, 0, 255)',
                  'rgba(153, 153, 255)','rgba(204, 0, 255)',
                  'rgba(255, 51, 204)','rgba(204, 0, 0)',
                  'rgba(255, 153, 0)','rgba(204, 255, 51)',
                  'rgba(0, 153, 0)']
        for x in range(1):
            y=random.randint(1,14)
            color = c_list[y]
        for i3 in range(0,len(water_level)):
            if  water_level[' Water Level'][i3]<0:
                water_level[' Water Level'][i3]=0
        true_data = true_data.set_index(pd.DatetimeIndex(true_data['Date Time']))
        water_level = water_level.set_index(pd.DatetimeIndex(water_level['Date Time']))
        storm_begin = '2003-09-10 00:00:00'
        storm_end = '2003-09-24 00:00:00'    
        peak.append(np.max(water_level[' Water Level'][storm_begin:storm_end])-np.max(true_data[' Water Level'][storm_begin:storm_end]))
    trace = go.Scatter(x = week[1:],y = peak[1:],
            mode = 'markers',
            line = dict(
                color = (color)))
    data=[trace]  
    return data

def ec_map():
    url_base = 'http://server.arcgisonline.com/ArcGIS/rest/services/'
    service = 'World_Imagery/MapServer/tile/{z}/{y}/{x}'
    tileset = url_base + service
    m = folium.Map(width=500,height=500,location=[37.5, -75], zoom_start=6,control_scale = True, tiles="Stamen Toner", attr='USGS style')
    folium.Marker(
        location=[36.2, -75.756],
        popup='NOAA Tide Station Duck NC',
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

    folium.Marker(
        location=[37.6, -75.6],
        popup='NOAA Tide Station Wachapreague VA',
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    folium.Marker(
        location=[38.3, -75.08],
        popup='NOAA Tide Station Ocean City MD',
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    folium.Marker(
        location=[39.3, -74.4],
        popup='NOAA Tide Station Altantic City NJ',
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    folium.Marker(
        location=[38.8, -75.14],
        popup='NOAA Tide Station Lewes, DE',
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    return m


def noaa_surge(station,start,end):
    data = []
    pred = pd.read_csv('https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date='+start+'&end_date='+end+'&datum=MSL&station='+station+'&time_zone=GMT&units=metric&interval=h&format=csv')
    obs  = pd.read_csv('https://tidesandcurrents.noaa.gov/api/datagetter?product=hourly_height&application=NOS.COOPS.TAC.WL&begin_date='+start+'&end_date='+end+'&datum=MSL&station='+station+'&time_zone=GMT&units=metric&format=csv')
    storm_begin = '2003-09-10 00:00:00'
    storm_end = '2003-09-24 00:00:00'
    obs = obs.set_index(pd.DatetimeIndex(obs['Date Time']))
    pred = pred.set_index(pd.DatetimeIndex(pred['Date Time']))
    trace = go.Scatter(x = obs['Date Time'][storm_begin:storm_end],y = obs[' Water Level'][storm_begin:storm_end]-pred[' Prediction'][storm_begin:storm_end],
                    name = 'NOAA Observation',mode = 'lines',
                    line = dict(
                        color = ('rgb(100, 100, 53)')))
    data = [trace]
    return data

