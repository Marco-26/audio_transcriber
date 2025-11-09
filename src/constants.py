import os
from dotenv import load_dotenv
load_dotenv()

MODEL_SIZES=[
  "tiny.en", 
  "tiny", 
  "base.en", 
  "base", 
  "small.en", 
  "small", 
  "medium.en", 
  "medium", 
  "large-v1", 
  "large-v2", 
  "large-v3", 
  "large", 
  "distil-large-v2", 
  "distil-medium.en", 
  "distil-small.en", 
  "distil-large-v3", 
  "large-v3-turbo", 
  "turbo"
]

MODEL_TYPES=["local","openai"]

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

WORKER_THREAD_COUNT=4