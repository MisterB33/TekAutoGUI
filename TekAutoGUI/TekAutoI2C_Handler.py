#Majid Reza Barghi 
#TekAutoI2C.py the purpose of this script is to automate I2C measurments and compile data to a directory for automated 
#Report Generation 


import time # std module
from datetime import datetime # std module for getting current date and time 
import pyvisa as visa # http://github.com/hgrecco/pyvisa 

import numpy as np # http://www.numpy.org/

import os.path 




class I2C_Scope:
    def __init__(self,visa_address= "",FILE_NAME="", FILE_LOCATION="",adress=''):
        print(visa_address)
        self.adress = adress
        self.visa_address = visa_address 
        self.rm = visa.ResourceManager()
        self.myI2C_Scope = self.rm.open_resource(self.visa_address)
        print("scope exception succesfull!")
            
        self.FILE_NAME = FILE_NAME
        self.FILE_LOCATION = FILE_LOCATION
        self.TestPoints = open(FILE_LOCATION+"\\list.txt","a")

#DEVICE_ADDRESS='TCPIP0::10.110.4.67::inst0::INSTR'
#self.FILE_LOCATION=os.path.abspath(os.getcwd())
#TestPoints = open("list.txt", "a")

    def ParseScopeInfo(self,ScopeString):
        tmp = ScopeString.split(";")
        ScopeStringtmp = [None]*len(tmp)
        for i in range(len(tmp)):
            tmpstring = tmp[i].split(",")
            newFloattmpstring = [float(tmpstring[3]),float(tmpstring[4])]
            ScopeStringtmp[i]  = newFloattmpstring
            print(ScopeStringtmp[i])
        return ScopeStringtmp
        
    def findValues(self,start,stop,EdgeArray):
        FoundValues = []
        for item in EdgeArray:
            if item[0] > start and item[0] < stop:
                FoundValues.append(item)
        print(FoundValues)
        
        return FoundValues
    def DrawZoom(self,zoomvalue):
        zoomstring = "ZOOm:ZOOM1:POSition "+str(zoomvalue)
        print(zoomstring)
        self.myI2C_Scope.write("ZOOM:MODE ON")
        self.myI2C_Scope.write("ZOOm:ZOOM1:SCAle 1E-6")
        self.myI2C_Scope.write(zoomstring)
        time.sleep(2.0)
        
        
    
        
    def runI2C(self):
        print("\n")
    
        self.FILE_LOCATION=self.FILE_LOCATION+"\\"+self.FILE_NAME
    
        if not os.path.exists(self.FILE_LOCATION):
            os.makedirs(self.FILE_LOCATION)
        self.TestPoints.write(self.FILE_NAME+"\n")
    
        if os.path.exists(self.FILE_LOCATION+"\\results.txt"):
            os.remove(self.FILE_LOCATION+"\\results.txt")
        
        if os.path.exists(self.FILE_LOCATION+"\\PicList.txt"):
            os.remove(self.FILE_LOCATION+"\\PicList.txt")    
    
    
        picList=open(self.FILE_LOCATION+"\\PicList.txt","a")    
        results=open(self.FILE_LOCATION+"\\results.txt","a")
    
   # visa_address =DEVICE_ADDRESS
    #fileSaveLocation=self.FILE_LOCATION
   #print(fileSaveLocation)
    #print(visa_address)
    
    
    
        self.myI2C_Scope.write('*cls') # clear ESR
        self.myI2C_Scope.write('*rst') # reset 
        self.myI2C_Scope.timeout = 30000 # ms
        self.myI2C_Scope.encoding = 'latin_1'
        self.myI2C_Scope.read_termination = '\n'
        self.myI2C_Scope.write_termination = None
        self.myI2C_Scope.write('*cls') # clear ESR
        self.myI2C_Scope.write('*rst') # reset 
    
    #initial conditions of the scope 
    #Turn on the channel
        self.myI2C_Scope.write('select:CH2 ON ')
        self.myI2C_Scope.write('select:CH1 ON')
        self.myI2C_Scope.write('select:B1 ON ')

        self.myI2C_Scope.write('header 0')
        self.myI2C_Scope.write('data:encdg SRIBINARY')
    
    #sets the scope scale 
        self.myI2C_Scope.write('CH1:SCAle 2000E-3')
        self.myI2C_Scope.write('CH2:SCAle 2000E-3')
        self.myI2C_Scope.write('HORizontal:SCAle 100E-6')
        self.myI2C_Scope.write('HORizontal:POSition 9')
    
    #Labels for each channel 
        CH1_label = 'CH1:LABel  " '+self.FILE_NAME+' SDA"'
        CH2_label = 'CH2:LABel  " '+self.FILE_NAME+' SCLK"'
    
        self.myI2C_Scope.write(CH1_label)
        self.myI2C_Scope.write(CH2_label)
    
    #sets the postion of channel 1& 2 
        self.myI2C_Scope.write('CH1:POSition 1.6')
        self.myI2C_Scope.write('CH2:POSition -1.0')
        self.myI2C_Scope.write('BUS:B1:POSition -1.6')
    
    #Bus set up 
        self.myI2C_Scope.write('BUS:B1:TYPe I2C')
        self.myI2C_Scope.write('BUS:B1:I2C:SCLk:SOUrce CH2')
        self.myI2C_Scope.write('BUS:B1:I2C:SDAta:SOUrce CH1')
        self.myI2C_Scope.write('BUS:THReshold:CH1 920E-3')
        self.myI2C_Scope.write('BUS:THReshold:CH2 920E-3')
        self.myI2C_Scope.write('BUS:B1:DISplay:TYPe BOTh')
    
    #Trigger for I2C 
        self.myI2C_Scope.write('TRIGGER:A:TYPE BUS')
        print(self.adress)
        self.myI2C_Scope.write('TRIGger:A:BUS:B1:I2C:CONDition ADDRess')
        self.myI2C_Scope.write('TRIGger:A:BUS:B1:I2C:ADDRess:MODe ADDR7')
        #self.myI2C_Scope.write('TRIGger:A:BUS:B1:I2C:ADDRess:TYPe GENeralcall')
        self.myI2C_Scope.write('TRIGger:A:BUS:B1:I2C:DATa:DIRection WRITE')
        a = '"'+self.adress+'"'
        c = 'TRIGger:A:BUS:B1:I2C:ADDRess:VALue '+a
        print(c)
        
        self.myI2C_Scope.write(c)
        b = self.myI2C_Scope.query('TRIGger:A:BUS:B1:I2C:ADDRess:VALue?')
        print(b)
    #sets the trigger to stop on sequence 
        self.myI2C_Scope.write('acquire:state OFF') # stop
        self.myI2C_Scope.write('acquire:stopafter SEQUENCE') # single
        self.myI2C_Scope.write('acquire:state ON') # run
    
        time.sleep(5.0)
    #declares a float array of 15 
        value = [0.0]*19 
        units = [""]*19
    
        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH2') 
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe Frequency')
        value[0] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[0] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("Frequency value is:"+str(value[0])+str(units[0]).replace('"',""))
    
        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH2') 
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe PWidth')
        value[1] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[1] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("High Period value is:"+str(value[1])+str(units[1]).replace('"',""))

        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH2') 
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe NWidth')
        value[2] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[2] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("Low Period value is:"+str(value[2])+str(units[2]).replace('"',"")) 

        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH2') 
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe Maximum')
        value[3] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[3] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("SCL Vmax value is:"+str(value[3])+str(units[3]).replace('"',""))

        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH2') 
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe Minimum')
        value[4] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[4] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("SCL Vmin value is:"+str(value[4])+str(units[4]).replace('"',"")) 

        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH2') 
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe HIGH')
        value[5] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[5] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("SCL Vih value is:"+str(value[5])+str(units[5]).replace('"',"")) 

        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH2')
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe LOW')
        value[6] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[6] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("SCL Vil value is:"+str(value[6])+str(units[6]).replace('"',""))

        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH1') 
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe Maximum')
        value[7] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[7] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("SDA Vmax value is:"+str(value[7])+str(units[7]).replace('"',""))
        
        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH1') 
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe Minimum')
        value[8] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[8] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("SDA Vmin value is:"+str(value[8])+str(units[8]).replace('"',"")) 
        
        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH1') 
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe HIGH')
        value[9] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[9] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("SDA Vih value is:"+str(value[9])+str(units[9]).replace('"',"")) 

        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH1')
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe LOW')
        value[10] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[10] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("SDA Vil value is:"+str(value[10])+str(units[10]).replace('"',""))

        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH2') 
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe Rise')
        value[11] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[11] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("SLC Rise Time value is:"+str(value[11])+str(units[11]).replace('"',""))


        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH2') 
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe FaLL')
        value[12] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[12] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("SLC Fall Time value is:"+str(value[12])+str(units[12]).replace('"',""))  


        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH1') 
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe Rise')
        value[13] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[13] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("SDA Rise Time value is:"+str(value[13])+str(units[13]).replace('"',""))


        self.myI2C_Scope.write('MEASUrement:IMMed:SOUrce CH1') 
        self.myI2C_Scope.write('MEASUrement:IMMed:TYPe FaLL')
        value[14] = self.myI2C_Scope.query(':MEASUrement:IMMed:VALue?') 
        units[14] = self.myI2C_Scope.query(':MEASUrement:IMMed:Units?')
        print("SDA Fall Time value is:"+str(value[14])+str(units[14]).replace('"',""))
        
        

        
        print('Saving Screen shot....')

        self.myI2C_Scope.write("SAVe:IMAGe:FILEFormat PNG")
        self.myI2C_Scope.write("SAVe:IMAGe:INKSaver OFF")
        self.myI2C_Scope.write("HARDCopy STARt")
        imgData = self.myI2C_Scope.read_raw()
        
        imgFile = open(self.FILE_LOCATION+"\\"+self.FILE_NAME+".png", "wb")
        imgFile.write(imgData)
        imgFile.close()
        

        print("Screen Shot Saved")
        
        picList.write(self.FILE_NAME+".png\n")
        print("clock Start Edges ")
        print("====================")
        
        self.myI2C_Scope.write("CURSor:FUNCtion SCREEN")
        self.myI2C_Scope.write("CURSor:SOUrce CH2 ")
        self.myI2C_Scope.write("SEARCH:SEARCH1:STATE ON")
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:TYPe BUS")
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:BUS:SOUrce B1")
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:BUS:B1:I2C:CONDition STARt")
        time.sleep(2.0) # Scope needs some time to get the data
        self.myI2C_Scope.write("MARK:SAVEALL TOUSER")
        start = self.myI2C_Scope.query("MARK:USERLIST?")
        StartPoints = self.ParseScopeInfo(start)
        print("Stop Condition")
        print("====================")

        self.myI2C_Scope.write("MARK:DELEte ALL")
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:BUS:B1:I2C:CONDition STOP")
        time.sleep(2.0) #Scope needs some time to get the data 
        self.myI2C_Scope.write("MARK:SAVEALL TOUSER")
        stop = self.myI2C_Scope.query("MARK:USERLIST?")
        StopPoints = self.ParseScopeInfo(stop)
        self.myI2C_Scope.write("MARK:DELEte ALL")
        print("Data Edges ")
        print("====================")
        
   
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:TYPe EDGE")
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:EDGE:SLOpe RISE")
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:EDGE:SOUrce CH1")
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:LEVel:CH1 2.9")
        time.sleep(2.0) #Scope needs some time to get the data 
        self.myI2C_Scope.write("MARK:SAVEALL TOUSER")
        Rise = True
        RiseEdgeHit = int(self.myI2C_Scope.write("SEARCH:SEARCH1:TOTal?"))
        print(RiseEdgeHit)
        if RiseEdgeHit == 0:
            self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:EDGE:SLOpe FALL")
            Rise = False
            time.sleep(2.0)
        edges = self.myI2C_Scope.query("MARK:USERLIST?")
        DataEdgePoints = self.ParseScopeInfo(edges)
        self.myI2C_Scope.write("MARK:DELEte ALL")
        
        print("clock Falling Edges ")
        print("====================")
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:EDGE:SLOpe FALL")
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:EDGE:SOUrce CH2")
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:LEVel:CH2 2.9")
        time.sleep(2.0) #Scope needs some time to get the data 
        self.myI2C_Scope.write("MARK:SAVEALL TOUSER")
        edges = self.myI2C_Scope.query("MARK:USERLIST?")
        ClkFallEdgePoints = self.ParseScopeInfo(edges)
        self.myI2C_Scope.write("MARK:DELEte ALL")
        
        
        
        print("clock Rising Edges ")
        print("====================")
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:EDGE:SLOpe RISE")
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:EDGE:SOUrce CH2")
        self.myI2C_Scope.write("SEARCH:SEARCH1:TRIGger:A:LEVel:CH2 2.9")
        time.sleep(2.0) #Scope needs some time to get the data 
        self.myI2C_Scope.write("MARK:SAVEALL TOUSER")
        edges = self.myI2C_Scope.query("MARK:USERLIST?")
        ClkRiseEdgePoints = self.ParseScopeInfo(edges)
        self.myI2C_Scope.write("MARK:DELEte ALL")
        
        t_start = StartPoints[0]
        t_stop = StopPoints[0]
        
        print("First Clock Edge ")
        print("==================")
        temp = self.findValues(t_start[0],t_stop[0],ClkFallEdgePoints)
        t_down = temp[0]
        print(t_down)
       
        
        print("Found Edge at")
        print("==================")
        temp1 = self.findValues(t_down[0],t_stop[0],DataEdgePoints)
        t_edge = temp1[0]
        print(t_edge)
        
        print("Found Data Hold Edge at")
        print("==================")
        temp2 = self.findValues(t_start[0],t_edge[0],ClkFallEdgePoints)
        t_DataHold = temp2[-1]
        print(t_DataHold)
        
        print("Found Data Set up Edge at")
        print("==================")
        temp3 = self.findValues(t_edge[0],t_stop[0],ClkRiseEdgePoints)
        t_setup = temp3[0]
        print(t_setup)
        
        print("Last Clock Edge ")
        print("==================")
        temp4 = self.findValues(t_start[0],t_stop[0],ClkRiseEdgePoints)
        t_up = temp[-1]
        print(t_down)
        
        
        
        
        #self.myI2C_Scope.write("MARK NEXT")
        
        self.DrawZoom(t_edge[0])
        
        

        Tdelta = .0000005
        # set up for finding the Data Hold time 
        print("Finding Data Set up Time")
        print("=============")
        
        #Position Cursor 
        print(self.myI2C_Scope.query("CURSor?"))
        vpos1 = "CURSor:VBArs:POSITION1 "+str(t_DataHold[1]-Tdelta)
        vpos2 = "CURSor:VBArs:POSITION2 "+str(t_edge[1]+Tdelta)
        self.myI2C_Scope.write("CURSor:FUNCtion SCREEN")
        self.myI2C_Scope.write("MEASUrement:GATing CURSor")
        time.sleep(3.0)
        self.myI2C_Scope.write(vpos1)
        self.myI2C_Scope.write(vpos2)
        print(self.myI2C_Scope.query("CURSor:VBArs:POSITION1?"))
        print(self.myI2C_Scope.query("CURSor:VBArs:POSITION2?"))
        time.sleep(2.0)
        print(self.myI2C_Scope.query("CURSor?"))
        self.myI2C_Scope.write("MEASUrement:GATing CURSor")
        
        #setting up Delay for data hold Measurement 
        self.myI2C_Scope.write("MEASUrement:IMMed:SOUrce1 CH2")
        self.myI2C_Scope.write("MEASUrement:IMMed:SOUrce2 CH1")
        self.myI2C_Scope.write("MEASUrement:IMMed:TYPe Delay")
        
        #Check if we have a rising or Falling Edge 
        
        delayM = "MEASUrement:IMMed:DELay:EDGE2 Rise"
        self.myI2C_Scope.write("MEASUrement:REFLevel:PERCent:MID1 30")
        midref = "MEASUrement:REFLevel:PERCent:MID2 70"
        if Rise == False :     
            delayM = "MEASUrement:IMMed:DELay:EDGE2 FALL"
            midref = "MEASUrement:REFLevel:PERCent:MID2 30"
        self.myI2C_Scope.write(delayM)
        self.myI2C_Scope.write(midref)
        self.myI2C_Scope.write("MEASUrement:IMMed:DELay:EDGE1 FALL")
        print(self.myI2C_Scope.query('MEASUrement:IMMed:VALue?'))
        print(self.myI2C_Scope.query('MEASUrement:IMMed:UNIts?') )
        units[15] = self.myI2C_Scope.query('MEASUrement:IMMed:UNIts?')
        value[15] = self.myI2C_Scope.query('MEASUrement:IMMed:VALue?')
        
        #Screen Shot for Data Holdtime up.
          
          
        self.myI2C_Scope.write("SAVe:IMAGe:FILEFormat PNG")
        self.myI2C_Scope.write("SAVe:IMAGe:INKSaver OFF")
        self.myI2C_Scope.write("HARDCopy STARt")
        imgData = self.myI2C_Scope.read_raw()
        
  
        imgFile = open(self.FILE_LOCATION+"\\"+self.FILE_NAME+"DataHoldTime.png", "wb")
        imgFile.write(imgData)
        imgFile.close()
        
        
        
        #Writing to Pic List 
        
        print("Screen Shot Saved")
        picList.write(self.FILE_NAME+"DataHoldTime.png\n")
        
        
        #Screen Shot for Data Setup Time.
        print("Finding Data Set up Time")
        print("=============")
        #Draw zoom 
        
        self.DrawZoom(t_edge[0]+.1)
        
        
        #Check if we have a rising or Falling Edge
        
        vpos1 = "CURSor:VBArs:POSITION1 "+str(t_DataHold[1]-Tdelta)
        vpos2 = "CURSor:VBArs:POSITION2 "+str(t_setup[1]+Tdelta)
        self.myI2C_Scope.write(vpos1)
        self.myI2C_Scope.write(vpos2)
        time.sleep(3.0)
        print(self.myI2C_Scope.query("CURSor:VBArs:POSITION1?"))
        print(self.myI2C_Scope.query("CURSor:VBArs:POSITION2?"))
        time.sleep(2.0)
        print(self.myI2C_Scope.query("CURSor?"))
        self.myI2C_Scope.write("CURSor:SOUrce CH1")
        self.myI2C_Scope.write("CURSor:FUNCtion SCREEN")
        self.myI2C_Scope.write("MEASUrement:GATing CURSor")
        time.sleep(2.0)
        self.myI2C_Scope.write("MEASUrement:IMMed:SOUrce1 CH1")
        self.myI2C_Scope.write("MEASUrement:IMMed:SOUrce2 CH2")
        self.myI2C_Scope.write("MEASUrement:IMMed:TYPe Delay")
        
        delayM = "MEASUrement:IMMed:DELay:EDGE1 Rise"
        self.myI2C_Scope.write("MEASUrement:REFLevel:PERCent:MID2 30")
        midref = "MEASUrement:REFLevel:PERCent:MID1 70"
        if Rise == False :     
            delayM = "MEASUrement:IMMed:DELay:EDGE1 FALL"
            midref = "MEASUrement:REFLevel:PERCent:MID1 30"
        self.myI2C_Scope.write(delayM)
        self.myI2C_Scope.write("MEASUrement:IMMed:DELay:EDGE2 RISE")
        print(self.myI2C_Scope.query('MEASUrement:IMMed:VALue?'))
        print(self.myI2C_Scope.query('MEASUrement:IMMed:UNIts?') )
        units[16] = self.myI2C_Scope.query('MEASUrement:IMMed:UNIts?')
        value[16] = self.myI2C_Scope.query('MEASUrement:IMMed:VALue?')
        


        self.myI2C_Scope.write("SAVe:IMAGe:FILEFormat PNG")
        self.myI2C_Scope.write("SAVe:IMAGe:INKSaver OFF")
        self.myI2C_Scope.write("HARDCopy STARt")
        imgData = self.myI2C_Scope.read_raw()
        
        imgFile = open(self.FILE_LOCATION+"\\"+self.FILE_NAME+"DataSetupTime.png", "wb")
        imgFile.write(imgData)
        imgFile.close()
        

        print("Screen Shot Saved")
        picList.write(self.FILE_NAME+"DataSetupTime.png\n")
        
        
    #Screen Shot for Start Condition Hold Time.
        print("Finding Start Condition Hold Time")
        print("=============")
        #Draw zoom 
        
        self.DrawZoom(t_start[0])
        
        
        #Check if we have a rising or Falling Edge
        
        vpos1 = "CURSor:VBArs:POSITION1 "+str(t_start[1]-Tdelta)
        vpos2 = "CURSor:VBArs:POSITION2 "+str(t_down[1]+Tdelta)
        self.myI2C_Scope.write(vpos1)
        self.myI2C_Scope.write(vpos2)
        time.sleep(3.0)
        print(self.myI2C_Scope.query("CURSor:VBArs:POSITION1?"))
        print(self.myI2C_Scope.query("CURSor:VBArs:POSITION2?"))
        time.sleep(2.0)
        print(self.myI2C_Scope.query("CURSor?"))
        self.myI2C_Scope.write("CURSor:SOUrce CH1")
        self.myI2C_Scope.write("CURSor:FUNCtion SCREEN")
        time.sleep(2.0)
        self.myI2C_Scope.write("MEASUrement:GATing CURSor")
        
        self.myI2C_Scope.write("MEASUrement:IMMed:SOUrce1 CH1")
        self.myI2C_Scope.write("MEASUrement:IMMed:SOUrce2 CH2")
        self.myI2C_Scope.write("MEASUrement:IMMed:TYPe Delay")
        
        delayM = "MEASUrement:IMMed:DELay:EDGE1 FALL"
        self.myI2C_Scope.write("MEASUrement:REFLevel:PERCent:MID2 30")
        midref = "MEASUrement:REFLevel:PERCent:MID1 30"
        self.myI2C_Scope.write(delayM)
        self.myI2C_Scope.write("MEASUrement:IMMed:DELay:EDGE2 FALL")
        print(self.myI2C_Scope.query('MEASUrement:IMMed:VALue?'))
        print(self.myI2C_Scope.query('MEASUrement:IMMed:UNIts?') )
        units[17] = self.myI2C_Scope.query('MEASUrement:IMMed:UNIts?')
        value[17] = self.myI2C_Scope.query('MEASUrement:IMMed:VALue?')
        
        
        
        
        
        
        
        
        self.myI2C_Scope.write("SAVe:IMAGe:FILEFormat PNG")
        self.myI2C_Scope.write("SAVe:IMAGe:INKSaver OFF")
        self.myI2C_Scope.write("HARDCopy STARt")
        imgData = self.myI2C_Scope.read_raw()

        imgFile = open(self.FILE_LOCATION+"\\"+self.FILE_NAME+"StartConditionHoldTime.png", "wb")
        imgFile.write(imgData)
        imgFile.close()
        

        print("Screen Shot Saved")
        picList.write(self.FILE_NAME+"StartConditionHoldTime.png\n")
       
        
        
    #Screen Shot for Stop Condition Set time up.
        print("Finding Stop Condition Setup Time")
        print("=============")
        #Draw zoom 
        
        self.DrawZoom(t_stop[0])
        
        
        #Check if we have a rising or Falling Edge
        
        vpos1 = "CURSor:VBArs:POSITION1 "+str(t_up[1]-Tdelta)
        vpos2 = "CURSor:VBArs:POSITION2 "+str(t_stop[1]+Tdelta)
        self.myI2C_Scope.write(vpos1)
        self.myI2C_Scope.write(vpos2)
        time.sleep(3.0)
        print(self.myI2C_Scope.query("CURSor:VBArs:POSITION1?"))
        print(self.myI2C_Scope.query("CURSor:VBArs:POSITION2?"))
        time.sleep(2.0)
        print(self.myI2C_Scope.query("CURSor?"))
        self.myI2C_Scope.write("CURSor:SOUrce CH1")
        self.myI2C_Scope.write("CURSor:FUNCtion SCREEN")
        time.sleep(2.0)
        self.myI2C_Scope.write("MEASUrement:GATing CURSor")
        
        self.myI2C_Scope.write("MEASUrement:IMMed:SOUrce1 CH2")
        self.myI2C_Scope.write("MEASUrement:IMMed:SOUrce2 CH1")
        self.myI2C_Scope.write("MEASUrement:IMMed:TYPe Delay")
        
        delayM = "MEASUrement:IMMed:DELay:EDGE1 Rise"
        self.myI2C_Scope.write("MEASUrement:REFLevel:PERCent:MID2 70")
        midref = "MEASUrement:REFLevel:PERCent:MID1 70"
        self.myI2C_Scope.write(delayM)
        self.myI2C_Scope.write("MEASUrement:IMMed:DELay:EDGE2 Rise")
        print(self.myI2C_Scope.query('MEASUrement:IMMed:VALue?'))
        print(self.myI2C_Scope.query('MEASUrement:IMMed:UNIts?') )
        units[18] = self.myI2C_Scope.query('MEASUrement:IMMed:UNIts?')
        value[18] = self.myI2C_Scope.query('MEASUrement:IMMed:VALue?')
    
    
    
    
    
    

        self.myI2C_Scope.write("SAVe:IMAGe:FILEFormat PNG")
        self.myI2C_Scope.write("SAVe:IMAGe:INKSaver OFF")
        self.myI2C_Scope.write("HARDCopy STARt")
        imgData = self.myI2C_Scope.read_raw()
        
        imgFile = open(self.FILE_LOCATION+"\\"+self.FILE_NAME+"StopConditionSetupTime.png", "wb")
        imgFile.write(imgData)
        imgFile.close()
        

        print("Screen Shot Saved")
        picList.write(self.FILE_NAME+"StopConditionSetupTime.png\n")
        
        self.myI2C_Scope.write("CURSor:FUNCtion SCREEN")
        self.myI2C_Scope.write("CURSor:SOUrce CH2 ")
        
        print("Writting data...\n")
        
        #writing to I2C Results file 
        for i in range(len(value)):
            results.write(str(value[i])+str(units[i])+"\n")
        results.close()
        picList.close()
        print("Data Saved!")
        self.TestPoints.close()
    

    
    
        