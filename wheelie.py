import numpy as np
import tkinter as tk
import os
import pandas as pd
from tkinter import filedialog
from tkinter import Canvas
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

## Ignoring CUDA, working with normal CPUs
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Loading machine learning model

model = ResNet50(weights='imagenet')

path = 0
prob = 0

## Functions

# Function to run image recognition / Funzione per riconoscimento immagini


def scanimg(path):
    global prob
    img = preprocess_input(
        np.expand_dims(
            image.img_to_array(
                image.load_img(
                    path,
                    target_size=(224,224)
                )
            )
            ,axis = 0
        )
    )
    preds = model.predict(img)
    decoded = pd.DataFrame(decode_predictions(preds, top=20)[0],columns=["id","obj","p"]).query("obj == 'ashcan'")
    if len(decoded):
        canvasleft.itemconfig(lightleft, fill='red')
        canvasright.itemconfig(lightright, fill='red')
        prob = str(round(decoded.iloc[0]["p"]*100,1))
        with open("alarm","w+") as fin:
            pass
        return "Warning: wheelie bin detected (Probability: " + str(prob) + " %)"
    else:
        return "No wheelie bin detected"

            
def stopalarm():
    canvasleft.itemconfig(lightleft, fill='green')
    canvasright.itemconfig(lightright, fill='green')
    if "alarm" in os.listdir():
        os.remove("alarm")
    
def callscan():
    global path
    l_guide.configure(
        text="Please select an image to scan" if not path else scanimg(path)
    )

def getimg():
    global path 
    path = filedialog.askopenfilename(
        initialdir = "/",
        title = "Select image to scan",
        filetypes = (
            (".jpg","*.jpg*"),
            ("all files","*.*")
        )
    )
    # Change label contents 
#    l_guide.configure(text="File Opened: " + path) 

## GUI / Interfaccia grafica

window = tk.Tk()

window.title("Object Detector")

window.geometry('350x150')

l_guide = tk.Label(
    window,
    text="Select file to begin",
    font=("Arial Bold", 10),
    wraplength=200,
    width = 30
)

b_selectfile = tk.Button(
    window,
    text = "Browse Files",
    command = getimg,
    width=15
)

b_selectfile.grid(column = 1, row = 2,columnspan=3)

l_guide.grid(column=1, row=0, rowspan=2, columnspan=2)

b_scan = tk.Button(window, text="Scan", command = callscan, width=15)

b_scan.grid(column=1, row=3, columnspan=3)

canvasleft = Canvas(
    window,
    width=50,
    height=50
)

canvasright = Canvas(
    window,
    width=50,
    height=50
)

canvasleft.grid(row=1, column=0, sticky='ew', columnspan=1, rowspan=2)
canvasright.grid(row=1, column=4, sticky='ew', columnspan=1, rowspan=2)

#canvas.pack()

#canvas.create_oval(5.0,5.0,25.0,25.0,fill="green" if prob == 0 else "red")
lightleft = canvasleft.create_oval(5.0,5.0,45.0,45.0,fill="green" if prob == 0 else "red")
lightright = canvasright.create_oval(5.0,5.0,45.0,45.0,fill="green" if prob == 0 else "red")
#canvas.itemconfig(light, fill='red')

window.mainloop()
