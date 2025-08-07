from tkinter import *


class Converter:

    def __init__(self, parent):

        # contains formatting
        padding_x = 10
        padding_y = 10
        background_color = "light blue"

        # GUI
        # Frame set up
        self.converter_frame = Frame(parent,  bg=background_color, padx=padding_x, pady=padding_y)
        self.converter_frame.grid()

        # Create GUI
        self.heading_label = Label(self.converter_frame, text="Temperature Converter", font=("Arial", "16", "bold"),
                                   bg=background_color)
        self.heading_label.grid(row=0, columnspan=2, padx=20, pady=20)

        self.var1 = IntVar()    # variable holds result of button push

        self.rb1 = Radiobutton(self.converter_frame, text="Degrees to Farenheit", variable=self.var1,
                               bg=background_color, value=1, command=self.convert)
        self.rb1.grid(row=1, column=0, sticky=E)

        self.rb2 = Radiobutton(self.converter_frame, text="Farenheit to Degrees", variable=self.var1,
                               bg=background_color, value=2, command=self.convert)
        self.rb2.grid(row=1, column=1, sticky=W)

        self.temp_scale = Scale(self.converter_frame, from_=-50, to=120, orient=HORIZONTAL, length=200,
                                bg=background_color)
        self.temp_scale.grid(row=2, columnspan=2, padx=20, pady=20)

        self.convert_it = Button(self.converter_frame, text="convert", command=self.convert)
        self.convert_it.grid(row=3, column=0, padx=10, pady=10)

        self.answer_label = Label(self.converter_frame, text="Choose an option", bg=background_color)
        self.answer_label.grid(row=3, column=1, padx=10, pady=10, sticky=E)

    def convert(self):

        answer = self.temp_scale.get()
        if self.var1.get() == 2:
            from_f = (answer - 32) * 5 / 9
            choice = ("{} degrees F is {:.2f} degrees C".format(answer, from_f))
        else:
            from_c = (9 / 5)*answer + 32
            choice = ("{} degrees C is {:.2f} degrees F".format(answer, from_c))

        self.answer_label.configure(text=choice)
        return self.var1.get()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Convertor")
    convert_it = Converter(root)
    # uncomment the line below to see what it does (helps instance understanding)
    # convert_it_two = Converter (root)
    root.mainloop()