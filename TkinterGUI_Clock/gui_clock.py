"""
File: gui_clock.py

Author: Abdelrahman Mohamed

Task Description: This file contains the main program logic for the clock GUI application.
The GUI is created using the Tkinter library and includes a display for the current time,
day of week, and date, as well as buttons for starting/stopping a timer, selecting the timer file location,
and setting a countdown timer. The program updates the display and handles user input
using event-driven programming techniques.

"""

# Import necessary modules
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import time


# Define a class called ClockApp
class ClockApp:
    # Initialize the ClockApp object with a root window
    def __init__(self, root):
        # Assign the root window to an instance variable
        self.root = root
        # Assign the root window to an instance variable
        self.root.title("Clock App")

        # Set the initial timer state to not running
        self.timer_running = False
        # Set the initial start and end times to 0
        self.start_time = 0
        self.end_time = 0

        # create and format clock display
        self.clock_display = tk.Label(
            self.root,
            font=("Arial", 30),
            fg="blue",
            bg="pink",
            width=20,
            height=2
        )
        self.clock_display.pack(pady=10)

        # create and format day of week display
        self.day_display = tk.Label(self.root, font=("Arial", 20))
        self.day_display.pack(pady=5)

        # create and format date display
        self.date_display = tk.Label(self.root, font=("Arial", 20))
        self.date_display.pack(pady=5)

        # create timer button
        self.timer_button = tk.Button(self.root, text="Start Timer", font=("Arial", 14), command=self.toggle_timer)
        self.timer_button.pack(pady=10)

        # create and format editable text field for timer file location
        self.timer_file_path = tk.StringVar()
        self.timer_file_path.set("timings.txt")
        self.file_entry = tk.Entry(self.root, textvariable=self.timer_file_path, font=("Arial", 12), width=30)
        self.file_entry.pack(pady=5)

        # create button for file selection
        self.file_button = tk.Button(self.root, text="Choose File", font=("Arial", 12), command=self.choose_file)
        self.file_button.pack(pady=5)

        # update clock display and day of week and date labels
        self.update_clock()
        self.update_day_date()

        # create and format minutes entry field
        self.minutes_entry = tk.Entry(self.root, font=("Arial", 14), width=5)
        self.minutes_entry.pack(side="left", padx=10, pady=10)

        # create and format seconds entry field
        self.seconds_entry = tk.Entry(self.root, font=("Arial", 14), width=5)
        self.seconds_entry.pack(side="left", padx=10, pady=10)

        # create and format start button for countdown timer
        self.start_button = tk.Button(self.root, text="Start Countdown", font=("Arial", 14),
                                      command=self.start_countdown)
        self.start_button.pack(side="left", padx=10, pady=10)

        # create and format countdown display
        self.countdown_display = tk.Label(self.root, font=("Arial", 30), fg="red")
        self.countdown_display.pack(pady=10)

    def update_clock(self):
        # Update the clock display every second
        current_time = time.strftime("%I:%M:%S %p")
        self.clock_display.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def update_day_date(self):
        # Update the day and date display every second
        current_day = time.strftime("%A")
        current_date = time.strftime("%d.%B %Y")
        self.day_display.config(text=current_day)
        self.date_display.config(text=current_date)
        self.root.after(1000, self.update_day_date)

    def toggle_timer(self):
        # Start or stop the timer depending on its current state
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_button.config(text="Stop Timer", bg="red")
            self.timer_running = True
        else:
            self.end_time = time.time()
            self.timer_button.config(text="Start Timer", bg="green")
            self.timer_running = False
            self.save_timings()

    def save_timings(self):
        # Save the start and end times, and the duration of the timer to a file
        duration = self.end_time - self.start_time
        with open(self.timer_file_path.get(), "a") as f:
            f.write(f"Start time: {time.ctime(self.start_time)}, "
                    f"End time: {time.ctime(self.end_time)}, "
                    f"Duration: {duration:.2f} seconds\n")

    def choose_file(self):
        # Open a file dialog to let the user choose a file for the timer data
        file_path = filedialog.askopenfilename(initialdir="/", title="Select File",
                                               filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        self.timer_file_path.set(file_path)

    def start_countdown(self):
        minutes = int(self.minutes_entry.get())
        seconds = int(self.seconds_entry.get())

        # calculate total countdown time in seconds
        total_seconds = minutes * 60 + seconds

        # disable entry fields and start button
        self.minutes_entry.config(state="disabled")
        self.seconds_entry.config(state="disabled")
        self.start_button.config(state="disabled")

        # start countdown
        self.countdown(total_seconds)

    def countdown(self, remaining):
        if remaining >= 0:
            # convert remaining time to minutes and seconds
            minutes = remaining // 60
            seconds = remaining % 60

            # update countdown display
            self.countdown_display.config(text=f"{minutes:02d}:{seconds:02d}")

            # decrement remaining time and call countdown function again
            self.root.after(1000, self.countdown, remaining - 1)
        else:
            # re-enable entry fields and start button
            self.minutes_entry.config(state="normal")
            self.seconds_entry.config(state="normal")
            self.start_button.config(state="normal")

            # show message box
            messagebox.showinfo("Countdown Finished", "The countdown has finished!")


root = tk.Tk()
app = ClockApp(root)
root.mainloop()
