from PIL import Image, ImageEnhance
import numpy as np
import io

class ImageProcessor:
    def __init__(self, brightness=1.0, contrast=1.0):
        self.brightness = brightness
        self.contrast = contrast

    def convert_negative_to_positive(self, img):
        img = img.convert("RGBA")
        img_np = np.array(img)
        rgb = img_np[..., :3]
        alpha = img_np[..., 3:]
        positive_rgb = 255 - rgb
        positive_np = np.concatenate([positive_rgb, alpha], axis=-1)
        positive_img = Image.fromarray(positive_np.astype('uint8'), 'RGBA')
        return positive_img

    def enhance_image(self, img):
        img = ImageEnhance.Brightness(img).enhance(self.brightness)
        img = ImageEnhance.Contrast(img).enhance(self.contrast)
        return img

    def process(self, img):
        positive_img = self.convert_negative_to_positive(img)
        enhanced_img = self.enhance_image(positive_img)
        return enhanced_img

    def get_bytes(self, img, fmt="PNG"):
        buf = io.BytesIO()
        img.save(buf, format=fmt)
        return buf.getvalue()
