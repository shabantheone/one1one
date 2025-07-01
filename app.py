import os
import uuid
import logging
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from PIL import Image, ImageFilter, ImageDraw
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import tempfile
import io
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload and processed directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def crop_to_square(img):
    """Crop image to perfect square from center."""
    width, height = img.size
    
    # Find the smaller dimension to create a square
    min_dimension = min(width, height)
    
    # Calculate center crop coordinates
    left = (width - min_dimension) // 2
    top = (height - min_dimension) // 2
    right = left + min_dimension
    bottom = top + min_dimension
    
    # Crop to square
    return img.crop((left, top, right, bottom))

def crop_to_circle(img):
    """Crop image to circle from center."""
    # First crop to square
    square_img = crop_to_square(img)
    size = square_img.size[0]
    
    # Create circular mask
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Apply circular mask
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(square_img, (0, 0))
    output.putalpha(mask)
    
    # Convert back to RGB with white background
    final = Image.new('RGB', (size, size), (255, 255, 255))
    final.paste(output, (0, 0), output)
    return final

def apply_crop(img, crop_data):
    """Apply crop to image based on crop data from frontend."""
    try:
        # Calculate the scale factor from canvas to original image
        original_width, original_height = img.size
        canvas_width = crop_data.get('canvasWidth', original_width)
        canvas_height = crop_data.get('canvasHeight', original_height)
        
        scale_x = original_width / canvas_width
        scale_y = original_height / canvas_height
        
        # Convert crop coordinates to original image scale
        crop_x = int(crop_data['x'] * scale_x)
        crop_y = int(crop_data['y'] * scale_y)
        crop_width = int(crop_data['width'] * scale_x)
        crop_height = int(crop_data['height'] * scale_y)
        
        # Ensure crop bounds are within image
        crop_x = max(0, min(crop_x, original_width - 1))
        crop_y = max(0, min(crop_y, original_height - 1))
        crop_width = min(crop_width, original_width - crop_x)
        crop_height = min(crop_height, original_height - crop_y)
        
        # Crop the image
        cropped = img.crop((crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))
        
        # For circle crop, create a circular mask
        if crop_data.get('type') == 'crop-circle':
            # Create a square image for the circle
            size = min(crop_width, crop_height)
            cropped = cropped.resize((size, size), Image.Resampling.BILINEAR)
            
            # Create circular mask
            mask = Image.new('L', (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            
            # Apply circular mask
            output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            output.paste(cropped, (0, 0))
            output.putalpha(mask)
            
            # Convert back to RGB with white background
            final = Image.new('RGB', (size, size), (255, 255, 255))
            final.paste(output, (0, 0), output)
            return final
        
        return cropped
        
    except Exception as e:
        print(f"Error applying crop: {e}")
        return img

def process_image_to_square(image_path, output_path, size=512, mode='stretch', bg_color=None, blur_intensity=15, crop_data=None):
    """
    Process an image to create a perfect square.
    
    Args:
        image_path: Path to the input image
        output_path: Path where the processed image will be saved
        size: Size of the output square (default: 512x512 for WhatsApp)
        mode: Processing mode ('stretch', 'fit', 'blur', 'center', 'left-right', 'crop-square', 'crop-circle')
        bg_color: Background color for 'fit' mode (hex color like '#ffffff')
        blur_intensity: Blur radius for 'blur' mode (default: 15)
        crop_data: Dictionary containing crop coordinates and dimensions
    """
    try:
        # Open and process the image
        img = Image.open(image_path)
        
        # Always convert to RGB mode for JPEG compatibility
        if img.mode == 'RGBA':
            # Create white background for transparent images
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        elif img.mode == 'LA':
            # Convert grayscale with alpha to RGB
            background = Image.new('RGB', img.size, (255, 255, 255))
            img_rgb = img.convert('RGBA')
            background.paste(img_rgb, mask=img_rgb.split()[-1])
            img = background
        elif img.mode == 'P':
            # Convert palette mode to RGB
            if 'transparency' in img.info:
                img = img.convert('RGBA')
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            else:
                img = img.convert('RGB')
        elif img.mode in ('L', 'CMYK', '1'):
            # Convert other modes to RGB
            img = img.convert('RGB')
        
        # Ensure we have RGB mode
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Handle crop modes with user-defined areas
        if mode in ['crop-square', 'crop-circle'] and crop_data:
            img = apply_crop(img, crop_data)
        elif mode == 'crop-square':
            img = crop_to_square(img)
        elif mode == 'crop-circle':
            img = crop_to_circle(img)
        
        if mode == 'stretch':
            # Resize to perfect square by stretching (not cropping)
            square_img = img.resize((size, size), Image.Resampling.BILINEAR)
        elif mode == 'fit':
            # Fit image into square with background color
            img_width, img_height = img.size
            scale = min(size / img_width, size / img_height)
            
            # Calculate new dimensions
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Resize the image maintaining aspect ratio
            resized_img = img.resize((new_width, new_height), Image.Resampling.BILINEAR)
            
            # Create square canvas with background color
            if bg_color and bg_color.startswith('#'):
                # Convert hex to RGB
                bg_color = bg_color.lstrip('#')
                bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))
            else:
                bg_rgb = (255, 255, 255)  # Default white
            
            square_img = Image.new('RGB', (size, size), bg_rgb)
            
            # Calculate position to center the image
            x = (size - new_width) // 2
            y = (size - new_height) // 2
            
            # Paste the resized image onto the square canvas
            square_img.paste(resized_img, (x, y))
        elif mode == 'blur':
            # Add blur effect and fit into square
            from PIL import ImageFilter
            
            img_width, img_height = img.size
            scale = min(size / img_width, size / img_height)
            
            # Calculate new dimensions
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Resize the image maintaining aspect ratio
            resized_img = img.resize((new_width, new_height), Image.Resampling.BILINEAR)
            
            # Create blurred background
            bg_img = img.resize((size, size), Image.Resampling.BILINEAR)
            blurred_bg = bg_img.filter(ImageFilter.GaussianBlur(radius=blur_intensity))
            
            # Calculate position to center the clear image
            x = (size - new_width) // 2
            y = (size - new_height) // 2
            
            # Paste the clear image onto the blurred background
            blurred_bg.paste(resized_img, (x, y))
            square_img = blurred_bg
        elif mode == 'center':
            # Center Same Left Right Resize: Stretch 5% left edge and 5% right edge, keep 90% center untouched
            img_width, img_height = img.size
            
            # Scale image to fit square height
            scale_factor = size / img_height
            scaled_img = img.resize((int(img_width * scale_factor), size), Image.Resampling.BILINEAR)
            scaled_width = scaled_img.width
            
            # Calculate exact pixel widths to avoid gaps
            target_left_width = int(size * 0.05)  # 5% of final square
            target_right_width = int(size * 0.05)  # 5% of final square
            target_center_width = size - target_left_width - target_right_width  # Remaining 90%
            
            # Create final square image
            square_img = Image.new('RGB', (size, size), (255, 255, 255))
            
            # If scaled image is wider than needed, crop and position properly
            if scaled_width >= target_center_width:
                # Extract center portion that will remain unchanged
                center_start = (scaled_width - target_center_width) // 2
                center_section = scaled_img.crop((center_start, 0, center_start + target_center_width, size))
                
                # Extract thin left and right edges for stretching
                left_edge_width = max(1, scaled_width // 50)  # Very thin left edge
                right_edge_width = max(1, scaled_width // 50)  # Very thin right edge
                
                left_edge = scaled_img.crop((0, 0, left_edge_width, size))
                right_edge = scaled_img.crop((scaled_width - right_edge_width, 0, scaled_width, size))
                
                # Stretch edges to fill the 5% sections
                left_stretched = left_edge.resize((target_left_width, size), Image.Resampling.BILINEAR)
                right_stretched = right_edge.resize((target_right_width, size), Image.Resampling.BILINEAR)
                
                # Combine sections perfectly
                square_img.paste(left_stretched, (0, 0))
                square_img.paste(center_section, (target_left_width, 0))
                square_img.paste(right_stretched, (target_left_width + target_center_width, 0))
            else:
                # If image is narrower, center it and fill sides with stretched edges
                x_offset = (size - scaled_width) // 2
                square_img.paste(scaled_img, (x_offset, 0))
                
                # Fill left and right gaps with stretched edge content
                if x_offset > 0:
                    left_edge = scaled_img.crop((0, 0, 1, size))
                    right_edge = scaled_img.crop((scaled_width-1, 0, scaled_width, size))
                    
                    left_fill = left_edge.resize((x_offset, size), Image.Resampling.BILINEAR)
                    right_fill = right_edge.resize((size - x_offset - scaled_width, size), Image.Resampling.BILINEAR)
                    
                    square_img.paste(left_fill, (0, 0))
                    square_img.paste(right_fill, (x_offset + scaled_width, 0))
                
        elif mode == 'left-right':
            # Left Right Same Center Resize: Keep left 25% and right 25% EXACTLY the same, stretch ONLY center 50%
            img_width, img_height = img.size
            
            # First, scale the entire image to fit the square height
            scale_factor = size / img_height
            scaled_img = img.resize((int(img_width * scale_factor), size), Image.Resampling.BILINEAR)
            scaled_width = scaled_img.width
            
            # Create the final square image
            square_img = Image.new('RGB', (size, size), (255, 255, 255))
            
            # Calculate sections of the scaled image
            left_end = scaled_width // 4  # First 25%
            center_start = scaled_width // 4  # Center starts at 25%
            center_end = 3 * scaled_width // 4  # Center ends at 75%
            right_start = 3 * scaled_width // 4  # Right starts at 75%
            
            # Extract sections
            left_section = scaled_img.crop((0, 0, left_end, size))
            center_section = scaled_img.crop((center_start, 0, center_end, size))
            right_section = scaled_img.crop((right_start, 0, scaled_width, size))
            
            # Target dimensions
            target_left_width = size // 4  # 25% of final
            target_center_width = size // 2  # 50% of final
            target_right_width = size // 4  # 25% of final
            
            # Keep left and right EXACTLY the same, STRETCH ONLY center section
            left_same = left_section.resize((target_left_width, size), Image.Resampling.NEAREST)  # Keep same
            center_stretched = center_section.resize((target_center_width, size), Image.Resampling.BILINEAR)  # Stretch
            right_same = right_section.resize((target_right_width, size), Image.Resampling.NEAREST)  # Keep same
            
            # Combine sections
            square_img.paste(left_same, (0, 0))
            square_img.paste(center_stretched, (target_left_width, 0))
            square_img.paste(right_same, (target_left_width + target_center_width, 0))
        elif mode == 'center-left-right':
            # Center Same Left Right Resize: Height to 640px, center 320px preserved, left/right stretched to 160px each
            img_width, img_height = img.size
            target_height = 640
            target_width = 640
            center_width = 320
            side_width = 160
            
            # Step 1: Resize image height to 640px while maintaining aspect ratio
            scale_factor = target_height / img_height
            scaled_width = int(img_width * scale_factor)
            scaled_img = img.resize((scaled_width, target_height), Image.Resampling.BILINEAR)
            
            # Step 2: Extract center 320px width (or full width if smaller)
            if scaled_width >= center_width:
                # Image is wide enough, extract center portion
                center_start = (scaled_width - center_width) // 2
                center_end = center_start + center_width
                center_part = scaled_img.crop((center_start, 0, center_end, target_height))
                
                # Extract left and right parts for stretching
                if center_start > 0:
                    # Get left part (from start to center)
                    left_part = scaled_img.crop((0, 0, center_start, target_height))
                    # Get right part (from center end to end)
                    right_part = scaled_img.crop((center_end, 0, scaled_width, target_height))
                else:
                    # No left/right parts available, create from edge pixels
                    left_edge = scaled_img.crop((0, 0, 1, target_height))
                    right_edge = scaled_img.crop((scaled_width-1, 0, scaled_width, target_height))
                    left_part = left_edge
                    right_part = right_edge
            else:
                # Image is narrower than 320px, use entire image as center and create edges
                center_part = scaled_img
                # Pad center to 320px if needed
                if scaled_width < center_width:
                    padded_center = Image.new('RGB', (center_width, target_height), (255, 255, 255))
                    x_offset = (center_width - scaled_width) // 2
                    padded_center.paste(scaled_img, (x_offset, 0))
                    center_part = padded_center
                
                # Create left and right parts from edge pixels
                left_edge = scaled_img.crop((0, 0, 1, target_height))
                right_edge = scaled_img.crop((scaled_width-1, 0, scaled_width, target_height))
                left_part = left_edge
                right_part = right_edge
            
            # Step 3: Stretch left and right parts to 160px each
            left_stretched = left_part.resize((side_width, target_height), Image.Resampling.BILINEAR)
            right_stretched = right_part.resize((side_width, target_height), Image.Resampling.BILINEAR)
            
            # Step 4: Combine all parts into 640x640 square
            square_img = Image.new('RGB', (target_width, target_height), (255, 255, 255))
            
            # Paste: left (0-160) + center (160-480) + right (480-640)
            square_img.paste(left_stretched, (0, 0))
            square_img.paste(center_part, (side_width, 0))
            square_img.paste(right_stretched, (side_width + center_width, 0))
        elif mode == 'left-right-center':
            # Left Right Same Centre Resize: Crop left and right equally, keep them original, stretch center to 320px
            img_width, img_height = img.size
            target_height = 640
            target_width = 640
            center_width = 320
            side_width = (target_width - center_width) // 2  # 160px each side
            
            # Step 1: Resize image height to 640px while maintaining aspect ratio
            scale_factor = target_height / img_height
            scaled_width = int(img_width * scale_factor)
            scaled_img = img.resize((scaled_width, target_height), Image.Resampling.BILINEAR)
            
            # Step 2: Calculate equal crop amounts from left and right
            if scaled_width <= target_width:
                # Image is narrower than target, use entire width and pad
                left_part = scaled_img.crop((0, 0, min(side_width, scaled_width//3), target_height))
                right_part = scaled_img.crop((max(0, scaled_width - side_width), 0, scaled_width, target_height))
                center_part = scaled_img.crop((min(side_width, scaled_width//3), 0, max(0, scaled_width - side_width), target_height))
                
                # If center is too small, use the whole image
                if center_part.size[0] <= 0:
                    center_part = scaled_img
            else:
                # Image is wider than target, crop equally from left and right
                total_crop = scaled_width - target_width
                left_crop = total_crop // 2
                right_crop = total_crop - left_crop
                
                # After cropping, we'll have exactly 640px width
                cropped_img = scaled_img.crop((left_crop, 0, scaled_width - right_crop, target_height))
                
                # Now extract the parts from the cropped image
                left_part = cropped_img.crop((0, 0, side_width, target_height))
                right_part = cropped_img.crop((target_width - side_width, 0, target_width, target_height))
                center_part = cropped_img.crop((side_width, 0, target_width - side_width, target_height))
            
            # Step 3: Keep left and right parts EXACTLY as they are (no resizing)
            # Only stretch the center part horizontally to exactly 320px
            if center_part.size[0] > 0:
                center_stretched = center_part.resize((center_width, target_height), Image.Resampling.BILINEAR)
            else:
                # Fallback: create center from edge blend
                center_stretched = Image.new('RGB', (center_width, target_height), (128, 128, 128))
            
            # Ensure left and right parts are exactly 160px wide
            if left_part.size[0] != side_width:
                left_part = left_part.resize((side_width, target_height), Image.Resampling.NEAREST)
            if right_part.size[0] != side_width:
                right_part = right_part.resize((side_width, target_height), Image.Resampling.NEAREST)
            
            # Step 4: Combine all parts into 640x640 square
            square_img = Image.new('RGB', (target_width, target_height), (255, 255, 255))
            
            # Paste: left (0-160) + center_stretched (160-480) + right (480-640)
            square_img.paste(left_part, (0, 0))
            square_img.paste(center_stretched, (side_width, 0))
            square_img.paste(right_part, (side_width + center_width, 0))
        else:
            # Default to stretch
            square_img = img.resize((size, size), Image.Resampling.BILINEAR)
        
        # Save with optimized settings for faster processing
        square_img.save(
            output_path, 
            format='JPEG',
            quality=85,  # Reduced quality for faster processing
            optimize=False,  # Disable optimization for speed
            progressive=False
        )
        
        # Explicitly close images to prevent corruption
        img.close()
        square_img.close()
        
        # Verify the saved file exists and has content
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return True
        else:
            logging.error("Saved file is empty or doesn't exist")
            return False
            
    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        return False

@app.route('/')
def index():
    """Main page with upload form."""
    response = app.make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'public, max-age=300'  # 5 minute cache
    return response

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported. Please upload JPG or PNG files.'}), 400
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        if not file.filename:
            return jsonify({'error': 'Invalid filename'}), 400
            
        original_filename = secure_filename(file.filename)
        if not original_filename or '.' not in original_filename:
            return jsonify({'error': 'Invalid filename'}), 400
            
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        
        # Save uploaded file temporarily
        upload_filename = f"{file_id}.{file_extension}"
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_filename)
        file.save(upload_path)
        
        # Get processing parameters
        mode = request.form.get('mode', 'stretch')
        bg_color = request.form.get('bg_color', '#ffffff')
        blur_intensity = int(request.form.get('blur_intensity', 15))
        crop_data_str = request.form.get('crop_data')
        crop_data = None
        
        if crop_data_str:
            try:
                crop_data = json.loads(crop_data_str)
            except (json.JSONDecodeError, TypeError):
                crop_data = None
        
        # Process the image
        processed_filename = f"{file_id}_square.jpg"
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
        
        if process_image_to_square(upload_path, processed_path, mode=mode, bg_color=bg_color, blur_intensity=blur_intensity, crop_data=crop_data):
            # Keep original file for potential reprocessing
            return jsonify({
                'success': True,
                'file_id': file_id,
                'processed_filename': processed_filename,
                'original_filename': original_filename,
                'upload_filename': upload_filename
            })
        else:
            # Clean up on failure
            if os.path.exists(upload_path):
                os.remove(upload_path)
            return jsonify({'error': 'Failed to process image. Please try again.'}), 500
            
    except Exception as e:
        logging.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your image.'}), 500

@app.route('/reprocess', methods=['POST'])
def reprocess_image():
    """Reprocess an existing image with new parameters."""
    try:
        data = request.get_json()
        file_id = data.get('file_id')
        mode = data.get('mode', 'stretch')
        bg_color = data.get('bg_color', '#ffffff')
        blur_intensity = data.get('blur_intensity', 15)
        upload_filename = data.get('upload_filename')
        crop_data = data.get('crop_data')
        
        if not file_id or not upload_filename:
            return jsonify({'error': 'Missing file information'}), 400
        
        # Check if original file exists
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_filename)
        if not os.path.exists(upload_path):
            return jsonify({'error': 'Original file not found'}), 404
        
        # Process the image with new parameters
        processed_filename = f"{file_id}_square.jpg"
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
        
        if process_image_to_square(upload_path, processed_path, mode=mode, bg_color=bg_color, blur_intensity=blur_intensity, crop_data=crop_data):
            return jsonify({
                'success': True,
                'processed_filename': processed_filename
            })
        else:
            return jsonify({'error': 'Failed to reprocess image'}), 500
            
    except Exception as e:
        logging.error(f"Reprocess error: {str(e)}")
        return jsonify({'error': 'An error occurred while reprocessing your image.'}), 500

@app.route('/preview/<filename>')
def preview_image(filename):
    """Serve processed image for preview."""
    try:
        # Sanitize filename to prevent path traversal
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
            
        # Verify file is not empty
        if os.path.getsize(file_path) == 0:
            return jsonify({'error': 'File is corrupted'}), 500
        
        # Serve the image with proper headers
        response = send_file(file_path, mimetype='image/jpeg')
        response.headers['Content-Type'] = 'image/jpeg'
        response.headers['Cache-Control'] = 'public, max-age=300'  # Cache for 5 minutes
        
        return response
        
    except Exception as e:
        logging.error(f"Preview error: {str(e)}")
        return jsonify({'error': 'Error loading preview'}), 500

@app.route('/uploads/<filename>')
def serve_upload(filename):
    """Serve uploaded images for crop interface."""
    try:
        # Sanitize filename to prevent path traversal
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
            
        # Verify file is not empty
        if os.path.getsize(file_path) == 0:
            return jsonify({'error': 'File is corrupted'}), 500
        
        # Serve the image with proper headers
        response = send_file(file_path, mimetype='image/jpeg')
        response.headers['Cache-Control'] = 'public, max-age=300'  # Cache for 5 minutes
        
        return response
        
    except Exception as e:
        logging.error(f"Upload serve error: {str(e)}")
        return jsonify({'error': 'Error loading image'}), 500

@app.route('/download/<filename>')
def download_image(filename):
    """Download processed image."""
    try:
        # Sanitize filename to prevent path traversal
        filename = secure_filename(filename)
        file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
            
        # Verify file is not empty
        if os.path.getsize(file_path) == 0:
            return jsonify({'error': 'File is corrupted'}), 500
        
        # Create a clean filename for download
        clean_filename = f"whatsapp_profile_square.jpg"
        
        # Use send_file with proper headers for WhatsApp compatibility
        response = send_file(
            file_path,
            as_attachment=True,
            download_name=clean_filename,
            mimetype='image/jpeg'
        )
        
        # Add additional headers for better compatibility
        response.headers['Content-Type'] = 'image/jpeg'
        response.headers['Content-Disposition'] = f'attachment; filename="{clean_filename}"'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
        
    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        return jsonify({'error': 'Error downloading file'}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    return jsonify({'error': 'Internal server error. Please try again.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
