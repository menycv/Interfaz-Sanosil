from tkinter import *

class Programas():
	def __init__(self, root, root_frame, previous_frame, programa):
		self.root = root
		self.root_frame = root_frame
		self.program = programa
		if self.program == "Normal":
			self.normal()
		elif self.program == "Step":
			self.step()
		elif self.program == "Testing":
			self.testing()
		elif self.program == "Manual":
			self.manual()

	def normal(self):
            self.root.pin_on(self.root.bomba_entrada, 0)
            self.root.after(100, self.measure_ml)

	def step(self):
		pass

	def testing(self):
		pass

	def manual(self):
		pass

#        def measure_ml(self):
 #           if self.root.current_button_state == 1:
  #              self.flujo = (self.root.pulsos/.1)/1633.333
   #             self.root.pulsos = 0
    #            self.root.after(100, measure_ml)