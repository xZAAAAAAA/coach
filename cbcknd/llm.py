import os
import requests

from llama_cpp import Llama

DEFAULT_MODEL = "https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf"
MODEL_DIR = "llm_models"


def load_model(model=DEFAULT_MODEL):

    model_base = model.split("/")[-1]

    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR, exists_ok=True)

    model_path = os.path.join(MODEL_DIR, model_base)

    response = requests.get(model, allow_redirects=True)
    open(model_path, "wb").write(response.content)

    return Llama(model_path=model_path)


if __name__ == "__main__":
    model = load_model()
    # print(model.generate("Hello, my name is"))