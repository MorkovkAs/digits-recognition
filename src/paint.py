from __future__ import absolute_import, division, print_function, unicode_literals

from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import io

import tensorflow as tf
from tensorflow import keras

import matplotlib.pyplot as plt


class Paint(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.canv_size = 350
        self.parent = parent
        self.setUI()
        self.brush_size = 10
        self.brush_color = "black"
        self.draw_numpy_array()

    def setUI(self):
        self.parent.title("Digits Recognition")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(9, weight=1)
        self.rowconfigure(3, weight=1)

        self.canvIn = Canvas(self, width=self.canv_size, height=self.canv_size, bg="white")
        self.canvIn.grid(row=3, column=0, columnspan=7, padx=5, pady=5, sticky=NW)
        self.canvIn.bind("<B1-Motion>", self.draw)

        # self.canvOut = Canvas(self, bg="white")
        # self.canvOut.grid(row=2, column=4, columnspan=2, padx=5, pady=5, sticky=E + W + S + N)
        # self.canvOut.bind("<B1-Motion>", self.draw)

        color_lab = Label(self, text="Color: ")
        color_lab.grid(row=0, column=0, padx=6)

        red_btn = Button(self, text="Red", width=6, command=lambda: self.set_color("red"))
        red_btn.grid(row=0, column=1)

        green_btn = Button(self, text="Green", width=6, command=lambda: self.set_color("green"))
        green_btn.grid(row=0, column=2)

        blue_btn = Button(self, text="Blue", width=6, command=lambda: self.set_color("blue"))
        blue_btn.grid(row=0, column=3)

        black_btn = Button(self, text="Black", width=6, command=lambda: self.set_color("black"))
        black_btn.grid(row=0, column=4)

        white_btn = Button(self, text="White", width=6, command=lambda: self.set_color("white"))
        white_btn.grid(row=0, column=5)

        clear_btn = Button(self, text="Clear all", width=6, command=lambda: self.canvIn.delete("all"))
        clear_btn.grid(row=0, column=6)

        clear_btn = Button(self, text="Train", width=6, command=lambda: self.train())
        clear_btn.grid(row=0, column=7)

        clear_btn = Button(self, text="Check", width=6, command=lambda: self.check_image())
        clear_btn.grid(row=0, column=8, sticky=W)

        size_lab = Label(self, text="Brush size: ")
        size_lab.grid(row=1, column=0, padx=5)

        one_btn = Button(self, text="One", width=6, command=lambda: self.set_brush_size(1))
        one_btn.grid(row=1, column=1)

        two_btn = Button(self, text="Two", width=6, command=lambda: self.set_brush_size(2))
        two_btn.grid(row=1, column=2)

        five_btn = Button(self, text="Five", width=6, command=lambda: self.set_brush_size(5))
        five_btn.grid(row=1, column=3)

        seven_btn = Button(self, text="Seven", width=6, command=lambda: self.set_brush_size(7))
        seven_btn.grid(row=1, column=4)

        ten_btn = Button(self, text="Ten", width=6, command=lambda: self.set_brush_size(10))
        ten_btn.grid(row=1, column=5)

        twenty_btn = Button(self, text="Save", width=6, command=lambda: self.save_image())
        twenty_btn.grid(row=1, column=6, sticky=W)

        print("width and height of canvIn should be ", self.canvIn.cget("width"), self.canvIn.cget("height"))

    def draw(self, event):
        self.canvIn.create_oval(event.x - self.brush_size,
                                event.y - self.brush_size,
                                event.x + self.brush_size,
                                event.y + self.brush_size,
                                fill=self.brush_color, outline=self.brush_color)

    def set_color(self, new_color):
        self.brush_color = new_color

    def set_brush_size(self, new_brush_size):
        self.brush_size = new_brush_size

    def draw_numpy_array(self):
        data = np.array(np.random.random((self.canv_size, self.canv_size)) * 255, dtype=int)
        self.im = Image.fromarray(data.astype('uint8'))
        self.photo = ImageTk.PhotoImage(image=self.im)
        self.canvIn.create_image(0, 0, image=self.photo, anchor=NW)

    def save_image(self):
        ps = self.canvIn.postscript(colormode='color', pagewidth=28 - 1, pageheight=28 - 1)
        img = Image.open(io.BytesIO(ps.encode('utf-8'))).convert('L')
        img.save('image_canvas.jpg')
        print('Saved image image_canvas.jpg')

    def load_image(self):
        im = Image.open('image_canvas.jpg')
        img_array = np.asarray(im)
        print('Loaded image image_canvas.jpg with shape: ', img_array.shape)
        return img_array

    def train(self):
        print('tensorflow -v: ', tf.__version__)

        digits_mnist = keras.datasets.mnist
        (x_train, y_train), (x_test, y_test) = digits_mnist.load_data()

        self.class_names = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']

        print('Train data shape:', x_train.shape)
        print('Train data labels length:', len(y_train))
        print('Train data labels value:', y_train)

        print('\nTest data shape:', x_test.shape)
        print('Test data labels length:', len(y_test))
        print('Test data labels value:', y_test)

        x_train, x_test = x_train / 255.0, x_test / 255.0

        model = keras.Sequential([
            keras.layers.Flatten(input_shape=(28, 28)),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(10, activation=tf.nn.softmax)
        ])

        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        model.fit(x_train, y_train, epochs=5)
        test_loss, test_acc = model.evaluate(x_test, y_test)
        print('Test accuracy:', test_acc)
        self.model = model

    def check_image(self):
        print('\nStart predicting')
        self.save_image()
        im = Image.open('image_canvas.jpg')
        img_array = np.asarray(im)
        print('Loaded image image_canvas.jpg with shape: ', img_array.shape)
        #img_array = self.load_image()

        img_array = 1 - img_array / 255.0
        img = (np.expand_dims(img_array, 0))

        predictions = self.model.predict(img)
        print('Number of max class prediction:', np.argmax(predictions[0]))
        print('Name of class prediction:', self.class_names[np.argmax(predictions[0])])

        plt.figure(figsize=(6, 3))
        plt.subplot(1, 2, 1)
        self.plot_image(0, predictions, img)
        plt.subplot(1, 2, 2)
        self.plot_value_array(0, predictions)
        plt.show()

    def plot_image(self, i, predictions_array, img):
        predictions_array, img = predictions_array[i], img[i]
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])

        plt.imshow(img, cmap=plt.cm.binary)
        predicted_label = np.argmax(predictions_array)
        plt.xlabel("{} {:2.0f}%".format(self.class_names[predicted_label],
                                        100 * np.max(predictions_array),
                                        color='blue'))

    def plot_value_array(self, i, predictions_array):
        predictions_array = predictions_array[i]
        plt.grid(False)
        plt.xticks([])
        plt.yticks([])
        thisplot = plt.bar(range(10), predictions_array, color="#777777")
        plt.ylim([0, 1])
        predicted_label = np.argmax(predictions_array)

        thisplot[predicted_label].set_color('blue')
        _ = plt.xticks(range(10), self.class_names, rotation=45)


def main():
    root = Tk()
    root.geometry("700x450+300+300")
    app = Paint(root)

    root.mainloop()


if __name__ == "__main__":
    main()
