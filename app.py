import gradio as gr
from kokoro_onnx import Kokoro
import soundfile as sf
import numpy as np

MODEL_PATH = "models/kokoro-v1.0.onnx"
VOICES_PATH = "models/voices-v1.0.bin"

# Initialize engine using your local files
kokoro = Kokoro(MODEL_PATH, VOICES_PATH)

def get_available_voices():
    """Reads all custom and built-in voices directly from voices-v1.0.bin."""
    with np.load(VOICES_PATH, allow_pickle=True) as _v:
        loaded_keys = sorted(list(_v.files))
    stock_prefixes = (
        "af_", "am_", "bf_", "bm_", "ef_", "em_", "ff_",
        "hf_", "hm_", "if_", "im_", "jf_", "jm_", "pf_", "pm_", "zf_", "zm_"
    )
    custom_keys = [k for k in loaded_keys if not k.startswith(stock_prefixes)]
    stock_keys = [k for k in loaded_keys if k.startswith(stock_prefixes)]
    return custom_keys + stock_keys

def refresh_dropdown():
    """Reloads voices-v1.0.bin into Kokoro and updates the dropdown choices live."""
    global kokoro
    kokoro = Kokoro(MODEL_PATH, VOICES_PATH)
    voices = get_available_voices()
    return gr.update(choices=voices)

def generate_voice(text, primary_voice, use_blend, secondary_voice, blend_ratio, speed):
    if use_blend:
        v1 = kokoro.get_voice_style(primary_voice)
        v2 = kokoro.get_voice_style(secondary_voice)
        blend_style = v1 * blend_ratio + v2 * (1.0 - blend_ratio)
        samples, sample_rate = kokoro.create(text, voice=blend_style, speed=speed, lang="en-us")
    else:
        samples, sample_rate = kokoro.create(text, voice=primary_voice, speed=speed, lang="en-us")
        
    sf.write("output.wav", samples, sample_rate)
    return "output.wav"

initial_voices = get_available_voices()
first_voice = next(iter(initial_voices), "am_adam")
default_voice = "Steven" if "Steven" in initial_voices else first_voice

# Create advanced studio interface layout
with gr.Blocks(title="Kokoro Offline Studio") as interface:
    gr.Markdown("# 🎙️ Kokoro Local Text-to-Speech Studio")
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Type text to speak:", 
                placeholder="Type or paste paragraphs here for completely local offline playback...", 
                lines=5
            )
            
            speed_slider = gr.Slider(minimum=0.5, maximum=2.0, value=1.0, step=0.1, label="Speech Speed Rate")
            
            gr.Markdown("### Voice Selection & Custom Expansion")
            voice_1 = gr.Dropdown(choices=initial_voices, value=default_voice, label="Primary Voice Select")
            
            enable_blend = gr.Checkbox(label="Enable Custom Voice Blending (Mix a brand new voice profile)", value=False)
            
            with gr.Group() as blend_options:
                voice_2 = gr.Dropdown(choices=initial_voices, value="am_michael", label="Secondary Voice Mix Target")
                ratio = gr.Slider(minimum=0.0, maximum=1.0, value=0.5, step=0.05, label="Voice Fusion Balance (1.0 = Primary Only / 0.0 = Secondary Only)")
            
            submit_btn = gr.Button("Generate Audio Natively", variant="primary")
            
        with gr.Column():
            audio_output = gr.Audio(label="Local Generated Audio Output Playback")

    # Auto-refresh dropdowns whenever clicked so newly extracted voices appear immediately
    voice_1.focus(fn=refresh_dropdown, inputs=None, outputs=voice_1)
    voice_2.focus(fn=refresh_dropdown, inputs=None, outputs=voice_2)

    submit_btn.click(
        fn=generate_voice,
        inputs=[text_input, voice_1, enable_blend, voice_2, ratio, speed_slider],
        outputs=audio_output
    )

if __name__ == "__main__":
    interface.launch(server_name="127.0.0.1", server_port=7860)
