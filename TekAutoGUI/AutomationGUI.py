#import ctkinter as ctk 
import customtkinter as ctk
import TekAutoI2C_Handler as I2C_Scope 
from PIL import Image
import TestRunTek as TrT

import os 


window = ctk.CTk()
ctk.set_appearance_mode("dark")
#ctk.set_default_color_theme("red")
window.geometry('900x980')
#window.config(background = "dark-blue" )
window.title("Celestica I2C Physical Signal Test")

#initial Conditions

WORKING_DIR = ""
FILE_NAME = ""
FILE_LOCATION = "" 


def ConvertHextoBin(HexString):
    tmp = list(HexString)
    hextmp = [None]*len(tmp)
    for i in range(len(tmp)): 
        if tmp[i] == '0':
            hextmp[i] = '0000'    
        elif tmp[i] =='1':
            hextmp[i] = '0001'
        elif tmp[i] =='2':
            hextmp[i] = '0010'
        elif tmp[i] =='3':
            hextmp[i] = '0011'
        elif tmp[i] =='4':
            hextmp[i] = '0100'
        elif tmp[i] =='5':
            hextmp[i] = '0101'
        elif tmp[i] =='6':
            hextmp[i] = '0110'
        elif tmp[i] =='7':
            hextmp[i] = '0111'
        elif tmp[i] =='8':
            hextmp[i] = '1000'
        elif tmp[i] =='9':
            hextmp[i] = '1001'
        elif tmp[i] =='A' or tmp[i] == 'a':
            hextmp[i] = '1010'
        elif tmp[i] =='B' or tmp[i] == 'b':
            hextmp[i] = '1011'
        elif tmp[i] =='C' or tmp[i] == 'c':
            hextmp[i] = '1100'
        elif tmp[i] =='D' or tmp[i] == 'd':
            hextmp[i] = '1101'
        elif tmp[i] =='E' or tmp[i] == 'e':
            hextmp[i] = '1110'
        elif tmp[i] =='F' or tmp[i] == 'f':
            hextmp[i] = '1111'
            
    hexfinal = ''
    for hexval in hextmp:
        hexfinal = hexfinal+hexval
    return(hexfinal[1:])


def on_click_savePath():
    global WORKING_DIR
    window.filename = ctk.filedialog.askdirectory()
    print(window.filename)
    WORKING_DIR = str(window.filename)
    print(WORKING_DIR)
    lbl.configure(text="Now saving in : "+WORKING_DIR)

def create_Directory():
    global WORKING_DIR
    global lbl_testFileName 
    lbl_testFileName.configure(text="Scope Running...")
    print(WORKING_DIR)
    HEXVALUE = ConvertHextoBin(address_entry.get())
    StringIP =  "TCPIP0::"+entryIP.get()+"::inst0::INSTR"
    BertScope = I2C_Scope.I2C_Scope(FILE_NAME=entry.get(),FILE_LOCATION=WORKING_DIR,adress=HEXVALUE,visa_address=StringIP)
    BertScope.runI2C()
    global my_image
    my_image.configure(light_image=Image.open(WORKING_DIR+"\\"+entry.get()+"\\"+entry.get()+".png"))
    lbl_testFileName.configure(text="Enter Test File Name")
    finishLabel.configure(text="File Saved at: "+WORKING_DIR+"\\"+entry.get()+"\\"+entry.get())

def create_Report():
    global WORKING_DIR
    a = WORKING_DIR
    a.replace("/","\\")
    print(a)
    #print(WORKING_DIR)
    TrT.runTek(WORK_DIR=a,RN=entryReport.get())


def get_filename():
    text = entry.get()
    entry.delete(0,ctk.END)
    FILE_NAME = text 
    print(FILE_NAME)

frame = ctk.CTkFrame(window)
frame.grid(row=1,column = 2, columnspan=10)

DirFrame = ctk.CTkFrame(window)
DirFrame.grid(row = 0, column = 2, columnspan=10,padx=(20, 20), pady=(20, 20),)


btn = ctk.CTkButton(DirFrame, text="Select Working Directory", command = on_click_savePath,fg_color='#bf1616',hover_color='#9f0404')
btn.grid(row= 0, column = 0,padx=(20, 20), pady=(20, 20), sticky="nsew")

lbl = ctk.CTkLabel(DirFrame, text = "No Working Directory Selected")
lbl.grid(row = 0, column = 1,columnspan=3,padx=(20, 20), pady=(20, 20), sticky="nsew")

lbl_IP = ctk.CTkLabel(frame, text = "Please Enter IP Adress of Scope")
lbl_IP.grid(row = 1, column = 0,padx=(20, 20), pady=(20, 20), sticky="nsew")
entryIP = ctk.CTkEntry(frame)
entryIP.grid(row=1, column=1)

lbl_testFileName = ctk.CTkLabel(frame, text = "Enter Test File Name")
lbl_testFileName.grid(row = 2, column = 0,padx=(20, 20), pady=(20, 20), sticky="nsew")

entry = ctk.CTkEntry(frame)
entry.grid(row=2,column=1)




lbl_add = ctk.CTkLabel(frame, text = "Please Enter I2C Adress")
lbl_add.grid(row = 5, column = 0,padx=(20, 20), pady=(20, 20), sticky="nsew")

address_entry = ctk.CTkEntry(frame)
address_entry.grid(row=5,column=1)

btnRunTest = ctk.CTkButton(frame, text="RunTest", command = create_Directory,fg_color='#bf1616',hover_color='#9f0404')
btnRunTest.grid(row= 6, column = 0,columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

finishLabel = ctk.CTkLabel(frame, text = "")
finishLabel.grid(row = 7, column = 0, sticky="nsew")

entryReport = ctk.CTkEntry(frame)
entryReport.grid(row=8,column=1)
entrylbl_add = ctk.CTkLabel(frame, text = "Please enter Report name")
entrylbl_add.grid(row = 8, column = 0,padx=(20, 20), pady=(20, 20), sticky="nsew")
entrybtn = ctk.CTkButton(frame, text="Generate Report", command = create_Report,fg_color='#bf1616',hover_color='#9f0404')
entrybtn.grid(row= 8, column = 2,padx=(20, 20), pady=(20, 20), sticky="nsew")




frame_Image = ctk.CTkFrame(window)
frame_Image.grid(row=2,column = 2, columnspan=5,padx=(20, 20), pady=(20, 20))






my_image = ctk.CTkImage(light_image=Image.open("C:\\Users\\us62019230\\Documents\\PythonScripts\\TekAutoGUI\\CLS_Logo.png"),size=(750, 450))


image_label = ctk.CTkLabel(frame_Image, image=my_image, text="")
image_label.grid(row=6,column=0,padx=(20, 20), pady=(20, 20), sticky="nsew")
window.mainloop()

