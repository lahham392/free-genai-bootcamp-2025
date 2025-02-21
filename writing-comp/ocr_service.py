import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import numpy as np

class HandwritingRecognizer:
    def __init__(self):
        """Initialize the TrOCR model and processor"""
        self.processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
        self.model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
        
        # Move model to GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        
    def preprocess_image(self, image_array):
        """Convert numpy array to PIL Image and preprocess for model"""
        try:
            import cv2
            
            # Handle different image formats
            if len(image_array.shape) == 2:  # Grayscale
                image_array = np.stack([image_array] * 3, axis=-1)
            elif len(image_array.shape) == 3:
                if image_array.shape[-1] == 4:  # RGBA
                    # Create white background
                    background = np.ones((image_array.shape[0], image_array.shape[1], 3), dtype=np.uint8) * 255
                    alpha = image_array[:, :, 3:4] / 255.0
                    image_array = (image_array[:, :, :3] * alpha + background * (1 - alpha)).astype(np.uint8)
                elif image_array.shape[-1] != 3:  # Not RGB
                    raise ValueError(f"Unexpected number of channels: {image_array.shape[-1]}")
            else:
                raise ValueError(f"Unexpected image dimensions: {image_array.shape}")

            # Convert to grayscale for preprocessing
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            
            # Apply adaptive thresholding
            binary = cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,  # Block size
                2    # C constant
            )
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(binary)
            
            # Convert back to RGB
            enhanced = cv2.cvtColor(denoised, cv2.COLOR_GRAY2RGB)
            
            # Convert to PIL Image
            image = Image.fromarray(enhanced)
            
            # Resize if too small
            min_size = 224  # TrOCR's vision encoder typically expects at least 224x224
            if image.width < min_size or image.height < min_size:
                ratio = max(min_size/image.width, min_size/image.height)
                new_size = (int(image.width * ratio), int(image.height * ratio))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Ensure contrast is good
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)  # Increase contrast by 50%
            
            # Ensure it's RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            return image
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            print(f"Image array shape: {image_array.shape}, dtype: {image_array.dtype}")
            raise
        
    def recognize_text(self, image_array):
        """Recognize text from numpy array image"""
        try:
            print(f"Input image array shape: {image_array.shape}, dtype: {image_array.dtype}")
            
            # Preprocess image
            image = self.preprocess_image(image_array)
            print(f"Preprocessed image size: {image.size}, mode: {image.mode}")
            
            # Prepare image for model
            print("Processing image with TrOCR processor...")
            pixel_values = self.processor(image, return_tensors="pt").pixel_values
            print(f"Processor output shape: {pixel_values.shape}")
            
            pixel_values = pixel_values.to(self.device)
            print(f"Using device: {self.device}")
            
            # Generate text
            print("Generating text with TrOCR model...")
            generated_ids = self.model.generate(pixel_values)
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            print(f"Raw generated text: {generated_text}")
            
            # Clean up the text: remove numbers and extra whitespace
            cleaned_text = ''.join(c for c in generated_text if not c.isdigit())
            cleaned_text = ' '.join(cleaned_text.split())  # Remove extra whitespace
            print(f"Cleaned text: {cleaned_text}")
            
            return cleaned_text.strip().lower()
            
        except Exception as e:
            print(f"Error recognizing text: {e}")
            import traceback
            print(traceback.format_exc())
            return None
