from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
from prompts.creating import creating_prompt_template

class CreatorAgent:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash-preview-image-generation"
        self.name = "CreatorAgent"
    
    def get_name(self):
        return self.name
    
    def create_image(self, prompt):
        try:
            # Use Gemini multimodal model - model requires both TEXT and IMAGE modalities
            text_input = f"Generate an image: {prompt}"
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[text_input],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE'],  # Model requires both, but we'll only use IMAGE
                    candidate_count=1  # Limit to one candidate for simplicity
                ),
            )
            
            # Extract only images from response (ignore text)
            if response.candidates and len(response.candidates) > 0:
                for part in response.candidates[0].content.parts:
                    # Only process image parts, skip text parts
                    if part.inline_data is not None:
                        # Convert image data to base64 for web display
                        image_bytes = part.inline_data.data
                        
                        # Create PIL Image for processing
                        image = Image.open(BytesIO(image_bytes))
                        
                        # Convert to base64 for web display
                        buffered = BytesIO()
                        image.save(buffered, format="PNG")
                        img_base64 = base64.b64encode(buffered.getvalue()).decode()
                        
                        return {
                            "success": True,
                            "image_data": img_base64,
                            "original_prompt": prompt,
                            "agent": self.name,
                            "model_used": self.model
                        }
            
            # If no images found
            return {
                "success": False,
                "error": "No images generated in response",
                "agent": self.name
            }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    def createAvatar(self, prompt):
        # Alias method for backward compatibility
        return self.create_image(creating_prompt_template(prompt))