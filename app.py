import gradio as gr
import os
import json
from kokoro_onnx import Kokoro

# Boot the underlying engine
kokoro = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")

# 1. Base Default System Voices List
built_in_voices = [
    "af_heart", "af_bella", "am_adam", "am_michael", "af_alloy", "af_aoede", 
    "af_jessica", "af_kore", "af_nicole", "af_nova", "af_river", "af_sarah", 
    "af_sky", "am_echo", "am_eric", "am_fenrir", "am_liam", "am_onyx", 
    "am_puck", "am_santa"
]

# 2. Dynamically look for any files added through Button 2
custom_voices_tracker = os.path.join("src", "custom_voices.json")
custom_voices = []

if os.path.exists(custom_voices_tracker):
    try:
        with open(custom_voices_tracker, "r") as f:
            custom_voices = json.load(f)
    except:
        pass

# Combine lists cleanly, placing your files right at the top of the menu selector
all_voices = custom_voices + built_in_voices
default_selection = all_voices[0] if all_voices else "am_adam"

def generate_voice(text, primary_voice, speed):
    if not text.strip():
        return None
    samples, sample_rate = kokoro.create(text, voice=primary_voice, speed=speed, lang="en-us")
    return (sample_rate, samples)

with gr.Blocks(title="Kokoro TTS Interface") as interface:
    gr.Markdown("# 🎙️ Kokoro Text-To-Speech Studio Workspace")
    
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(label="Text to Synthesize", placeholder="Type your text track scripts here...", lines=5)
            voice_choice = gr.Dropdown(choices=all_voices, value=default_selection, label="Voice Model Select")
            speed_slider = gr.Slider(minimum=0.5, maximum=2.0, value=1.0, step=0.1, label="Speech Tempo Speed")
            submit_btn = gr.Button("Generate Audio Track", variant="primary")
            
        with gr.Column():
            output_audio = gr.Audio(label="Synthesized Audio Player Output")

    submit_btn.click(fn=generate_voice, inputs=[input_text, voice_choice, speed_slider], outputs=output_audio)

if __name__ == "__main__":
    interface.launch(server_name="127.0.0.1", server_port=7860)
