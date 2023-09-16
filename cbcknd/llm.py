import os
import requests
import openai
import json
import prompt_templates

from llama_cpp import Llama

DEFAULT_MODEL = "https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
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

    return Llama(model_path=model_path, n_ctx=5000)


def prompt_model(llm, prompt, num_tokens=10000):
    resp = llm(prompt, max_tokens=num_tokens, echo=False)
    print(resp)
    return resp["choices"][0]["text"]



def ask_llm(prompt):
    openai.api_key = "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"
    output = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    return output["choices"][0]["message"]["content"]


if __name__ == "__main__":
    response = ask_llm(prompt_templates.build_update_prompt())
    print(response)
   


