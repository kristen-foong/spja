from keras.models import Sequential
from keras.layers import Flatten, Dense
from keras.datasets import mnist
import matplotlib.pyplot as plt

# CS231n Convolutional Neural Networks for Visual Recognition (Stanford course)
# http://cs231n.github.io/
# https://www.youtube.com/playlist?list=PL3FW7Lu3i5JvHM8ljYj-zLfQRF3EO8sYv

model = Sequential([
    Flatten(),
    Dense(512, activation='relu'),
    Dense(10, activation='softmax')
])
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

history = model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test, y_test, batch_size=128)

model.save("mnist.net")

plt.plot(history.history['accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.show()

plt.plot(history.history['loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.show()
