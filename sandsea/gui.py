import tkinter
from tkinter import Tk
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import Frame
from tkinter import Text

bg = "black"
fg = "white"
font = lambda size : ("Terminal", size)

print("Loading window ...")
window = Tk()
window.config(bg="black")
window.title("Sandsea Session")

print("Loading elementView ...")
elementView = Frame(window, bg=bg)
elementView.grid(row=1, column=1)

print("Loading consoleView ...")
consoleView = Frame(window, bg=bg)
consoleView.grid(row=1, column=2)

print("Loading console ...")
console = Text(consoleView, bg=bg, fg=fg, height=25, width=150, font=font(12))
console.grid(row=1, column=1, columnspan=2)

print("Loading consoleCommandEntry ...")
consoleCommandEntry = Entry(consoleView, bg=bg, fg=fg, width=120, font=font(14))
consoleCommandEntry.grid(row=2, column=1)

print("Loading consoleCommandButton ...")
consoleCommandButton = Button(consoleView, text="Execute", bg=bg, fg=fg, width=60, font=font(14))
consoleCommandButton.grid(row=2, column=2)

print("Loading logDirEntry ...")
logDirEntry = Entry(consoleView, bg=bg, fg=fg, width=100, font=font(12))
logDirEntry.grid(row=3, column=1)

print("Loading logButton ...")
logButton = Button(consoleView, text="Log Console Output to File", bg=bg, fg=fg, width=50, font=font(12))
logButton.grid(row=3, column=2)

def log(text):
	console.insert("end", "\n" + text)

window.mainloop()
