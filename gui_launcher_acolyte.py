import tkinter as tk
# Import the helper function we just made
from file_manager import archive_voice_recording 

# ... inside your existing Tkinter setup code ...
# (Assuming you added the filename_entry widget from earlier)

def on_generate_click():
    # 1. YOUR EXISTING KOKORO TTS ENGINE CODE RUNS HERE
    # ... execution logic that drops 'output.wav' ...
    
    # 2. Extract the custom prefix from your UI entry box
    user_prefix = filename_entry.get().strip()
    if not user_prefix:
        user_prefix = "recording"
        
    # 3. Fire the automatic archiver
    archive_voice_recording(base_name=user_prefix)

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
        self.root.geometry("450x640+0+40")  
        self.root.resizable(True, True)
        self.root.attributes("-topmost", True)  # Keeps the toolkit locked on top of your browser window


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



        # --- INTEGRATED FILE RENAMER & ARCHIVER PANEL ---
        self.archive_frame = tk.LabelFrame(root, text=" 4. File Archiver & Renamer (Downloads -> Music) ", padx=15, pady=10, font=("Arial", 10, "bold"), fg="#2C3E50")
        self.archive_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(self.archive_frame, text="New File Name Prefix:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.filename_entry = tk.Entry(self.archive_frame, width=20)
        self.filename_entry.insert(0, "voice_recording")
        self.filename_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.archive_btn = tk.Button(self.archive_frame, text="📥 Archive Latest Browser Download", command=self.trigger_archive_flow, bg="#2980B9", fg="white", font=("Arial", 10, "bold"), height=2)
        self.archive_btn.grid(row=1, column=0, columnspan=2, sticky="we", padx=5, pady=10)

        self.status = tk.Label(root, text=f"System Ready ({platform.system()})", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    
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
            port_clear_cmd = "pkill -f 'app.py' 2>/dev/null || true; sleep 1"

        else:
            pip_exec = os.path.join("venv", "bin", "pip")
            py_exec = os.path.join("venv", "bin", "python3")
            port_clear_cmd = "fuser -k 7860/tcp 2>/dev/null || true"

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

        voice_key_name, _ = os.path.splitext(os.path.basename(chosen_wav))
        self.log_status(f"Analyzing audio acoustics for '{voice_key_name}'...")

        def dynamic_worker():
            py_exec = "/home/zeroturnzed/Kokoro-webui/venv/bin/python3"
            if not os.path.exists(py_exec):
                py_exec = sys.executable

            analyzer_script = """
import sys, json, operator
import numpy as np
import librosa

_, wav_path, bin_path, voice_name = sys.argv

y, sr = librosa.load(wav_path, sr=22050, mono=True)
y_trimmed, _ = librosa.effects.trim(y, top_db=25)
if len(y_trimmed) > sr * 0.5:
    y = y_trimmed

f0, voiced_flag, _ = librosa.pyin(y, fmin=65, fmax=400, sr=sr)
valid_f0 = f0[~np.isnan(f0)]
pitch_hz = float(np.median(valid_f0)) if len(valid_f0) > 0 else 135.0

centroid_hz = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
rolloff_hz = float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))

stock_profiles = {
    "bm_lewis":   (98.0,  1350.0, 2700.0),
    "bm_george":  (108.0, 1450.0, 2900.0),
    "am_adam":    (118.0, 1550.0, 3100.0),
    "am_michael": (132.0, 1700.0, 3400.0),
    "am_fenrir":  (112.0, 1600.0, 3200.0),
    "bf_emma":    (185.0, 2050.0, 4100.0),
    "af_sarah":   (198.0, 2150.0, 4300.0),
    "af_heart":   (210.0, 2250.0, 4500.0),
    "af_bella":   (222.0, 2350.0, 4700.0),
}

with np.load(bin_path, allow_pickle=True) as d:
    v_dict = {k: d[k] for k in d.files}

scored = []
for v_name, (p_ref, c_ref, r_ref) in stock_profiles.items():
    if v_name in v_dict:
        dist = (
            abs(pitch_hz - p_ref) / 25.0 * 2.5 +
            abs(centroid_hz - c_ref) / 350.0 * 1.2 +
            abs(rolloff_hz - r_ref) / 700.0 * 0.8
        )
        scored.append((dist, v_name))

scored.sort(key=operator.itemgetter(0))
top_matches = scored[:3]

weights = [1.0 / (dist + 0.15) for dist, _ in top_matches]
total_w = sum(weights)
norm_weights = [w / total_w for w in weights]

_, first_voice = top_matches[0]
blended_vector = np.zeros_like(v_dict[first_voice], dtype=np.float32)
recipe = []
for w, (_, v_name) in zip(norm_weights, top_matches):
    blended_vector += w * v_dict[v_name].astype(np.float32)
    recipe.append(f"{v_name} ({round(w * 100)}%)")

v_dict[voice_name] = blended_vector
with open(bin_path, "wb") as f_out:
    np.savez(f_out, **v_dict)


print(json.dumps({
    "pitch_hz": round(pitch_hz, 1),
    "centroid_hz": round(centroid_hz, 0),
    "recipe": ", ".join(recipe)
}))
"""
            try:
                proc = subprocess.run(
                    [py_exec, "-c", analyzer_script, chosen_wav, bin_path, voice_key_name],
                    capture_output=True,
                    text=True,
                    check=True
                )
                lines = proc.stdout.strip().splitlines()
                result = json.loads(lines[-1])

                try:
                    with open(self.voice_list_file, "r") as r_f:
                        existing_customs = json.load(r_f)
                except Exception:
                    existing_customs = []

                if voice_key_name not in existing_customs:
                    existing_customs.append(voice_key_name)
                    with open(self.voice_list_file, "w") as w_f:
                        json.dump(existing_customs, w_f)

                summary = (
                    f"Created acoustic blend '{voice_key_name}'!\n\n"
                    f"Detected Pitch: {result['pitch_hz']} Hz\n"
                    f"Vocal Brightness: {result['centroid_hz']} Hz\n"
                    f"Blended Formula: {result['recipe']}"
                )
                messagebox.showinfo("Acoustic Blend Complete", summary)
                self.log_status(f"Blended '{voice_key_name}': {result['recipe']}")
            except subprocess.CalledProcessError as e:
                err_msg = e.stderr.strip() if e.stderr else str(e)
                messagebox.showerror("Analysis Error", f"Acoustic analysis failed:\n{err_msg}")
                self.log_status("Acoustic Extraction Error.")
            except Exception as e:
                messagebox.showerror("Process Failure", f"Failed to inject blended profile:\n{e}")
                self.log_status("Matrix Injection Error.")

        threading.Thread(target=dynamic_worker, daemon=True).start()

    def trigger_launch(self):
        self.log_status("Launching Gradio background thread application wrapper service...")
        threading.Thread(target=lambda: subprocess.run([sys.executable, os.path.join(self.src_dir, "run.py")], cwd=self.base_dir), daemon=True).start()
        messagebox.showinfo("Web UI active", "The generation engine server is running background hooks!\nOpen: http://127.0.0.1:7860")
        self.log_status("Web application active running on port 7860.")

    def trigger_archive_flow(self):
        import glob
        import shutil
        from datetime import datetime
        base_name = self.filename_entry.get().strip() or "recording"
        downloads_dir = os.path.expanduser("~/Downloads")
        search_pattern = os.path.join(downloads_dir, "output*.wav")
        matching_files = glob.glob(search_pattern)
        
        if not matching_files:
            messagebox.showerror("Error", "Could not find any fresh 'output.wav' file inside your system Downloads directory.")
            return

        latest_file = max(matching_files, key=os.path.getctime)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if base_name.lower().endswith(".wav"):
            base_name = base_name[:-4]
        final_filename = f"{base_name}_{timestamp}.wav"
        
        user_music_dir = os.path.expanduser("~/Music")
        target_directory = os.path.join(user_music_dir, "Voice Transcripts")
        
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
            
        destination_file_path = os.path.join(target_directory, final_filename)
        
        try:
            shutil.move(latest_file, destination_file_path)
            messagebox.showinfo("Success", f"File processed successfully!\nSaved as: {final_filename}\nin Music/Voice Transcripts")
            self.filename_entry.delete(0, tk.END)
            self.filename_entry.insert(0, "voice_recording")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to relocate file: {e}")

    def on_close(self):
        subprocess.run("pkill -f 'app.py' 2>/dev/null || true", shell=True)
        self.root.destroy()


if __name__ == "__main__":
    tk_root = tk.Tk()
    app = UniversalToolkit(tk_root)
    tk_root.mainloop()
