import io
from PIL import Image
from transformers import pipeline
from typing import List
from .models import Tag

class AIService:
    def __init__(self):
        print("Loading AI Model (this may take a moment on first run)...")
        # specific model for better results, using BLIP for captioning
        self.classifier = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
        print("AI Model Loaded successfully!")

    async def analyze_image(self, file_bytes: bytes) -> List[Tag]:
        """
        Analyzes the image using BLIP to generate a caption, then extracts tags.
        """
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        
        # Run inference to get caption
        # results = [{'generated_text': 'a man smiling...'}]
        results = self.classifier(image)
        caption = results[0]['generated_text']
        
        # Simple extraction strategy: Split caption into words, filter common stopwords
        # In a real app, you might use a lightweight NLP lib (spacy/nltk), 
        # but for this MVP, we'll confirm 3-5 key words.
        
        stopwords = {"a", "an", "the", "on", "in", "with", "of", "and", "is", "to", "at", "looking", "camera", "standing", "sitting"}
        words = caption.replace(".", "").lower().split()
        
        unique_tags = []
        for word in words:
            if word not in stopwords and len(word) > 2:
                # Capitalize
                tag_label = word.title()
                if tag_label not in [t.label for t in unique_tags]:
                     # Mock confidence for caption words as they are high confidence by definition of the model
                    unique_tags.append(Tag(label=tag_label, confidence=0.95))

        return unique_tags
