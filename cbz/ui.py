from io import BytesIO
from tkinter import (Tk, Button, BOTTOM, TOP, PhotoImage, Scrollbar, X, Y, Canvas, HORIZONTAL, VERTICAL, YES, BOTH,
                     SUNKEN, RIGHT, LEFT, DISABLED, NORMAL, Label, Frame, ALL)
from PIL import ImageTk, Image


class ScrolledCanvas(Frame):
    image_cursor: int = -2
    info_text: str = ''
    pages = list()
    next_btn = None
    prev_btn = None
    counter = None
    image: PhotoImage

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.master.title('Spectrogram Viewer')
        self.pack(expand=YES, fill=BOTH)
        self.canvas = Canvas(self, relief=SUNKEN)
        self.canvas.config(width=400, height=200)
        self.canvas.config(highlightthickness=0)

        s_bar_v = Scrollbar(self, orient=VERTICAL)
        s_bar_h = Scrollbar(self, orient=HORIZONTAL)

        s_bar_v.config(command=self.canvas.yview)
        s_bar_h.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=s_bar_v.set)
        self.canvas.config(xscrollcommand=s_bar_h.set)

        s_bar_v.pack(side=RIGHT, fill=Y)
        s_bar_h.pack(side=BOTTOM, fill=X)

        self.canvas.pack(side=LEFT, expand=YES, fill=BOTH)

    def set_text(self) -> None:
        self.canvas.delete('image')
        self.canvas.create_text(0, 0, anchor='nw', text=self.info_text, tags='image')
        self.canvas.config(scrollregion=self.canvas.bbox(ALL))

    def set_image(self, content: bytes) -> None:
        self.canvas.delete('image')
        with BytesIO(content) as f:
            with Image.open(f) as image:
                self.image = ImageTk.PhotoImage(image)
                self.canvas.create_image(0, 0, anchor='nw', image=self.image, tags='image')
                self.canvas.config(scrollregion=self.canvas.bbox(ALL))

    def show_image(self, n: int) -> None:
        self.image_cursor += n
        if self.image_cursor == -1:
            self.set_text()
            self.prev_btn.config(state=DISABLED)
            self.next_btn.config(state=NORMAL if self.pages else DISABLED)
        elif self.image_cursor >= 0:
            self.set_image(self.pages[self.image_cursor].content)
            if self.image_cursor == len(self.pages) - 1:
                self.next_btn.config(state=DISABLED)
                self.prev_btn.config(state=NORMAL)
            else:
                self.prev_btn.config(state=NORMAL)
                self.next_btn.config(state=NORMAL)
        self.counter.config(text=f'{self.image_cursor + 1}/{len(self.pages)}')
        self.canvas.yview_moveto(0)
        self.canvas.xview_moveto(0)


def show_in_tk(title, pages, info):
    root = Tk()
    root.geometry('700x700')
    frame = ScrolledCanvas(root)
    frame.info_text = '\n'.join([f'{key}: {value}' for key, value in info.items()])
    frame.pages = pages
    frame.pack(side=TOP)
    button_frame = Frame(root)
    button_next = Button(button_frame, text='Next', command=lambda: frame.show_image(1))
    button_exit = Button(button_frame, text='Exit', command=root.quit)
    counter = Label(button_frame)
    button_prev = Button(button_frame, text='Previous', command=lambda: frame.show_image(-1))
    counter.grid(row=0, column=1)
    button_exit.grid(row=0, column=2)
    button_next.grid(row=0, column=3)
    button_prev.grid(row=0, column=0)
    frame.next_btn = button_next
    frame.prev_btn = button_prev
    frame.counter = counter
    button_frame.pack(side=BOTTOM)
    root.bind('<Left>', lambda x: frame.show_image(-1) if button_prev['state'] == NORMAL else True)
    root.bind('<Right>', lambda x: frame.show_image(1) if button_next['state'] == NORMAL else True)
    root.bind('<Escape>', lambda x: root.quit())
    frame.show_image(1)
    root.title(title)
    root.mainloop()
