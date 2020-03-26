import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, Button, Label, Canvas
from PIL import ImageTk, Image, ImageGrab
import cv2 
from tensorflow import keras
import numpy as np 
import os
import matplotlib.pyplot as plt
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
#os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
class Model:
    def __init__(self):
        pass
    
    def predict(self):
        img = cv2.imread('image.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('Processed', img)
        img = cv2.resize(img, (28, 28), interpolation = cv2.INTER_AREA)
        img = img.astype('float32')
        img /= 255
        #plt.imshow(img)
        #plt.plot()
        #plt.show()
        img  = np.reshape(img, (1, 28, 28, 1)) 
        model = keras.models.load_model('model.h5')
        return model.predict_classes(img)[0]
        
class MainApp:
    def __init__(self):
        self.pre = None
        #Model object which will predict our number
        self.model = Model()
        #Creating root
        self.root = Tk()
        self.root.title("Digit Recognizer")
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file='Images/icon.png'))
        self.root.resizable(0,0)
        #Creating GUI Elements
        self.lbl_drawhere = LabelFrame(text = "Draw Here with Mouse")
        self.area_draw = Canvas(self.lbl_drawhere, width = 308, height = 308, bg = 'black')
        self.area_draw.bind('<B1-Motion>',self.draw)
        
        self.lbl_image = LabelFrame(text = "Image")
        self.area_img = Label(self.lbl_image, image = "", text = "Select an Image to\nview it here!",padx = 150, pady = 150)
        self.lbl_cur_img = Label(self.lbl_image, text = "Current Image", bg = "grey")
        
        self.btn_reset = Button(self.lbl_drawhere, text = "Reset Drawing", bg = "lightblue", command = self.reset_drawing)
        self.btn_load_img = Button(self.lbl_image, text = "Browse Image", bg = "lightblue", command = self.browse_image)
        self.btn_camera_img = Button(self.lbl_image, text = "Open camera", bg = "lightblue", command = self.open_camera)
        
        self.btn_predict = Button(self.root, text = "Predict Digit", bg = "red", command = self.predict_digit)
        #Fitting in GUI
        self.lbl_drawhere.pack(in_=self.root, side = LEFT, fill = X)
        self.area_draw.pack()
        self.area_img.pack()   
        self.btn_reset.pack()
        self.btn_predict.pack(in_ = self.root, side = LEFT)
        self.lbl_image.pack(in_=self.root, side = RIGHT, fill = X)
        self.btn_load_img.pack(in_ = self.lbl_image, side = LEFT, fill = Y)
        self.btn_camera_img.pack(in_ = self.lbl_image, side = RIGHT, fill = Y)
        self.lbl_cur_img.pack()  

    def draw(self,event):
        self.area_draw.create_oval(event.x, event.y, event.x + 9, event.y + 9, outline = 'white',fill = 'white')    
        self.area_draw.create_rectangle(event.x, event.y, event.x + 8, event.y + 8, outline = 'white',fill = 'white')
        self.pre = 'D'
            
    def run(self):
        self.root.mainloop()
    
    def reset_drawing(self):
        self.area_draw.delete('all')
        
    def browse_image(self):
        try:
            self.area_img.text = ""
            file = filedialog.askopenfilename(filetypes=[('Images',['*jpeg','*png','*jpg'])]) 
            file = Image.open(file)
            file = file.resize((320, 320)) 
            file.save('image.jpg')
            file = ImageTk.PhotoImage(file)
            self.area_img.configure(image = file)
            self.area_img.image = file
            self.pre = 'C'
        except Exception as e:
            messagebox.showerror("An Error Occured", e)
                    
    def open_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Cannot open webcam")
        
        while True:
            ret, frame = cap.read()
            cv2.rectangle(img = frame, pt1 = (220, 140), pt2 = (420, 340), color = (0, 0, 255), thickness = 2)
            cv2.putText(frame, 'Lineup Digit in below Rectangle and press ENTER', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow('Input', frame)
            c = cv2.waitKey(1)
            ref_point = [ [222, 142], [418, 338]]
            if c == 13:
                crop_img = frame[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
                cv2.imshow("crop_img", crop_img)
                cv2.imwrite('image.jpg', crop_img)
                file = Image.open('image.jpg')
                file = file.resize((320, 320)) 
                file = ImageTk.PhotoImage(file)
                self.area_img.configure(image = file)
                self.area_img.image = file
                break
        cap.release()
        cv2.destroyAllWindows()
        self.pre = 'C'
        
    def predict_digit(self):
        if(self.pre == None):
            messagebox.showerror(title = '0 Images/Drawing found', message = "First Draw, Browse or Capture image before prediction !")
        else:
            if(self.pre == 'D'):
                x = self.root.winfo_rootx() + self.area_draw.winfo_x()
                y = self.root.winfo_rooty() + self.area_draw.winfo_y()
                x1 = x + self.area_draw.winfo_width()
                y1 = y + self.area_draw.winfo_height()
                ImageGrab.grab().crop((x,y + 10,x1,y1 )).save('image.jpg')
                messagebox.showinfo(title = "Prediction", message = f"I Predict you have drawn {self.model.predict()}")
            else:
                messagebox.showinfo(title = "Prediction", message = f"I Predict number in image is {self.model.predict()}")                
        
if __name__ == "__main__":
    MainApp().run()