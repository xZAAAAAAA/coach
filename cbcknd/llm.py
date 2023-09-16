import os
import requests

from llama_cpp import Llama

DEFAULT_MODEL = "https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf"
MODEL_DIR = "llm_models"


def load_model(model=DEFAULT_MODEL):

    model_base = model.split("/")[-1]

    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR, exist_ok=True)

    model_path = os.path.join(MODEL_DIR, model_base)

    if not os.path.exists(model_path):
        print("Downloading model from", model, " ...")
        response = requests.get(model, allow_redirects=True)
        with open(model_path, "wb") as f:
            f.write(response.content)
        print("Downloaded model to", model_path)

    return Llama(model_path=model_path)


def prompt_model(llm, prompt, num_tokens=1024):
    resp = llm(prompt, max_tokens=num_tokens, stop=["Q:", "\n"], echo=True)

    return resp["choices"][0]["text"]


if __name__ == "__main__":
    model = load_model()
    test_text = prompt_model(model, "Hello, my name is")
    print(test_text)
