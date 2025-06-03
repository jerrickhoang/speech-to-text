from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import torchaudio
import io
import ffmpeg

app = FastAPI()

# Allow CORS for all origins (for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_name = "openai/whisper-large-v3"
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name)
model.eval()

def prepare_whisper_input(audio_bytes):
    input_buffer = io.BytesIO(audio_bytes)
    out, err = (
        ffmpeg
        .input('pipe:0')
        .output('pipe:1', format='wav', ac=1, ar='16000')
        .run(input=input_buffer.read(), capture_stdout=True, capture_stderr=True)
    )
    output_buffer = io.BytesIO(out)
    output_buffer.seek(0)
    waveform, sample_rate = torchaudio.load(output_buffer)
    if sample_rate != 16000:
        waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)
    return waveform.squeeze().numpy()

@app.post("/api/speech_to_text")
async def speech_to_text(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    audio = prepare_whisper_input(audio_bytes)
    # Set language and task
    inputs = processor(
        audio,
        sampling_rate=16000,
        return_tensors="pt",
        language="en",
        task="transcribe"
    )
    # Get forced_decoder_ids for English
    forced_decoder_ids = processor.get_decoder_prompt_ids(language="en", task="transcribe")
    with torch.no_grad():
        generated_ids = model.generate(
            inputs["input_features"],
            forced_decoder_ids=forced_decoder_ids
        )
    transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return JSONResponse({"transcription": transcription}) 