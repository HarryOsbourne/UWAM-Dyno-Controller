# TODO List
# Watchdog
# Dead mans switch (Back up for watchdog)
# Export to CSV file for test (single then for all)
# Test pofiles for controlling the motor controller

import random
import threading
import queue
import time
import csv
# from pyb import CAN, SPI

def getData(length, step):
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

def safetySupervisor(temperature, rpm, torque):
    tempCutOff = 180
    rpmCutOff = 5000
    torqCutOff = 2500
    CutOffPercent = 0.9
    systemMessage = {'type':-1,'msg':''}
    if temperature == -1 or rpm == -1 or torque == -1:
        error = {'type':0,'msg':'!!! A sensor failed to return data'}
    else:
        if temperature > tempCutOff:
            systemMessage = {'type':0,'msg':'!!! Temperature exceeded '+str(tempCutOff)+' degrees'}
        elif rpm > rpmCutOff:
            systemMessage = {'type':0,'msg':'!!! Revolutions exceeded '+str(rpmCutOff)+' per minute'}
        elif torque > torqCutOff:
            systemMessage = {'type':0,'msg':'!!! Torque exceeded '+str(torqCutOff)+' newtons'}
        elif temperature > tempCutOff*CutOffPercent:
            systemMessage = {'type':1,'msg':'*** Temperature exceeded '+str(int(CutOffPercent*100))+'% of Cut off'}
        elif rpm > rpmCutOff*CutOffPercent:
            systemMessage = {'type':1,'msg':'*** RPM exceeded '+str(int(CutOffPercent*100))+'% of Cut off'}
        elif torque > torqCutOff*CutOffPercent:
            systemMessage = {'type':1,'msg':'*** Torque exceeded '+str(int(CutOffPercent*100))+'% of Cut off'}
    return systemMessage

def saveData(type, data):
    savedData.append([type, data])

def csvWriter():
    pass
    '''
    with open('Dyno_Test.csv','w',newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', qouting=csv.QUOTE_MINIMAL)
        writer.writerow([tempData[0],rpmData[0],torqueData[0],])
    '''

def retreiveData():
    sysMsgData, tempData, rpmData, torqueData = [],[],[],[]
    for data in savedData:
        if data[0] == 1:
            tempData.append(data[1])
        elif data[0] == 2:
            rpmData.append(data[1])
        elif data[0] == 3:
            torqueData.append(data[1])
        elif data[0] == 4:
            sysMsgData.append(data[1])
    printTable(sysMsgData, tempData, rpmData, torqueData)
    
def printTable(sysMsgData, tempData, rpmData, torqueData):
    print ('{:-^50}'.format(' Recorded Data '))
    columnNames = ['Temp' , 'Rpm' , 'Torque', 'System Message']
    row_format = '{:<9}' * (len(columnNames)+1)
    print (row_format.format('Cycle',*columnNames))
    for cycle in range(cycles):
        row = [tempData[cycle], rpmData[cycle], torqueData[cycle], sysMsgData[cycle]]
        print (row_format.format(cycle+1, *row))

def pollSensor(length, step, sensor, out_queue):
    data = getData(length, step)
    out_queue.put(data, sensor)
    saveData(sensor, data)

def systemSupervisor():
    global savedData, cycles, go
    cycles, savedData, go = 0, [], 'n'
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
    run = True
    tempTestList = [[200,10,1],[6000,100,2],[2800,100,3]]
    while run:
        cycles +=1
        data_queue = queue.PriorityQueue()
        temperature, rpm, torque = -1,-1,-1
        for arg in tempTestList:
            t = threading.Thread(target=pollSensor,args=(arg[0],arg[1],arg[2], data_queue))
            t.start()
        # Sleeps for one second
        time.sleep(1)
        if threading.active_count() <= 1:
            temperature = data_queue.get()
            torque = data_queue.get()
            rpm = data_queue.get()
            error = safetySupervisor(temperature, rpm, torque)
            saveData(4,error['msg'])
        if error['type'] == 0:
            run = False
    print("!!! Dyno Stopped ("+str(error['msg'])+") on cycle",cycles,"\n" )
    retreiveData()
    # CAN.deinit() # Turns off the can controller

# runs the in the setup stage when the BB boots
def systemSetup():
    global savedData, cycles, go
    go = input('\nRun New Test? (y or n)' )
    while go == 'y':
        print("\nCommecing Test")
        systemSupervisor()
        go = input('\nRun New Test? (y or n) ')
    print("Dyno testing ended by user")

systemSetup()