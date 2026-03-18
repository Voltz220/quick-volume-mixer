import pythoncom
from pycaw.pycaw import AudioUtilities
import keyboard
import tkinter as tk

class AudioController:
    def __init__(self, process_name):
        self.process_name = process_name
        self.volume = self.process_volume()

    def _get_sessions(self):
        return AudioUtilities.GetAllSessions()

    def process_volume(self):
        for session in self._get_sessions():
            if session.Process and session.Process.name() == self.process_name:
                vol = session.SimpleAudioVolume.GetMasterVolume()
                print("Current volume:", vol)
                return vol
        return 0.5  # default value

    def set_volume(self, value):
        value = min(1.0, max(0.0, value))
        for session in self._get_sessions():
            if session.Process and session.Process.name() == self.process_name:
                session.SimpleAudioVolume.SetMasterVolume(value, None)
                self.volume = value
                print("Defined volume:", value)

    def decrease_volume(self, value):
        for session in self._get_sessions():
            if session.Process and session.Process.name() == self.process_name:
                self.volume = max(0.0, self.volume - value)
                session.SimpleAudioVolume.SetMasterVolume(self.volume, None)
                print("Volume decreased:", self.volume)
                overlay.show(self.volume)

    def increase_volume(self, value):
        for session in self._get_sessions():
            if session.Process and session.Process.name() == self.process_name:
                self.volume = min(1.0, self.volume + value)
                session.SimpleAudioVolume.SetMasterVolume(self.volume, None)
                print("Volume increased:", self.volume)
                overlay.show(self.volume)
    
    def toggle_mute(self):
        for session in self._get_sessions():
            if session.Process and session.Process.name() == self.process_name:
               interface = session.SimpleAudioVolume
               current = interface.GetMute()
               new_state = 0 if current else 1
               interface.SetMute(new_state, None)

               if new_state:
                   print(self.process_name, "muted")
               else:
                   print(self.process_name, "unmuted")
        overlay.show(0 if new_state else self.volume)

class VolumeOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.85)

        self.width = 300
        self.height = 50

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int((screen_width - self.width) / 2)
        y = int(screen_height * 0.8)

        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height,
                                bg="black", highlightthickness=0)
        self.canvas.pack()

        self.bar_bg = self.canvas.create_rectangle(20, 20, 280, 30, fill="gray")
        self.bar = self.canvas.create_rectangle(20, 20, 20, 30, fill="lime")
        self.text = self.canvas.create_text(150, 10, text="", fill="white")

        self.root.withdraw()  # hidden

    def show(self, volume):
        self.root.deiconify()

        vol_width = 20 + (260 * volume)
        self.canvas.coords(self.bar, 20, 20, vol_width, 30)
        self.canvas.itemconfig(self.text, text=f"{int(volume * 100)}%")

        # hiddes after a second
        self.root.after(1000, self.root.withdraw)

        self.root.update_idletasks()
        self.root.update()

overlay = VolumeOverlay()

def main(inc, dec, mute=False):
    pythoncom.CoInitialize()  # ESSENTIAL

    audio = AudioController("firefox.exe") #choose the process
    if mute:
        audio.toggle_mute()
        return
    if inc > 0:
        audio.decrease_volume(inc)
    if dec > 0:
        audio.increase_volume(dec)
    elif inc == 69:
        audio.set_volume(1.0)

# Hotkeys
keyboard.add_hotkey('ctrl+down', lambda: main(0.1, 0))   # lower
keyboard.add_hotkey('ctrl+up', lambda: main(0, 0.1))     # raise
keyboard.add_hotkey('ctrl+left', lambda: main(0, 0, True))  # mute toggle
keyboard.add_hotkey('ctrl+esc', lambda: main(69,420)) # exit and reset volume to be the same as the master/main
print("Press 'ctrl+down' to lower and 'ctrl+up' to raise the volume of the program")
print("Press Ctrl + ESC to exit")

def exit():
    try:
        overlay.root.destroy()
    except:
        pass
    exit()

keyboard.add_hotkey('ctrl+esc', exit)
overlay.root.mainloop()

#Com o sol batendo nas minhas costas eu caminhava
#Me olhavam com um tremendo orgulho
#Acreditavam que eu tinha um propósito
#Eu nunca acreditava no que falavam
#Até por que a calada da noite
#Sempre me foi mais confortável
#Agoro eu rondo por ai entre o Amanhacer e o Entardecer
#Em busca do dito propósito
