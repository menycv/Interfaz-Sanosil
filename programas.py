from tkinter import *
# import RPi.GPIO as GPIO
from datetime import date, datetime

class Programas():
	def __init__(self, root, root_frame, previous_frame, programa):
		self.root = root
		self.root_frame = root_frame
		self.previous_frame = previous_frame
		self.program = programa
		self.root.fecha_inicio = date.today()
		self.root.hora_inicio = datetime.now().strftime("%H:%M:%S")

		if self.program == "Normal":
			self.normal()
		elif self.program == "Step":
			self.step()
		elif self.program == "Testing":
			self.testing()
		elif self.program == "Manual":
			self.manual()

	def set_previous_frame(self, previous_frame):
		self.previous_frame = previous_frame

	def normal(self):
			self.inicio = 0
			self.root.ml = 0
			self.tiempo_salida = 5

			self.root.color_alertas = "orange"
			self.previous_frame.alertas_frame.config(bg=self.root.color_alertas)
			self.previous_frame.alertas_label.config(bg=self.root.color_alertas)
			self.root.mensaje = "STATUS: Comenzando a operar salga de la habitación en " + str(self.tiempo_salida) + " seg"
			self.previous_frame.alertas_label.config(text=self.root.mensaje)
			if self.root.concentracion != 0 and self.root.vol != 0:
				self.total_ml = self.root.concentracion * self.root.vol
				self.root.after(1000, self.salida_start)
				self.tiempo_a_sanitizar = 2 * self.total_ml

	def salida_start(self):
		self.tiempo_salida = self.tiempo_salida - 1
		if self.root_frame.current_menu == "START/STOP":
			self.root.mensaje = "STATUS: Comenzando a operar salga de la habitación en " + str(self.tiempo_salida) + " seg"
			self.previous_frame.alertas_label.config(text=self.root.mensaje)
		if self.tiempo_salida == 0:
			self.root.color_alertas = self.root.color
			if self.root_frame.current_menu =="START/STOP":
				self.previous_frame.alertas_frame.config(bg=self.root.color_alertas)
				self.previous_frame.alertas_label.config(text=self.root.mensaje,
					bg=self.root.color_alertas)
			self.root.pin_on(self.root.bomba_entrada, 0)
			self.root.after(100, self.measure_ml)
		else:
			self.root.after(1000, self.salida_start)

	def step(self):
		pass

	def testing(self):
		pass

	def manual(self):
		pass

	def measure_ml(self):
            if self.root.current_button_state == 1:
                # flujo en ml/s
                # self.flujo = ((self.root.pulsos/0.1)/80)*(1000/60)
                self.flujo = 12.5
                self.root.pulsos = 0
                self.root.ml = self.root.ml + (self.flujo * .1)
                self.root.mensaje = "STATUS: LLENANDO; " + str(self.root.ml) + " ml UTILIZADOS"
                if self.root_frame.current_menu == "START/STOP":
                    self.previous_frame.alertas_label.config(text=self.root.mensaje)

                # if GPIO.input(self.root.flotador) == 0:
                #     self.root.pin_on(self.root.bomba_entrada, 1)
                #     self.root.after(120000, self.llenar_tanque)
                if self.root.ml >= 300 and self.inicio == 0:
                    self.inicio = 1
                    self.root.ml = 0
                    self.root.after(100, self.measure_ml)
                    self.root.tanque_lleno = 1
                elif self.root.ml >= self.total_ml and self.inicio == 1:
                    # Fin de programa
                    self.root.pin_on(self.root.bomba_entrada, 1)
                    self.root.mensaje = "STATUS: SANITIZANDO "
                    if self.root_frame.current_menu == "START/STOP":
                        self.previous_frame.alertas_label.config(text=self.root.mensaje)
                    self.root.after(1000, self.terminar_normal)
                else:
                    # Después de 100 ms se vuelven a medir los ml
                    self.root.after(100, self.measure_ml)
            else:
                self.root.pulses = 0
                self.root.ml = 0
                self.root.pin_on(self.root.bomba_entrada, 1)
                self.root.pin_on(self.root.bomba_salida, 0)
                self.root.after(80000, self.apagar_bomba)

	def terminar_normal(self):
		if self.root.current_button_state == 1:
			self.tiempo_a_sanitizar = self.tiempo_a_sanitizar - 1
			self.root.mensaje = "STATUS: TERMINANDO SANITIZADO EN  " + str(self.tiempo_a_sanitizar) + " SEG"
			if self.root_frame.current_menu == "START/STOP":
				self.previous_frame.alertas_label.config(text=self.root.mensaje)

			if self.tiempo_a_sanitizar <= 0:
				self.root.pin_on(self.root.bomba_salida, 0)
				self.root.after(60000, self.apagar_bomba)
				self.root.color_alertas = "green"
				self.root.mensaje = "STATUS: PROGRAMA TERMINADO; LOG FILE GENERADO "
				if self.root_frame.current_menu == "START/STOP":
					self.previous_frame.alertas_label.config(text=self.root.mensaje,
						bg=self.root.color_alertas)
					self.previous_frame.alertas_frame.config(bg=self.root.color_alertas)
				self.root_frame.after(5000, self.end)
			else:
				self.root.after(1000, self.terminar_normal)
		else:
			self.root.pin_on(self.root.bomba_salida, 0)
			self.root.after(60000, self.apagar_bomba)

	def end(self):
		self.root.fecha_termino = date.today()
		self.root.hora_termino = datetime.now()
		if self.root.tanque_lleno == 0:
			self.root.current_button_state = 0
			self.root.mensaje = "STATUS: LISTO PARA OPERAR"
			self.root_frame.grid_forget()
			self.root.color_alertas = self.root.color
			self.root_frame.__init__(self.root, self.root_frame.current_menu)
		else:
			if self.root_frame.current_menu == "START/STOP":
				self.root.mensaje = "STATUS: VACIANDO TANQUE"
				self.previous_frame.alertas_label.config(text=self.root.mensaje,
					bg=self.root.color_alertas)
				self.previous_frame.alertas_frame.config(bg=self.root.color_alertas)
				self.root.after(1000, self.end)

	def llenar_tanque(self):
                self.root.pin_on(self.root.bomba_entrada, 0)
                self.root.after(100, self.measure_ml)

	def apagar_bomba(self):
		self.root.tanque_lleno = 0
		self.root.pin_on(self.root.bomba_salida, 1)
