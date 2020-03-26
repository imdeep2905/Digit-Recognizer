# Digit-Recognizer
![logo](https://github.com/imdeep2905/Digit-Recognizer/blob/master/Images/icon.png)<br>
![Demo](https://github.com/imdeep2905/Digit-Recognizer/blob/master/Images/demo.gif)
# Contents
1. [Introduction](#Introduction)
2. [How to run](#How-to-run) 
3. [For ML nerds](#For-all-ML-nerds)
4. [Credits](#Credits)
# Introduction
This is a little project which implements ML model (trained on **"Hello World of ML" - MNIST Digit Dataset**) in real life. You can hand draw digit in GUI, Browse an exsisting image and open your webcam and capture digit. Although model is really unstable with noisy images.(Maybe i'll try to improve it in future.)<br>
Some screenshots of Digit Recognizer:<br>
![Main Screen](https://github.com/imdeep2905/Digit-Recognizer/blob/master/Images/mainscreen.PNG)<br>
![Main Screen2](https://github.com/imdeep2905/Digit-Recognizer/blob/master/Images/mainscreen2.PNG)<br>
![Main Screen3](https://github.com/imdeep2905/Digit-Recognizer/blob/master/Images/mainscreen3.PNG)<br>

# How to run
  1. Fulfill ```requirements.txt``` (i.e. ```pip install -r requirements.txt```).
  2. Run with command ```python main.py```.

# For all ML nerds
For all the ML nerds out there model was trained on following architecture:
```
model = keras.models.Sequential([
keras.layers.Conv2D(64, (2, 2), padding = 'same' , activation = 'elu', input_shape = [28, 28, 1]),
keras.layers.MaxPooling2D(2),
keras.layers.Conv2D(128, (3, 3), padding = "same", activation = "elu"),
keras.layers.Conv2D(256, (4, 4), padding = "same", activation = "elu"),
keras.layers.Dropout(0.5),
keras.layers.MaxPooling2D(2),
keras.layers.Flatten(),
keras.layers.Dense(128, activation = "elu"),
keras.layers.Dropout(0.25),
keras.layers.Dense(10, activation = "softmax")
])

model.compile(loss = "sparse_categorical_crossentropy", metrics = ["accuracy"], optimizer = keras.optimizers.SGD(lr = 0.08))
``` 
It's accuracy was around ```0.99``` on training data and ```0.95-0.97(not sure)``` on testing data.<br>
At last you can load pretrained model (```model.h5```) and play with it.

# Credits

Contributors :computer: : 
   * [Deep Raval](https://github.com/imdeep2905)

Without these excellant libraries :heart: this would not have been possible.
   * tensorflow
   * pillow
   * opencv-python
   * numpy
