import customtkinter
from page import Page
from cargarConfig import loadConfiguration

textFont, fontSize, darkMode = loadConfiguration()

customtkinter.set_appearance_mode(darkMode)
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class AbrirArchivoPage(Page):
    def __init__(self, master, previous_page):
        super().__init__(master)
        self.previous_page = previous_page

        self.text = customtkinter.CTkLabel(self.frame, text="Elegir formato de análisis", font=(textFont, fontSize + 12))
        self.text.pack(pady=30)
        self.cell1 = customtkinter.CTkButton(self.frame, text="Imagen", width=10, font=(textFont, fontSize), command=self.analisis_imagen)
        self.cell1.pack()
        self.cell2 = customtkinter.CTkButton(self.frame, text="Video", width=10, font=(textFont, fontSize), command=self.analisis_video)
        self.cell2.pack(pady=30)
        self.cell3 = customtkinter.CTkButton(self.frame, text="En vivo", width=10, font=(textFont, fontSize), command=self.analisis_transmision)
        self.cell3.pack()

        volver_button = customtkinter.CTkButton(self.frame, text="Regresar", width=10, font=(textFont, fontSize), command=self.volver, fg_color = 'dark red'  )
        volver_button.pack(pady=30)

    def analisis_imagen(self):
        self.master.show_analisis_foto_page()

    def analisis_video(self):
        self.master.show_analisis_video_page()

    def analisis_transmision(self):
        self.master.show_analisis_transmision_page()

    def volver(self):
        self.hide()
        self.previous_page.show()