from tkinter import *
from functools import partial  # to prevent unwanted windows
import all_constants as c
import conversion_rounding as cr
from datetime import date


# ---------- Helper functions ----------

def build_calculation_string(calculations, max_calcs):
    """Return a newline-separated string of calculations, newest first."""
    newest_first_list = list(reversed(calculations))
    if len(newest_first_list) <= max_calcs:
        return "\n".join(newest_first_list)
    return "\n".join(newest_first_list[:max_calcs])


def recolour_widgets(widgets, bg):
    """Apply a background colour to multiple widgets."""
    for w in widgets:
        w.config(bg=bg)

def export_calculations_to_txt(filename, calculations, date_obj):
    """Write calculations to a .txt file with header and date."""
    day, month, year = date_obj.strftime("%d"), date_obj.strftime("%m"), date_obj.strftime("%Y")

    with open(f"{filename}.txt", "w") as text_file:
        text_file.write("***** Weight Calculations ******\n")
        text_file.write(f"Generated: {day}/{month}/{year}\n\n")
        text_file.write("Here is your calculation history (oldest to newest)...\n")
        for item in calculations:
            text_file.write(item + "\n")


# ---------- Main Converter Class ----------

class Converter:
    """
    Weight conversion tool
    """

    def __init__(self):
        self.all_calculations_list = []

        self.weight_frame = Frame(padx=10, pady=10)
        self.weight_frame.grid()

        self.weight_heading = Label(
            self.weight_frame,
            text="Weight Convertor",
            font=("Arial", 16, "bold")
        )
        self.weight_heading.grid(row=0)

        instructions = ("Please enter a weight below and then press "
                        "one of the buttons to convert it from Grams "
                        "to Ounces.")
        self.weight_instructions = Label(
            self.weight_frame,
            text=instructions,
            wraplength=250, width=40,
            justify="left"
        )
        self.weight_instructions.grid(row=1)

        self.weight_entry = Entry(self.weight_frame, font=("Arial", 14))
        self.weight_entry.grid(row=2, padx=10, pady=10)

        error = "Please enter a number"
        self.answer_error = Label(
            self.weight_frame, text=error,
            fg="#084C99", font=("Arial", 14, "bold")
        )
        self.answer_error.grid(row=3)

        # Conversion, help and history / export buttons
        self.button_frame = Frame(self.weight_frame)
        self.button_frame.grid(row=4)

        button_details_list = [
            ["To Grams", "#692617", lambda: self.check_weight(c.ABS_ZERO_OUNCES), 0, 0],
            ["To Ounces", "#193A75", lambda: self.check_weight(c.ABS_ZERO_GRAMS), 0, 1],
            ["Help / Info", "#3F1975", self.to_help, 1, 0],
            ["History / Export", "#00B3A4", self.to_history, 1, 1]
        ]

        self.button_ref_list = []
        for item in button_details_list:
            make_button = Button(
                self.button_frame,
                text=item[0], bg=item[1],
                fg="#FFFFFF", font=("Arial", 12, "bold"),
                width=12, command=item[2]
            )
            make_button.grid(row=item[3], column=item[4], padx=5, pady=5)
            self.button_ref_list.append(make_button)

        self.to_help_button = self.button_ref_list[2]
        self.to_history_button = self.button_ref_list[3]
        self.to_history_button.config(state=DISABLED)

    def check_weight(self, min_weight):
        """Check if weight input is valid and run conversion."""
        to_convert = self.weight_entry.get().strip()

        self.answer_error.config(fg="#004C99", font=("Arial", 13, "bold"))
        self.weight_entry.config(bg="#FFFFFF")

        error = f"Enter a number more than / equal to {min_weight}"
        has_errors = False

        try:
            to_convert = float(to_convert)
            if to_convert >= min_weight:
                self.convert(min_weight, to_convert)
            else:
                has_errors = True
        except ValueError:
            has_errors = True

        if has_errors:
            self.answer_error.config(text=error, fg="#9C0000", font=("Arial", 10, "bold"))
            self.weight_entry.config(bg="#F4CCCC")
            self.weight_entry.delete(0, END)

    def convert(self, min_weight, to_convert):
        if min_weight == c.ABS_ZERO_GRAMS:
            answer = cr.to_ounces(to_convert)
            answer_statement = f"{to_convert}G is {answer}Oz"
        else:
            answer = cr.to_grams(to_convert)
            answer_statement = f"{to_convert}Oz is {answer}G"

        self.to_history_button.config(state=NORMAL)
        self.answer_error.config(text=answer_statement)
        self.all_calculations_list.append(answer_statement)
        print(self.all_calculations_list)

    def to_help(self):
        DisplayHelp(self)

    def to_history(self):
        HistoryExport(self, self.all_calculations_list)


# ---------- Help Window ----------

class DisplayHelp:

    def __init__(self, partner):
        background = "#CCDAFF"
        self.help_box = Toplevel()

        partner.to_help_button.config(state=DISABLED)
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200)
        self.help_frame.grid()

        self.help_heading_label = Label(
            self.help_frame,
            text="Help / Info",
            font=("Arial", 14, "bold")
        )
        self.help_heading_label.grid(row=0)

        help_text = ("To use the program, simply enter the weight "
                     "you wish to convert and then choose to convert "
                     "to either Grams or Ounces.\n\n"
                     "Please note that you cannot input a weight value below 0. "
                     "If you try to convert a weight that is less than 0, "
                     "you will get an error message.\n\n"
                     "To see your calculation history and export it to a text "
                     "file, please click the 'History / Export' button.")

        self.help_text_label = Label(
            self.help_frame,
            text=help_text, wraplength=350,
            justify="left"
        )
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(
            self.help_frame,
            font=("Arial", 12, "bold"),
            text="Dismiss", bg="#005CCC",
            fg="#FFFFFF",
            command=partial(self.close_help, partner)
        )
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        recolour_widgets([self.help_frame, self.help_heading_label,
                          self.help_text_label], background)

    def close_help(self, partner):
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


# ---------- History / Export Window ----------

class HistoryExport:

    def __init__(self, partner, calculations):
        self.history_box = Toplevel()

        partner.to_history_button.config(state=DISABLED)
        self.history_box.protocol('WM_DELETE_WINDOW',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box)
        self.history_frame.grid()

        if len(calculations) <= c.MAX_CALCS:
            calc_back = "#D5E8D4"
            calc_amount = "all your"
        else:
            calc_back = "#ffe6cc"
            calc_amount = (f"your recent calculations - "
                           f"showing {c.MAX_CALCS} / {len(calculations)}")

        recent_intro_txt = (f"Below are {calc_amount} calculations "
                           )

        newest_first_string = build_calculation_string(calculations, c.MAX_CALCS)

        export_instruction_txt = ("Please push <Export> to save your calculations in "
                                  "a file. If the filename already exists, it will be replaced.")

        history_labels_list = [
            ["History / Export", ("Arial", 16, "bold"), None],
            [recent_intro_txt, ("Arial", 11), None],
            [newest_first_string, ("Arial", 14), calc_back],
            [export_instruction_txt, ("Arial", 11), None],
        ]

        history_label_ref = []
        for count, item in enumerate(history_labels_list):
            make_label = Label(
                self.history_box, text=item[0], font=item[1],
                bg=item[2],
                wraplength=300, justify="left", pady=10, padx=20
            )
            make_label.grid(row=count)
            history_label_ref.append(make_label)

        self.export_filename_label = history_label_ref[3]

        self.history_button_frame = Frame(self.history_box)
        self.history_button_frame.grid(row=4)

        button_details_list = [
            ["Export", "#004C99", lambda: self.export_data(calculations), 0, 0],
            ["Close", "#666666", partial(self.close_history, partner), 0, 1],
        ]

        for btn in button_details_list:
            make_button = Button(
                self.history_button_frame,
                font=("Arial", 12, "bold"),
                text=btn[0], bg=btn[1],
                fg="#FFFFFF", width=12,
                command=btn[2]
            )
            make_button.grid(row=btn[3], column=btn[4], padx=10, pady=10)

    def export_data(self, calculations):
        today = date.today()
        file_name = f"weights_{today.strftime('%Y_%m_%d')}"
        success_string = f"Export Successful! The file is called {file_name}.txt"

        self.export_filename_label.config(
            bg="#009900", text=success_string, font=("Arial", 12, "bold")
        )

        export_calculations_to_txt(file_name, calculations, today)

    def close_history(self, partner):
        partner.to_history_button.config(state=NORMAL)
        self.history_box.destroy()


# ---------- Main Routine ----------

if __name__ == "__main__":
    root = Tk()
    root.title("Weight Convertor")
    Converter()
    root.mainloop()
