from google import genai
import os
from prompts.analyzing import analyzing_prompt

class AnalyzerAgent:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash-exp"
        self.name = "AnalyzerAgent"
    
    def get_name(self):
        return self.name
    
    def analyze_image(self, image_path, caption="Analyze this image"):
        try:
            # Check if image file exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Upload the image file using the correct API
            my_file = self.client.files.upload(file=image_path)
            
            caption = analyzing_prompt.format(caption=caption)
            # Generate content with image and prompt
            response = self.client.models.generate_content(
                model=self.model,
                contents=[my_file, caption],
            )
            
            return {
                "success": True,
                "analysis": response.text,
                "agent": self.name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }