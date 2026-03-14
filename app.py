"""
OMM SAI TRADERS - HuggingFace Spaces Deployment
This file serves as the entry point for HuggingFace Spaces.

In Spaces settings, set:
  - SDK: Docker  OR  use this with Python
  - Port: 7860
  - Secrets: SUPABASE_URL, SUPABASE_KEY
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# HuggingFace runs on port 7860
os.environ.setdefault("PORT", "7860")

from main import app
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
