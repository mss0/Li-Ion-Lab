import pandas as pd
import numpy as np
import scipy, matplotlib
import matplotlib.pyplot as plt
from math import log
from datetime import datetime
from scipy.optimize import curve_fit

def timecode_to_seconds(timecode, framerate):

    '''
    Converts the timecode given as minutes:seconds:frames into seconds
    '''

    if type(timecode) != str:
        timecode = timecode.strftime('%H:%M:%S')
    timecode = timecode.split(':')
    time = int(timecode[0]) * 60 + int(timecode[1]) + int(timecode[2]) / framerate 
    return time

framerate = 29.97

mode = 'thick_discharge' # choose which process to study

data_path = mode.split('_')
data_path = './data/'+ data_path[0] + ' ' + data_path[1] + '.xlsx'

# one may limit the data range if they wish to remove outliers
inf = 1000
start_index = {'thick_discharge': 3,
               'thick_charge': 0,
               'thin_discharge': 0,
               'thin_charge': 0}
stop_index = {'thick_discharge': inf,
              'thick_charge' : 69,
              'thin_discharge' : inf,
              'thin_charge' : inf}

data = pd.read_excel(data_path)
data = data[['timecode', 'current']]
data = data.iloc[start_index[mode] : stop_index[mode]]

data['time'] = data['timecode'].apply(timecode_to_seconds, args=[framerate])
data['log_current'] = data['current'].map(lambda x: log(x))
data['log_time'] = data['time'].map(lambda x: log(x))
start_time = data.at[start_index[mode], 'time']
# set the start time of the measurements as 0
data['time'] = data['time'].map(lambda x: x - start_time)

# curve fitting model 1
t_data = data['time'].to_numpy()
I_data = data['current'].to_numpy()

def model(I, b1, b2):
    return b1 + b2 / I

popt, pcov = curve_fit(model, I_data, t_data)
b1_fit, b2_fit = popt

I_fit = np.linspace(min(I_data), max(I_data), 200)
t_fit = model(I_fit, b1_fit, b2_fit)

plt.scatter(t_data, I_data, label="Data", color="red")
plt.plot(t_fit, I_fit, label="Fit", color="blue")
plt.xlabel("Time")
plt.ylabel("Current")
plt.legend()
plt.show()

# plotting raw
fig = data.plot(x='time', y='current', kind='scatter')
fig.set_xlabel('Time')
fig.set_ylabel('Current')
plt.show()

# plotting exponential decay attempt
fig = data.plot(x='time', y='log_current', kind='scatter')
fig.set_xlabel('Time')
fig.set_ylabel('ln(Current)')
plt.show()

# plotting peukert attempt
fig = data.plot(x='log_time', y='log_current', kind='scatter')
fig.set_xlabel('ln(Time)')
fig.set_ylabel('ln(Current)')
plt.show()
