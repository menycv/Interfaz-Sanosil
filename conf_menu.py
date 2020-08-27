from tkinter import *
from datetime import datetime, date

class Conf_menu():
    def __init__(self, root, root_frame):
        # variables
        self.root = root
        now = datetime.now()
        self.root_frame = root_frame
        self.primera_mitad = Frame(self.root_frame.main_container, bg="white")
        self.primera_mitad.pack(side=LEFT)
        # Barra de fecha y hora con texto
        self.barra_FyH = Frame(self.primera_mitad, bd=3,
            bg=self.root.selected_color, relief=RIDGE)
        self.barra_FyH.pack(pady=(50,10), side=TOP)
        self.FyH_label = Label(self.barra_FyH, text="Fecha y Hora",
            bg=self.root.selected_color, font=("Verdana", 14, "bold"))
        self.FyH_label.pack(padx=80, pady=10)
        # Frame de hora y fecha editable
        self.FyH_frame = Frame(self.primera_mitad, bd=3,
            relief=SUNKEN, bg="yellow")
        self.FyH_frame.pack(side=TOP, padx=45, pady=(10,20))
        self.FyH_valores = Label(self.FyH_frame, font=self.root.myFont,
            bg="yellow")
        self.FyH_valores.pack(padx=70, pady=10)
        self.FyH_valores.bind("<Button-1>", self.set_date_time)
        # frame segunda segunda mitad
        self.segunda_mitad = Frame(self.root_frame.main_container, bg="white")
        self.segunda_mitad.pack(fill=BOTH, expand=YES, side=LEFT)
        # Frame de timer
        self.barra_timer = Frame(self.segunda_mitad, bd=3,
            bg=self.root.selected_color, relief=RIDGE)
        self.barra_timer.pack(side=TOP, pady=(50,15))
        self.timer_label = Label(self.barra_timer, bg=self.root.selected_color,
            font=("Verdana", 14, "bold"), text="Configurar Timer")
        self.timer_label.pack(padx=75, pady=10)
        # Valore editables del timer
        self.timer_valores_frame = Frame(self.segunda_mitad, bg="white")
        self.timer_valores_frame.pack(side=TOP, padx=10, pady=(10,20))
        for i, bg in self.root_frame.timer_valores:
            self.dias(self.timer_valores_frame, i, bg)

        # Botón de usuario
        self.frame_inferior = Frame(self.root_frame, bg="white")
        self.frame_inferior.grid(column=0, row=2, sticky="nw", ipady=78)
        self.settings = [("USUARIO", self.user_settings),
                         ("IDIOMA", self.language_settings),
                         ("WI-FI", self.wifi_settings),
                         ("PROGRAMA", self.program_settings)
                        ]
        for text, command in self.settings:
            self.settings_buttons(text, command)

        self.actualizar_hora()



    def settings_buttons(self, text, command):
        Button(self.frame_inferior, fg="white", command=command,
            font=("Verdana", 18), text=text, bg="red", bd=5).pack(
            side=LEFT, padx=28)


    def dias(self, frame, text, bg):
        dia = Label(frame, text=text, bg=bg, fg="white", font=("Verdana", 15),
            bd=3, relief=RAISED)
        dia.pack(side=LEFT)
        dia.bind("<Button-1>", self.edit_timer)

    def user_settings(self):
        print("user settings")

    def language_settings(self):
        print("Language settings")

    def wifi_settings(self):
        print("Wi fi settings")

    def edit_timer(self, event=None):
        print("edit timer")

    def set_date_time(self, event=None):
        print("set date and time")

    def program_settings(self, event=None):
        print("Program settings")

    def actualizar_hora(self):
        if self.root_frame.current_menu == "CONF":
            today = date.today()
            now = datetime.now()
            today_str = today.strftime("%d/%m/%y") + " " + now.strftime("%H:%M:%S")
            self.FyH_valores.config(text=today_str)
            self.root.after(1000, self.actualizar_hora)
