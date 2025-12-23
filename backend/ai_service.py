import requests
import os
import time
from typing import List
from .models import Tag

class AIService:
    def __init__(self):
        # We use the free Hugging Face Inference API
        self.api_url = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
        print("AI Service initialized in Cloud API Mode (Lightweight)")
        
    async def analyze_image(self, file_bytes: bytes) -> List[Tag]:
        # Retry logic for model loading (cold start)
        # Without an API key, the free tier puts models to sleep. We need more patience.
        max_retries = 15
        delay = 5
        
        # Ideally, user should set this env var. If not, it might hit rate limits or require one.
        api_key = os.environ.get("HF_API_KEY")
        
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
            
        for attempt in range(max_retries):
            try:
                # Post raw bytes directly to the API
                response = requests.post(self.api_url, headers=headers, data=file_bytes)
                
                # 503 means the model is loading on the server side
                if response.status_code == 503:
                    print(f"Model loading on server... retrying ({attempt+1}/{max_retries})")
                    time.sleep(delay)
                    continue
                    
                if response.status_code != 200:
                    print(f"API Error: {response.status_code} - {response.text}")
                    return [Tag(label="API Error", confidence=0.0)]
                    
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                     # BLIP returns: [{'generated_text': 'a photography of a cat...'}]
                    caption = result[0].get("generated_text", "")
                    
                    # Tag extraction logic
                    stopwords = {"a", "an", "the", "on", "in", "with", "of", "and", "is", "to", "at", "looking", "camera", "standing", "sitting"}
                    words = caption.replace(".", "").lower().split()
                    
                    unique_tags = []
                    for word in words:
                        if word not in stopwords and len(word) > 2:
                            tag_label = word.title()
                            if tag_label not in [t.label for t in unique_tags]:
                                unique_tags.append(Tag(label=tag_label, confidence=0.95))
                                
                    return unique_tags
                
                return [Tag(label="No Data", confidence=0.0)]
                
            except Exception as e:
                print(f"Connection Error: {e}")
                if attempt == max_retries - 1:
                    return [Tag(label="Service Unavailable", confidence=0.0)]
                    
        return [Tag(label="Timeout", confidence=0.0)]
