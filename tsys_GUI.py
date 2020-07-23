import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import PySimpleGUI as sg
#import time

################ Functions #################

# Creates Tsys array Y
def create_Y(file_dir, name) :

    #Reads file name and splits
    f = open(file_dir,'r')
    textFile = f.read()
    data = textFile.split('\n')

    line = 0
    #find the selected station
    for i in range(len(data)):
        if name in data[i] :
            break
        line = line+1

    #Removes redundant lines
    data = data[line:]
    antal = int(data[0][-6:])
    data = data[2:-2]
    data[0] = data[0][-7:]

    #Finds number och channels and number of measurements
    chan_num = 0
    for i in range(len(data)):
        if " 2 " in data[i] :
            break
        chan_num = chan_num+1

    # Reads data and puts in to 2D array by channel
    Y = np.zeros((antal,chan_num))
    for i in range(len(data)):
        temp = data[i].split(" ")
        if i == (antal)*chan_num:
            break 
        for l in range(len(temp)):
            if temp[l].find('.') != -1:
                
                tempf = float(temp[l])
                Y[i//chan_num][i-i//chan_num*chan_num] = tempf

    return [Y,antal, chan_num]
        
# Creates X array for elevation and azimuth
def X_el_az(f, name,chan_num, antal):

    #Reads file
    f_el = open(f,'r')
    el_textFile = f_el.read()
    data_el = el_textFile.split('\n')

    # Finds the selected station
    line = 0
    for i in range(len(data_el)):
        if name in data_el[i] :
            break
        line = line+1

    # Removes reduntant lines
    data_el = data_el[line:]
    data_el = data_el[2:-2]

    data_el[0] = data_el[0][-7:]

    #Reads data and puts in t array
    X = np.zeros(antal)
    k = 0
    for i in range(len(data_el)):
        temp = data_el[i].split("   ")
        if k == antal :
            break
        if (i% 2) == 0:
            for l in range(len(temp)):
                if temp[l].find('.') != -1:
                    tempf = float(temp[l])
                    X[k] = tempf
                    k = k+1
    return X

# Creates t array for time
def X_time(f, name,chan_num, antal):

    # open and read file
    f = open(f,'r')
    textFile = f.read()
    data = textFile.split('\n')

    #find the selected station
    line = 0
    for i in range(len(data)):
        if name in data[i] :
            break

        line = line+1
    
    # Remove redundant lines
    data = data[line:]
    data = data[2:-2]

    #Puts data into t array
    X = np.zeros(antal)
    for i in range(len(data)):
        if i == antal :
            break
        data[i] = data[i][-35:]
        temp = data[i].split('  ')
        X[i] = float(temp[0])*24*3600+ float(temp[1])*3600+ float(temp[2])*60+float(temp[4])
    
    #Set first measurement as time 0
    X = X- X[0]
    return X

# Reads frequency channels
def freq(f,name, chan_num):
    #open and reads file
    f = open(f,'r')
    textFile = f.read()

    #Splits into string list
    data = textFile.split('\n')

    #Find given station
    line = 0
    for i in range(len(data)):
        if name in data[i] :
            break
        line = line+1

    data = data[line+2:]

    S = []
    X = []
    #Checks if the frequency is above or below 4000
    for i in range(len(data)):
        temp = data[i].split(" ")
        if i == chan_num :
            break
        for l in range(len(temp)):
            if temp[l].find('.') != -1:
                    tempf = float(temp[l])
                    if tempf > 4000:
                        X = i
                    else :
                        S= i
    return [S,X]


##########################################################################################
 
# Opens file 

file_dir = '/home/ugne/Documents/NVI/dmp_mult/Tsys_mult.dmp'
f = open(file_dir,'r')
textFile = f.read()
data = textFile.split('\n')

# finds all the stations in file dir 
# Should be not to difficult to make it only one loop
s_name = []
for i in range(len(data)):
     if 'BEGIN STATION' in data[i] :
         s_name.append(i)

s_real_name = []
for i in range(len(s_name)):
    temp = data[s_name[i]].split('#')
    s_real_name.append(temp[0][14:])
    
# Creates window for input 
sg.theme('DarkAmber') 
lines = [[sg.CB('', key=x), sg.T(s_real_name[x])] for x in range(len(s_real_name))]
form = sg.FlexForm('files')

layout = [[
    sg.Frame('Pick stations',[*lines
           ]), 
    sg.Frame('Options',[
        [   sg.Text('Chose parameter:'), sg.Combo(['Elevation', 'Azimuth', 'Time'])], 
        [sg.Text('Chose bandwidth'),sg.Combo(['S-band', 'X-band'])],
        [sg.Button('Specific channel') ],
        ])],
    [sg.OK()]
]

# Creates the Window and event loop
window = sg.Window('Window Title', layout)
while True:
    event, values = window.read()
   ## This part does not do much yet
   # The idea is that a new identical window opens up where the choice of chanels comes up. 
    if event == 'Specific channel':
        
        sg.theme('DarkAmber') 
        lines = [[sg.CB('', key=x, default = values[x]), sg.T(s_real_name[x])] for x in range(len(s_real_name))]
        form = sg.FlexForm('files')

        channels = [[sg.CB('', key=x, default = values[x]), sg.T(s_real_name[x])] for x in range(len(s_real_name))]

        layout2 = [[
            sg.Frame('Pick stations',[*lines
                ]), 
            sg.Frame('Options',[
                [   sg.Text('Chose parameter:'), sg.Combo(['Elevation', 'Azimuth', 'Time'])], 
                [sg.Text('Chose bandwidth'),sg.Combo(['S-band', 'X-band', 'Channel specific'],), ],
                [ sg.Text('Chose channel:')], 
                ])],
            [sg.OK()]
        ]

        # Create the Window and event loop
        window1 = sg.Window('Window Title', layout2)
        
        while True:
            event, values = window1.read()
            if event == sg.WIN_CLOSED or event == 'OK': 
                break
        window.close()
        window1.close()
    if event == sg.WIN_CLOSED or event == 'OK': 
        break

# Checks what station names have been checked 
names = []
for i in range(len(lines)):
    if values[i] == True:
        names.append(s_real_name[i])

#Creates a figure with the number of stations subplots
fig, axs = plt.subplots(len(names))   
f = '/home/ugne/Documents/NVI/dmp_mult/Freq_mult.dmp'

# Loops through the names of stations
for i in range(len(names)):
    [Y, antal, chan_num] = create_Y(file_dir, names[i])

    [Sb,Xb] = freq(f,names[i], chan_num)

    # Checks which parameter and depending on it calls a function to get the X-value
    if values['00'] == 'Elevation' :
        xlabel = 'Elevation [°]'
        f_time ='/home/ugne/Documents/NVI/dmp_mult/El_mult.dmp'
        X = X_el_az(f_time, names[i], chan_num, antal)
        X = X*90/1.5
    elif values['00'] == 'Azimuth':
        xlabel = 'Azimuth'
        f_az ='/home/ugne/Documents/NVI/dmp_mult/Az_mult.dmp'
        X = X_el_az(f_az,names[i],chan_num, antal)
    elif values['00'] == 'Time':
        xlabel = 'Time [s]'
        f_el = '/home/ugne/Documents/NVI/dmp_mult/Time_mult.dmp'
        X = X_time(f_el, names[i],chan_num, antal)

    if values['11'] == 'X-band':
        l = range(0,Xb)

    elif values['11'] == 'S-band':
        l = range(Xb+1,chan_num-1)
    
    #plots
    for k in l:
        axs[i].scatter(X,Y[:,k],s = 3, c = 'black')

    axs[i].set_title(names[i])
 
plt.tight_layout()   
plt.show()

   


        
        
