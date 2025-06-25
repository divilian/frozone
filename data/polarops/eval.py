from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
)
from datasets import load_from_disk
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support
)

from fine_tune import prep_dataset

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

model = AutoModelForSequenceClassification.from_pretrained(
    './polarops-finetuned-distilbert-base-uncased')
tokenizer = AutoTokenizer.from_pretrained(
    './polarops-finetuned-distilbert-base-uncased')
trainer = Trainer(
    model=model,
    processing_class=tokenizer,
    compute_metrics=compute_metrics
)

ds = load_from_disk(f'./polarops-finetuned_split_dataset')
label_mapper = ds['test'].features['label'].int2str
results = trainer.evaluate(ds['test'])
for result in sorted(results):
    print(f"{result:>30}: {results[result]:.3f}")
