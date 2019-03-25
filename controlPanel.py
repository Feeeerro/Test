# -*- coding: utf-8 -*-
from Tkinter import *
from pynput import keyboard
import serial
import serial.tools.list_ports
import time
import threading
import driverSerial

class ControlPanel(object):
	def __init__(self):
#-------------------------------- VARIABILI GLOBALI -------------------------------------
		
		self.testo = ""
		self.firstConnection = True
		self.firstEntrance = True
		self.firstClick = True
		self.contaRighe = 0
		self.indexMatrix = 0
		self.input = 'start'
		self.bgConnection = "red"
		self.fileName = "instruction.txt"
		
		self.matrix = [["VEE", 3.25, 3.35],
						["VSCLE", 3.25, 3.35],
						["VSDAE", 3.25, 3.35],
						["CURRENT", 3.25, 3.35]]
			
#------------------------------ FINE VARIABILI GLOBALI ----------------------------------
		self.mainWindow = Tk()
		self.mainWindow.geometry("740x115+680+150")	# Ridimensiona la finestra all'avvio
		# Dichiarazione dell'oggetto che punta al file driverSerial.py
		self.serialCom = driverSerial.DriverSerial()
		# Il quadro principale si chiama 'mioContenitore1'
		self.mioContenitore1 = Frame(self.mainWindow)
		self.mioContenitore1.pack(side = LEFT)
		# Il quadro degli elementi superiori
		self.quadro_pulsanti = Frame(self.mioContenitore1, borderwidth = 5, background = "grey34")
		self.quadro_pulsanti.pack(side = TOP, fill = BOTH, expand = YES,)
		# quadro alto: contenitore di quadro_sinistra e quadro_destra
		self.quadro_alto = Frame(self.mioContenitore1, background = "white", borderwidth = 5, relief = RIDGE, height = 400, width = 750,)
		self.quadro_alto.pack_propagate(0)
		self.quadro_alto.pack(side = TOP, fill = BOTH, expand = 1,)
		# Gestione della casella di testo relativa alle porte
		self.com_in = Entry(self.quadro_pulsanti, width=10)
		self.com_in.configure(width = 30,)
		self.com_in.insert(END, 'Insert the correct port...')
		self.com_in.pack(side = LEFT,padx = "2m",)
		# Gestione del pulsante 'CONNECTION'
		self.connection = Button(self.quadro_pulsanti, command = self.connectionEvent)
		self.connection.configure(text = "CONNECTION", background = "red", width = 15)
		self.connection.configure(padx = "1m", pady = "2m",)
		self.connection.pack(side = LEFT, anchor = NE, expand = YES, fill = X,)
		self.connection.bind("<Return>", self.connectionEvent_a)
		# Gestione del pulsante 'LIST PORT'
		self.refresh = Button(self.quadro_pulsanti, command = self.list_port)
		self.refresh.configure(text = "LIST PORT", background = "dodger blue", width = 15)
		self.refresh.configure(padx = "1m", pady = "2m",)
		self.refresh.pack(side = LEFT, anchor = E, expand = YES, fill = X,)
		self.refresh.bind("<Return>", self.list_port_a)
		# Schermo superiore della finestra
		self.screen = Text(self.quadro_alto, takefocus = 0)
		self.main_scroll = Scrollbar(self.screen, orient="vertical", command=self.screen.yview)
		self.screen.configure(yscrollcommand=self.main_scroll.set, background = "pale turquoise")
		self.main_scroll.pack(side="right")
		self.screen.pack(side = TOP, anchor = N, fill="both")

	def enable_GUI(self):

		self.mainWindow.geometry("740x492+680+150")
		
	    
		# Riquadro basso (label, casella di testo, CONFIRM)
		self.quadro_basso = Frame(self.mioContenitore1, borderwidth = 5, background = "grey34",height = 110,)
		self.quadro_basso.pack(side = LEFT, fill = BOTH, expand = YES,)
		# Schermo di output
		self.screen_output = Text(self.quadro_alto, takefocus = 0)
		self.output_scroll = Scrollbar(self.screen_output, orient="vertical", command=self.screen_output.yview)
		self.screen_output.configure(yscrollcommand=self.output_scroll.set, width = 100)
		self.output_scroll.pack(side="right", fill="y")
		self.screen_output.insert(END, "OUTPUT:\n")
		self.screen_output.pack(side = LEFT, fill="both", expand = 1)
		self.screen_output.see("end")
		# Schermo di input
		self.screen_input = Text(self.quadro_alto, takefocus = 0)
		self.input_scroll = Scrollbar(self.screen_input, orient="vertical", command=self.screen_input.yview)
		self.screen_input.configure(yscrollcommand=self.input_scroll.set, width = 60)
		self.input_scroll.pack(side="right", fill="y")
		self.screen_input.insert(END, "INPUT:\n")
		self.screen_input.pack(side = LEFT, fill="both", expand = 1)
		self.screen_input.see("end")

#---------------------------------- FINESTRA ISTRZIONI ----------------------------------
		

#---------------- TOGLIERE I COMMENTI PER APRIRE FINESTRA DELLE ISTRUZIONI --------------

		self.inst_window = Toplevel()
		self.inst_window.geometry("650x750+0+0")

		self.inst_text = Text(self.inst_window)
		self.inst_scroll = Scrollbar(self.inst_window, orient="vertical", command=self.inst_text.yview)
		self.inst_text.configure(yscrollcommand=self.inst_scroll.set)
		self.inst_scroll.pack(side="right", fill="y")
		self.inst_text.pack(side="left", fill="both", expand=True)
		
		# Inserisce le istruzioni nella casella di testo
		f = open(self.fileName, "r")
		for line in f: 
			self.inst_text.insert(END, line)
		f.close()

		# Sezione che gestisce il testo delle istruzioni (colori, grassetto, grandezze...)
		self.inst_text.tag_add("title","1.0","1.11")
		self.inst_text.tag_config("title", font=("Times New Roman", 16, "bold"), foreground="red")
		self.inst_text.tag_add("subtitle","2.0","2.75")
		self.inst_text.tag_config("subtitle", font=("Times", 11, "bold"), foreground="black")
		self.inst_text.tag_add("red","4.49","4.68")
		self.inst_text.tag_config("red", foreground="red")
		self.inst_text.tag_add("gold","4.69","4.94")
		self.inst_text.tag_config("gold", foreground="gold")
		self.inst_text.tag_add("green","5.0","5.25")
		self.inst_text.tag_config("green", foreground="green")
		self.inst_text.tag_add("procedure","13.0","13.75")
		self.inst_text.tag_config("procedure", font=("Times New Roman", 16, "bold"), foreground="red")
		self.inst_text.tag_add("connected","15.32","15.42")
		self.inst_text.tag_config("connected", font=("Times New Roman", 11, "bold"), foreground="black")
		self.inst_text.tag_add("message","17.0","19.81")
		self.inst_text.tag_config("message", foreground="gold2")
		self.inst_text.tag_add("advice","19.29","19.80")
		self.inst_text.tag_config("advice", font=("Times New Roman", 11, "bold"),  foreground="gold3")
		self.inst_text.tag_add("confirm","22.23","22.30")
		self.inst_text.tag_config("confirm", font=("Times New Roman", 11, "bold"), foreground="black")
		self.inst_text.tag_add("errorMessage","27.72","28.36")
		self.inst_text.tag_config("errorMessage", foreground="red")
#----------------------------------------------------------------------------------------
#------------------------------- FINE FINESTRA ISTRUZIONI -------------------------------
		# Creazione dell'etichetta che indica i valori da calcolare
		self.label = Label(self.quadro_basso)
		self.label.configure(background = "white", borderwidth = 1, width = 8,)
		self.label.pack(side = LEFT, padx = "1m",)
		# Creazione della casella di testo relativa ai valori da inserire
		self.text_box = Entry(self.quadro_basso,)
		self.text_box.configure(width = 73,)
		self.text_box.insert(END, 'Write Here!')
		self.text_box.pack(side = LEFT,padx = "1m",)
		self.text_box.focus_force()
		# Gestione del pulsante 'CONFIRM'
		self.confirm = Button(self.quadro_basso, command = self.confirmEvent)
		self.confirm.configure(text = "CONFIRM", background = "green")
		self.confirm.configure(width = 30, padx = "1m", pady = "1m",)
		self.confirm.pack(side = LEFT)
		self.confirm.bind("<Return>", self.confirmEvent_a)
		self.confirm.bind("<KeyPress>", self.keydown)

#------------------------------------ SEZIONE FUNZIONI ----------------------------------
	# Le funzioni che terminano con _a gestiscono la conferma dei pulsanti con lo SPAZIO
	def confirmEvent_a(self,evento): 
		self.confirmEvent()
		
	def list_port_a(self,evento):
		self.list_port()

	def connectionEvent_a(self,evento):		
		self.connectionEvent()
	
	def keydown(self, e):
			print 1 
			print e.char
	
	# Funzione che gestisce gli eventi del tasto 'CONNECTION'
	def connectionEvent(self):
		self.connnectionInterface()
		if (self.firstConnection == True) and (self.bgConnection == "green"):			
			self.enable_GUI()
			self.delete_input_output_screen()
			self.firstConnection = False
			self.serialCom.serial_write('')
			self.thread = threading.Thread(target = self.printing_answer)
			self.thread.start()		
		self.contaRighe = 0

	# Funzione che gestisce gli eventi del tasto 'CONFIRM'
	def confirmEvent(self):
		# se la connessione non è attiva non attivare il tasto
		if(self.bgConnection != "red"):
		# gestisco l'eccezione nel caso si inseriscano stringhe
			try:			
				self.testo = self.text_box.get()
				#controllo che il valore inserito sia nell'intervallo
				self.value = float(self.testo)
				self.unit = self.matrix[self.indexMatrix]
				if ((self.value > self.unit[1]) and (self.value < self.unit[2])) or (self.firstClick == False):
					self.screen.delete(1.0, END)
					self.screen.insert(END, "Value is correct!")
					self.screen.tag_add("confirm_correct", "1.0", "1.50")
					self.screen.tag_config("confirm_correct", foreground="green4")
					self.serial_write_Interface(self.testo)
					self.stampaTesto()
					self.text_box.focus_force()
				else:
					self.screen.delete(1.0, END)
					self.screen.insert(END, "The value that you insert is not in the intervall...\nChange the value or click again CONFIRM to insert that value!")
					self.screen.tag_add("confirm_error", "1.0", "2.75")
					self.screen.tag_config("confirm_error", foreground="gold4")
					self.firstClick = False
					self.text_box.focus_force()
					
			except:
				self.screen.delete(1.0, END)
				self.screen.insert(END, "The value is not a number... Insert ONLY numbers in the text box!")
				self.screen.tag_add("string_error", "1.0", "1.75")
				self.screen.tag_config("string_error", foreground="red")
				self.text_box.focus_force()	
	# Funzione che aggiorna la lista delle porte e interrompe la connessione
	def list_port(self):
		self.serialCom.serial_close()
		if(self.bgConnection == "green"):
			self.connection.config(bg="gold")
			self.connection.config(text="Restore Connection")
			self.bgConnection = "red"
			self.delete_input_output_screen()
		self.screen.delete(1.0, END)
		ports = list(serial.tools.list_ports.comports())		# --> crea una lista contenenti le porte attive
		self.screen.insert(END, "List of available ports: \n")
		for p in ports:
			self.screen.insert(END, "-> " + str(p) + "\n")

		# questo ciclo aggiorna i colori del testo
		for i in range(30):
			if(i+1 != 1):
				self.screen.tag_add("list", str(i+1) + ".0", str(i+1) + ".02")
				self.screen.tag_add("list", str(i+1) + ".8", str(i+1) + ".75")
				self.screen.tag_add("port", str(i+1) + ".3", str(i+1) + ".07")
				self.screen.tag_config("list", foreground="blue")
				self.screen.tag_config("port", foreground="red")
			else:
				self.screen.tag_add("list", str(i+1) + ".0", str(i+1) + ".75")
				self.screen.tag_config("list", foreground="blue")
		self.screen.insert(END, "\n\n")
	# Funzione che inserisce nello schermo di input il testo inserito e restituisce OK se tutto è corretto
	def stampaTesto(self):
		self.screen_input.insert(END, str(self.contaRighe) + " - " + self.testo + " --> OK!" "\n")
		self.firstClick = True
		self.contaRighe += 1
		self.indexMatrix += 1
	# Funzione che gestisce gli eventi del tasto 'CONNECTION'
	def connnectionInterface(self):
		self.screen.delete(1.0, END)
		try:
			port = self.com_in.get()
			self.serialCom.serial_open(port)
			self.connection.config(bg="green")
			self.connection.config(text="Connection OK")
			self.bgConnection = "green"
			self.screen.insert(END, "Successful connection!\n...\nPort: " + port + "\n\n")
			self.screen.tag_add("success", "1.0", "1.25")
			self.screen.tag_config("success", foreground="green4")
		except:
			self.connection.config(bg="red")
			self.connection.config(text="Connection Error")
			self.bgConnection = "red"
			self.screen.insert(END, "Connection failed!\n\n")
			self.screen.tag_add("failure", "1.0", "1.25")
			self.screen.tag_config("failure", foreground="red")
	# Fuzione gestisce l'invio dei segnali all'hardware e la relativa interfaccia		
	def serial_write_Interface(self, messaggio):
		self.input = messaggio		
		try:
			self.serialCom.serial_isOpen()
			self.serialCom.serial_write(self.input)
		except:
			self.connection.config(bg="red")
			self.connection.config(text="Connection Error")
			self.bgConnection = "red"
			self.screen.delete(1.0, END)
			self.screen.insert(END, "Comunication Error...restore the connection and try again\n\n")
			self.screen.tag_add("failure", "1.0", "1.60")
			self.screen.tag_config("failure", foreground="red")
	# Funzione che stampa nello schermo di output la risposta dell'hardware
	def printing_answer(self):
		self.firstTime = True
		while True:
			if (self.serialCom.CHAR == unichr(10)):
				self.screen_output.insert(END, "> " + self.serialCom.OUTPUT)
				self.aggiornaLabel()
				self.serialCom.CHAR = ''
				self.serialCom.OUTPUT = ''
				
	def delete_input_output_screen(self):
		self.screen_input.delete(1.0, END)
		self.screen_output.delete(1.0, END)
		self.screen_output.insert(END, "OUTPUT:\n")
		self.screen_input.insert(END, "INPUT:\n")	
	# Funzione che cambia il contenuto della label (VEE, VSCLE, VSDAE, )
	def aggiornaLabel(self):
		#prendo la risposta dell'hardwere e stampo solo quello che chiede
		self.reverse = list(reversed(list(self.serialCom.OUTPUT)))
		if (self.firstEntrance == True) and (self.reverse[24] == ' '):
			self.text_label = self.reverse[25:28]
			self.firstEntrance = False
		else:
			self.text_label = self.reverse[23:28]
		self.text_label = list(reversed(self.text_label))
		''.join(self.text_label)
		self.label.configure(text = self.text_label)
		
#---------------------------------- FINE SEZIONE FUNZIONI -------------------------------		
	