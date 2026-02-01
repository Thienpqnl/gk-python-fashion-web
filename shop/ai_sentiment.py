import os
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pyvi import ViTokenizer
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'shop', 'phobert_model')


tokenizer = None
model = None

def load_model():
    global tokenizer, model
    if model is None:
        try:
            print(f"Đang load AI từ: {MODEL_PATH}")
            tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
            model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
            
            model.eval() 
            print("Đã load xong")
        except Exception as e:
            print(f"Lỗi load model AI: {e}")
        

load_model()

def predict_sentiment(text):
    global tokenizer, model
    if model is None or not text:
        return 0, 0.0
    try:

        text_segmented = ViTokenizer.tokenize(text)
        inputs = tokenizer(
            text_segmented, 
            return_tensors="pt", 
            truncation=True, 
            max_length=128, 
            padding=True
        )

        with torch.no_grad():
            outputs = model(**inputs)
        # 4. Tính xác suất (Softmax)
        probs = F.softmax(outputs.logits, dim=1)
        # Lấy nhãn có xác suất cao nhất
        confidence, predicted_label = torch.max(probs, dim=1)
        return predicted_label.item(), confidence.item()

    except Exception as e:
        print(f"Lỗi dự đoán AI: {e}")
        return 0, 0.0