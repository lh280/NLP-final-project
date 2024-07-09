from transformers import MarianMTModel, MarianTokenizer
from typing import List, Dict
import torch

src = "es"  # source language
trg = "en"  # target language
# name of model using 
model_name = f"Helsinki-NLP/opus-mt-{src}-{trg}"
# load model from name
model = MarianMTModel.from_pretrained(model_name)
# load tokenizer from name
tokenizer = MarianTokenizer.from_pretrained(model_name)

def translate(input_text):
    # create tensors from the text we have (tokens from input_text, creates input_ids & attention mask) - returned in pytorch
    batch = tokenizer([input_text], return_tensors="pt")
    # generates translations by putting tensors as input to the model (outputs: logits [the prediction scores of the language modeling head] & translation (text)] & many others)
    gen = model.generate(**batch)
    # takes the token ids and converts back to english
    translation = tokenizer.batch_decode(gen, skip_special_tokens=True)

    # list of tokens we have previously decoded
    decoder_ids = torch.Tensor([[tokenizer.pad_token_id]]).to(torch.long)

    # number of probable tokens that we store for each word in the model 
    n_tokens = 20

    generated_options = {}

    # loop through each generated token
    for i in range(gen.size()[1]):
        # encoded form of sentence (ids) - batch = (input tokens passed thru tokenizer)
        encoded = model.get_encoder().forward(batch["input_ids"])
        # need decoder output to get logits - model on encoded input & decoded ids (so model can predict next thing)
        decoder_output = model(encoder_outputs=encoded, decoder_input_ids=decoder_ids)
    
        # retrieve logits from decoded output
        logits = decoder_output.logits
        # softmax for probability
        token_probs = torch.softmax(logits[0, -1, :], 0)
        # sort for most probable first 
        sorted_token_ids = torch.argsort(token_probs, descending=True)
        # shorten list for performance reasons (exponentially slow down model with more tokens)
        top_token_ids = sorted_token_ids[:n_tokens]
        
        # decode each token - from numeral id to word 
        top_tokens = [tokenizer.decode(token_id) for token_id in top_token_ids]
        # what we return - dictionary, keys are most probable word in generated sentence, lists for each key are other probable words in that place and their probabilities 
        generated_options[tokenizer.decode(top_token_ids[:1].item())] = (dict(zip(top_tokens, token_probs[top_token_ids].tolist())))

        # cannot append to tensor, workaround is looping through the tensor to get raw values
        prev_decoded = []
        for j in range(decoder_ids.size()[1]):
            prev_decoded.append(decoder_ids[0][j].item())

        # append token id previously looked at to decoded array
        prev_decoded.append(top_token_ids[:1])
        # create new tensor from list of raw values
        decoder_ids = torch.Tensor([prev_decoded]).to(torch.long)
        
        decoded_translation = " ".join(list(generated_options.keys()))
    # return translated text and probabilities
    return translation[0], decoded_translation, generated_options