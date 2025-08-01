import tkinter as tk
from datetime import datetime, timedelta
from tkinter import font as tkfont
import hijri_converter
import pytz
import locale

class EnhancedNeonCalendarClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Neon Calendar Clock")
        self.root.geometry("1000x800")
        self.root.configure(bg='#111111')
        
        # Initialize glow effect variables first
        self.glow_phase = 0
        self.glow_direction = 1
        
        # Set default timezone (Asia/Dhaka)
        self.local_tz = pytz.timezone('Asia/Dhaka')
        
        # Set locale to English for Gregorian dates
        try:
            locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
        except:
            locale.setlocale(locale.LC_TIME, '')
        
        # Enhanced neon color scheme with glow effect
        self.colors = {
            'time': ('#00ffff', '#00ffff', '#00ffff'),  # Cyan with glow
            'bangla': ('#ff00ff', '#ff00ff', '#ff00ff'),  # Magenta
            'hijri': ('#cc00ff', '#cc00ff', '#cc00ff'),   # Purple
            'bengali': ('#00ff99', '#00ff99', '#00ff99'), # Green
            'title': ('#ffff00', '#ffff00', '#ffff00'),   # Yellow
            'border': ('#222222', '#444444', '#666666')   # Border shades
        }
        
        # Font configuration with fallbacks
        self.fonts = {
            'time': self.get_font("Arial", 100, "bold"),
            'date': self.get_font("Arial", 50),
            'bangla': self.get_font("SolaimanLipi", 50, fallback="Vrinda"),
            'title': self.get_font("Arial", 30, "bold")
        }
        
        # Main container with gradient border
        self.main_frame = tk.Frame(root, bg='black', bd=5, 
                                  relief=tk.RIDGE, highlightthickness=3,
                                  highlightbackground=self.colors['border'][0],
                                  highlightcolor=self.colors['border'][2])
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Create displays
        self.create_time_display()
        self.create_calendar_display()
        
        # Initial update
        self.update_clock()
    
    def get_font(self, family, size, weight="normal", fallback=None):
        """Get font with fallback options"""
        try:
            return tkfont.Font(family=family, size=size, weight=weight)
        except:
            if fallback:
                return tkfont.Font(family=fallback, size=size, weight=weight)
            return tkfont.Font(family="Arial", size=size, weight=weight)
    
    def create_time_display(self):
        """Create the centered time display with glow effect"""
        time_frame = tk.Frame(self.main_frame, bg='black')
        time_frame.pack(pady=(40, 30))
        
        # Local time label with subtle border
        tk.Label(
            time_frame,
            text="LOCAL TIME",
            font=self.fonts['title'],
            fg=self.colors['title'][0],
            bg='black',
            bd=2,
            relief=tk.RIDGE
        ).pack(pady=(0, 10))
        
        # English time with multiple layers for glow
        self.english_time = tk.Label(
            time_frame,
            font=self.fonts['time'],
            fg=self.colors['time'][0],
            bg='black'
        )
        self.english_time.pack(pady=(10, 0))
        
        # Bangla time with shadow effect
        self.bangla_time = tk.Label(
            time_frame,
            font=self.fonts['bangla'],
            fg=self.colors['bangla'][0],
            bg='black'
        )
        self.bangla_time.pack(pady=(20, 0))
    
    def create_calendar_display(self):
        """Create the calendar display with better spacing"""
        calendar_frame = tk.Frame(
            self.main_frame,
            bg='black',
            padx=40,
            pady=20
        )
        calendar_frame.pack(expand=True)
        
        # Gregorian calendar with border
        gregorian_frame = tk.Frame(calendar_frame, bg='black', bd=2, relief=tk.RIDGE)
        gregorian_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            gregorian_frame,
            text="GREGORIAN DATE",
            font=self.fonts['title'],
            fg=self.colors['title'][0],
            bg='black'
        ).pack()
        
        self.gregorian_date = tk.Label(
            gregorian_frame,
            font=self.fonts['date'],
            fg='white',
            bg='black'
        )
        self.gregorian_date.pack(pady=(5, 10))
        
        # Hijri calendar with transition note
        hijri_frame = tk.Frame(calendar_frame, bg='black', bd=2, relief=tk.RIDGE)
        hijri_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            hijri_frame,
            text="HIJRI DATE",
            font=self.fonts['title'],
            fg=self.colors['hijri'][0],
            bg='black'
        ).pack()
        
        self.hijri_date = tk.Label(
            hijri_frame,
            font=self.fonts['date'],
            fg=self.colors['hijri'][0],
            bg='black'
        )
        self.hijri_date.pack(pady=(5, 10))
        
        # Bengali calendar with transition note
        bengali_frame = tk.Frame(calendar_frame, bg='black', bd=2, relief=tk.RIDGE)
        bengali_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            bengali_frame,
            text="BENGALI DATE",
            font=self.fonts['title'],
            fg=self.colors['bengali'][0],
            bg='black'
        ).pack()
        
        self.bengali_date = tk.Label(
            bengali_frame,
            font=self.fonts['bangla'],
            fg=self.colors['bengali'][0],
            bg='black'
        )
        self.bengali_date.pack(pady=(5, 10))
    
    def to_bangla_digits(self, number):
        """Convert to Bangla digits with proper formatting"""
        bangla_digits = {
            '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪',
            '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'
        }
        return ''.join([bangla_digits.get(d, d) for d in str(number)])
    
    def get_local_time(self):
        """Get current local time with timezone"""
        return datetime.now(self.local_tz)
    
    def get_hijri_date(self):
        """Get accurate Hijri date with proper sunset transition (showing 1 day less)"""
        now = self.get_local_time()
        
        # Calculate sunset time (simplified - in reality should use proper calculation)
        sunset_hour = 18  # 6 PM as approximation
        
        # Get today's Gregorian date
        gregorian_date = now.date()
        
        # Convert to Hijri and subtract 1 day
        hijri = hijri_converter.Gregorian(
            gregorian_date.year,
            gregorian_date.month,
            gregorian_date.day
        ).to_hijri()
        
        # Subtract one day from the Hijri date
        hijri_day = hijri.day - 1
        hijri_month = hijri.month
        hijri_year = hijri.year
        
        # Handle day underflow (previous month)
        if hijri_day < 1:
            hijri_month -= 1
            if hijri_month < 1:
                hijri_month = 12
                hijri_year -= 1
            # Get days in previous month
            prev_month = hijri_converter.Hijri(hijri_year, hijri_month, 1)
            hijri_day = prev_month.month_length()
        
        # Only show tomorrow's date if it's after sunset AND the Hijri date would actually change
        if now.hour >= sunset_hour:
            tomorrow = (now + timedelta(days=1)).date()
            hijri_tomorrow = hijri_converter.Gregorian(
                tomorrow.year,
                tomorrow.month,
                tomorrow.day
            ).to_hijri()
            
            # Subtract one day from tomorrow's date
            hijri_tomorrow_day = hijri_tomorrow.day - 1
            hijri_tomorrow_month = hijri_tomorrow.month
            hijri_tomorrow_year = hijri_tomorrow.year
            
            if hijri_tomorrow_day < 1:
                hijri_tomorrow_month -= 1
                if hijri_tomorrow_month < 1:
                    hijri_tomorrow_month = 12
                    hijri_tomorrow_year -= 1
                # Get days in previous month
                prev_month = hijri_converter.Hijri(hijri_tomorrow_year, hijri_tomorrow_month, 1)
                hijri_tomorrow_day = prev_month.month_length()
            
            # Only use tomorrow's date if it's different
            if hijri.day != hijri_tomorrow.day or hijri.month != hijri_tomorrow.month:
                hijri_tomorrow = hijri_converter.Hijri(hijri_tomorrow_year, hijri_tomorrow_month, hijri_tomorrow_day)
                return f"{hijri_tomorrow_day} {hijri_tomorrow.month_name()}, {hijri_tomorrow_year} AH"
        
        hijri = hijri_converter.Hijri(hijri_year, hijri_month, hijri_day)
        return f"{hijri_day} {hijri.month_name()}, {hijri_year} AH"
    
    def get_bengali_date(self):
        """Get Bengali date with proper sunrise transition"""
        now = self.get_local_time()
        
        # Calculate sunrise time (simplified - 6 AM as approximation)
        sunrise_hour = 6
        
        # If current time is after sunrise, use today's date
        if now.hour >= sunrise_hour:
            gregorian_date = now.date()
        else:
            gregorian_date = (now - timedelta(days=1)).date()
        
        bangla_months = [
            'বৈশাখ', 'জ্যৈষ্ঠ', 'আষাঢ়', 'শ্রাবণ',
            'ভাদ্র', 'আশ্বিন', 'কার্তিক', 'অগ্রহায়ণ',
            'পৌষ', 'মাঘ', 'ফাল্গুন', 'চৈত্র'
        ]
        
        # Calculate Bengali year (1429 = 2022-2023)
        if (gregorian_date.month > 4) or (gregorian_date.month == 4 and gregorian_date.day >= 14):
            bengali_year = gregorian_date.year - 593
        else:
            bengali_year = gregorian_date.year - 594
            
        # Calculate Bengali month and day
        month_offset = 3 if gregorian_date.day > 13 else 4
        bengali_month = (gregorian_date.month - month_offset) % 12
        if bengali_month == 0:
            bengali_month = 12
            
        bengali_day = gregorian_date.day - 13 if gregorian_date.day > 13 else (31 if gregorian_date.month-1 in [0,2,4,6,7,9,11] else 30) - (13 - gregorian_date.day)
        
        return f"{self.to_bangla_digits(bengali_day)} {bangla_months[bengali_month-1]}, {self.to_bangla_digits(bengali_year)}"
    
    def update_glow_effect(self):
        """Update the glow effect animation"""
        self.glow_phase += 0.1 * self.glow_direction
        if self.glow_phase >= 1:
            self.glow_direction = -1
        elif self.glow_phase <= 0:
            self.glow_direction = 1
        
        # Update colors based on glow phase
        for color_name in self.colors:
            base_color = self.colors[color_name][0]
            r, g, b = [int(base_color[i:i+2], 16) for i in (1, 3, 5)]
            r = min(255, int(r * (0.8 + 0.2 * self.glow_phase)))
            g = min(255, int(g * (0.8 + 0.2 * self.glow_phase)))
            b = min(255, int(b * (0.8 + 0.2 * self.glow_phase)))
            glow_color = f"#{r:02x}{g:02x}{b:02x}"
            self.colors[color_name] = (base_color, glow_color, base_color)
    
    def update_clock(self):
        """Update all displays with animations"""
        local_time = self.get_local_time()
        
        # Update glow effect
        self.update_glow_effect()
        
        # Update time displays with glow
        self.english_time.config(
            text=local_time.strftime("%I:%M:%S %p"),
            fg=self.colors['time'][1]
        )
        
        # Bangla time with glow
        hour = self.to_bangla_digits(local_time.strftime("%I"))
        minute = self.to_bangla_digits(local_time.strftime("%M"))
        second = self.to_bangla_digits(local_time.strftime("%S"))
        ampm = "PM" if local_time.strftime("%p") == "PM" else "AM"
        self.bangla_time.config(
            text=f"{hour}:{minute}:{second} {ampm}",
            fg=self.colors['bangla'][1]
        )
        
        # Update calendar displays
        # Force English locale for Gregorian date
        self.gregorian_date.config(text=local_time.strftime("%A, %B %d, %Y"))
        
        # Hijri date with glow (showing 1 day less)
        self.hijri_date.config(
            text=self.get_hijri_date(),
            fg=self.colors['hijri'][1]
        )
        
        # Bengali date with glow
        self.bengali_date.config(
            text=self.get_bengali_date(),
            fg=self.colors['bengali'][1]
        )
        
        # Schedule next update
        self.root.after(100, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedNeonCalendarClock(root)
    root.mainloop()