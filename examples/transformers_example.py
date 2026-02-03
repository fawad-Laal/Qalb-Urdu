"""
QALB Urdu AI Testing - Hugging Face Transformers Example
=========================================================

This script demonstrates how to interact with the Qalb model using 
Hugging Face Transformers library.

Requirements:
    pip install transformers torch bitsandbytes accelerate

Note: Requires a CUDA-capable GPU with at least 8GB VRAM (with 4-bit quantization)
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


# Model configuration
MODEL_NAME = "enstazao/Qalb-1.0-8B-Instruct"

# System prompt in Urdu
SYSTEM_PROMPT = "آپ ایک مددگار اور بے ضرر مصنوعی ذہانت کے اسسٹنٹ ہیں۔ آپ اردو میں سوالات کے درست جوابات دیتے ہیں۔"


def load_model(use_4bit: bool = True):
    """
    Load the Qalb model with optional 4-bit quantization.
    
    Args:
        use_4bit: Whether to use 4-bit quantization (reduces VRAM usage)
        
    Returns:
        Tuple of (model, tokenizer)
    """
    print(f"⏳ Loading model: {MODEL_NAME}")
    
    if use_4bit:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )
        print("   Using 4-bit quantization for memory efficiency")
    else:
        bnb_config = None
        print("   Using full precision (requires more VRAM)")
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto"
    )
    
    print("✅ Model loaded successfully!")
    return model, tokenizer


def format_prompt(user_message: str, system_prompt: str = SYSTEM_PROMPT) -> str:
    """
    Format the prompt using Llama-3 chat template.
    
    Args:
        user_message: The user's question/message
        system_prompt: System prompt for the assistant
        
    Returns:
        Formatted prompt string
    """
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""


def generate_response(
    model, 
    tokenizer, 
    user_message: str,
    system_prompt: str = SYSTEM_PROMPT,
    max_new_tokens: int = 256,
    temperature: float = 0.1,
    top_p: float = 0.9,
    repetition_penalty: float = 1.1,
) -> str:
    """
    Generate a response from the model.
    
    Args:
        model: The loaded model
        tokenizer: The tokenizer
        user_message: User's input message
        system_prompt: System prompt
        max_new_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        top_p: Nucleus sampling parameter
        repetition_penalty: Penalty for repetition
        
    Returns:
        Generated response text
    """
    prompt = format_prompt(user_message, system_prompt)
    
    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]
    
    inputs = tokenizer([prompt], return_tensors="pt").to(model.device)
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        eos_token_id=terminators,
        pad_token_id=tokenizer.eos_token_id,
    )
    
    response = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:], 
        skip_special_tokens=True
    )
    
    return response


def main():
    """Run example queries with Qalb using Transformers."""
    
    print("=" * 60)
    print("🇵🇰 QALB Urdu AI Testing - Transformers Example")
    print("=" * 60)
    print()
    
    # Check CUDA availability
    if torch.cuda.is_available():
        print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
        print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("⚠️  CUDA not available. This will be very slow on CPU.")
    print()
    
    # Load model
    model, tokenizer = load_model(use_4bit=True)
    print()
    
    # Example questions
    test_questions = [
        ("سوال عام معلومات", "پاکستان کا قومی پھول کیا ہے؟"),
        ("شہر کی معلومات", "اسلام آباد کیوں بنایا گیا؟"),
        ("ترجمہ", "اردو میں ترجمہ کریں: 'Education is the key to success.'"),
    ]
    
    for category, question in test_questions:
        print(f"📂 Category: {category}")
        print(f"❓ Question: {question}")
        print("-" * 40)
        
        try:
            response = generate_response(model, tokenizer, question)
            print(f"✅ Response:\n{response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
        print("=" * 60)
        print()


if __name__ == "__main__":
    main()
