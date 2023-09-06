import customtkinter
from page import Page
from settings import app_settings

app_settings.load_configuration()

# Convierte el valor booleano a una cadena "dark" o "light"
mode_string = "dark" if app_settings.darkMode else "light"
# Establece el modo de apariencia
customtkinter.set_appearance_mode(mode_string)
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class AbrirArchivoPage(Page):
    def __init__(self, master, previous_page):
        super().__init__(master)
        self.previous_page = previous_page

        self.frame.grid_rowconfigure((0,1,2,3), weight=1)
        self.frame.grid_columnconfigure((0,1,2), weight=1)

        self.textFont = app_settings.textFont
        self.fontSize = app_settings.fontSize

        self.text = customtkinter.CTkLabel(self.frame, text="Elegir formato de análisis", font=(self.textFont, self.fontSize + 12))
        self.text.grid(row=0, column=1, columnspan=1, pady=30, padx=30, sticky="n")

        self.cell1 = customtkinter.CTkButton(self.frame, text="Imagen", width=10, font=(self.textFont, self.fontSize), command=self.analisis_imagen)
        self.cell1.grid(row=1, column=1, pady=30, padx=30, sticky="nsew")

        self.cell2 = customtkinter.CTkButton(self.frame, text="Video", width=10, font=(self.textFont, self.fontSize), command=self.analisis_video)
        self.cell2.grid(row=2, column=1, pady=30, padx=30, sticky="nsew")

        self.cell3 = customtkinter.CTkButton(self.frame, text="En vivo", width=10, font=(self.textFont, self.fontSize), command=self.analisis_transmision)
        self.cell3.grid(row=3, column=1, pady=30, padx=30, sticky="nsew")

        self.volver_button = customtkinter.CTkButton(self.frame, text="Regresar", width=10, font=(self.textFont, self.fontSize), command=self.volver, fg_color='dark red')
        self.volver_button.grid(row=4, column=1, pady=30, padx=30, sticky="nsew")

    def analisis_imagen(self):
        self.master.show_analisis_foto_page()

    def analisis_video(self):
        self.master.show_analisis_video_page()

    def analisis_transmision(self):
        self.master.show_analisis_transmision_page()

    def volver(self):
        self.hide()
        self.previous_page.show()

    def update_widgets_font_and_size(self):
        # Actualizar la fuente y el tamaño de letra de los widgets en esta página
        self.textFont = app_settings.textFont
        self.fontSize = app_settings.fontSize

        self.text.configure(font=(self.textFont, self.fontSize + 12))
        self.cell1.configure(font=(self.textFont, self.fontSize))
        self.cell2.configure(font=(self.textFont, self.fontSize))
        self.cell3.configure(font=(self.textFont, self.fontSize))
        self.volver_button.configure(font=(self.textFont, self.fontSize))
