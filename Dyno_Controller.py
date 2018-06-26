# TODO List
# systemMessageings
# Threading of sensor readings
# Watchdog
# Dead mans switch (Back up for watchdog)
# Export to CSV file for test (single then for all)
# Test pofiles for controlling the motor controller

import random
import threading
import time
# from pyb import CAN, SPI

def getData(type, length, step):
    data = random.randrange(0, length, step)
    return data

def spiCommunicator():
    pass
    '''
    # read of pins x, y, z
    SCK = 1
    MOSI = 2
    MISO = 3
    # do some things
    SPI.init(baudrate=1000000, *, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=None, mosi=None, miso=None, pins=(SCK, MOSI, MISO))
    '''

def canBusCommunicator():
    pass
    '''
    CAN = CAN(1, CAN.LOOPBACK) # 
    CAN.setfilter(0, CAN.LIST16, 0, (123, 124, 125, 126))  # set a filter to receive messages with id=123, 124, 125 and 126
    CAN.send('message!', 123)   # send a message with id 123
    CAN.recv(0)                 # receive message on FIFO 0
    '''

def safetySupervisor(): # returns true if safe to continue the test
    tempCutOff = 180
    rpmCutOff = 10000
    torqCutOff = 2500
    CutOffPercent = 0.8
    systemMessage = []
    if temperature >= tempCutOff:
        systemMessage = [0,"!!! Temperature exceeded 180 degrees !!!"]
    elif rpm >= rpmCutOff:
        systemMessage = [0,"!!! Revolutions exceeded 10,000 per minute !!!"]
    elif torque >= torqCutOff:
        systemMessage = [0,"!!! Torque exceeded 2,500 newtons !!!"]
    # elif temperature > tempCutOff*CutOffPercent:
    #     systemMessage = [1,"!!! Temperature exceeded " + str(int(CutOffPercent*100)) + "% of Cut off !!!"]
    # elif rpm > rpmCutOff*CutOffPercent:
    #     systemMessage = [1,"!!! RPM exceeded " + str(int(CutOffPercent*100)) + "% of Cut off !!!"]
    # elif torque > torqCutOff*CutOffPercent:
    #     systemMessage = [1,"!!! Torque exceeded " + str(int(CutOffPercent*100)) + "% of Cut off !!!"]
    return systemMessage

def saveData(type, data):
    savedData.append([type, data])

def retreiveData():
    errorData, tempData, rpmData, torqueData = [],[],[],[]
    for data in savedData:
        if data[0] == 1:
            tempData.append(data[1])
        elif data[0] == 2:
            rpmData.append(data[1])
        elif data[0] == 3:
            torqueData.append(data[1])
        elif data[0] == 0:
            errorData.append(data[1])
    
    # Table outputting
    print ('{:-^36}'.format(' Recorded Data '))
    columnNames = ['Temp' , 'Rpm' , 'Torque']
    row_format = '{:<9}' * (len(columnNames)+1)
    print (row_format.format('Cycle',*columnNames))
    for cycle in range(cycles):
        row = [tempData[cycle], rpmData[cycle], torqueData[cycle]]
        print (row_format.format(cycle+1, *row))
        if errorData[cycle] != []:
            print ('{:<}'.format(errorData[cycle][1]))
    print ('{:<}'.format(errorData[len(errorData)-1][1]))
            
def systemSupervisor():
    global temperature, rpm, torque, savedData, cycles, go
    '''
    # CAN bus stuff
    canState = CAN.state()
    While canState != CAN.ERROR_ACTIVE:
        if canState == CAN.STOPPED:
            CAN.init(mode, extframe=False, prescaler=100, *, sjw=1, bs1=6, bs2=8, auto_restart=False)
        elif canState == CAN.BUS_OFF
            CAN.restart()
        elif canState == CAN.ERROR_systemMessageING:
            print("The controller is on and in the Error systemMessageing state (at least one of TEC or REC is 96 or greater)")
        elif canState == CAN.ERROR_PASSIVE:
            print("The controller is on and in the Error Passive state (at least one of TEC or REC is 128 or greater)")
        canState = CAN.state()
    '''
    while True:
        temperature = getData("i",200,10)
        rpm = getData("i",1100,100)
        torque = getData("i",2800,100)
        saveData(1,temperature)
        saveData(2,rpm)
        saveData(3,torque)
        error = safetySupervisor()
        saveData(0,error)
        cycles +=1
        if error != [] and error[0] == 0:
            print("!!! Dyno Stopped")
            break
    print("!!! Dyno Stopped (", error[1],")\n" )
    retreiveData()
    # CAN.deinit() # Turns off the can controller

# runs the in the setup stage when the BB boots
def systemSetup():
    global temperature, rpm, torque, savedData, cycles, go
    cycles, savedData, go = 0, [], 'n'
    go = input('\n Run New Test? (y or n)')
    while go == 'y':
        print("Commecing Test")
        systemSupervisor()
        go = input('\n Run New Test? (y or n)')
    print("Dyno testing ended by user")

systemSetup()