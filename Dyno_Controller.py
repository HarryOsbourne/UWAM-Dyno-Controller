import random
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

def safetySupervisor():# returns true if safe to continue the test
    error = None
    if temperature > 180:
        error = "!!! Temperature exceeded 180 degrees !!!"
    elif rpm > 10000:
        error = "!!! Revolutions exceeded 10,000 per minute !!!"
    elif torque > 2500:
        error = "!!! Torque exceeded 2,500 newtons !!!"
    return error

def saveData(type, data):
    savedData.append([type, data])
    pass

def retreiveData():
    errorLi, tempLi, rpmLi, torqueLi = [],[],[],[]
    for i in savedData:
        if i[0] == 1:
            tempLi.append(i[1])
        if i[0] == 2:
            rpmLi.append(i[1])
        if i[0] == 3:
            torqueLi.append(i[1])
        if i[0] == 0:
            errorLi.append(i[1])
    
    # Table outputting
    print ('{:-^36}'.format(' Recorded Data '))
    columnNames = ['Temp' , 'Rpm' , 'Torque']
    row_format = '{:<9}' * (len(columnNames)+1)
    print (row_format.format('Cycle',*columnNames))
    for cycle in range(cycles):
        row = [tempLi[cycle], rpmLi[cycle], torqueLi[cycle]]
        print (row_format.format(cycle+1, *row))
    print ('{:<}'.format(errorLi[0]))
            
def systemSupervisor():
    global temperature, rpm, torque, savedData, cycles
    cycles, savedData = 0, []
    go = input('\n Run New Test? (y or n)')
    if go =='y':
        '''
        # CAN bus stuff
        canState = CAN.state()
        While canState != CAN.ERROR_ACTIVE:
            if canState == CAN.STOPPED:
                CAN.init(mode, extframe=False, prescaler=100, *, sjw=1, bs1=6, bs2=8, auto_restart=False)
            elif canState == CAN.BUS_OFF
                CAN.restart()
            elif canState == CAN.ERROR_WARNING:
                print("The controller is on and in the Error Warning state (at least one of TEC or REC is 96 or greater)")
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
            cycles +=1
            if error != None:
                saveData(0,error)
                break
        print("!!! Dyno Stopped (", savedData[len(savedData)-1][1],")\n" )
        retreiveData()
    # CAN.deinit() # Turns off the can controller
    print("Dyno testing ended by user")

systemSupervisor()