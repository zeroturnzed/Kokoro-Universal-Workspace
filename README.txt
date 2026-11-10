===========================================================================
               🎙️ KOKORO TTS UNIVERSAL WORKSPACE GUIDE 🎙️
===========================================================================

This bundle provides a completely self-contained, cross-platform studio for 
Kokoro Text-to-Speech audio generation. It automatically builds paths, sets 
up isolation sandboxes, and patches internal library validation blocks.

---------------------------------------------------------------------------
📁 FIRST TIME WORKSPACE INITIALIZATION
---------------------------------------------------------------------------
1. Put 'gui_launcher.py' and 'app.py' inside your main workspace folder.
2. Run 'python3 gui_launcher.py' to generate the directory trees.
3. Place your system master model files into the newly created folders:
   -> Move 'kokoro-v1.0.onnx' into the 'models/' folder.
   -> Move 'voices-v1.0.bin' into the 'models/' folder.

---------------------------------------------------------------------------
🛠️ DEPLOYMENT INSTRUCTIONS (When moving to another computer)
---------------------------------------------------------------------------
Follow the numbering rules on the control panel buttons in sequence:

STEP 1: Click "1. Build Environment & Patch Engine"
   - This builds your clean local python virtual environment ('venv').
   - Installs all backend packages (Gradio, NumPy, Torch, ONNX Runtime).
   - Silently finds and modifies internal library scripts to handle custom keys.

STEP 2: Prepare your Custom Voice Model
   - Drop your custom recorded vocal sample file into:
     'input_audio/my_voice.wav'
   - Click "2. Process & Inject Voice Vector".
   - This writes your target key slot securely into the model voice matrix database.

STEP 3: Fire up the Studio Application
   - Click "3. Launch Web Interface Server".
   - This instantly releases any zombie port processes locking up your network.
   - Open your browser window and navigate to: http://127.0.0.1:7860

---------------------------------------------------------------------------
💡 MURPHY'S LAW SAFETY RULES & TROUBLESHOOTING
---------------------------------------------------------------------------
* "Port Already in Use Error" -> Click Button 3 again. It force-kills hanging
  ghost servers in the system memory before launching.
* "ModuleNotFoundError" -> Ensure you ran Button 1 on the computer first to
  provision the isolated python libraries.
* Slashes look strange? -> The application logic uses native abstraction blocks. 
  It runs perfectly on Linux (/), Windows (\), and macOS out of the box.
===========================================================================



