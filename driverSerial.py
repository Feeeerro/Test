# -*- coding: utf-8 -*-
from Tkinter import *
import serial
import serial.tools.list_ports
import time
import threading
import controlPanel

class DriverSerial(object):
	def __init__(self):
#-------------------------------- VARIABILI GLOBALI -------------------------------------
		self.ser = serial.Serial(
			baudrate=9600,
			parity=serial.PARITY_ODD,
			stopbits=serial.STOPBITS_TWO,
			bytesize=serial.SEVENBITS,
			timeout= None
		)
		self.OUTPUT = ''
		self.CHAR = ''	
#------------------------------ FINE VARIABILI GLOBALI ---------------------------------- 
	# APRO LA PORTA CORRETTA E FACCIO PARTIRE IL THREAD
	def serial_open(self, port):
		self.ser.port = port
		self.ser.open()                                             
		self.thread = threading.Thread(target = self.polling_usb_data)
		self.thread.start()
	# SCRIVO ALL'HARDWARE TRAMITE IL COLLEGAMENTO SERIALE
	def serial_write(self, messaggio):
		self.input = messaggio
		self.ser.write(self.input + '\r\n')
	# GESTISCO CON UN THREAD LA RISPOSTA DELL'HARDWARE
	def polling_usb_data(self):	
		while True:
			if self.ser.isOpen():   
				time.sleep(1)
				while self.ser.inWaiting() > 0:
					self.CHAR = self.ser.read(1)
					self.OUTPUT += self.CHAR
			else:
				self.connection_bn.config(bg="red")
				self.connection_bn.config(text="Connection Error")
	# CHIUDO LA PORTA SERIALE
	def serial_close(self):
		self.ser.close()
	# CONTROLLO SE LA PORTA È GIÀ APERTO	
	def serial_isOpen(self):
		self.ser.isOpen()

serialCom = DriverSerial()