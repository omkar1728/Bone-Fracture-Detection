from keras.layers import Conv2D, Dense, MaxPooling2D, Softmax, Dropout, BatchNormalization, Flatten
from keras import Sequential 
import keras

model = Sequential()
model.add(Conv2D(input_shape = (512,512,1), activation="relu", filters= 64, strides=1, kernel_size= (8,8)))
model.add(MaxPooling2D(pool_size= (8,8)))
model.add(BatchNormalization())
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(100, activation="relu"))
model.add(Dense(2,"softmax"))

model.compile(loss="binary_crossentropy",
              optimizer = "RMSprop",metrics=["accuracy"])
callback = keras.callbacks.EarlyStopping(monitor='loss', patience=2)

print(model)
print('done without error')