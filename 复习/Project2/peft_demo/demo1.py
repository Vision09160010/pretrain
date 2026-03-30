from peft import LoraConfig,TaskType
from peft import get_peft_model
peft_config = LoraConfig(
    task_type=TaskType.SEQ_2_SEQ_LM,
    inference_mode=False,
    r=8,
    lora_alpha=32,
    lora_dropout=0.1
)
from transformers import AutoModelForSeq2SeqLM, TrainingArguments

model = AutoModelForSeq2SeqLM.from_pretrained("bigscience/mt0-large")

model = get_peft_model(model, peft_config)

model.print_trainable_parameters()

training_args = TrainingArguments(
    output_dir="bigscience/mt0-large-lora",
    learning_rate = 1e-3,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    num_train_epochs=2,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args = training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset = tokenized_datasets["test"],
    processing_class = tokenizers,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
)

trainer.train()


model.save_pretrained("output_dir")