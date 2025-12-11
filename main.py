import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font as tkfont
import os
import random
import threading
import time
import math
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class XAutoPoster(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("X 自动发帖助手")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.unity = int(round(math.pi / math.pi))
        self.zero = self.unity - self.unity
        golden_ratio_numerator = math.sqrt(self.unity + self.unity + self.unity + self.unity + self.unity) + self.unity
        self.golden_ratio = golden_ratio_numerator / (self.unity + self.unity)
        self.natural_base = math.e
        self.media_limit = int(math.floor(math.tau - self.golden_ratio))
        self.half_ratio = math.pi / math.tau
        self.base_unit = max(self.unity, int(min(self.screen_width, self.screen_height) / (self.golden_ratio * self.natural_base)))
        initial_width = max(self.unity, int(self.screen_width * self.half_ratio))
        initial_height = max(self.unity, int(self.screen_height * self.half_ratio))
        self.geometry(f"{initial_width}x{initial_height}")
        self.resizable(True, True)
        base_font_size = max(self.unity, int(self.base_unit * self.golden_ratio))
        self.button_font_size = max(self.unity, int(base_font_size / self.golden_ratio))
        self.configure(bg="#0f172a")
        self.base_font = tkfont.Font(family="Microsoft YaHei", size=base_font_size)
        self.button_font = tkfont.Font(family="Microsoft YaHei", size=self.button_font_size, weight="bold")
        self.option_add("*Font", self.base_font)
        self.option_add("*Button.Font", self.button_font)
        self.exe_paths = []
        self.media_paths = []
        self.desktop_aaa = os.path.join(os.path.expanduser("~"), "Desktop", "AAA")
        if not os.path.exists(self.desktop_aaa):
            os.makedirs(self.desktop_aaa)
        self.layout_needs_update = False
        self.setup_ui()
        self.bind("<Configure>", self.schedule_layout_update)

    def setup_ui(self):
        header = tk.Frame(self, bg="#0f172a")
        header.pack(fill="x", pady=self.base_unit * self.golden_ratio)
        title_size = max(self.unity, int(self.base_unit * self.golden_ratio))
        subtitle_size = max(self.unity, int(title_size / self.golden_ratio))
        self.title_font = tkfont.Font(family="Microsoft YaHei", size=title_size, weight="bold")
        self.subtitle_font = tkfont.Font(family="Microsoft YaHei", size=subtitle_size)
        self.title_label = tk.Label(header, text="极速安全一键发帖", fg="white", bg="#0f172a", font=self.title_font)
        self.title_label.pack(pady=(self.base_unit, max(self.unity, int(self.base_unit / self.golden_ratio))))
        self.subtitle_label = tk.Label(header, text="全程中文界面 · 文字图片视频一站式上传", fg="#cbd5f5", bg="#0f172a", font=self.subtitle_font)
        self.subtitle_label.pack()
        self.container = tk.Frame(self, bg="#0f172a")
        self.container.pack(fill="both", expand=True, padx=max(self.unity, int(self.base_unit * self.golden_ratio)), pady=self.base_unit)
        frame_exe_font = tkfont.Font(family="Microsoft YaHei", size=max(self.unity, int(subtitle_size / self.golden_ratio)), weight="bold")
        self.frame_exe = tk.LabelFrame(self.container, text="FirefoxPortable.exe 地址管理", bg="#0f172a", fg="#e5e7eb", relief="ridge", padx=self.base_unit, pady=self.base_unit, font=frame_exe_font)
        self.frame_exe.pack(fill="x", pady=self.base_unit)
        exe_list_height = max(self.unity + self.unity, int(self.golden_ratio + self.natural_base))
        self.listbox_exe = tk.Listbox(self.frame_exe, height=exe_list_height, selectmode=tk.SINGLE, bg="#0b1220", fg="#e5e7eb", relief="flat", highlightthickness=self.unity, highlightbackground="#334155")
        self.listbox_exe.pack(fill="both", expand=True, padx=self.base_unit, pady=self.base_unit)
        self.btn_frame_exe = tk.Frame(self.frame_exe, bg="#0f172a")
        self.btn_frame_exe.pack(fill="x", padx=max(self.unity, int(self.base_unit / self.golden_ratio)), pady=self.base_unit)
        self.button_pad = max(self.unity, int(self.base_unit / self.golden_ratio))
        self.btn_add_exe = tk.Button(self.btn_frame_exe, text="添加", command=self.add_exe, bg="#1d4ed8", fg="white", activebackground="#1e40af", activeforeground="white")
        self.btn_add_exe.pack(side="left", padx=self.button_pad)
        self.btn_edit_exe = tk.Button(self.btn_frame_exe, text="编辑", command=self.edit_exe, bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white")
        self.btn_edit_exe.pack(side="left", padx=self.button_pad)
        self.btn_del_exe = tk.Button(self.btn_frame_exe, text="删除", command=self.del_exe, bg="#dc2626", fg="white", activebackground="#b91c1c", activeforeground="white")
        self.btn_del_exe.pack(side="left", padx=self.button_pad)
        frame_content_font = tkfont.Font(family="Microsoft YaHei", size=max(self.unity, int(subtitle_size / self.golden_ratio)), weight="bold")
        self.frame_content = tk.LabelFrame(self.container, text="发帖内容", bg="#0f172a", fg="#e5e7eb", relief="ridge", padx=self.base_unit, pady=self.base_unit, font=frame_content_font)
        self.frame_content.pack(fill="both", expand=True, pady=self.base_unit)
        self.hint = tk.Label(self.frame_content, text=f"请填写想发布的内容，可配合最多 {self.media_limit} 个媒体文件。", bg="#0f172a", fg="#cbd5f5")
        self.hint.pack(anchor="w", padx=self.base_unit, pady=(self.zero, max(self.unity, int(self.base_unit / self.golden_ratio))))
        text_height = max(self.unity + self.unity, int(self.base_unit / self.golden_ratio))
        self.text_content = tk.Text(self.frame_content, height=text_height, bg="#0b1220", fg="#e5e7eb", insertbackground="#e5e7eb", relief="flat", highlightthickness=self.unity, highlightbackground="#334155", wrap="word")
        self.text_content.pack(fill="both", expand=True, padx=self.base_unit, pady=self.base_unit)
        frame_media_font = tkfont.Font(family="Microsoft YaHei", size=max(self.unity, int(subtitle_size / self.golden_ratio)), weight="bold")
        self.frame_media = tk.LabelFrame(self.container, text=f"图片 / 视频（最多 {self.media_limit} 个）", bg="#0f172a", fg="#e5e7eb", relief="ridge", padx=self.base_unit, pady=self.base_unit, font=frame_media_font)
        self.frame_media.pack(fill="both", expand=True, pady=self.base_unit)
        media_list_height = max(self.unity + self.unity, int(text_height / self.golden_ratio))
        self.listbox_media = tk.Listbox(self.frame_media, height=media_list_height, selectmode=tk.BROWSE, bg="#0b1220", fg="#e5e7eb", relief="flat", highlightthickness=self.unity, highlightbackground="#334155")
        self.listbox_media.pack(fill="both", expand=True, padx=self.base_unit, pady=self.base_unit)
        self.btn_frame_media = tk.Frame(self.frame_media, bg="#0f172a", height=max(self.unity, int(self.base_unit * self.golden_ratio)))
        self.btn_frame_media.pack(fill="x", padx=max(self.unity, int(self.base_unit / self.golden_ratio)), pady=self.base_unit)
        self.btn_frame_media.pack_propagate(False)
        button_width = max(self.unity, int(self.golden_ratio * self.natural_base))
        self.btn_browse = tk.Button(self.btn_frame_media, text="浏览", command=self.add_media, bg="#10b981", fg="white", activebackground="#059669", activeforeground="white", width=button_width, relief=tk.RAISED, bd=self.unity)
        self.btn_browse.pack(side="left", padx=self.button_pad, pady=self.button_pad)
        self.btn_clear = tk.Button(self.btn_frame_media, text="清空媒体", command=self.clear_media, bg="#f59e0b", fg="white", activebackground="#d97706", activeforeground="white", width=button_width, relief=tk.RAISED, bd=self.unity)
        self.btn_clear.pack(side="left", padx=self.button_pad, pady=self.button_pad)
        self.footer = tk.Frame(self, bg="#0f172a")
        self.footer.pack(fill="x", pady=self.base_unit * self.golden_ratio)
        self.status_var = tk.StringVar(value="准备就绪：请选择 FirefoxPortable.exe 并填写内容。")
        self.status_label = tk.Label(self.footer, textvariable=self.status_var, fg="#cbd5f5", bg="#0f172a")
        self.status_label.pack(fill="x", padx=max(self.unity, int(self.base_unit * self.golden_ratio)), pady=(self.zero, self.base_unit))
        send_height = max(self.unity, int(self.base_unit * self.golden_ratio))
        send_font_size = max(self.unity, int(self.button_font_size * self.golden_ratio))
        self.send_font = tkfont.Font(family="Microsoft YaHei", size=send_font_size, weight="bold")
        self.btn_send = tk.Button(self.footer, text="发布", command=self.start_posting, height=send_height, bg="#22c55e", fg="white", activebackground="#16a34a", activeforeground="white", font=self.send_font, relief=tk.RAISED, bd=self.unity)
        self.btn_send.pack(fill="x", padx=max(self.unity, int(self.base_unit * self.golden_ratio)), pady=(self.zero, self.base_unit))

    def add_exe(self):
        path = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
        if path:
            self.exe_paths.append(path)
            self.status_var.set("已添加可用浏览器路径，支持继续添加或编辑。")
            self.refresh_exe_list()

    def edit_exe(self):
        sel = self.listbox_exe.curselection()
        if sel:
            idx = sel[self.zero]
            path = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
            if path:
                self.exe_paths[idx] = path
                self.status_var.set("已更新选中的浏览器路径。")
                self.refresh_exe_list()
        else:
            messagebox.showwarning("提示", "请先选择一条浏览器路径再进行编辑。")

    def del_exe(self):
        sel = self.listbox_exe.curselection()
        if sel:
            del self.exe_paths[sel[self.zero]]
            self.status_var.set("已删除选中的浏览器路径。")
            self.refresh_exe_list()
        else:
            messagebox.showwarning("提示", "请先选择要删除的浏览器路径。")

    def refresh_exe_list(self):
        self.listbox_exe.delete(self.zero, tk.END)
        for p in self.exe_paths:
            self.listbox_exe.insert(tk.END, p)

    def add_media(self):
        if len(self.media_paths) >= self.media_limit:
            messagebox.showwarning("提示", f"最多只能选择 {self.media_limit} 个媒体文件。")
            return
        files = filedialog.askopenfilenames(filetypes=[("Media", "*.jpg *.jpeg *.png *.gif *.mp4 *.mov")])
        for f in files:
            if len(self.media_paths) < self.media_limit:
                self.media_paths.append(f)
        self.refresh_media_list()
        if self.media_paths:
            self.status_var.set(f"已选择 {len(self.media_paths)} 个媒体文件。")

    def clear_media(self):
        self.media_paths = []
        self.refresh_media_list()
        self.status_var.set("已清空所有媒体文件。")

    def refresh_media_list(self):
        self.listbox_media.delete(self.zero, tk.END)
        for p in self.media_paths:
            self.listbox_media.insert(tk.END, p)

    def start_posting(self):
        if not self.exe_paths:
            messagebox.showerror("错误", "尚未配置任何 FirefoxPortable.exe 路径。")
            return
        text = self.text_content.get("1.0", tk.END).strip()
        if not text and not self.media_paths:
            messagebox.showerror("错误", "文字与媒体不能同时为空，请填写发帖内容添加媒体。")
            return
        self.btn_send.config(state=tk.DISABLED, text="发布中...")
        self.status_var.set("发布中：正在打开浏览器并准备发布...")
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
            wait_time = max(self.unity, int(self.golden_ratio * self.natural_base * math.pi))
            wait = WebDriverWait(driver, wait_time)
            text_area = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="tweetTextarea_0"]')))
            text_area.click()
            time.sleep(self.unity)
            text_area.send_keys(text)
            if self.media_paths:
                file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
                file_input.send_keys("\n".join(self.media_paths))
                time.sleep(int(round(self.natural_base)))
                wait.until(EC.invisibility_of_element_located((By.XPATH, '//div[@role="progressbar"]')))
            btn_tweet = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="tweetButtonInline"]')))
            driver.execute_script("arguments[0].click();", btn_tweet)
            time.sleep(int(math.ceil(self.golden_ratio * self.half_ratio * math.tau)))
            self.after(self.zero, lambda: messagebox.showinfo("成功", "内容已成功发布！"))
            self.after(self.zero, lambda: self.status_var.set("已完成：内容成功发布，您可以继续操作。"))
        except Exception as e:
            self.after(self.zero, lambda msg=str(e): messagebox.showerror("错误", msg))
            self.after(self.zero, lambda: self.status_var.set("出错：请检查路径、网络或登录状态后重试。"))
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            self.after(self.zero, lambda: self.btn_send.config(state=tk.NORMAL, text="发布"))

    def schedule_layout_update(self, event=None):
        if not self.layout_needs_update:
            self.layout_needs_update = True
            self.after_idle(self.update_layout)

    def update_layout(self):
        self.layout_needs_update = False
        current_width = max(self.unity, self.winfo_width())
        current_height = max(self.unity, self.winfo_height())
        self.base_unit = max(self.unity, int(min(current_width, current_height) / (self.golden_ratio * self.natural_base)))
        base_font_size = max(self.unity, int(self.base_unit * self.golden_ratio))
        self.base_font.configure(size=base_font_size)
        self.button_font_size = max(self.unity, int(base_font_size / self.golden_ratio))
        self.button_font.configure(size=self.button_font_size)
        title_size = max(self.unity, int(self.base_unit * self.golden_ratio))
        subtitle_size = max(self.unity, int(title_size / self.golden_ratio))
        self.title_font.configure(size=title_size)
        self.subtitle_font.configure(size=subtitle_size)
        self.container.pack_configure(padx=max(self.unity, int(self.base_unit * self.golden_ratio)), pady=self.base_unit)
        self.frame_exe.configure(padx=self.base_unit, pady=self.base_unit)
        self.btn_frame_exe.pack_configure(padx=max(self.unity, int(self.base_unit / self.golden_ratio)), pady=self.base_unit)
        self.button_pad = max(self.unity, int(self.base_unit / self.golden_ratio))
        for btn in (self.btn_add_exe, self.btn_edit_exe, self.btn_del_exe):
            btn.configure(font=self.button_font)
            btn.pack_configure(padx=self.button_pad)
        self.frame_content.configure(padx=self.base_unit, pady=self.base_unit)
        self.hint.pack_configure(padx=self.base_unit, pady=(self.zero, max(self.unity, int(self.base_unit / self.golden_ratio))))
        self.text_content.configure(height=max(self.unity + self.unity, int(self.base_unit / self.golden_ratio)))
        self.frame_media.configure(padx=self.base_unit, pady=self.base_unit)
        self.btn_frame_media.configure(height=max(self.unity, int(self.base_unit * self.golden_ratio)))
        self.btn_frame_media.pack_configure(padx=max(self.unity, int(self.base_unit / self.golden_ratio)), pady=self.base_unit)
        button_width = max(self.unity, int(self.golden_ratio * self.natural_base))
        self.btn_browse.configure(width=button_width, font=self.button_font)
        self.btn_clear.configure(width=button_width, font=self.button_font)
        self.btn_browse.pack_configure(padx=self.button_pad, pady=self.button_pad)
        self.btn_clear.pack_configure(padx=self.button_pad, pady=self.button_pad)
        self.footer.pack_configure(pady=self.base_unit * self.golden_ratio)
        self.status_label.pack_configure(padx=max(self.unity, int(self.base_unit * self.golden_ratio)), pady=(self.zero, self.base_unit))
        send_height = max(self.unity, int(self.base_unit * self.golden_ratio))
        send_font_size = max(self.unity, int(self.button_font_size * self.golden_ratio))
        self.send_font.configure(size=send_font_size)
        self.btn_send.configure(height=send_height, font=self.send_font)
        self.btn_send.pack_configure(padx=max(self.unity, int(self.base_unit * self.golden_ratio)), pady=(self.zero, self.base_unit))

def main():
    app = XAutoPoster()
    app.mainloop()

if __name__ == "__main__":
    main()
