#!/usr/bin/env python3
"""
Optional Backend Server for WhatsApp DP Resizer
This provides server-side image processing as a backup to the frontend Canvas processing
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image, ImageFilter
import io
import base64
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image_backend(image_data, mode, bg_color='#ffffff', blur_intensity=15):
    """
    Server-side image processing that mirrors the frontend Canvas implementation
    """
    try:
        # Decode base64 image
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        size = 640  # WhatsApp DP size
        
        if mode == 'full-resize':
            # Stretch to square
            processed_img = img.resize((size, size), Image.Resampling.LANCZOS)
            
        elif mode == 'center-left-right':
            # Center Same Left Right Resize
            img_width, img_height = img.size
            scale_factor = size / img_height
            scaled_width = int(img_width * scale_factor)
            scaled_img = img.resize((scaled_width, size), Image.Resampling.LANCZOS)
            
            if scaled_width <= size:
                # Create with stretched edges
                center_width = int(scaled_width * 0.9)
                edge_width = (size - center_width) // 2
                
                processed_img = Image.new('RGB', (size, size))
                
                # Left edge (stretched)
                left_edge = scaled_img.crop((0, 0, int(scaled_width * 0.05), size))
                left_edge_resized = left_edge.resize((edge_width, size), Image.Resampling.LANCZOS)
                processed_img.paste(left_edge_resized, (0, 0))
                
                # Center
                center = scaled_img.crop((int(scaled_width * 0.05), 0, int(scaled_width * 0.95), size))
                center_resized = center.resize((center_width, size), Image.Resampling.LANCZOS)
                processed_img.paste(center_resized, (edge_width, 0))
                
                # Right edge (stretched)
                right_edge = scaled_img.crop((int(scaled_width * 0.95), 0, scaled_width, size))
                right_edge_resized = right_edge.resize((edge_width, size), Image.Resampling.LANCZOS)
                processed_img.paste(right_edge_resized, (edge_width + center_width, 0))
            else:
                # Crop and process
                crop_width = size / scale_factor
                crop_start = (img_width - crop_width) / 2
                cropped_img = img.crop((crop_start, 0, crop_start + crop_width, img_height))
                processed_img = cropped_img.resize((size, size), Image.Resampling.LANCZOS)
                
        elif mode == 'left-right-center':
            # Left Right Same Centre Resize
            img_width, img_height = img.size
            scale_factor = size / img_height
            scaled_width = int(img_width * scale_factor)
            scaled_img = img.resize((scaled_width, size), Image.Resampling.LANCZOS)
            
            if scaled_width <= size:
                side_width = int(scaled_width * 0.45)
                center_width = size - (side_width * 2)
                
                processed_img = Image.new('RGB', (size, size))
                
                # Left side
                left_side = scaled_img.crop((0, 0, int(scaled_width * 0.45), size))
                left_side_resized = left_side.resize((side_width, size), Image.Resampling.LANCZOS)
                processed_img.paste(left_side_resized, (0, 0))
                
                # Center (stretched)
                center = scaled_img.crop((int(scaled_width * 0.45), 0, int(scaled_width * 0.55), size))
                center_resized = center.resize((center_width, size), Image.Resampling.LANCZOS)
                processed_img.paste(center_resized, (side_width, 0))
                
                # Right side
                right_side = scaled_img.crop((int(scaled_width * 0.55), 0, scaled_width, size))
                right_side_resized = right_side.resize((side_width, size), Image.Resampling.LANCZOS)
                processed_img.paste(right_side_resized, (side_width + center_width, 0))
            else:
                crop_width = size / scale_factor
                crop_start = (img_width - crop_width) / 2
                cropped_img = img.crop((crop_start, 0, crop_start + crop_width, img_height))
                processed_img = cropped_img.resize((size, size), Image.Resampling.LANCZOS)
                
        elif mode == 'crop-colors':
            # Fit with colored background
            img_width, img_height = img.size
            scale = min(size / img_width, size / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert hex color to RGB
            if bg_color.startswith('#'):
                bg_color = bg_color.lstrip('#')
                bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                bg_rgb = (255, 255, 255)
            
            processed_img = Image.new('RGB', (size, size), bg_rgb)
            x = (size - new_width) // 2
            y = (size - new_height) // 2
            processed_img.paste(resized_img, (x, y))
            
        elif mode == 'set-blur':
            # Blur background with sharp center
            img_width, img_height = img.size
            scale = min(size / img_width, size / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Create blurred background
            bg_img = img.resize((size, size), Image.Resampling.LANCZOS)
            blurred_bg = bg_img.filter(ImageFilter.GaussianBlur(radius=blur_intensity))
            
            # Resize sharp image
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Paste sharp image on blurred background
            x = (size - new_width) // 2
            y = (size - new_height) // 2
            blurred_bg.paste(resized_img, (x, y))
            processed_img = blurred_bg
        
        else:
            # Default: stretch
            processed_img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Convert to base64
        output_buffer = io.BytesIO()
        processed_img.save(output_buffer, format='JPEG', quality=90, optimize=True)
        output_buffer.seek(0)
        
        processed_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        return f"data:image/jpeg;base64,{processed_base64}"
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'WhatsApp DP Backend Server',
        'status': 'running',
        'endpoints': ['/process', '/health']
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/process', methods=['POST'])
def process_image():
    try:
        data = request.json
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        image_data = data['image']
        mode = data.get('mode', 'full-resize')
        bg_color = data.get('bg_color', '#ffffff')
        blur_intensity = int(data.get('blur_intensity', 15))
        
        processed_image = process_image_backend(image_data, mode, bg_color, blur_intensity)
        
        if processed_image:
            return jsonify({
                'success': True,
                'processed_image': processed_image,
                'mode': mode
            })
        else:
            return jsonify({'error': 'Failed to process image'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting WhatsApp DP Backend Server...")
    print("Server will run on http://localhost:5000")
    print("Endpoints:")
    print("  GET  /        - Server info")
    print("  GET  /health  - Health check")
    print("  POST /process - Process image")
    
    app.run(debug=True, host='0.0.0.0', port=5000)