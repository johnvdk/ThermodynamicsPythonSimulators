#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 21:18:07 2018

@author: jeremy
"""

#Output 0 – 5 V
#
#Nominal conversion factor of 10 mV/◦C
#
#Nominal accuracy ±1 K at room temperature
#
#Can be calibrated to much better than that!
#
#Simple test: put six together and compare outputs
#
#Absolute temperature not as important as differences


from datetime import datetime #'2011-05-03 17:45:35.177000'
import csv
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation
import numpy as np


#print(serial.__file__)

isData = False
yes = input("Are you recording data? [y/n]: ")
if yes == "y" or yes  == 'y':
    isData = True
#
#if isData:
#    com = 'com16'
#    ser = serial.Serial(
#        port=com,
#        baudrate=9600,
#    )

    freq = "Frequency = " + input("Enter info about the data: ") 
    info = "1 = 5mV change which is 0.5 degree C"

    firstLine = [freq, info]
realX = [0.013, 0.082, 0.152, 0.222, 0.292]

Sx = 0.01 #m
St = 0.5 #s
I = 10000 #Iterations
k = 205   #W/m*k
c = 921   #J/kg*C   heat capacitance
dens = 2700 #kg/m^3
Tamb = 296
a = 0.01
kc = 7.9 
Eo = 5.67*10**(-8) #W/m^2/K^4
#area of end piece
area = 3.14*a**2 + 2*3.14*a*Sx
#Initialize temperature array
T = [294]
for x in range (0,30):
    T.append(294)

#Initialize x coordinates array
Tx = []
for x in range(0,31):
    Tx.append(x*0.01)
    
count  = 0
#Calculate temperatures after set amount of interations
read = False
power = 10
switch = 245
powerOn = True
    
#Call loop method to see step by step change
def loop():
    global count 
    global power
#    count = count + 1
#    if (count > switch):
#        frequency = 2500  # Set Frequency To 2500 Hertz
#        duration = 100  # Set Duration To 1000 ms == 1 second
#        winsound.Beep(frequency, duration)
    if (powerOn):
        print("power is on")
        power = 12
    else:
        print("power is off")
        power = 0
    T[0] = T[0] - k*(T[0] - T[1])/(c*dens*Sx**2)*St
    P = area*(kc*(T[0]-Tamb) + Eo*(T[0]**4-Tamb**4))
    T[0] = T[0] + P*St/(c*dens*3.14*a**2*Sx)
    #calculate last
    T[-1] = T[-1] + k*(T[-2] - T[-1])/(c*dens*Sx**2)*St
    P = power -area*(kc*(T[-1]-Tamb) + Eo*(T[-1]**4-Tamb**4))
    T[-1] = T[-1] + P*St/(c*dens*3.14*a**2*Sx)
    for x in range(1,30):
        T[x] = T[x] + (k*St)/(c*dens)*(T[x-1] - 2*T[x] + T[x+1])/(Sx**2)
        T[x] = T[x] - St*(2*kc*(T[x] - Tamb)/(c*dens*a) + 2*Eo*(T[x]**4 - Tamb**4)/(c*dens*a))

def getTempTime(dataString):
    T1 = []
    T2 = []
    T3 = []
    T4 = []
    T5 = []
    Times = []
    time = 0
    with open(dataString) as file:
        read = csv.reader(file, delimiter=',')
        for row in read:
            if (len(row) > 2):
                count = 1
                print(row)
                time += 1
                for number in row:
                    temp = (float(number) - 20.46)/2.046 - 40 + 273
                    if (count == 1):
                        T1.append(temp)
                    if (count == 2):
                        T2.append(temp)
                    if (count == 3):
                        T3.append(temp)
                    if (count == 4):
                        T4.append(temp)
                    if (count == 5):
                        T5.append(temp)
                    count += 1
    
    for t in range (0, time):
        Times.append(2*t)
    plt.plot(Times[:], T1[:], 'r')
    plt.plot(Times[:], T2[:], 'b')
    plt.plot(Times[:], T3[:], 'y')
    plt.plot(Times[:], T4[:], 'g')
    plt.plot(Times[:], T5[:], 'm')
    plt.ylabel('Temperature [K]')
    plt.xlabel('Time[m]')
    plt.title('Temperature vs Time Graph of Aluminum Rod')
    plt.show()
                    
                    
  
def parse(dataString):
    data = []
    number = ""
    for letter in dataString:
        if letter == "," or letter == ',':
            data.append(int(number))
            number = ""
        if letter.isdigit():
            number = number + letter
    return data


if isData:
    roughTime = str(datetime.now())
    time = ""
    for letter in roughTime:
        if letter == ":" or letter == ':' or letter == " " or letter == ' ':
            letter = "."
        time = time + letter
    
    filename = "AluminumRod_" + time + ".csv"
    with open(filename,'w') as file:
        writer = csv.writer(file)
        writer.writerow(firstLine)
        x = 0
        while x<12000:
            if(ser.inWaiting()>0):
                data = str(ser.readline())
                line = parse(data)
                writer.writerow(line)
                for x in range(0,0):
                    loop()
                loop()
                temps = []
                for number in line:
                    if number == 1:
                        powerOn = True
                    elif number == 0:
                        powerOn = False
                    else:
                        temp = (number - 20.46)/2.046 - 40 + 273
                        temps.append(temp)
                print(line)
                plt.plot(Tx[:], T[:], 'b')
                plt.plot(realX[:], temps[:], 'ro')
                plt.ylabel('Temperature [K]')
                plt.xlabel('Distance [m]')
                plt.title('Temperature vs Position Graph of Aluminum Rod')
                plt.show()
                x =x +1
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
def analyze(filename):
    with open(filename) as file:
        read = csv.reader(file, delimiter=',')
        for row in read:
            if (len(row) > 2):
                print(row)
                #plt.plot(Tx[:], T[:], 'b')
                plt.plot(realX[:], row[:], 'ro')
                plt.ylabel('Temperature [K]')
                plt.xlabel('Distance [m]')
                plt.title('Temperature vs Position Graph of Aluminum Rod')
                plt.show()
                time.sleep(0.05)


def animate(filename):
    plt.ion()
    plt.figure()
    count = 0
    with open(filename) as file:
        read = csv.reader(file, delimiter=',')
        for row in read:
            count = count + 1
            if(count > 4):
                count = 0
                if (len(row) > 2):
                    temps = []
                    for number in row:
                        temp = (float(number) - 20.46)/2.046 - 40 + 273
                        temps.append(temp)
                    #plt.plot(Tx[:], T[:], 'b')
                    plt.clf() 
                    plt.plot(realX[:], temps[0:5], 'ro')
                    plt.xlabel('Length [m]', fontsize=10)  # X axis label
                    plt.ylabel('Temperature in $^o C$', fontsize=10)  # Y axis label
                    plt.title('Temperature in a rod')
                    plt.grid(True)  # Enabling gridding
                    plt.axis((-0.0, 0.3, 290, 320))  # Making axis rigid
                    plt.pause(0.0005)
                

ani = input("Wanna animate?")
if ani == "y":
    filenam = input("File plz")
    animate(filenam)
grph = input("Wanna graph the Temperature time plot?")
if grph == "y":
    filenam = input("File plz")
    getTempTime(filenam)
