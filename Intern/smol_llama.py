# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("BEE-spoke-data/smol_llama-101M-GQA")
model = AutoModelForCausalLM.from_pretrained("BEE-spoke-data/smol_llama-101M-GQA")