from tkinter import * 
from PIL import ImageTk,Image  
import os
from paddleocr import PaddleOCR
import shutil


# Constants
FILE_SAVE_PATH = os.path.join(os.getcwd(),"texts")
FILE_DISCARD_PATH = os.path.join(os.getcwd(),"discard")

# Global Variables
img_index = 0
path = os.path.join(os.getcwd(),"picsum")
zoom_idx = 1
zoomout_idx = 1
# List of images in folder
img_list = os.listdir(path)

# Backend Functionalities 
# Global OCR Object
ocr = PaddleOCR( lang='en')

# OCR Functionality 
def get_ocr_text(path):
    result = ocr.ocr(path, rec=True, cls=False)
    str = ''
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            str += line[1][0] + '\n'
    return str

def get_resized_image(img_obj = False):
    '''
        Function to get resized image using the logic according to canvas width and image width.
        Argument Takes img_obj having PIL Image Object
        Return PIL.ImageTk.PhotoImg object.
    '''
    if img_obj:
        if img_obj.width > 500 and img_obj.height > 500:
            # print("Resizing")            
            img = ImageTk.PhotoImage(img_obj.resize((500,500)))
        elif img_obj.width < 500 and img_obj.height < 500:
            # print(" Not Resizing")
            img = ImageTk.PhotoImage(img_obj.resize((img_obj.width,img_obj.height)))
        elif img_obj.width < 500 and img_obj.height > 500:
            # print(" Width Resizing ")
            img = ImageTk.PhotoImage(img_obj.resize((img_obj.width,500)))
        elif img_obj.height < 500 and img_obj.width > 500:
            # print(" Height Resizing ")
            img = ImageTk.PhotoImage(img_obj.resize((500,img_obj.height)))
        else:
            img = ImageTk.PhotoImage(img_obj)
        return img 
    else:
        return False

# Function to load images
def load_img(start=False):
    '''
        Function to Load Next and First Image in the canvas from the folder.
        Single Positional argument called start by default False to load next image. 
        If Start is true then it'll load first image.
    '''
    global img_index
    global img_list
    if start:
        img_index = 0
    else:
        img_index += 1
    if img_index >= len(img_list):
        img_index = 0
    img_obj = Image.open(os.path.join( path, img_list[img_index]))
    # print(img_obj.info)
    # print(img_obj.width, img_obj.height)
    if img_obj.width > 500 and img_obj.height > 500:
        # print("Resizing")            
        img = ImageTk.PhotoImage(img_obj.resize((500,500)))
    elif img_obj.width < 500 and img_obj.height < 500:
        # print(" Not Resizing")
        img = ImageTk.PhotoImage(img_obj.resize((img_obj.width,img_obj.height)))
    elif img_obj.width < 500 and img_obj.height > 500:
        # print(" Width Resizing ")
        img = ImageTk.PhotoImage(img_obj.resize((img_obj.width,500)))
    elif img_obj.height < 500 and img_obj.width > 500:
        # print(" Height Resizing ")
        img = ImageTk.PhotoImage(img_obj.resize((500,img_obj.height)))
    else:
        img = ImageTk.PhotoImage(img_obj)
    canvas.create_image(0,0, anchor=NW, image=img)
    canvas.image = img
    canvas.imscale = 0.9
    cnt_text = str(img_index+1) + "/" + str(len(img_list))
    cnt_label.config(text=cnt_text)
    text = get_ocr_text(os.path.join( path, img_list[img_index]))
    text_box.delete("1.0",END)
    text_box.insert(END, text)
    canvas.update()
    return

def load_prev_img():
    '''
        Load the previous image in the folder.
        Global Variable img_index is used to keep track of the current image.
    '''
    global img_index
    global img_list
    img_index -= 1
    if img_index < 0:
        img_index = len(img_list) - 1
    img_obj = Image.open(os.path.join( path, img_list[img_index]))
    # print(img_obj.info)
    # print(img_obj.width, img_obj.height)
    img = get_resized_image(img_obj)
    canvas.create_image(0,0, anchor=NW, image=img)
    canvas.image = img
    canvas.imscale = 0.9
    cnt_text = str(img_index+1) + "/" + str(len(img_list))
    cnt_label.config(text=cnt_text)
    text = get_ocr_text(os.path.join( path, img_list[img_index]))
    text_box.delete("1.0",END)
    text_box.insert(END, text)
    canvas.update()
    return

def save_text():
    ''' 
        Save the text in the text box to a text file with the same name as the image.
        If the text file already exists, it will be overwritten.
        The Text which is saved is taken from the text box where updated values can be directly entered.
    '''
    text = text_box.get("1.0",END)
    print(text)
    with open(os.path.join(FILE_SAVE_PATH, img_list[img_index]) + '.txt', 'w') as f:
        f.write(text)
    return

def move_img():
    ''' 
        Move the current image and its corroesponding text file to discard folder. Prints error if text file not found. and only moves the image
    '''
    try:
        try:
            shutil.move(os.path.join(path, img_list[img_index]), os.path.join(FILE_DISCARD_PATH, img_list[img_index]))
        except FileNotFoundError as e:
            os.mkdir(FILE_DISCARD_PATH)
            shutil.move(os.path.join(path, img_list[img_index]), os.path.join(FILE_DISCARD_PATH, img_list[img_index]))
        
        if os.path.exists(os.path.join(FILE_SAVE_PATH , img_list[img_index]) + '.txt'):
            try:
                shutil.move(os.path.join(FILE_SAVE_PATH , img_list[img_index]) + '.txt', os.path.join(FILE_DISCARD_PATH , img_list[img_index]) + '.txt')
            except FileNotFoundError as e:
                os.mkdir(os.path.join(FILE_DISCARD_PATH))
                shutil.move(os.path.join(FILE_SAVE_PATH , img_list[img_index]) + '.txt', os.path.join(FILE_DISCARD_PATH , img_list[img_index]) + '.txt')
        else:
            print("No text file found for this image")
    except FileNotFoundError as e:
        print(e)
    return

# Key Release Event Handler
# def kr(event):
#     if event.keysym == 'Right':
#         load_img()
#         return
    
#     elif event.keysym == 'Left':
#         load_prev_img()
#         return
    
#     elif event.keysym == 'Space':
#         print(" Space Pressed ")
#         save_text()
#         return
    
#     elif event.keysym == 'Escape':
#         root.destroy()
#         return


# def focus_in(event):
#     root.unbind_all('<KeyRelease>')
#     return

# def focus_out(event):
#     print("Focus Out")
#     var = root.bind_all('<KeyRelease>', kr)
#     print(var)
#     return


def wheel(event):
    # scale = 1.0
    # if event.delta == -120:
    #     scale *= event.delta
    #     canvas.imscale *= event.delta
    # if event.delta == 120:
    #     scale /= event.delta
    #     canvas.imscale *= event.delta
    # x = canvas.canvasx(event.x)
    # y = canvas.canvasy(event.y)
    # canvas.scale('all', x, y, scale, scale)
    # # load_img()
    # canvas.configure(scrollregion=canvas.bbox('all'))
    # canvas.update()
    print("Event :" , event)
    if (event.delta > 0):
        print(event.x,event.y)
        canvas.scale("all", event.x, event.y, 1.1, 1.1)
    elif (event.delta < 0):
        canvas.scale("all", event.x, event.y, 0.9, 0.9)
    # canvas.configure(scrollregion = canvas.bbox("all"))

def zoom():
    global zoom_idx
    global zoomout_idx
    zoom_idx += 1
    zoomout_idx -=1
    if zoom_idx <=0 :
        zoom_idx = 1
        zoomout_idx = 1
    img_obj = Image.open(os.path.join( path, img_list[img_index]))
    img = get_resized_image(img_obj)
    img = img._PhotoImage__photo.zoom(zoom_idx)
    canvas.create_image(0,0,image=img,anchor = NW)
    canvas.image = img

def zoom_out():
    global zoom_idx 
    global zoomout_idx
    zoom_idx -=1
    zoomout_idx += 1
    if zoomout_idx<=0:
        zoom_idx = 1
        zoomout_idx = 1
    img_obj = Image.open(os.path.join( path, img_list[img_index]))
    img = get_resized_image(img_obj)
    img = img._PhotoImage__photo.subsample(zoomout_idx)
    canvas.create_image(0,0,image=img,anchor = NW)
    canvas.image = img

# create root window
root = Tk()                          

root.geometry("1100x1200")

# canvas inside root window
canvas = Canvas(root)
canvas.place(relx = 0.01,rely=0.01 , anchor=NW , relheight= 0.7 , relwidth=0.5 ,scrollregion=canvas.bbox("all"))
canvas.bind('<MouseWheel>' , wheel)


text_box = Text(root, bg="black", fg="white"  , cursor="arrow" , font=("Courier", 12) , wrap="word" , insertbackground="white" , highlightbackground="white" , highlightcolor="white" , padx=10 , pady=10, selectbackground="white" , selectforeground="black" , undo=True, yscrollcommand=True )
text_box.place(relx = 0.6, rely = 0.01,relwidth=0.45,relheight=0.7, anchor=NW )


# button inside root window
button_next = Button(root, text="Next", padx = 10 , pady=4, bg="black", fg="white" , command=load_img)
button_next.place(relx=0.3,rely=0.8,anchor=S)

button_exit = Button(root, text="Back", padx = 10 , pady=4, bg="black", fg="white" , command=load_prev_img)
button_exit.place(relx=0.4,rely=0.8,anchor=S)

button_move = Button(root, text="Save", padx = 10 , pady=4, bg="black", fg="white" , command=save_text)
button_move.place(relx=0.5,rely=0.8,anchor=S )

button_save = Button(root, text="Move", padx = 10 , pady=4, bg="black", fg="white" ,command=move_img)
button_save.place(relx=0.6,rely=0.8,anchor=S)

button_save = Button(root, text="Exit", padx = 10 , pady=4, bg="black", fg="white" , command=root.quit)
button_save.place(relx=0.7,rely=0.8,anchor=S )

button_zoom = Button(root,text="+", padx = 6 , pady=4, bg="black", fg="white" , command=zoom)
button_zoom.place(relx= 0.20 , rely=0.7 )

button_zoom_out = Button(root,text="-", padx = 6 , pady=4, bg="black", fg="white" , command=zoom_out)
button_zoom_out.place(relx= 0.24 , rely=0.7 )

scroll_x = Scrollbar(canvas, orient="horizontal", command=canvas.xview  )
scroll_x.pack(side=BOTTOM , fill= X)
scroll_y = Scrollbar(canvas, orient="vertical", command=canvas.yview  )
scroll_y.pack(side=RIGHT , fill= Y)

# canvas['yscrollcommand'] = scroll_y.set
# canvas['xscrollcommand'] = scroll_x.set
# canvas.update()

curr_img = 1
total_img = 10
cnt_text = str(curr_img) + "/" + str(total_img) 

cnt_label = Label(root, text=cnt_text, padx = 10 , pady=4, bg="black", fg="white")
cnt_label.place(relx=0.5,rely=0.9,anchor=S)


load_img(True)

# Key Press Functionalities 
# root.bind_all('<KeyRelease>', kr)
# text_box.bind("<FocusIn>" , focus_in)
# text_box.bind("<FocusOut>" , focus_out)

# Tkinter event loop
root.mainloop()