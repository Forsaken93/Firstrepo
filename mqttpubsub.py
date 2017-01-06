import paho.mqtt.client as mqtt
import time 
import threading
import tkinter as tk
from tkinter import *
from re import findall
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as md
import numpy as np
import datetime as dt


grzalka = 'READ'
dozownik = 'READ'
swiatlo = 'READ'
temperatura = '11'
data = 'READ'
wentylator = 'READ'


def on_connect(mosq, obj, rc):
         mqttc.subscribe("f", 0)
         print("rc: " + str(rc))

def on_message(mosq, obj, msg):
         global grzalka
         global dozownik
         global temperatura
         global data
         global swiatlo
         global wentylator
         print(msg.topic +" " + str(msg.qos) + " " + str(msg.payload))
         
         if msg.topic == 'grzalka':
                  grzalka = msg.payload
         elif msg.topic == "dozownik":
                  dozownik = msg.payload
         elif msg.topic == "temperatura":
                  temperatura = msg.payload
                  temperatura = temperatura.decode("utf-8")
                  temperatura = float(temperatura)
         elif msg.topic == "data":
                  data = msg.payload
                  data = data.decode("utf-8")
                  
         elif msg.topic == "swiatlo":
                  swiatlo = msg.payload
         elif msg.topic == "wentylator":
                  wentylator = msg.payload
         else:
                  print()

         
def on_publish(mosq, obj, mid):
         print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
         print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
         print(string)

mqttc = mqtt.Client()

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
#Connect
mqttc.connect("192.168.1.100", 1883, 60)
mqttc.subscribe("grzalka", qos=0)
mqttc.subscribe("wentylator", qos=0)
mqttc.subscribe("dozownik", qos=0)
mqttc.subscribe("temperatura", qos=0)
mqttc.subscribe("swiatlo", qos=0)
mqttc.subscribe("data", qos=0)
#Continue the network loop

mqttc.loop_start()


root = Tk()
frame = Frame(root, width=1200, height=800)
frame.pack()



mainlabel = Label(frame, text = "Obsługa akwarium roślinnego", font="helvetica 30 bold", fg="green")
mainlabel.grid(row = 0, columnspan = 6, column = 0)

plt.ion()
x = []
y = []


#dates = md.date2num(list_of_datetimes)
dates = [dt.datetime.now() + dt.timedelta(hours=i) for i in range (60)]

def plot():
         y.append(temperatura)
         x.append(time.time())
         f = Figure(figsize = (10,5), dpi=100)
         a = f.add_subplot(111)
         lines, = a.plot([],[])
         a.set_autoscaley_on(True)
         a.set_xlabel('czas [sec]')
         a.set_ylabel('temperatura [*C]')
         lines.set_ydata(y)
         lines.set_xdata(x)
         #f.autofmt_xdate()
         
         a.relim()
         a.autoscale_view()
         canvas = FigureCanvasTkAgg(f, master = frame)
         canvas.show()
         canvas.get_tk_widget().grid(column = 0, columnspan=5, row = 7)
         threading.Timer(10,plot).start()
plot()


#definicja sprawdzajca datę
def check_data():
         varData.set(data)
         threading.Timer(1,check_data).start()
         dat = data[:10]
         now = time.gmtime(time.time())        

         if now.tm_min % 10 ==0:
                  if now.tm_sec % 59 ==0:                           
                           f = open(dat, 'a')
                           f.write(str(data) + (' ') + str(temperatura) + '\n')
                           f.close()





varData = StringVar(root)
labData = Label(frame, textvariable = varData, font="verdena 20 bold")
labData.grid(column = 4, row = 1)
labData1 = Label(frame, text = "data i czas: ", font="verdena 20 bold")
labData1.grid(column = 3, row = 1)
check_data()

# kontrolka temperatury
#definicja sprawdzająca temperaturę

def check_temp():
         varTemp.set(temperatura)
         threading.Timer(1,check_temp).start()
#definicja wyciągająca temperaturę 

         
         
         
#wyświetlanie temperatury w oknie 
varTemp = StringVar(root)
labTemp = Label(frame, textvariable = varTemp, font="verdena 20 bold")
labTemp.grid(column = 1, row = 1)
check_temp()


labtemp1= Label(frame, text = "Temperatura w akwarium wynosi: ", font="verdena 20 bold")
labtemp1.grid(column = 0, row = 1)
#Zapisywanie temperatury do pliku .txt

#Obsuga przycisków wyboru trybu pracy 
labster = Label(frame, text = "Sterowanie manualne", font="verdena 20 bold")
labster.grid(column = 0, row = 2)
sterauto = Button(frame, text="tryb auto", font="-weight bold") #Przycisk włączania
sterauto.config(height = 2, width = 30)
sterauto.grid(row = 2, column = 1)

stermanual = Button(frame, text="tryb manual", font="-weight bold") #Przycisk wyłączania
stermanual.config(height = 2, width = 30)
stermanual.grid(row = 2, column = 2)




#Definicja przycisku wysyłającego sygnał włącz/wyłącz zawór co2                  
def sendValveOn(event):
         mqttc.publish("inTopic", '2')

def sendValveOff(event):
         mqttc.publish("inTopic", '3')
         
        
#definicja funkcji sprawdzającej status dozownika co2
def check():
         var1.set(dozownik)
         threading.Timer(1,check).start()


var1 = StringVar(root)
label_1 = Label(frame, textvariable = var1, font="verdena 20 bold")
label_1.grid(row = 3, column = 0)

check()




#przyciski obsługi zaworu CO2

co2_on = Button(frame, text="CO2 ON", font="-weight bold") #Przycisk włączania
co2_on.config(height = 2, width = 30)
co2_on.bind("<Button-1>", sendValveOn)
co2_on.grid(row = 3, column = 1)

co2_off = Button(frame, text="CO2 OFF", font="-weight bold") #Przycisk wyłączania
co2_off.config(height = 2, width = 30)
co2_off.bind("<Button-1>", sendValveOff)
co2_off.grid(row = 3, column = 2)



#definicje przycisków włącz wyłącz grzalke

def sendHeatOn(event):
         mqttc.publish("inTopic", '1')

def sendHeatOff(event):
         mqttc.publish("inTopic", '0')

#definicja funkcji sprawdzającej status podgrzewania
def check_heat():
         var2.set(grzalka)
         threading.Timer(1,check_heat).start()



var2 = StringVar(root)
label_2 = Label(frame, textvariable = var2, font="verdena 20 bold")
label_2.grid(row =4, column = 0)
check_heat()

#przyciski obsługi grzałki

heat_on = Button(frame, text="podgrzewanie ON", font="-weight bold") #przycisk włączania
heat_on.config(height = 2, width = 30)
heat_on.bind("<Button-1>", sendHeatOn)
heat_on.grid(column = 1, row = 4)

heat_off = Button(frame, text="podgrzewanie OFF", font="-weight bold") #przycisk wyłączania
heat_off.config(height = 2, width = 30)
heat_off.bind("<Button-1>", sendHeatOff)
heat_off.grid(column = 2, row = 4)


#definicje przycisków włącz wyłącz wentylator

def sendFanOn(event):
         mqttc.publish("inTopic", '6')

def sendFanOff(event):
         mqttc.publish("inTopic", '7')

#definicja funkcji sprawdzającej status wentylatora
def check_fan():
         var3.set(wentylator)
         threading.Timer(1,check_fan).start()



var3 = StringVar(root)
label_3 = Label(frame, textvariable = var3, font="verdena 20 bold")
label_3.grid(row =5, column = 0)
check_fan()

#przyciski obsługi wentylatora

fan_on = Button(frame, text="wentylator ON", font="-weight bold") #przycisk włączania
fan_on.config(height = 2, width = 30)
fan_on.bind("<Button-1>", sendFanOn)
fan_on.grid(column = 1, row = 5)

fan_off = Button(frame, text="wentylator OFF", font="-weight bold") #przycisk wyłączania
fan_off.config(height = 2, width = 30)
fan_off.bind("<Button-1>", sendFanOff)
fan_off.grid(column = 2, row = 5)




#definicje przycisków włącz wyłącz oświetlenie

def sendLightOn(event):
         mqttc.publish("inTopic", '4')

def sendLightOff(event):
         mqttc.publish("inTopic", '5')

#definicja funkcji sprawdzającej status oświetlenia
def check_light():
         var4.set(swiatlo)
         threading.Timer(1,check_light).start()

var4 = StringVar(root)
label_4 = Label(frame, textvariable = var4, font="verdena 20 bold")
label_4.grid(row =6, column = 0)
check_light()

#przyciski obsługi oświetlenia

light_on = Button(frame, text="oswietlenie ON", font="-weight bold") #przycisk włączania
light_on.config(height = 2, width = 30)
light_on.bind("<Button-1>", sendLightOn)
light_on.grid(column = 1, row = 6)

light_off = Button(frame, text="oswietlenie OFF", font="-weight bold") #przycisk wyłączania
light_off.config(height = 2, width = 30)
light_off.bind("<Button-1>", sendLightOff)
light_off.grid(column = 2, row = 6)



root.mainloop()
root.update_idletasks()
