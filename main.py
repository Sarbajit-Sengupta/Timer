from countdown import Countdown, parse_duration
from tkinter import *
from tkinter import messagebox

# creating Tk window
root = Tk()

# setting geometry of tk window
root.geometry("300x250")

# Using title() to display a message in
# the dialogue box of the message in the
# title bar.
root.title("Time Counter")

# Declaration of variables
hour = StringVar()
minute = StringVar()
second = StringVar()

# setting the default value as 0
hour.set("00")
minute.set("00")
second.set("00")

# Use of Entry class to take input from the user
hourEntry = Entry(root, width=3, font=("Arial", 18, ""),
                  textvariable=hour)
hourEntry.place(x=80, y=20)

minuteEntry = Entry(root, width=3, font=("Arial", 18, ""),
                    textvariable=minute)
minuteEntry.place(x=130, y=20)

secondEntry = Entry(root, width=3, font=("Arial", 18, ""),
                    textvariable=second)
secondEntry.place(x=180, y=20)


def display(hours, minutes, seconds):
    hour.set(f"{hours:02d}")
    minute.set(f"{minutes:02d}")
    second.set(f"{seconds:02d}")


timer = Countdown(root, display,
                  lambda: messagebox.showinfo("Time Countdown", "Time's up"))


def submit():
    try:
        duration = parse_duration(hour.get(), minute.get(), second.get())
    except ValueError:
        messagebox.showerror("Invalid time", "Enter nonnegative whole numbers.")
        return
    timer.start(duration)


def close():
    timer.cancel()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close)


# button widget
btn = Button(root, text='Set Time Countdown', bd='5',
             command=submit)
btn.place(x=70, y=120)

# infinite loop which is required to
# run tkinter program infinitely
# until an interrupt occurs
root.mainloop()