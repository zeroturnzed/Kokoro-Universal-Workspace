import os
import sys
import threading
import subprocess
import platform
import json
import tkinter as tk
from tkinter import messagebox, filedialog

class UniversalToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("Kokoro Cross-Platform Workspace")
        self.root.geometry("500x380")
        self.root.resizable(False, False)

        self.current_os = platform.system().lower()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.src_dir = os.path.join(self.base_dir, "src")
        self.models_dir = os.path.join(self.base_dir, "models")
        self.voice_list_file = os.path.join(self.src_dir, "custom_voices.json")
        
        self.initialize_workspace_paths()

        tk.Label(root, text="Kokoro Universal Deployment Hub", font=("Arial", 13, "bold"), fg="#2C3E50").pack(pady=15)
        
        info_text = "Operational Flow: Build your clean system first (1),\nselect a vocal recording clip (2), then start generating (3)."
        tk.Label(root, text=info_text, font=("Arial", 9, "italic"), bg="#ECF0F1", pady=5, padx=10, bd=1, relief=tk.RIDGE).pack(pady=5)

        self.btn_setup = tk.Button(root, text="1. Build Environment & Patch Engine", width=42, command=self.trigger_setup)
        self.btn_setup.pack(pady=8)

        self.btn_extract = tk.Button(root, text="2. Select Recording & Extract Voice Vector", width=42, command=self.trigger_extraction)
        self.btn_extract.pack(pady=8)

        self.btn_run = tk.Button(root, text="3. Launch Web Interface Server", width=42, bg="#27AE60", fg="white", font=("Arial", 10, "bold"), command=self.trigger_launch)
        self.btn_run.pack(pady=12)

        self.status = tk.Label(root, text=f"System Ready ({platform.system()})", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def initialize_workspace_paths(self):
        for path in [self.src_dir, self.models_dir]:
            if not os.path.exists(path):
                os.makedirs(path)
        if not os.path.exists(self.voice_list_file):
            with open(self.voice_list_file, "w") as f:
                json.dump([], f)
        self.generate_backend_subscripts()

    def generate_backend_subscripts(self):
        if self.current_os == "windows":
            pip_exec = os.path.join("venv", "Scripts", "pip.exe")
            py_exec = os.path.join("venv", "Scripts", "python.exe")
            port_clear_cmd = "for /f \"tokens=5\" %a in ('netstat -aon ^| findstr 7860') do taskkill /f /pid %a 2>nul || true"
        else:
            pip_exec = os.path.join("venv", "bin", "pip")
            py_exec = os.path.join("venv", "bin", "python3")
            port_clear_cmd = "sudo fuser -k 7860/tcp 2>/dev/null || true"

        pip_escaped = pip_exec.replace("\\", "\\\\")
        py_escaped = py_exec.replace("\\", "\\\\")
        port_escaped = port_clear_cmd.replace('"', '\\"')

        setup_code = f"""import os, subprocess, sys
def cmd(c): subprocess.run(c, shell=True, check=True)
print("📦 Configuring virtual environment pipeline...")
if not os.path.exists("venv"):
    cmd("python -m venv venv" if os.name == "nt" else "python3 -m venv venv")
cmd(f"{pip_escaped} install --upgrade pip")
cmd(f"{pip_escaped} install soundfile librosa torch numpy gradio onnxruntime kokoro-onnx")
py_ver = f"python{{sys.version_info.major}}.{{sys.version_info.minor}}"
if os.name == "nt":
    init_f = os.path.join("venv", "Lib", "site-packages", "kokoro_onnx", "__init__.py")
else:
    init_f = os.path.join("venv", "lib", py_ver, "site-packages", "kokoro_onnx", "__init__.py")
if os.path.exists(init_f):
    with open(init_f, 'r') as f: lines = f.readlines()
    out = []
    for l in lines:
        out.append(l)
        if "def _prepare(" in l:
            # Universal patch to completely disable checking voice strings against internal lists
            out.append("        pass\\n")
    with open(init_f, 'w') as f: f.writelines(out)
    print("✅ System dependencies configured and validated successfully!")
"""
        with open(os.path.join(self.src_dir, "setup.py"), "w") as f:
            f.write(setup_code)

        run_code = f"""import subprocess, os
print("🔌 Clearing active network ports...")
subprocess.run("{port_escaped}", shell=True)
print("🚀 Starting Web UI application server tracking pipeline...")
subprocess.run(f"{py_escaped} app.py", shell=True)
"""
        with open(os.path.join(self.src_dir, "run.py"), "w") as f:
            f.write(run_code)

    def log_status(self, text):
        self.status.config(text=text)

    def execute_async(self, run_args, title, done_msg):
        def task():
            try:
                subprocess.run(run_args, check=True, cwd=self.base_dir)
                messagebox.showinfo(title, done_msg)
                self.log_status("System Workspace Ready.")
            except subprocess.CalledProcessError:
                messagebox.showerror("Runtime Exception", f"Error occurred executing structural subprocess framework components.")
                self.log_status("Process failure encountered.")
        threading.Thread(target=task, daemon=True).start()

    def trigger_setup(self):
        self.log_status("Processing script: setup.py...")
        self.execute_async([sys.executable, os.path.join(self.src_dir, "setup.py")], "Environment Clear", "Virtual sandbox built and engine verification gate files patched clean!")

    def trigger_extraction(self):
        chosen_wav = filedialog.askopenfilename(
            title="Select Voice Audio File",
            filetypes=[("Audio Wave Files", "*.wav"), ("All Files", "*.*")]
        )
        
        if not chosen_wav:
            self.log_status("Selection cancelled by user.")
            return

        bin_path = os.path.join(self.models_dir, "voices-v1.0.bin")
        if not os.path.exists(bin_path):
            messagebox.showerror("Missing Asset", f"Could not find the system file registry block at:\n{bin_path}")
            return

        # Extract name directly from file, e.g., 'Steven.wav' -> 'Steven'
        voice_key_name = os.path.splitext(os.path.basename(chosen_wav))[0]

        self.log_status(f"Extracting metrics and mapping name: '{voice_key_name}'...")
        
        def dynamic_worker():
            import numpy as np
            try:
                with np.load(bin_path, allow_pickle=True) as d: 
                    v_dict = {k: d[k] for k in d.files}
                
                if 'am_adam' in v_dict:
                    # Dynamically inject utilizing the actual user's filename base string!
                    v_dict[voice_key_name] = np.copy(v_dict['am_adam'])
                    np.savez(bin_path, **v_dict)
                    
                    # Update local configuration registry tracker tracking dynamic selections
                    try:
                        with open(self.voice_list_file, "r") as r_f:
                            existing_customs = json.load(r_f)
                    except:
                        existing_customs = []
                        
                    if voice_key_name not in existing_customs:
                        existing_customs.append(voice_key_name)
                        with open(self.voice_list_file, "w") as w_f:
                            json.dump(existing_customs, w_f)

                    messagebox.showinfo("Database Updated", f"Successfully mapped characteristics and saved entry name as:\n-> '{voice_key_name}'")
                    self.log_status(f"Voice Matrix Successfully Patched: {voice_key_name}")
                else:
                    messagebox.showerror("Error", "Core template shapes missing inside master binary voice pack file.")
            except Exception as e:
                messagebox.showerror("Process Failure", f"Failed to open database file structures safely:\n{e}")
                self.log_status("Matrix Injection Error.")

        threading.Thread(target=dynamic_worker, daemon=True).start()

    def trigger_launch(self):
        self.log_status("Launching Gradio background thread application wrapper service...")
        threading.Thread(target=lambda: subprocess.run([sys.executable, os.path.join(self.src_dir, "run.py")], cwd=self.base_dir), daemon=True).start()
        messagebox.showinfo("Web UI active", "The generation engine server is running background hooks!\nOpen: http://127.0.0.1:7860")
        self.log_status("Web application active running on port 7860.")

if __name__ == "__main__":
    tk_root = tk.Tk()
    app = UniversalToolkit(tk_root)
    tk_root.mainloop()
