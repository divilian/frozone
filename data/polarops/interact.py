import torch

from fine_tune import fine_tune


model, tokenizer, label_mapper = fine_tune(
    base_model_name='distilbert-base-uncased',
    ft_model_name='polarops-finetuned-distilbert-base-uncased',
    additional_data='polarops.csv',
    return_cached=True
)

text = input("Enter text (or 'done'): ")
while text != "done":
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)
        for i, prob in enumerate(probs[0]):
            if torch.isclose(prob, probs[0].max()):
                label = label_mapper(i).upper()
            else:
                label = label_mapper(i)
            print(f"{label:>10}: {prob.item():.3f}")
    text = input("Enter text (or 'done'): ")
