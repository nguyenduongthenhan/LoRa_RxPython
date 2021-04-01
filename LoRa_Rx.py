# dmesg | grep tty : finf port on cmd
import time
import serial
from datetime import datetime

def initLoraSetup(freq, bw, sf):
    ser.write('mac pause\r\n'.encode('utf-8'))
    macpauseOK=ser.readline()
    print(macpauseOK)
    ##########################
    ser.write(('radio set mod lora\r\n').encode('utf-8'))
    setmodeOK = ser.readline()
    print(setmodeOK)
    #################
    print(freq)
    ser.write(('radio set freq '+freq+'\r\n').encode('utf-8'))
    freqOK = ser.readline()
    print(freqOK)
    #############################################
    ser.write(('radio set bw '+bw+'\r\n').encode('utf-8'))
    bwOK = ser.readline()
    print(bwOK)
    #############################################
    ser.write(('radio set sf sf' + sf + '\r\n').encode('utf-8'))
    sfOK = ser.readline()
    print(sfOK)
    #############################################
    ser.write(('radio set pwr 14\r\n').encode('utf-8'))
    pwrOK = ser.readline()
    print(pwrOK)
    #############################################
    ser.write(('radio set crc on\r\n').encode('utf-8'))
    crcOK = ser.readline()
    print(crcOK)
    #############################################
    ser.write(('radio set iqi off\r\n').encode('utf-8'))
    iqicOK = ser.readline()
    print(iqicOK)
    #############################################
    ser.write(('radio set cr 4/5\r\n').encode('utf-8'))
    crOK = ser.readline()
    print(crOK)
    #############################################
    ser.write(('radio set wdt 0\r\n').encode('utf-8'))
    wdtOK = ser.readline()
    print(wdtOK)#############################################
    ser.write(('radio set sync 12\r\n').encode('utf-8'))
    syncOK = ser.readline()
    print(syncOK)

def LoraRxText(RxSreing, packetType, TxTimeout):
    ser.write('radio rx 0\r\n'.encode('utf-8'))
    ######################confirm send ok
    RxOk=ser.readline()
    while RxOk != b'ok\r\n':
        #RxOk == b'busy':
        time.sleep(10)
        ser.write('radio rx 0\r\n'.encode('utf-8'))
        RxOk = ser.readline()

    print('send command ok:\r\n')
    print(RxOk)
    RxData = ser.readline()
    print('received data:\r\n')
    print(RxData)
    ###################################################
    ser.write('radio rxstop\r\n'.encode('utf-8'))
    RxStop = ser.readline()
    while RxStop != b'ok\r\n':
        # RxOk == b'busy':
        time.sleep(10)
        ser.write('radio rxstop\r\n'.encode('utf-8'))
        RxStop = ser.readline()

    print('Confirm stop:\r\n')
    print(RxStop)
    ####################################

    print(type(RxData))
    print(RxData[10:len(RxData)-2:1])
    print(len(RxData))
    RxDataString=RxData[10:len(RxData)-2:1].decode('utf-8')
    print(RxDataString)
    #drawString=(RxData[10:len(RxData)-2:1]).decode('hex')
    print('rx ok:##########################################:')
    print(RxData[0:7:1])
    if RxData[0:8:1] == b'radio_rx':
        plainString = bytearray.fromhex(RxDataString).decode()
    else:
        plainString ='error by weak signal or low link budget'

    print(plainString)
    return plainString

    #text_file.write(RxDataString)
    #text_file.write('\r\n')
    #text_file.close()
# configure the serial connections (the parameters differs on the device  you are connecting to)

SDI_time_filename = datetime.now().strftime('%Y%m%d%H%M%S+')
SDI_filename = '/home/duong/VWC_EC/'+SDI_time_filename+'.txt'
#SDI_filename = 'cho.tx'
SDI_file=open(SDI_filename,'wt')
SDI_file.write('Year Month Day Hour Minute Second SDI VWC Temperature EC\r\n')
SDI_file.close()


ser = serial.Serial('/dev/ttyUSB0',57600)
#    port='/dev/ttyS0',
    #'COM17',
 #   baudrate=9600,
  #  parity=serial.PARITY_ODD,
   # stopbits=serial.STOPBITS_TWO,
    #bytesize=serial.SEVENBITS
#)
ser.isOpen()
print('ser:')
print(ser.name)
print('Enter your commands below.\r\nInsert "exit" to leave the application.')

ser.write('sys get ver\r\n'.encode('utf-8'))
textarduino =ser.readline()
print('LoRa version:')
print(textarduino)
print('test function:')
#aaaaa='ff'+str(int(12))+'ccc'
#print(aaaaa)

while 1:
    initLoraSetup('866550000','125','10')
    SDI_text = LoraRxText(1,2,3)
    SDI_text=SDI_text.replace('+',' ')
    SDI_file = open(SDI_filename, 'at')
    SDI_time = datetime.now().strftime('%Y %m %d %H %M %S ')
    SDI_file.write(SDI_time)
    SDI_file.write(SDI_text + '\r\n')
    SDI_file.close()
    #while 1:
 #   bytesToRead=ser.inWaiting()
  #  textarduino = ser.read(bytesToRead)
#print(textarduino)