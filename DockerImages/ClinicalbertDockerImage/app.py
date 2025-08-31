from transformers import AutoTokenizer, AutoModel

# Load the tokenizer and model from Hugging Face
model_name = "emilyalsentzer/Bio_ClinicalBERT"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Example usage (you can replace this with your own logic)
text = "The patient was admitted with a history of heart failure and shortness of breath."

# Tokenize the input text
inputs = tokenizer(text, return_tensors="pt")

# Get the model's output
outputs = model(**inputs)

# You can now use the outputs for your specific task, e.g.,
# outputs.last_hidden_state (for embeddings)
# or pass it to a classification head.

print("Model loaded successfully!")
print("Input text:", text)
print("Tokenized inputs:", inputs)
print("Model outputs:", outputs.last_hidden_state.shape)