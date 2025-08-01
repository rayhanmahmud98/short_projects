import tkinter as tk
import time
import math
from datetime import datetime
from hijri_converter import Gregorian
import bangla  # ✅ Correct way to import


# Clock setup
root = tk.Tk()
root.title("🕒 Neon Analog Clock with Dates")

canvas_size = 360
center_x = center_y = canvas_size // 2
clock_radius = canvas_size // 2 - 20
canvas = tk.Canvas(root, width=canvas_size, height=canvas_size + 80, bg='black')
canvas.pack()

# Hour colors (different neon shades)
hour_colors = [
    "#FF00FF", "#00FFFF", "#7FFF00", "#FF4500", "#00FF00", "#00BFFF",
    "#FFD700", "#DC143C", "#00CED1", "#FF69B4", "#ADFF2F", "#1E90FF"
]

def draw_clock_face():
    canvas.delete("clock_face")
    # Outer circle
    canvas.create_oval(center_x - clock_radius, center_y - clock_radius,
                       center_x + clock_radius, center_y + clock_radius,
                       outline="cyan", width=4, tags="clock_face")

    for hour in range(1, 13):
        angle = math.radians(hour * 30 - 90)
        x = center_x + math.cos(angle) * (clock_radius - 30)
        y = center_y + math.sin(angle) * (clock_radius - 30)
        canvas.create_text(x, y, text=str(hour),
                           fill=hour_colors[hour - 1],
                           font=("Helvetica", 14, "bold"),
                           tags="clock_face")

def draw_hands():
    canvas.delete("hands")
    now = datetime.now()
    hour = now.hour % 12
    minute = now.minute
    second = now.second

    # Angles
    hour_angle = math.radians((hour + minute / 60) * 30 - 90)
    minute_angle = math.radians(minute * 6 - 90)
    second_angle = math.radians(second * 6 - 90)

    # Hand lengths
    hour_length = clock_radius * 0.5
    minute_length = clock_radius * 0.7
    second_length = clock_radius * 0.9

    # Draw hands
    canvas.create_line(center_x, center_y,
                       center_x + hour_length * math.cos(hour_angle),
                       center_y + hour_length * math.sin(hour_angle),
                       fill="lime", width=6, tags="hands")

    canvas.create_line(center_x, center_y,
                       center_x + minute_length * math.cos(minute_angle),
                       center_y + minute_length * math.sin(minute_angle),
                       fill="deepskyblue", width=4, tags="hands")

    canvas.create_line(center_x, center_y,
                       center_x + second_length * math.cos(second_angle),
                       center_y + second_length * math.sin(second_angle),
                       fill="magenta", width=2, tags="hands")

def draw_dates():
    canvas.delete("date")
    now_date = datetime.now()
    eng_date = now_date.strftime("%A, %d %B %Y")

    # Bengali date as Bangla digits
    bengali_date = bangla.convert_english_digit_to_bangla_digit(now_date.strftime("%d-%m-%Y"))

    # Hijri date using hijri_converter
    arabic_date = Gregorian(now_date.year, now_date.month, now_date.day).to_hijri().isoformat()

    # Show under clock
    base_y = canvas_size + 10
    canvas.create_text(center_x, base_y, text=f"Gregorian: {eng_date}",
                       font=("Consolas", 10), fill='cyan', tags="date")
    canvas.create_text(center_x, base_y + 20, text=f"Bengali: {bengali_date}",
                       font=("Consolas", 10), fill='lime', tags="date")
    canvas.create_text(center_x, base_y + 40, text=f"Hijri: {arabic_date}",
                       font=("Consolas", 10), fill='magenta', tags="date")

def update_clock():
    draw_clock_face()
    draw_hands()
    draw_dates()
    root.after(1000, update_clock)

update_clock()
root.mainloop()
