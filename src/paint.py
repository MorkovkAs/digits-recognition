from tkinter import *
from PIL import Image, ImageTk
import numpy as np


class Paint(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.setUI()
        self.brush_size = 10
        self.brush_color = "black"
        self.draw_numpy_array()

    def setUI(self):
        self.parent.title("Digits Recognition")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(6, weight=1)
        self.rowconfigure(2, weight=1)

        self.canv = Canvas(self, bg="white")
        self.canv.grid(row=2, column=0, columnspan=7, padx=5, pady=5, sticky=E + W + S + N)
        self.canv.bind("<B1-Motion>", self.draw)

        color_lab = Label(self, text="Color: ")
        color_lab.grid(row=0, column=0, padx=6)

        red_btn = Button(self, text="Red", width=10, command=lambda: self.set_color("red"))
        red_btn.grid(row=0, column=1)

        green_btn = Button(self, text="Green", width=10, command=lambda: self.set_color("green"))
        green_btn.grid(row=0, column=2)

        blue_btn = Button(self, text="Blue", width=10, command=lambda: self.set_color("blue"))
        blue_btn.grid(row=0, column=3)

        black_btn = Button(self, text="Black", width=10, command=lambda: self.set_color("black"))
        black_btn.grid(row=0, column=4)

        white_btn = Button(self, text="White", width=10, command=lambda: self.set_color("white"))
        white_btn.grid(row=0, column=5)

        clear_btn = Button(self, text="Clear all", width=10, command=lambda: self.canv.delete("all"))
        clear_btn.grid(row=0, column=6, sticky=W)

        size_lab = Label(self, text="Brush size: ")
        size_lab.grid(row=1, column=0, padx=5)

        one_btn = Button(self, text="One", width=10, command=lambda: self.set_brush_size(1))
        one_btn.grid(row=1, column=1)

        two_btn = Button(self, text="Two", width=10, command=lambda: self.set_brush_size(2))
        two_btn.grid(row=1, column=2)

        five_btn = Button(self, text="Five", width=10, command=lambda: self.set_brush_size(5))
        five_btn.grid(row=1, column=3)

        seven_btn = Button(self, text="Seven", width=10, command=lambda: self.set_brush_size(7))
        seven_btn.grid(row=1, column=4)

        ten_btn = Button(self, text="Ten", width=10, command=lambda: self.set_brush_size(10))
        ten_btn.grid(row=1, column=5)

        twenty_btn = Button(self, text="Twenty", width=10, command=lambda: self.set_brush_size(20))
        twenty_btn.grid(row=1, column=6, sticky=W)

    def draw(self, event):
        self.canv.create_oval(event.x - self.brush_size,
                              event.y - self.brush_size,
                              event.x + self.brush_size,
                              event.y + self.brush_size,
                              fill=self.brush_color, outline=self.brush_color)

    def set_color(self, new_color):
        self.brush_color = new_color

    def set_brush_size(self, new_brush_size):
        self.brush_size = new_brush_size

    def draw_numpy_array(self):
        data = np.array(np.random.random((768, 1024)) * 100, dtype=int)
        self.im = Image.fromarray(data.astype('uint8'))
        self.photo = ImageTk.PhotoImage(image=self.im)
        self.canv.create_image(0, 0, image=self.photo, anchor=NW)


def main():
    root = Tk()
    root.geometry("1024x768+300+300")
    app = Paint(root)

    root.mainloop()


if __name__ == "__main__":
    main()
