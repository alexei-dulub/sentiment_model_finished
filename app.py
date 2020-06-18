import tkinter as tk
from sentiment import Analyzer

class Window(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.positive = ':)'
        self.neutral = ':l'
        self.negative = ':('
        self.create_widgets()
        
        self.analyzer = Analyzer()

    def create_widgets(self):
        self.master.bind('<Return>', self.change_emote)

        self.emote = tk.Label(self, text=self.neutral)
        self.emote.grid(row=0, column=0)

        self.text_field = tk.Entry(self)
        self.text_field.grid(row=1)

    
    def change_emote(self, event):
        result = self.analyzer.analyze(self.text_field.get())
        if result == 'Positive':
            self.emote['text'] = self.positive
        elif result == 'Negative':
            self.emote['text'] = self.negative
        else:
            self.emote['text'] = self.neutral



root = tk.Tk()
window = Window(master=root)
window.mainloop()