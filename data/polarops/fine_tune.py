import os

import polars as pl
import torch
import torch.nn as nn
import torch.functional as F
from transformers import (
    AutoTokenizer,
    PreTrainedTokenizerBase,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
from datasets import Dataset, ClassLabel, Features, Value, DatasetDict

def prep_dataset(
    csv_filename: str,
    seed: int,
    tokenizer: PreTrainedTokenizerBase
) -> DatasetDict:
    def tokenizer_fn(example):
        return tokenizer(
            example['text'],
            truncation=True,
            padding='max_length',
            max_length=512
        )

    df = (
        pl.read_csv(csv_filename, comment_prefix="#")
        #.select(text,polarized) Let's leave in the ID for now.
        .with_columns(label=pl.col("polarized"))
        .select(['comment_id','label','text'])
    )
    label_names = ["healthy", "polarized"]
    class_label = ClassLabel(num_classes=len(label_names), names=label_names)
    features = Features({
        "comment_id": Value("string"),
        "label": class_label,
        "text": Value("string")
    })
    ds = Dataset.from_pandas(df.to_pandas(), features=features)
    ds = ds.train_test_split(test_size=0.1, seed=seed)
    ds = ds.map(tokenizer_fn)
    return ds


def fine_tune(
    base_model_name: str,
    ft_model_prefix: str,
    additional_data_csv_filename: str,
    seed: int,
    return_cached: bool = True,
):
    ft_model_name = f'{ft_model_prefix}-{base_model_name}'

    print(f"Fine tuning {ft_model_name} (seed {seed})...")

    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    ds = prep_dataset(additional_data_csv_filename, seed, tokenizer)

    # Actually save the split dataset to disk, to ensure there's no mismatch
    # between training & test samples if I reload and run eval.py later.
    ds.save_to_disk(f'{ft_model_prefix}_split_dataset')
    label_mapper = ds['train'].features['label'].int2str

    if return_cached  and  os.path.exists(ft_model_name):
        print(f"Returning existing model {ft_model_name}...")
        return (
            AutoModelForSequenceClassification.from_pretrained(ft_model_name),
            AutoTokenizer.from_pretrained(ft_model_name),
            label_mapper
        )

    model = AutoModelForSequenceClassification.from_pretrained(base_model_name)

    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ds["train"],
        eval_dataset=ds["test"],
    )

    trainer.train()
    trainer.save_model(ft_model_name)
    tokenizer.save_pretrained(ft_model_name)
    return model, tokenizer, label_mapper


if __name__ == "__main__":
    model, tokenizer, label_mapper = fine_tune(
        base_model_name='distilbert-base-uncased',
        ft_model_prefix='polarops-finetuned',
        additional_data_csv_filename='polarops.csv',
        seed=1234,
        return_cached=False,
    )
