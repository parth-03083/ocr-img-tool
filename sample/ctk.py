from tkinter import *
from customtkinter import *
from PIL import ImageTk,Image

root = CTk()

root.geometry("1200x1100")


canvas = CTkCanvas(root, width=500, height=800)
canvas.place(relx = 0, rely = 0, anchor=W)
# image = CTkImage(Image.open("C:\\Users\\workp\\workspace\\doge.jpg.jpeg"))
# canvas.create_image(0,0, anchor=NW, image = image)

button = CTkButton(root, text="Hello World", width=10, height=2)
button.place(relx = 0.5, rely = 0.1, anchor=CENTER)

root.mainloop()