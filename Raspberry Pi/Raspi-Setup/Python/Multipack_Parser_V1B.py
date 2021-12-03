# Parser Multipack

import threading
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font as tkFont
import re
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
# imports for sockets
import socket
import sys

# IP Address of the Robot - Set to localhost only for testing
robot_ip = '192.168.0.1'

# Konstanten
#PATH_USB_STICK     = '/home/pi/python/'
PATH_USB_STICK  = '' 

# Konstanten für Datenstruktur
#List Index
LI_PALETTE_DATA = 0
LI_PACKAGE_DATA = 1
LI_LAYERTYPES = 2
LI_NUMBER_OF_LAYERS = 3
#Palette Values
LI_PALETTE_DATA_LENGTH = 0
LI_PALETTE_DATA_WIDTH = 1
LI_PALETTE_DATA_HEIGHT = 2
#Package Values
LI_PACKAGE_DATA_LENGTH = 0
LI_PACKAGE_DATA_WIDTH = 1
LI_PACKAGE_DATA_HEIGHT = 2
LI_PACKAGE_DATA_GAP = 3
#Position Values
LI_POSITION_XP = 0
LI_POSITION_YP = 1
LI_POSITION_AP = 2
LI_POSITION_XD = 3
LI_POSITION_YD = 4
LI_POSITION_AD = 5
LI_POSITION_NOP = 6
LI_POSITION_XVEC = 7
LI_POSITION_YVEC = 8
#Number of Entries
NOE_PALETTE_VALUES = 3
NOE_PACKAGE_VALUES = 4
NOE_LAYERTYPES_VALUES = 1
NOE_NUMBER_OF_LAYERS = 1
NOE_PACKAGE_PER_LAYER = 1
NOE_PACKAGE_POSITION_INFO = 9

#Globale Variablen

#Dateiname abfragen
def UR_SetFileName(Artikelnummer):
    global FILENAME
    
    FILENAME = (Artikelnummer + '.rob')
    #print(FILENAME)    
    return FILENAME    

#Daten auslesen
def UR_ReadDataFromUsbStick():
    global g_PalettenDim
    global g_PaketDim
    global g_LageArten
    global g_Daten
    global g_LageZuordnung
    global g_PaketPos
    global g_AnzahlPakete
    global g_AnzLagen
    global g_PaketeZuordnung
    global g_Zwischenlagen
    global g_Startlage
    
    
    g_Daten = []
    g_LageZuordnung = []
    g_PaketPos = []
    g_PaketeZuordnung = []
    g_Zwischenlagen = []
    
    try:
        with open(PATH_USB_STICK + FILENAME) as file:
            
            for line in file:
                str = line.strip()
                tmpList = line.split('\t')
                
                for i in range(len(tmpList)):
                    tmpList[i] = int(tmpList[i])
                    
                g_Daten.append(tmpList)
 
 
            pl = g_Daten[LI_PALETTE_DATA][LI_PALETTE_DATA_LENGTH]
            pw = g_Daten[LI_PALETTE_DATA][LI_PALETTE_DATA_WIDTH]
            ph = g_Daten[LI_PALETTE_DATA][LI_PALETTE_DATA_HEIGHT]
            g_PalettenDim = [pl, pw, ph]
            
            #Kartondaten
            pl = g_Daten[LI_PACKAGE_DATA][LI_PACKAGE_DATA_LENGTH]
            pw = g_Daten[LI_PACKAGE_DATA][LI_PACKAGE_DATA_WIDTH]
            ph = g_Daten[LI_PACKAGE_DATA][LI_PACKAGE_DATA_HEIGHT]
            pr = g_Daten[LI_PACKAGE_DATA][LI_PACKAGE_DATA_GAP]
            g_PaketDim = [pl, pw, ph, pr]
            
            #Lagearten
            g_LageArten = g_Daten[LI_LAYERTYPES][0]
            
            #Lagenzuordnung
            anzLagen = g_Daten[LI_NUMBER_OF_LAYERS][0]
            g_AnzLagen = anzLagen


            index       = LI_NUMBER_OF_LAYERS + 2
            end_index   = index + anzLagen


            while index < end_index:
                
                lagenart = g_Daten[index][0]
                zwischenlagen = g_Daten[index][1]

                g_LageZuordnung.append(lagenart)
                g_Zwischenlagen.append(zwischenlagen)
            
                index = index +1
            
            #Paketpositionen
            ersteLage   = 4 + (anzLagen + 1)
            index       = ersteLage
            anzahlPaket = g_Daten[index][0]
            g_AnzahlPakete = anzahlPaket #Achtung veraltet - Anzahl der Picks bei Multipick
            index_paketZuordnung = index
            
            for i in range(g_LageArten):
                
                anzahlPick = g_Daten[index_paketZuordnung][0]
                g_PaketeZuordnung.append(anzahlPick)
                index_paketZuordnung = index_paketZuordnung + anzahlPick + 1
                
            
            for i in range(g_LageArten):            
                index = index + 1 #Überspringe die Zeile mit der Anzahl der Pakete
                anzahlPaket = g_PaketeZuordnung[i]
                
                for j in range(anzahlPaket):
                    xp = g_Daten[index][LI_POSITION_XP]
                    yp = g_Daten[index][LI_POSITION_YP]
                    ap = g_Daten[index][LI_POSITION_AP]
                    xd = g_Daten[index][LI_POSITION_XD]
                    yd = g_Daten[index][LI_POSITION_YD]
                    ad = g_Daten[index][LI_POSITION_AD]
                    nop = g_Daten[index][LI_POSITION_NOP]
                    xvec = g_Daten[index][LI_POSITION_XVEC]
                    yvec = g_Daten[index][LI_POSITION_YVEC]
                    packagePos = [xp, yp, ap, xd, yd, ad, nop, xvec, yvec]
                    g_PaketPos.append(packagePos)
                    index = index + 1    

            return 0                
    except:
        print("Error")
        print(FILENAME)
    return 1

def UR_Palette():
    return g_PalettenDim

def UR_Karton():
    return g_PaketDim

def UR_Lagen():
    return g_LageZuordnung

def UR_Zwischenlagen():
    return g_Zwischenlagen

def UR_PaketPos(Nummer):
    print(Nummer)
    return g_PaketPos[Nummer]

def UR_AnzLagen():
    return g_AnzLagen

def UR_AnzPakete():
    return g_AnzahlPakete

def UR_PaketeZuordnung():
    return g_PaketeZuordnung

def UR_Paket_hoehe():
    g_Startlage = int(karton_int.get())
    return g_Startlage

def UR_Startlage():   
    g_PaketDim[2] = int(lage_spin.get())
    return g_PaketDim[2]


def Server_start():
    #server_stop_btn.configure(state="normal")
    global server
    server = SimpleXMLRPCServer(("", 8080), allow_none=True)
    print ("Start Server")
    server.register_function(UR_SetFileName, "UR_SetFileName")
    server.register_function(UR_ReadDataFromUsbStick, "UR_ReadDataFromUsbStick")
    server.register_function(UR_Palette, "UR_Palette")
    server.register_function(UR_Karton, "UR_Karton")
    server.register_function(UR_Lagen, "UR_Lagen")
    server.register_function(UR_Zwischenlagen, "UR_Zwischenlagen")
    server.register_function(UR_PaketPos, "UR_PaketPos")
    server.register_function(UR_AnzLagen, "UR_AnzLagen")
    server.register_function(UR_AnzPakete, "UR_AnzPakete") #Veraltet - nicht mehr verwenden
    server.register_function(UR_PaketeZuordnung, "UR_PaketeZuordnung") #Picks pro Lage
    server.register_function(UR_Paket_hoehe, "UR_Paket_hoehe") #Gemessene Pakethöhe
    server.register_function(UR_Startlage, "UR_Startlage") #Startlage für Neustart
    #print ("Oeffne serielle Schnittstelle")
    #ser = serial.Serial('/dev/ttyUSB0', 115200, timeout = 0.5)
    #print ("Serielle Schnittstelle " + ser.name + " 115200Baud")
    roboter_btn.configure(state="normal")
    server.serve_forever()
    #print ("Server läuft")
    return 0

def Server_stop():
    server.shutdown()

def Server_thread():
    xServerThread = threading.Thread(target=Server_start)
    xServerThread.start()

def Send_cmd_play():
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect the socket to the port where the server is listening
        server_address = (robot_ip, 29999)
        print ('connecting to %s port %s' %(server_address))
        sock.connect(server_address)
        
        # Send data
        message = 'play\n'
        print ('sending %s' %(message))
        sock.sendall(message.encode('utf-8'))
        
        # Print any response
        data = sock.recv(4096)
        print ('received %s' %(data))
        
    finally:
        print ('closing socket')
        sock.close()

def Send_cmd_pause():
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect the socket to the port where the server is listening
        server_address = (robot_ip, 29999)
        print ('connecting to %s port %s' %(server_address))
        sock.connect(server_address)
        
        # Send data
        message = 'pause\n'
        print ('sending %s' %(message))
        sock.sendall(message.encode('utf-8'))
        
        # Print any response
        data = sock.recv(4096)
        print ('received %s' %(data))
        
    finally:
        print ('closing socket')
        sock.close()

def Send_cmd_stop():
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect the socket to the port where the server is listening
        server_address = (robot_ip, 29999)
        print ('connecting to %s port %s' %(server_address))
        sock.connect(server_address)
        
        # Send data
        message = 'stop\n'
        print ('sending %s' %(message))
        sock.sendall(message.encode('utf-8'))
        
        # Print any response
        data = sock.recv(4096)
        print ('received %s' %(data))
        
    finally:
        print ('closing socket')
        sock.close()


#GUI

window = tk.Tk()

window.title("Paletierer")
window.geometry('1280x415')

helv = tkFont.Font(family='Helvetica', size=20, weight='bold')

tab_control = ttk.Notebook(window)

tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab_control.add (tab1, text='Palettierplan')
tab_control.add (tab2, text='Roboter')
tab_control.add (tab3, text='Aufnahmeposition')

#Palettierplan

lbl   = Label(tab1, text="Paletierplan:", pady=10, font=helv)
txt   = Entry(tab1, width=20, font=helv)

def laden():

    plan = txt.get()
    UR_SetFileName(plan)
    Err=UR_ReadDataFromUsbStick()

    if(Err == 0):
       rueck.configure(text= "erfolgreich geladen", fg="green")
       max_lage = UR_AnzLagen()
       lage_spin.configure(state="normal", to=max_lage)
       karton_int.configure(state="normal")
       karton_int.delete(0, END)
       karton_int.insert(0, g_PaketDim[2])
       server_btn.configure(state="normal")
       
    else:
        rueck.configure(text="Fehler beim Laden", fg="red")
        lage_spin.configure(state="disable", to=2)
        karton_int.configure(state="disable")
        server_btn.configure(state="disable")
        #server_stop_btn.configure(state="disable")

btn   = Button(tab1, text="Laden", command=laden, font=helv)
rueck = Label(tab1, text="kein Plan geladen", pady=10, font=helv)

lage_lbl = Label(tab1, text="Startlage wählen:", pady=10, font=helv)
lage_spin = Spinbox(tab1, from_=1, to=2, state=DISABLED, font=helv)

karton_lbl = Label(tab1, text="Kartonhöhe wählen:", pady=10, font=helv)
karton_int = Entry(tab1, width=22, state=DISABLED, font=helv)

server_btn = Button(tab1, text="Daten an Roboter senden", state=DISABLED, command=Server_thread, font=helv)

#server_stop_btn = Button(tab1, text="Stop RPC Server", state=DISABLED, font=helv, command=Server_stop)

#send_robot_cmd_play_btn = Button(tab1, text="Play", font=helv, command=Send_cmd_play)
send_robot_cmd_pause_btn = Button(tab1, text="Roboter Pause", font=helv, command=Send_cmd_pause)
send_robot_cmd_stop_btn = Button(tab1, text="Roboter Stop", font=helv, command=Send_cmd_stop)
roboter_btn = Button(tab1, text="Palettierung starten", state=DISABLED, command=Send_cmd_play, font=helv)

lbl.grid(column=0, row=0, sticky = W)
txt.grid(column=1, row=0, sticky = W)
btn.grid(column=2, row=0)
rueck.grid(column=3, row=0)
lage_lbl.grid(column=0, row=1, sticky = W)
lage_spin.grid(column=1, row=1, sticky = W)
karton_lbl.grid(column=0, row=2, sticky = W)
karton_int.grid(column=1, row=2, sticky = W)
server_btn.grid(column=0, columnspan=2, row=3)
roboter_btn.grid(column=2, columnspan=2, row=3)
#server_stop_btn.grid(column=0, columnspan=2, row=4)
#send_robot_cmd_play_btn.grid(column=0, columnspan=2, row=5)
send_robot_cmd_pause_btn.grid(column=0, columnspan=2, row=4)
send_robot_cmd_stop_btn.grid(column=2, columnspan=2, row=4)
tab1.columnconfigure(0, pad=10)
tab1.columnconfigure(1, pad=10)
tab_control.pack(expand=1, fill='both')

window.mainloop()






