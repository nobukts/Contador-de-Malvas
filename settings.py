class Settings:
    def __init__(self):
        self.textFont = "Monospace"
        self.fontSize = 24
        self.darkMode = True
        self.load_configuration()

    def load_configuration(self):
        try:
            with open("config.txt", "r") as f:
                lines = f.readlines()
                self.textFont = lines[0].split("\"")[1]
                self.fontSize = int(lines[1].split("= ")[1])
                self.darkMode = bool(int(lines[2].split("= ")[1]))
        except FileNotFoundError:
            pass

    def save_configuration(self):
        with open("config.txt", "w") as f:
            f.write(f'letterType = "{self.textFont}"\n')
            f.write(f'letterSize = {self.fontSize}\n')
            f.write(f'darkMode = {int(self.darkMode)}\n')

    # Define métodos para actualizar las configuraciones individuales
    def update_font(self, font):
        self.textFont = font

    def update_font_size(self, size):
        self.fontSize = size

    def update_dark_mode(self, mode):
        self.darkMode = mode
        self.save_configuration()  # Guarda el modo oscuro al cambiarlo

# Crea una instancia de la clase Settings
app_settings = Settings()
