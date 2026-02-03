"""
QALB Urdu AI Testing - Example Script using Ollama
================================================

This script demonstrates how to interact with the Qalb model using Ollama.
Make sure Ollama is installed and the model is pulled before running.

Setup:
    1. Install Ollama: https://ollama.com/download
    2. Pull model: ollama pull enstazao/qalb:8b-instruct-fp16
    3. Run this script: python ollama_example.py
"""

import ollama

# Qalb model on Ollama
MODEL_NAME = "enstazao/qalb:8b-instruct-fp16"

# System prompt in Urdu
SYSTEM_PROMPT = "آپ ایک مددگار اور بے ضرر مصنوعی ذہانت کے اسسٹنٹ ہیں۔ آپ اردو میں سوالات کے درست جوابات دیتے ہیں۔"


def chat_with_qalb(user_message: str, system_prompt: str = SYSTEM_PROMPT) -> str:
    """
    Send a message to Qalb and get a response.
    
    Args:
        user_message: The user's question/message in Urdu
        system_prompt: System prompt for the assistant
        
    Returns:
        The model's response as a string
    """
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        options={
            "temperature": 0.1,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
        }
    )
    return response["message"]["content"]


def simple_generate(prompt: str) -> str:
    """
    Simple text generation without chat format.
    
    Args:
        prompt: The prompt for generation
        
    Returns:
        Generated text
    """
    response = ollama.generate(
        model=MODEL_NAME,
        prompt=prompt,
        options={
            "temperature": 0.1,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
        }
    )
    return response["response"]


def main():
    """Run example queries with Qalb."""
    
    print("=" * 60)
    print("🇵🇰 QALB Urdu AI Testing - Ollama Example")
    print("=" * 60)
    print()
    
    # Example questions in Urdu
    test_questions = [
        # General Knowledge
        ("سوال عام معلومات", "پاکستان کا قومی کھیل کیا ہے؟"),
        
        # City Information
        ("شہر کی معلومات", "لاہور شہر کیوں مشہور ہے؟ مختصر وضاحت کریں۔"),
        
        # Historical Figure
        ("تاریخی شخصیت", "قائد اعظم محمد علی جناح کون تھے؟"),
        
        # Translation Task
        ("ترجمہ", "انگریزی میں ترجمہ کریں: 'محنت کامیابی کی کنجی ہے۔'"),
        
        # Creative Writing
        ("تخلیقی تحریر", "ایک مختصر نظم لکھیں جس کا موضوع 'وطن' ہو۔"),
        
        # Reasoning
        ("استدلال", "اگر علی کے پاس 5 سیب ہیں اور وہ 2 اپنے بھائی کو دے دیتا ہے، تو اس کے پاس کتنے سیب بچیں گے؟"),
    ]
    
    for category, question in test_questions:
        print(f"📂 Category: {category}")
        print(f"❓ Question: {question}")
        print("-" * 40)
        
        try:
            response = chat_with_qalb(question)
            print(f"✅ Response:\n{response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
        print("=" * 60)
        print()


if __name__ == "__main__":
    main()
