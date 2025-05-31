# Speech-to-Text App

This is a fullstack app that transcribes speech from your microphone to text using HuggingFace's Speech2Text model.

## Features
- Python FastAPI backend with HuggingFace Speech2Text
- Next.js frontend with microphone recording
- Deployable to Vercel (serverless)

## Project Structure

```
/               # Project root
  api/          # Python FastAPI backend (Vercel Python API)
    speech_to_text.py
  pages/        # Next.js frontend
    index.js
  requirements.txt
  package.json
  next.config.js
  README.md
```

## Local Development

### 1. Install Python dependencies
```
pip install -r requirements.txt
```

### 2. Install Node dependencies
```
npm install
```

### 3. Run the backend (for local dev)
```
uvicorn api.speech_to_text:app --reload
```

### 4. Run the frontend
```
npm run dev
```

## Deploy to Vercel
- Push this repo to GitHub
- Connect to Vercel
- Vercel will auto-detect Next.js and Python API
- Add a Vercel project, deploy, and you're done!

## References
- [HuggingFace Speech2Text](https://huggingface.co/docs/transformers/en/model_doc/speech_to_text)
- [Vercel Python API](https://vercel.com/docs/functions/python)
- [Next.js](https://nextjs.org/docs) 