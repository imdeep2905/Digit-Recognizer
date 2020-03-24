from tensorflow import keras
import os
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

x_train = x_train.reshape(x_train.shape[0], 28,28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
model = keras.models.Sequential([
keras.layers.Conv2D(64, (3,3), activation = "relu", padding = "same", input_shape = [28, 28, 1]),
keras.layers.MaxPooling2D(2),
keras.layers.Dropout(0.3),
keras.layers.Conv2D(128, (6,6), activation = "relu", padding = "same"),
keras.layers.MaxPooling2D(4),
keras.layers.Flatten(),
keras.layers.Dropout(0.25),
keras.layers.Dense(64, activation = "relu"),
keras.layers.Dense(10, activation = "softmax")
])

model.compile(loss = "sparse_categorical_crossentropy", metrics = ["accuracy"], optimizer = keras.optimizers.SGD(lr = 0.3))
print(model.summary())
model.fit(x_train, y_train, epochs = 2)
model.evaluate(x_test, y_test)
model.save('model.h5')