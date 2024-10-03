from transformers import AutoModelForCausalLM, AutoTokenizer

def load_model():
    """Load the Hugging Face model and tokenizer."""
    model_name = "meta-llama/Meta-Llama-3.1-8B"  # You can use smaller models if needed
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer
