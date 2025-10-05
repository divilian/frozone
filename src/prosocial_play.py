
### ATTEMPT 1

# #!/usr/bin/env python3
# # Interactive Prosocial Dialogue Playground
# # Project Frozone
# # (C) 2025

# import torch
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# # Pick a generation model (Flan-T5 is a good default for prosocial tasks)
# MODEL_NAME = "google/flan-t5-base"

# def load_model(model_name: str):
#     print(f"Loading model {model_name}...")
#     tok = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     model.to(device).eval()
#     return tok, model, device


# def chat_loop(tok, model, device):
#     history = []
#     print("Type 'done' to quit.\n")

#     user_input = input("You: ")
#     while user_input.strip().lower() != "done":
#         history.append(f"User: {user_input}")

#         # Construct prompt from conversation history
#         prompt = "\n".join(history) + "\nModel:"

#         encoded = tok(prompt, return_tensors="pt", truncation=True, max_length=512).to(device)

#         with torch.inference_mode():
#             out_ids = model.generate(
#                 **encoded,
#                 max_new_tokens=128,
#                 do_sample=True,
#                 temperature=0.7,
#                 top_p=0.9,
#                 pad_token_id=tok.eos_token_id,
#             )

#         reply = tok.decode(out_ids[0], skip_special_tokens=True)
#         print(f"Model: {reply}")
#         history.append(f"Model: {reply}")

#         user_input = input("You: ")


# if __name__ == "__main__":
#     tok, model, device = load_model(MODEL_NAME)
#     chat_loop(tok, model, device)


### ATTEMPT 2

# from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline, AutoModelForCausalLM
# import torch

# # 1. Toxicity detector
# detector_name = "unitary/toxic-bert"
# detector = pipeline("text-classification", model=detector_name, tokenizer=detector_name)

# # 2. Dialogue responder
# responder_name = "microsoft/DialoGPT-medium"
# tokenizer_resp = AutoTokenizer.from_pretrained(responder_name)
# model_resp = AutoModelForCausalLM.from_pretrained(responder_name)

# chat_history_ids = None

# def respond(user_input):
#     global chat_history_ids
    
#     # Step A: Detect toxicity
#     result = detector(user_input)[0]
#     toxic_prob = result['score'] if result['label'] == 'toxic' else 1 - result['score']
    
#     if toxic_prob > 0.6:
#         prompt = f"The user said something toxic: '{user_input}'. Reply in a calm, respectful, prosocial way."
#     else:
#         prompt = user_input
    
#     # Encode new input
#     new_input_ids = tokenizer_resp.encode(prompt + tokenizer_resp.eos_token, return_tensors='pt')
    
#     # Append to chat history (so bot remembers context)
#     bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids
    
#     # Generate response
#     chat_history_ids = model_resp.generate(
#         bot_input_ids,
#         max_length=1000,
#         pad_token_id=tokenizer_resp.eos_token_id,
#         do_sample=True,
#         top_k=50,
#         top_p=0.95,
#         temperature=0.7,
#     )
    
#     # Decode *only the new response tokens*
#     response_ids = chat_history_ids[:, bot_input_ids.shape[-1]:]
#     response = tokenizer_resp.decode(response_ids[0], skip_special_tokens=True)
#     return response.strip()

# # Try interactive loop
# if __name__ == "__main__":
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["quit", "exit"]: break
#         print("Bot:", respond(user_input))

#!/usr/bin/env python3
# Interactive Prosocial Retrieval Bot
# Uses allenai/prosocial-dialog dataset
# Option 1: retrieval-based prosocial responses
# (C) 2025

### ATTEMPT 3

# import random
# import torch
# from datasets import load_dataset  # I did pip install datasets
# from sentence_transformers import SentenceTransformer  # I did pip install sentence transformers
# import faiss  # I did pip install faiss-cpu

# # 1. Load dataset
# print("Loading dataset...")
# ds = load_dataset("allenai/prosocial-dialog", split="train")

# # We'll keep just toxic comment + prosocial response pairs
# pairs = [(ex["context"], ex["response"]) for ex in ds]

# # 2. Build embeddings for retrieval
# print("Building embeddings...")
# embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # small + CPU friendly
# corpus = [p[0] for p in pairs]
# corpus_embeddings = embedder.encode(corpus, convert_to_numpy=True, show_progress_bar=True)

# # 3. Build FAISS index for fast similarity search
# dim = corpus_embeddings.shape[1]
# index = faiss.IndexFlatL2(dim)
# index.add(corpus_embeddings)

# def get_prosocial_reply(user_input, top_k=3):
#     # Embed user input
#     q_emb = embedder.encode([user_input], convert_to_numpy=True)
#     # Search
#     D, I = index.search(q_emb, top_k)
#     # Pick one of the top replies at random for variety
#     best_idx = random.choice(I[0])
#     toxic_example, prosocial_reply = pairs[best_idx]
#     return prosocial_reply

# # 4. Interactive loop
# if __name__ == "__main__":
#     print("Prosocial Bot ready! Type 'quit' to exit.\n")
#     while True:
#         text = input("You: ")
#         if text.lower() in ["quit", "exit"]:
#             break
#         reply = get_prosocial_reply(text)
#         print("Bot:", reply)


### ATTEMPT 4

#!/usr/bin/env python3
# Conversational bot with prosocial responses for toxic input
# CPU-friendly, no FAISS
# (C) 2025

import random
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import numpy as np

# ------------------------------
# 1. Load toxicity detector
# ------------------------------
print("Loading toxicity detector...")
detector = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    tokenizer="unitary/toxic-bert",
)

# ------------------------------
# 2. Load conversational model (DialoGPT-medium)
# ------------------------------
print("Loading conversational model...")
tokenizer_chat = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model_chat = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
device = "cuda" if torch.cuda.is_available() else "cpu"
model_chat.to(device)

# ------------------------------
# 3. Load ProsocialDialog dataset and embeddings
# ------------------------------
print("Loading ProsocialDialog dataset...")
ds = load_dataset("allenai/prosocial-dialog", split="train")
pairs = [(ex["context"], ex["response"]) for ex in ds]

print("Building embeddings...")
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
corpus = [p[0] for p in pairs]
corpus_embeddings = embedder.encode(corpus, convert_to_numpy=True, show_progress_bar=True)

# ------------------------------
# 4. Function to retrieve prosocial reply
# ------------------------------
def get_prosocial_reply(user_input, history, top_k=3):
    # Include last few turns for context
    combined_input = " ".join(history[-5:] + [user_input])
    q_emb = embedder.encode([combined_input], convert_to_numpy=True)
    distances = ((corpus_embeddings - q_emb) ** 2).sum(axis=1)
    top_indices = distances.argsort()[:top_k]
    best_idx = random.choice(top_indices)
    return pairs[best_idx][1]

# ------------------------------
# 5. Interactive loop
# ------------------------------
chat_history = []

print("\nProsocial ChatBot ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        break

    chat_history.append(f"You: {user_input}")

    # Step 1: detect toxicity
    result = detector(user_input)[0]
    toxic_prob = result['score'] if result['label'] == 'toxic' else 1 - result['score']

    if toxic_prob > 0.6:
        # Step 2: retrieve prosocial response for toxic input
        reply = get_prosocial_reply(user_input, chat_history)
    else:
        # Step 3: normal conversational model
        new_input_ids = tokenizer_chat.encode(
            user_input + tokenizer_chat.eos_token, return_tensors='pt'
        ).to(device)

        # Include previous chat history
        if len(chat_history) > 1:
            history_ids = tokenizer_chat.encode(" ".join(chat_history), return_tensors='pt').to(device)
            bot_input_ids = torch.cat([history_ids, new_input_ids], dim=-1)
        else:
            bot_input_ids = new_input_ids

        with torch.inference_mode():
            output_ids = model_chat.generate(
                bot_input_ids,
                max_length=1000,
                pad_token_id=tokenizer_chat.eos_token_id,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.7
            )

        # Decode only new tokens
        reply = tokenizer_chat.decode(output_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

        # Fallback if model generates empty string
        if not reply.strip():
            reply = "Hmm, interesting."

    print("Bot:", reply)
    chat_history.append(f"Bot: {reply}")
