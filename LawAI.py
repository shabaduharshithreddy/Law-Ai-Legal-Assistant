import tkinter as tk 
from tkinter import scrolledtext 
import threading 
import time
import difflib 
from PIL import Image, ImageTk, ImageDraw, ImageFont 
from DB import LEGAL_DATA  # Importing legal data from DB module 


""""Voice Input & Speech Output   
    PDF & Document Support        
    Multi-Language Support    
    Offline Mode """
class LawAIGUI: 

    def __init__(self, root):                                                 #Constructor Method

        self.root = root 

        self.root.title("LAWAI") 

        self.root.geometry("800x700")  

        self.root.configure(bg="#1E1E1E") 

         

        self.active_tab = None  # Tracks active tab 

        self.tabs = {} 

        self.text_displays = {} 

        self.history = {} 

        self.tab_counter = 1 

 

        self.title_label = tk.Label(self.root, text="LawAI", font=("Times New Roman", 24, "bold"), fg="white", bg="#1E1E1E") 

        self.title_label.pack(pady=10) 

 

        self.tab_frame = tk.Frame(self.root, bg="#1E1E1E") 

        self.tab_frame.pack(fill=tk.X, side=tk.TOP) 

 

        self.create_chat_interface("Tab 1") 

 

    def create_curved_button(self, text, command, width=120, height=40, color="#0D6EFD", text_color="white"): 

        img = Image.new("RGBA", (width, height), (0, 0, 0, 0)) 

        draw = ImageDraw.Draw(img) 

        draw.rounded_rectangle((0, 0, width, height), radius=25, fill=color) 

 

        try: 

            font = ImageFont.truetype("Roman Times-Bold.ttf", 16) 

        except: 

            font = ImageFont.load_default() 

 

        text_bbox = draw.textbbox((0, 0), text, font=font) 

        text_x = (width - (text_bbox[2] - text_bbox[0])) // 2 

        text_y = (height - (text_bbox[3] - text_bbox[1])) // 2 

        draw.text((text_x, text_y), text, font=font, fill=text_color) 

 

        button_img = ImageTk.PhotoImage(img) 

        button = tk.Button(self.tab_frame if text.startswith("Tab") else self.input_frame, image=button_img, borderwidth=0, command=command, bg="#1E1E1E") 

        button.image = button_img 

        return button 

 

    def create_chat_interface(self, tab_name): 

        frame = tk.Frame(self.root, bg="#1E1E1E") 

        self.tabs[tab_name] = frame 

         

        tab_button = self.create_curved_button(tab_name, lambda: self.switch_tab(tab_name), 100, 40, "#4A4A4A") 

        tab_button.pack(side=tk.LEFT, padx=5, pady=5) 

        tab_button.bind("<Double-Button-1>", lambda event, name=tab_name: self.remove_tab(name, tab_button)) 

         

        self.text_displays[tab_name] = scrolledtext.ScrolledText(frame, bg="#252526", fg="white", wrap=tk.WORD, font=("Arial", 12), state=tk.DISABLED) 

        self.text_displays[tab_name].pack(pady=10, padx=10, fill=tk.BOTH, expand=True) 

 

        self.history[tab_name] = ["   Welcome to Law AI! Ask your legal questions here."] 

         

        self.input_frame = tk.Frame(frame, bg="#1E1E1E") 

        self.input_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5) 

 

        self.input_field = tk.Entry(self.input_frame, bg="#3A3A3A", fg="white", font=("Arial", 12), relief="flat", bd=5) 

        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5) 

        self.input_field.focus_set() 

 

        self.send_button = self.create_curved_button("Send", self.send_message, 100, 40, "#0D6EFD") 

        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5) 

 

        self.add_tab_button = self.create_curved_button("+", self.add_tab, 50, 40, "#4A4A4A") 

        self.add_tab_button.pack(side=tk.RIGHT, padx=5, pady=5) 

 

        self.switch_tab(tab_name) 

 

    def add_tab(self): 

        tab_name = f"Tab {self.tab_counter + 1}" 

        self.tab_counter += 1 

        self.create_chat_interface(tab_name) 

 

    def switch_tab(self, tab_name): 

        for name, frame in self.tabs.items(): 

            frame.pack_forget() 

        self.tabs[tab_name].pack(fill=tk.BOTH, expand=True) 

        self.active_tab = tab_name 

        self.update_display(tab_name) 

 

    def remove_tab(self, tab_name, tab_button): 

        if tab_name in self.tabs: 

            self.tabs[tab_name].destroy() 

            del self.tabs[tab_name] 

            del self.text_displays[tab_name] 

            del self.history[tab_name] 

            tab_button.destroy() 

 

            if self.tabs: 

                self.switch_tab(next(iter(self.tabs))) 

 

    def send_message(self): 

        user_input = self.input_field.get().strip().lower() 

        if user_input and self.active_tab: 

            self.history[self.active_tab].append(f"{' ' * 122}You: {user_input}") 

            self.input_field.delete(0, tk.END) 

            threading.Thread(target=self.process_response, args=(user_input, self.active_tab), daemon=True).start() 

 

    def process_response(self, user_input, active_tab): 

        self.history[active_tab].append("Loading...") 

        self.root.after(0, lambda: self.update_display(active_tab)) 

        time.sleep(1) 

 

        closest_match = difflib.get_close_matches(user_input, LEGAL_DATA.keys(), n=1, cutoff=0.6) 

        response = LEGAL_DATA.get(closest_match[0], "Sorry, I couldn't find relevant legal information. we will updateing the System.") if closest_match else "Sorry, I couldn't find relevant legal information. We will be Updating the System." 

         

        self.history[active_tab][-1] = f"Law AI: {response}" 

        self.root.after(0, lambda: self.update_display(active_tab)) 

 

    def update_display(self, tab_name): 
        text_display = self.text_displays[tab_name] 
        text_display.config(state=tk.NORMAL) 
        text_display.delete(1.0, tk.END) 
        for message in self.history[tab_name]: 
            text_display.insert(tk.END, f"{message}\n") 
        text_display.config(state=tk.DISABLED) 
        text_display.see(tk.END)

if __name__ == "__main__": 
    root = tk.Tk() 
    app = LawAIGUI(root) 
    root.mainloop() 



