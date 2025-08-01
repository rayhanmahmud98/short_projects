import tkinter as tk
from tkinter import font as tkfont
from datetime import datetime, timedelta
import hijri_converter
import pytz
import sys
import os
import json

class NeonCalendarScreensaver:
    def __init__(self, root, is_screensaver=True):
        self.root = root
        self.is_screensaver = is_screensaver
        self.config = self.load_config()
        
        # Screensaver setup
        if self.is_screensaver:
            self.root.attributes('-fullscreen', True)
            self.root.configure(cursor='none')
            self.root.bind('<Any-KeyPress>', self.exit_screensaver)
            self.root.bind('<ButtonPress>', self.exit_screensaver)
            self.root.bind('<Motion>', self.exit_screensaver)
        else:
            self.root.geometry("1000x800")
        
        # Timezone setup
        self.local_tz = pytz.timezone(self.config.get('timezone', 'Asia/Dhaka'))
        
        # Initialize glow effect
        self.glow_phase = 0
        self.glow_direction = 1
        self.glow_speed = 0.05
        
        # Color scheme
        self.colors = {
            'time': '#00ffff',  # Cyan
            'bangla': '#ff00ff',  # Magenta
            'hijri': '#cc00ff',   # Purple
            'bengali': '#00ff99', # Green
            'title': '#ffff00',   # Yellow
            'border': '#444444'   # Border
        }
        
        # Font setup
        self.fonts = {
            'time': self.get_font("Arial", 100, "bold"),
            'date': self.get_font("Arial", 50),
            'bangla': self.get_font("SolaimanLipi", 50, fallback="Vrinda"),
            'title': self.get_font("Arial", 30, "bold")
        }
        
        # Main UI setup
        self.setup_ui()
        self.update_clock()

    def get_font(self, family, size, weight="normal", fallback=None):
        try:
            return tkfont.Font(family=family, size=size, weight=weight)
        except:
            if fallback:
                return tkfont.Font(family=fallback, size=size, weight=weight)
            return tkfont.Font(family="Arial", size=size, weight=weight)

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Time display
        self.setup_time_display()
        
        # Calendar displays
        self.setup_calendar_display()

    def setup_time_display(self):
        time_frame = tk.Frame(self.main_frame, bg='black')
        time_frame.pack(pady=(40, 30))
        
        tk.Label(
            time_frame,
            text="LOCAL TIME",
            font=self.fonts['title'],
            fg=self.colors['title'],
            bg='black'
        ).pack()
        
        self.english_time = tk.Label(
            time_frame,
            font=self.fonts['time'],
            fg=self.colors['time'],
            bg='black'
        )
        self.english_time.pack(pady=(10, 0))
        
        self.bangla_time = tk.Label(
            time_frame,
            font=self.fonts['bangla'],
            fg=self.colors['bangla'],
            bg='black'
        )
        self.bangla_time.pack(pady=(20, 0))

    def setup_calendar_display(self):
        calendar_frame = tk.Frame(self.main_frame, bg='black', padx=40, pady=20)
        calendar_frame.pack(expand=True)
        
        # Gregorian date
        self.add_calendar_section(
            calendar_frame,
            "GREGORIAN DATE",
            self.colors['title'],
            'white',
            self.fonts['date']
        )
        
        # Hijri date
        self.add_calendar_section(
            calendar_frame,
            "HIJRI DATE",
            self.colors['hijri'],
            self.colors['hijri'],
            self.fonts['date']
        )
        
        # Bengali date
        self.add_calendar_section(
            calendar_frame,
            "BENGALI DATE",
            self.colors['bengali'],
            self.colors['bengali'],
            self.fonts['bangla']
        )

    def add_calendar_section(self, parent, title, title_color, text_color, font):
        frame = tk.Frame(parent, bg='black', bd=2, relief=tk.RIDGE)
        frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            frame,
            text=title,
            font=self.fonts['title'],
            fg=title_color,
            bg='black'
        ).pack()
        
        label = tk.Label(
            frame,
            font=font,
            fg=text_color,
            bg='black'
        )
        label.pack(pady=(5, 10))
        
        # Store reference to the label
        if "GREGORIAN" in title:
            self.gregorian_date = label
        elif "HIJRI" in title:
            self.hijri_date = label
        elif "BENGALI" in title:
            self.bengali_date = label

    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'screensaver_config.json')
        default_config = {
            'timezone': 'Asia/Dhaka',
            'hijri_offset': -1,  # Show 1 day less
            'glow_speed': 0.05
        }
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            return default_config

    def save_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'screensaver_config.json')
        with open(config_path, 'w') as f:
            json.dump(self.config, f)

    def exit_screensaver(self, event=None):
        if self.is_screensaver:
            self.root.destroy()
            sys.exit()

    def to_bangla_digits(self, number):
        bangla_digits = {
            '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪',
            '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'
        }
        return ''.join([bangla_digits.get(d, d) for d in str(number)])

    def get_local_time(self):
        return datetime.now(self.local_tz)

    def get_hijri_date(self):
        now = self.get_local_time()
        sunset_hour = 18  # 6 PM as approximation
        
        gregorian_date = now.date()
        hijri = hijri_converter.Gregorian(
            gregorian_date.year,
            gregorian_date.month,
            gregorian_date.day
        ).to_hijri()
        
        # Apply offset (show 1 day less)
        hijri_day = hijri.day + self.config.get('hijri_offset', -1)
        hijri_month = hijri.month
        hijri_year = hijri.year
        
        # Handle day underflow
        if hijri_day < 1:
            hijri_month -= 1
            if hijri_month < 1:
                hijri_month = 12
                hijri_year -= 1
            prev_month = hijri_converter.Hijri(hijri_year, hijri_month, 1)
            hijri_day = prev_month.month_length()
        
        # Handle sunset transition
        if now.hour >= sunset_hour:
            tomorrow = (now + timedelta(days=1)).date()
            hijri_tomorrow = hijri_converter.Gregorian(
                tomorrow.year,
                tomorrow.month,
                tomorrow.day
            ).to_hijri()
            
            hijri_tomorrow_day = hijri_tomorrow.day + self.config.get('hijri_offset', -1)
            hijri_tomorrow_month = hijri_tomorrow.month
            hijri_tomorrow_year = hijri_tomorrow.year
            
            if hijri_tomorrow_day < 1:
                hijri_tomorrow_month -= 1
                if hijri_tomorrow_month < 1:
                    hijri_tomorrow_month = 12
                    hijri_tomorrow_year -= 1
                prev_month = hijri_converter.Hijri(hijri_tomorrow_year, hijri_tomorrow_month, 1)
                hijri_tomorrow_day = prev_month.month_length()
            
            if hijri.day != hijri_tomorrow.day or hijri.month != hijri_tomorrow.month:
                hijri_tomorrow = hijri_converter.Hijri(hijri_tomorrow_year, hijri_tomorrow_month, hijri_tomorrow_day)
                return f"{hijri_tomorrow_day} {hijri_tomorrow.month_name()}, {hijri_tomorrow_year} AH"
        
        hijri = hijri_converter.Hijri(hijri_year, hijri_month, hijri_day)
        return f"{hijri_day} {hijri.month_name()}, {hijri_year} AH"

    def get_bengali_date(self):
        now = self.get_local_time()
        sunrise_hour = 6
        
        if now.hour >= sunrise_hour:
            gregorian_date = now.date()
        else:
            gregorian_date = (now - timedelta(days=1)).date()
        
        bangla_months = [
            'বৈশাখ', 'জ্যৈষ্ঠ', 'আষাঢ়', 'শ্রাবণ',
            'ভাদ্র', 'আশ্বিন', 'কার্তিক', 'অগ্রহায়ণ',
            'পৌষ', 'মাঘ', 'ফাল্গুন', 'চৈত্র'
        ]
        
        if (gregorian_date.month > 4) or (gregorian_date.month == 4 and gregorian_date.day >= 14):
            bengali_year = gregorian_date.year - 593
        else:
            bengali_year = gregorian_date.year - 594
            
        month_offset = 3 if gregorian_date.day > 13 else 4
        bengali_month = (gregorian_date.month - month_offset) % 12
        if bengali_month == 0:
            bengali_month = 12
            
        bengali_day = gregorian_date.day - 13 if gregorian_date.day > 13 else (31 if gregorian_date.month-1 in [0,2,4,6,7,9,11] else 30) - (13 - gregorian_date.day)
        
        return f"{self.to_bangla_digits(bengali_day)} {bangla_months[bengali_month-1]}, {self.to_bangla_digits(bengali_year)}"

    def update_glow_effect(self):
        self.glow_phase += self.glow_speed * self.glow_direction
        if self.glow_phase >= 1:
            self.glow_direction = -1
        elif self.glow_phase <= 0:
            self.glow_direction = 1
        
        for color_name in ['time', 'bangla', 'hijri', 'bengali', 'title']:
            base_color = self.colors[color_name]
            r, g, b = [int(base_color[i:i+2], 16) for i in (1, 3, 5)]
            r = min(255, int(r * (0.8 + 0.2 * self.glow_phase)))
            g = min(255, int(g * (0.8 + 0.2 * self.glow_phase)))
            b = min(255, int(b * (0.8 + 0.2 * self.glow_phase)))
            glow_color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Update all labels with this color
            for widget in self.main_frame.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget('fg') == base_color:
                    widget.config(fg=glow_color)

    def update_clock(self):
        local_time = self.get_local_time()
        
        self.update_glow_effect()
        
        # Update time displays
        self.english_time.config(text=local_time.strftime("%I:%M:%S %p"))
        
        hour = self.to_bangla_digits(local_time.strftime("%I"))
        minute = self.to_bangla_digits(local_time.strftime("%M"))
        second = self.to_bangla_digits(local_time.strftime("%S"))
        ampm = "PM" if local_time.strftime("%p") == "PM" else "AM"
        self.bangla_time.config(text=f"{hour}:{minute}:{second} {ampm}")
        
        # Update calendar displays
        self.gregorian_date.config(text=local_time.strftime("%A, %B %d, %Y"))
        self.hijri_date.config(text=self.get_hijri_date())
        self.bengali_date.config(text=self.get_bengali_date())
        
        self.root.after(100, self.update_clock)

def show_config_dialog():
    root = tk.Tk()
    root.title("Screensaver Settings")
    root.geometry("400x300")
    
    # Add your configuration controls here
    tk.Label(root, text="Screensaver Configuration").pack(pady=20)
    
    tk.Button(root, text="Save", command=root.destroy).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg.startswith('/p'):  # Preview
            root = tk.Tk()
            NeonCalendarScreensaver(root, is_screensaver=False)
            root.mainloop()
        
        elif arg.startswith('/s'):  # Fullscreen
            root = tk.Tk()
            NeonCalendarScreensaver(root)
            root.mainloop()
        
        elif arg.startswith('/c'):  # Configure
            show_config_dialog()
        
        else:  # Test mode
            root = tk.Tk()
            NeonCalendarScreensaver(root, is_screensaver=False)
            root.mainloop()
    else:
        root = tk.Tk()
        NeonCalendarScreensaver(root, is_screensaver=False)
        root.mainloop()