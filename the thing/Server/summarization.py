# from transformers import pipeline
# from speech_to_text import *

 
# summarizer = pipeline(task = 'summarization', model='/model_files', tokenizer='/model_files')
# output = summarizer(text, max_length=int(len(text.replace(" ", ""))/4), min_length=int(len(text)/8), do_sample=False)
# output = output[0]['summary_text']

# def summary():
#     return output
# #Run below two lines ones seperately if above code doesn't work and try again with same code. 

# #summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# #summarizer.save_pretrained('/model_files')

params = {
  "early_stopping": True,
#   "length_penalty": 2.0,
  "max_length": 142,
  "min_length": 56,
#   "no_repeat_ngram_size": 3,
  "num_beams": 4,
#   "pad_token_id": 1,
}
from transformers import T5Tokenizer, T5ForConditionalGeneration

def summary(text):
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    inputs = tokenizer.batch_encode_plus(["summarize: " + text], max_length=4096, return_tensors="pt", pad_to_max_length=True)  # Batch size 1
    outputs = model.generate(inputs['input_ids'], **params)

    final_output = ([tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in outputs])
    return final_output[0]