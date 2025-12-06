import tkinter as tk
from tkinter import ttk
import random


class LED(tk.Canvas):
    def __init__(self, parent, color="red", size="small"):
        self.status = "none"
        self.size = size
        # size settings
        if size == "small":
            self.diameter = 7
            pad = 1
        elif size == "big":
            self.diameter = 10
            pad = 1
        else:
            raise ValueError("size must be 'small' or 'big'")

        width = self.diameter + pad * 2
        height = self.diameter + pad * 2

        super().__init__(parent, width=width, height=height,
                         bg="white", highlightthickness=0)

        # pack automatically
        self.pack(pady=5)

        # draw LED
        self.oval = self.create_oval(
            pad, pad,
            pad + self.diameter, pad + self.diameter,
            fill=color,
            outline="black"
        )

    def set_color(self, color):
        """Change the LED color."""
        self.itemconfig(self.oval, fill=color)
        
    
    def set_status(self, status):
        self.status = status
        if self.size == "big":
            if self.status == "emergency":
                for i in range(20):
                    root.after(500 * i, lambda: self.set_color("#eb1313"))
                    root.after(500 * i + 250, lambda: self.set_color("#5c2828"))
            if self.status == "warning":
                self.set_color("#eb1313")
            elif self.status == "caution":
                self.set_color("#ebe72a")
            elif self.status == "ok":
                self.set_color("#3fe01b")
            else:
                self.set_color("#5c2828")

class LCD:
    def __init__(self, parent, lines=5, on_color="#151a14", off_color="#67a155", line_height_px=20):
        self.lines_count = lines
        self.mode = "off" #off, select, sent, compass
        self.line_height_px = line_height_px
        self.height_px = lines * line_height_px
        self.width_px = self.height_px * 2  # 2:1 aspect ratio
        self.safezone_angle = 45 

        # Colors for "on" and "off" pixels / text
        self.on_color = on_color
        self.off_color = off_color

        # Index of currently selected line (0-based)
        self.selected = 0

        # Text storage
        self.text_lines = [
            "Report Flooding",
            "Report Illness",
            "Rep. Road Damage",
            "Rep. Low Resources",
            "See Compass"
        ]

        # LCD frame and canvas
        self.frame = ttk.Frame(parent)
        self.frame.pack(side="left")

        self.canvas = tk.Canvas(
            self.frame,
            width=self.width_px,
            height=self.height_px,
            bg=self.off_color,
            highlightthickness=2,
            highlightbackground=off_color
        )
        self.canvas.pack()

        # Draw initial lines
        self.text_items = []
        for i in range(lines):
            y = i * line_height_px + line_height_px // 2
            item = self.canvas.create_text(
                5, y,
                anchor="w",
                text=self.text_lines[i],
                font=("Courier", 13),
                fill=self.on_color
            )
            self.text_items.append(item)

        self.update_display()

    def set_line(self, index, text):
        """Set text of a specific line (0-based) and update display."""
        if 0 <= index < self.lines_count:
            self.text_lines[index] = text
            self.update_display()

    def set_selected(self, index):
        """Set which line is inverted (0-based)."""
        if 0 <= index < self.lines_count:
            self.selected = index
            self.update_display()
    
    def seek_up(self):
        """Move selection up unless already at the top."""
        if self.selected > 0:
            self.set_selected(self.selected - 1)
        self.update_display()

    def seek_down(self):
        """Move selection down unless already at the bottom."""
        if self.selected < self.lines_count - 1:
            self.set_selected(self.selected + 1)
        self.update_display()
    
    def turn_on(self):
        self.mode = "select"
        self.update_display()

    def turn_off(self):
        self.mode = "off"
        self.update_display()
    
    def send(self):
        if self.selected < 4:
            self.mode = "sent"
            self.update_display()
        elif self.selected == 4:
            self.mode = "compass"
            self.update_display()
    
    def get_mode(self):
        return self.mode
    
    def select(self):
        self.mode = "select"
        self.update_display()

    def update_display(self):
        """Refresh the canvas to show current text and selected line."""
        if self.mode == "select":
            self.canvas.delete("all")
            self.text_items = []
            for i in range(self.lines_count):
                y = i * self.line_height_px + self.line_height_px // 2
                item = self.canvas.create_text(
                    5, y,
                    anchor="w",
                    text=self.text_lines[i],
                    font=("Courier", 13),
                    fill=self.on_color
                )
                self.text_items.append(item)
                
            for i, text in enumerate(self.text_lines):
                item = self.text_items[i]
                if i == self.selected:
                    # invert: off background, on text
                
                    self.canvas.itemconfig(item, fill=self.on_color)
                else:
                    # normal: on background, off text
                    self.canvas.itemconfig(item, fill=self.on_color)
                    
                    rect = self.canvas.create_rectangle(
                        0, i * self.line_height_px,
                        self.width_px, (i + 1) * self.line_height_px,
                        outline=self.on_color
                    )
                    
                self.canvas.coords(item, 5, i * self.line_height_px + self.line_height_px // 2)
                display_text = ""
                if i == self.selected:
                    # add two spaces before the text
                    display_text = "► " + text
                else:
                    display_text = text

                self.canvas.itemconfig(item, text=display_text)
        elif self.mode == "off":
            self.canvas.delete("all")
            self.canvas.create_rectangle(
                0, 0, self.width_px, self.height_px,
                fill=self.off_color,
                outline=""
            )
        elif self.mode == "sent":
            self.canvas.delete("all")
            self.canvas.create_rectangle(
                0, 0, self.width_px, self.height_px,
                fill=self.off_color,
                outline=""
            )
            y = 0 * self.line_height_px + self.line_height_px // 2
            item = self.canvas.create_text(
                5, y,
                anchor="w",
                text="Sent!",
                font=("Courier", 13),
                fill=self.on_color
            )
            self.canvas.itemconfig(item)
        elif self.mode == "compass":
            self.canvas.delete("all")

            # Fill background
            self.canvas.create_rectangle(
                0, 0, self.width_px, self.height_px,
                fill=self.off_color,
                outline=""
            )

            cx = self.width_px // 2
            cy = self.height_px // 2
            radius = min(self.width_px, self.height_px) // 3

            # --- Helper to compute endpoint from angle ---
            def endpoint(angle_deg):
                import math
                rad = math.radians(angle_deg)
                x = cx + radius * math.sin(rad)
                y = cy - radius * math.cos(rad)
                return x, y

            # --- North arrow (always straight up) ---
            nx, ny = endpoint(0)          # 0° = North
            self.canvas.create_line(
                cx, cy, nx, ny,
                fill=self.on_color,
                width=3
            )
            self.canvas.create_text(
                nx, ny - 10,
                text="N",
                fill=self.on_color,
                font=("Courier", 12)
            )

            # --- Safe zone direction arrow ---
            sx, sy = endpoint(self.safezone_angle)
            self.canvas.create_line(
                cx, cy, sx, sy,
                fill=self.on_color,
                width=3
            )
            self.canvas.create_text(
                sx, sy - 10,
                text="Z",
                fill=self.on_color,
                font=("Courier", 12)
            )

            return


def simulate_events():
    if system_on:
        status1 = random.choice(["emergency", "warning"])
        stat_led_1.set_status(status1)
        status2 = random.choice(["warning", "caution", "ok"])
        stat_led_2.set_status(status2)
        status3 = random.choice(["warning", "caution"])
        stat_led_3.set_status(status3)
        status4 = random.choice(["emergency", "warning", "caution", "ok"])
        stat_led_4.set_status(status4)
        root.after(10000, simulate_events)
    else:
        stat_led_1.set_status = "none"
        stat_led_2.set_status = "none"
        stat_led_3.set_status = "none"
        stat_led_4.set_status = "none"

class VerticalToggle(tk.Canvas):
    
    def __init__(self, parent, width=10, height=20, knob_height=None, **kwargs):
        super().__init__(parent, width=width, height=height,
                         bg="lightgray", highlightthickness=1,
                         highlightbackground="black", **kwargs)

        self.switch_width = width     # store width explicitly
        self.switch_height = height   # store height explicitly

        # Default knob height = half the switch height
        if knob_height is None:
            knob_height = height // 2

        self.knob_height = knob_height
        self.state = False  # OFF by default

        # Minimal padding
        self.pad = 1

        # Track
        self.track = self.create_rectangle(
            width // 2 - 1, self.pad,
            width // 2 + 2, height - self.pad,
            fill="gray30", outline=""
        )

        # Knob (start OFF = down)
        y = height - knob_height - self.pad
        self.knob = self.create_rectangle(
            1, y,
            width - 1, y + knob_height,
            fill="white", outline="black"
        )

        self.bind("<Button-1>", self.toggle)

    def toggle(self, event=None):
        global system_on
        self.state = not self.state
        self.update_knob()
        if self.state == True:
            led_on.set_color("#3fe01b")
            system_on = True
            simulate_events()
            lcd.turn_on()
        else:
            led_on.set_color("#325c28")
            system_on = False
            lcd.turn_off()

    def update_knob(self):
        if self.state:   # ON
            y = self.pad
        else:            # OFF
            y = self.switch_height - self.knob_height - self.pad

        self.coords(
            self.knob,
            1, y,
            self.switch_width - 1, y + self.knob_height
        )

def small_icon_button(parent, text, cmd):
    btn = tk.Button(
        parent,
        text=text,
        command=cmd,
        font=("Arial", 8),
        bd=1,                 # visible border
        relief="raised",      # normal button appearance
        padx=2, pady=1,       # small but still clickable
        width=5               # small width in characters
    )
    btn.pack(side="left", padx=3)
    return btn

def seek_up():
    if system_on:
        lcd.seek_up()

def confirm():
    global transmitting
    
    if system_on:
        transmit()

def transmit():
    if system_on:
        led_trans.set_color("#6359f0")
        lcd.send()

        for i in range(12):
            root.after(400 * i, lambda: led_trans.set_color("#6359f0"))
            root.after(400 * i + 200, lambda: led_trans.set_color("#2b2761"))

def cancel():
    if system_on:
        if lcd.mode == "sent" or lcd.mode == "compass":
            lcd.select()

def seek_down():
    if system_on:
        lcd.seek_down()

root = tk.Tk()
root.title("LED + LCD Display")

system_on = False

# --- TOP SECTION ---
top = ttk.Frame(root, padding=10)
top.pack(fill="both", expand=True)

# LEFT COLUMN: toggle + LED array vertically aligned
left_column = ttk.Frame(top)
left_column.pack(side="left", anchor="n", padx=(0, 20))

toggle = VerticalToggle(left_column)
toggle.pack(anchor="n", pady=2)

# LED array directly under the toggle
led_on = LED(parent=left_column, color="#325c28", size="small")
led_charge = LED(parent=left_column, color="#5c2828", size="small")
led_trans = LED(parent=left_column, color="#2b2761", size="small")
transmitting = False

# RIGHT SIDE — LCD display
lcd = LCD(top, lines=5)

# --- MIDDLE SECTION ---
middle = ttk.Frame(root, padding=(30, 2, 0, 2))
middle.pack(pady=(2, 0), anchor="center")

btn_seek_up = small_icon_button(middle, "▲", seek_up)
btn_confirm = small_icon_button(middle, "●", confirm)
btn_cancel = small_icon_button(middle, "✖", cancel)
btn_seek_down = small_icon_button(middle, "▼", seek_down)

# --- BOTTOM SECTION ---

bottom = ttk.Frame(root, padding=(30, 10, 10, 10))
bottom.pack(pady=(3, 0), anchor="center")

# LEDs in a row
led_row = ttk.Frame(bottom)
led_row.pack(side="left", padx=(0, 10))

stat_led_1 = LED(parent=led_row, color="#5c2828", size="big")
stat_led_2 = LED(parent=led_row, color="#5c2828", size="big")
stat_led_3 = LED(parent=led_row, color="#5c2828", size="big")
stat_led_4 = LED(parent=led_row, color="#5c2828", size="big")

# Text beside LEDs
text_row = ttk.Frame(bottom)
text_row.pack(side="left")

tk.Label(text_row, text="Flooding In Region", font=("Courier", 10)).pack(anchor="w")
tk.Label(text_row, text="Illness In Region", font=("Courier", 10)).pack(anchor="w")
tk.Label(text_row, text="Road/Building Damage", font=("Courier", 10)).pack(anchor="w")
tk.Label(text_row, text="Resource/Aid Available", font=("Courier", 10)).pack(anchor="w")

root.mainloop()

