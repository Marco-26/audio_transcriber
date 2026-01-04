import os
from enum import Enum
from dotenv import load_dotenv
load_dotenv()

class ModelSize(str, Enum):
  TINY_EN = "tiny.en"
  TINY = "tiny"
  BASE_EN = "base.en"
  BASE = "base"
  SMALL_EN = "small.en"
  SMALL = "small"
  MEDIUM_EN = "medium.en"
  MEDIUM = "medium"
  LARGE_V1 = "large-v1"
  LARGE_V2 = "large-v2"
  LARGE_V3 = "large-v3"
  LARGE = "large"
  DISTIL_LARGE_V2 = "distil-large-v2"
  DISTIL_MEDIUM_EN = "distil-medium.en"
  DISTIL_SMALL_EN = "distil-small.en"
  DISTIL_LARGE_V3 = "distil-large-v3"
  LARGE_V3_TURBO = "large-v3-turbo"
  TURBO = "turbo"

class Provider(str, Enum):
  LOCAL = "local"
  OPENAI = "openai"

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

WORKER_THREAD_COUNT=4