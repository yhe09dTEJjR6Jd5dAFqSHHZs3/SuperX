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
    def __init__(self):
        super().__init__()
        self.title("X 自动发帖助手")
        self.geometry("680x780")
        self.resizable(False, False)
        self.configure(bg="#0f172a")
        self.option_add("*Font", ("Microsoft YaHei", 10))
        self.option_add("*Button.Font", ("Microsoft YaHei", 10, "bold"))
        self.exe_paths = []
        self.media_paths = []
        self.desktop_aaa = os.path.join(os.path.expanduser("~"), "Desktop", "AAA")
        if not os.path.exists(self.desktop_aaa):
            os.makedirs(self.desktop_aaa)
        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self, bg="#0f172a")
        header.pack(fill="x", pady=10)
        title = tk.Label(header, text="极速安全一键发帖", fg="white", bg="#0f172a", font=("Microsoft YaHei", 18, "bold"))
        title.pack(pady=(5, 2))
        subtitle = tk.Label(header, text="全程中文界面 · 文字图片视频一站式上传", fg="#cbd5f5", bg="#0f172a", font=("Microsoft YaHei", 11))
        subtitle.pack()
        container = tk.Frame(self, bg="#0f172a")
        container.pack(fill="both", expand=True, padx=16, pady=6)
        frame_exe = tk.LabelFrame(container, text="FirefoxPortable.exe 地址管理", bg="#0f172a", fg="#e5e7eb", relief="ridge", padx=8, pady=6, font=("Microsoft YaHei", 10, "bold"))
        frame_exe.pack(fill="x", pady=6)
        self.listbox_exe = tk.Listbox(frame_exe, height=6, selectmode=tk.SINGLE, bg="#0b1220", fg="#e5e7eb", relief="flat", highlightthickness=1, highlightbackground="#334155")
        self.listbox_exe.pack(fill="x", padx=4, pady=4)
        btn_frame_exe = tk.Frame(frame_exe, bg="#0f172a")
        btn_frame_exe.pack(fill="x", padx=2, pady=4)
        tk.Button(btn_frame_exe, text="添加", command=self.add_exe, bg="#1d4ed8", fg="white", activebackground="#1e40af", activeforeground="white").pack(side="left", padx=3)
        tk.Button(btn_frame_exe, text="编辑", command=self.edit_exe, bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white").pack(side="left", padx=3)
        tk.Button(btn_frame_exe, text="删除", command=self.del_exe, bg="#dc2626", fg="white", activebackground="#b91c1c", activeforeground="white").pack(side="left", padx=3)
        frame_content = tk.LabelFrame(container, text="发帖内容", bg="#0f172a", fg="#e5e7eb", relief="ridge", padx=8, pady=6, font=("Microsoft YaHei", 10, "bold"))
        frame_content.pack(fill="both", expand=True, pady=6)
        hint = tk.Label(frame_content, text="请填写想发布的内容，可配合最多 4 个媒体文件。", bg="#0f172a", fg="#cbd5f5")
        hint.pack(anchor="w", padx=2, pady=(0, 4))
        self.text_content = tk.Text(frame_content, height=10, bg="#0b1220", fg="#e5e7eb", insertbackground="#e5e7eb", relief="flat", highlightthickness=1, highlightbackground="#334155", wrap="word")
        self.text_content.pack(fill="both", expand=True, padx=2, pady=4)
        frame_media = tk.LabelFrame(container, text="图片 / 视频（最多 4 个）", bg="#0f172a", fg="#e5e7eb", relief="ridge", padx=8, pady=6, font=("Microsoft YaHei", 10, "bold"))
        frame_media.pack(fill="x", pady=6)
        self.listbox_media = tk.Listbox(frame_media, height=4, selectmode=tk.BROWSE, bg="#0b1220", fg="#e5e7eb", relief="flat", highlightthickness=1, highlightbackground="#334155")
        self.listbox_media.pack(fill="x", padx=4, pady=4)
        btn_frame_media = tk.Frame(frame_media, bg="#0f172a", height=50)
        btn_frame_media.pack(fill="x", padx=2, pady=4)
        btn_frame_media.pack_propagate(False)
        tk.Button(btn_frame_media, text="浏览", command=self.add_media, bg="#10b981", fg="white", activebackground="#059669", activeforeground="white", width=10, relief=tk.RAISED, bd=2).pack(side="left", padx=3, pady=2)
        tk.Button(btn_frame_media, text="清空媒体", command=self.clear_media, bg="#f59e0b", fg="white", activebackground="#d97706", activeforeground="white", width=10, relief=tk.RAISED, bd=2).pack(side="left", padx=3, pady=2)
        footer = tk.Frame(self, bg="#0f172a")
        footer.pack(fill="x", pady=10)
        self.status_var = tk.StringVar(value="准备就绪：请选择 FirefoxPortable.exe 并填写内容。")
        status_label = tk.Label(footer, textvariable=self.status_var, fg="#cbd5f5", bg="#0f172a")
        status_label.pack(fill="x", padx=16, pady=(0, 6))
        self.btn_send = tk.Button(footer, text="发布", command=self.start_posting, height=2, bg="#22c55e", fg="white", activebackground="#16a34a", activeforeground="white", font=("Microsoft YaHei", 13, "bold"), relief=tk.RAISED, bd=2)
        self.btn_send.pack(fill="x", padx=16, pady=(0, 8))

    def add_exe(self):
        path = filedialog.askopenfilename(filetypes=[("Executable", "*.exe")])
        if path:
            self.exe_paths.append(path)
            self.status_var.set("已添加可用浏览器路径，支持继续添加或编辑。")
            self.refresh_exe_list()

    def edit_exe(self):
        sel = self.listbox_exe.curselection()
        if sel:
            idx = sel[0]
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
            del self.exe_paths[sel[0]]
            self.status_var.set("已删除选中的浏览器路径。")
            self.refresh_exe_list()
        else:
            messagebox.showwarning("提示", "请先选择要删除的浏览器路径。")

    def refresh_exe_list(self):
        self.listbox_exe.delete(0, tk.END)
        for p in self.exe_paths:
            self.listbox_exe.insert(tk.END, p)

    def add_media(self):
        if len(self.media_paths) >= 4:
            messagebox.showwarning("提示", "最多只能选择 4 个媒体文件。")
            return
        files = filedialog.askopenfilenames(filetypes=[("Media", "*.jpg *.jpeg *.png *.gif *.mp4 *.mov")])
        for f in files:
            if len(self.media_paths) < 4:
                self.media_paths.append(f)
        self.refresh_media_list()
        if self.media_paths:
            self.status_var.set(f"已选择 {len(self.media_paths)} 个媒体文件。")

    def clear_media(self):
        self.media_paths = []
        self.refresh_media_list()
        self.status_var.set("已清空所有媒体文件。")

    def refresh_media_list(self):
        self.listbox_media.delete(0, tk.END)
        for p in self.media_paths:
            self.listbox_media.insert(tk.END, p)

    def start_posting(self):
        if not self.exe_paths:
            messagebox.showerror("错误", "尚未配置任何 FirefoxPortable.exe 路径。")
            return
        text = self.text_content.get("1.0", tk.END).strip()
        if not text and not self.media_paths:
            messagebox.showerror("错误", "文字与媒体不能同时为空，请填写发帖内容或添加媒体。")
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
            self.after(0, lambda: messagebox.showinfo("成功", "内容已成功发布！"))
            self.after(0, lambda: self.status_var.set("已完成：内容成功发布，您可以继续操作。"))
        except Exception as e:
            self.after(0, lambda msg=str(e): messagebox.showerror("错误", msg))
            self.after(0, lambda: self.status_var.set("出错：请检查路径、网络或登录状态后重试。"))
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            self.after(0, lambda: self.btn_send.config(state=tk.NORMAL, text="发布"))

if __name__ == "__main__":
    app = XAutoPoster()
    app.mainloop()
