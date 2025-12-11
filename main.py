import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random
import threading
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class XAutoPoster(tk.Tk):
def init(self):
super().init()
self.title("X Auto Poster")
self.geometry("600x700")
self.resizable(False, False)
self.exe_paths = []
self.media_paths = []
self.desktop_aaa = os.path.join(os.path.expanduser("~"), "Desktop", "AAA")
if not os.path.exists(self.desktop_aaa):
os.makedirs(self.desktop_aaa)

code
Code
download
content_copy
expand_less
self.setup_ui()

def setup_ui(self):
    frame_exe = tk.LabelFrame(self, text="FirefoxPortable.exe Paths")
    frame_exe.pack(fill="x", padx=10, pady=5)

    self.listbox_exe = tk.Listbox(frame_exe, height=6)
    self.listbox_exe.pack(fill="x", padx=5, pady=5)

    btn_frame_exe = tk.Frame(frame_exe)
    btn_frame_exe.pack(fill="x", padx=5, pady=5)
    tk.Button(btn_frame_exe, text="Add", command=self.add_exe).pack(side="left", padx=2)
    tk.Button(btn_frame_exe, text="Edit", command=self.edit_exe).pack(side="left", padx=2)
    tk.Button(btn_frame_exe, text="Delete", command=self.del_exe).pack(side="left", padx=2)

    frame_content = tk.LabelFrame(self, text="Post Content")
    frame_content.pack(fill="both", expand=True, padx=10, pady=5)

    self.text_content = tk.Text(frame_content, height=10)
    self.text_content.pack(fill="both", expand=True, padx=5, pady=5)

    frame_media = tk.LabelFrame(self, text="Media (Max 4)")
    frame_media.pack(fill="x", padx=10, pady=5)

    self.listbox_media = tk.Listbox(frame_media, height=4)
    self.listbox_media.pack(fill="x", padx=5, pady=5)

    btn_frame_media = tk.Frame(frame_media)
    btn_frame_media.pack(fill="x", padx=5, pady=5)
    tk.Button(btn_frame_media, text="Add Media", command=self.add_media).pack(side="left", padx=2)
    tk.Button(btn_frame_media, text="Clear Media", command=self.clear_media).pack(side="left", padx=2)

    self.btn_send = tk.Button(self, text="Send", command=self.start_posting, height=2, bg="#1DA1F2", fg="white", font=("Arial", 12, "bold"))
    self.btn_send.pack(fill="x", padx=10, pady=15)

def add_exe(self):
    path = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
    if path:
        self.exe_paths.append(path)
        self.refresh_exe_list()

def edit_exe(self):
    sel = self.listbox_exe.curselection()
    if sel:
        idx = sel[0]
        path = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
        if path:
            self.exe_paths[idx] = path
            self.refresh_exe_list()

def del_exe(self):
    sel = self.listbox_exe.curselection()
    if sel:
        del self.exe_paths[sel[0]]
        self.refresh_exe_list()

def refresh_exe_list(self):
    self.listbox_exe.delete(0, tk.END)
    for p in self.exe_paths:
        self.listbox_exe.insert(tk.END, p)

def add_media(self):
    if len(self.media_paths) >= 4:
        messagebox.showwarning("Limit", "Max 4 media files allowed.")
        return
    files = filedialog.askopenfilenames(filetypes=[("Media", "*.jpg *.jpeg *.png *.gif *.mp4 *.mov")])
    for f in files:
        if len(self.media_paths) < 4:
            self.media_paths.append(f)
    self.refresh_media_list()

def clear_media(self):
    self.media_paths = []
    self.refresh_media_list()

def refresh_media_list(self):
    self.listbox_media.delete(0, tk.END)
    for p in self.media_paths:
        self.listbox_media.insert(tk.END, p)

def start_posting(self):
    if not self.exe_paths:
        messagebox.showerror("Error", "No Firefox paths configured.")
        return
    
    text = self.text_content.get("1.0", tk.END).strip()
    if not text and not self.media_paths:
        messagebox.showerror("Error", "Content cannot be empty.")
        return

    self.btn_send.config(state=tk.DISABLED, text="Sending...")
    threading.Thread(target=self.run_automation, args=(text,), daemon=True).start()

def run_automation(self, text):
    driver = None
    try:
        exe_path = random.choice(self.exe_paths)
        base_path = os.path.dirname(exe_path)
        profile_path = os.path.join(base_path, "Data", "profile")

        options = Options()
        options.binary_location = exe_path
        options.add_argument("-profile")
        options.add_argument(profile_path)
        
        log_path = os.path.join(self.desktop_aaa, "geckodriver.log")
        service = Service(log_output=log_path)

        driver = webdriver.Firefox(options=options, service=service)
        driver.maximize_window()
        
        driver.get("https://x.com/home")
        
        wait = WebDriverWait(driver, 40)
        
        text_area = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="tweetTextarea_0"]')))
        text_area.click()
        time.sleep(1)
        text_area.send_keys(text)

        if self.media_paths:
            file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
            file_input.send_keys("\n".join(self.media_paths))
            time.sleep(3) 
            wait.until(EC.invisibility_of_element_located((By.XPATH, '//div[@role="progressbar"]')))

        btn_tweet = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="tweetButtonInline"]')))
        driver.execute_script("arguments[0].click();", btn_tweet)
        
        time.sleep(5)
        
        messagebox.showinfo("Success", "Posted successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        self.after(0, lambda: self.btn_send.config(state=tk.NORMAL, text="Send"))

if name == "main":
app = XAutoPoster()
app.mainloop()
