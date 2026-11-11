import customtkinter as ctk
from frontend.app_gui import TextToSpeechApp

if __name__ == "__main__":
    # Setează tema implicită (Dark Mode și culoare de accent albastră)
    ctk.set_appearance_mode("System")  # Se adaptează automat la tema sistemului (Dark/Light)
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = TextToSpeechApp(root)
    root.mainloop()