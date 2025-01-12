"""
Text Generator Module
Handles story generation using language models
"""

import torch
from unsloth import FastLanguageModel

def setup_model():
    """Set up the language model for text generation"""
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="katsuchi/mistral-7b-instruct-wikipedia-finetune",
        max_seq_length=2048,
        dtype=None,
        load_in_4bit=True,
    )
    FastLanguageModel.for_inference(model)
    return model, tokenizer

def generate_story(title, model, tokenizer):
    alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

    inputs = tokenizer(
    [
        alpaca_prompt.format(
            "You are a knowledgeable assistant that creates engaging and informative facts about various topics from Wikipedia. You always start the sentence with 'Did you know that'. Each fact should provide context and detailed information while maintaining reader interest.", # instruction
            title, # input
            "", # output - leave this blank for generation!!
        ),
    ], return_tensors = "pt").to("cuda")

    outputs = model.generate(**inputs, max_new_tokens = 200, use_cache = True)
    response = tokenizer.batch_decode(outputs)
    response_start = response[0].split("### Response:")[-1].strip()
    
    # Remove "</s>" if present
    response_start = response_start.replace("</s>", "").strip()
    
    # Split into sentences
    sentences = response_start.split('.')
    
    # Remove empty sentences and clean each sentence
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # If the last sentence doesn't end with a period, remove it
    if sentences and not response_start.endswith('.'):
        sentences = sentences[:-1]
    
    # Remove duplicate sentences while preserving order
    seen_sentences = set()
    deduplicated_sentences = []
    for sentence in sentences:
        # Normalize the sentence for comparison (remove extra spaces, convert to lowercase)
        normalized = ' '.join(sentence.lower().split())
        if normalized not in seen_sentences:
            seen_sentences.add(normalized)
            deduplicated_sentences.append(sentence)
    
    # Rejoin sentences with periods and spaces
    if deduplicated_sentences:
        response_start = '. '.join(deduplicated_sentences) + '.'
    
    return response_start