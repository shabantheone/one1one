// WhatsApp DP Resizer with Android/Capacitor Support
// Complete Canvas-based image processing with native mobile features

// Import Capacitor plugins (when available)
let Camera, Filesystem, Share;
if (window.Capacitor) {
    import('@capacitor/camera').then(module => { Camera = module.Camera; });
    import('@capacitor/filesystem').then(module => { Filesystem = module.Filesystem; });
    import('@capacitor/share').then(module => { Share = module.Share; });
}

// Content definitions for navigation sections
const sectionContent = {
    privacy: `
        <h2 class="text-success mb-4">Privacy Policy</h2>
        <p class="text-muted small">Last Updated: 15 June 2025</p>
        
        <p>Welcome to WhatsApp Full DP ("we", "our", or "us"). Your privacy is important to us. This Privacy Policy explains how we collect, use, and protect your information when you use our web application.</p>
        
        <h4 class="text-success mt-4">1. Information We Collect</h4>
        <p>We do not collect any personal data such as name, address, or phone number.</p>
        <p>Images are processed entirely in your browser and never leave your device.</p>
        <p>We do not store or share your images on any servers. All processing is done locally.</p>
        
        <h4 class="text-success mt-4">2. Use of Information</h4>
        <p>Your uploaded images are only processed locally in your browser to generate WhatsApp DP.</p>
        <p>We do not use your images for any other purpose.</p>
        
        <h4 class="text-success mt-4">3. Data Processing</h4>
        <p>All image processing happens directly in your browser using HTML5 Canvas.</p>
        <p>No data is transmitted to external servers during processing.</p>
        
        <h4 class="text-success mt-4">4. Contact Us</h4>
        <p>If you have any questions about this Privacy Policy, you can email us at:</p>
        <p><strong>📧 itstheone786@gmail.com</strong></p>
    `,
    
    about: `
        <h2 class="text-success mb-4">About WhatsApp Full DP</h2>
        
        <p>At WhatsApp Full DP, our goal is simple — we help you upload your full-size photo as your WhatsApp DP without any cropping, compression, or unwanted borders. We know how frustrating it is when a beautiful photo gets cut off — that's why we built this simple and fast tool.</p>
        
        <p>Our frontend-only solution processes everything directly in your browser, ensuring your photos never leave your device for maximum privacy and security.</p>
        
        <p>No filters, no ads, no nonsense. Just your photo — exactly the way you want it.</p>
        
        <p>Whether it's a group photo, a scenic view, or a solo portrait — upload it, and we'll make sure it fits perfectly as your DP.</p>
        
        <p><strong>Thank you for using WhatsApp Full DP!</strong></p>
    `,
    
    contact: `
        <h2 class="text-success mb-4">Contact Us</h2>
        
        <p>If you have any feedback, questions, or suggestions, feel free to reach out to us.</p>
        
        <p><strong>Email:</strong> itstheone786@gmail.com</p>
        
        <p>We usually respond within 24–48 hours.</p>
    `,
    
    terms: `
        <h2 class="text-success mb-4">Terms of Service</h2>
        <p class="text-muted small">Last Updated: 15 June 2025</p>
        
        <p>Welcome to WhatsApp Full DP. By accessing or using our web application, you agree to comply with and be bound by the following terms:</p>
        
        <h4 class="text-success mt-4">1. Use of Service</h4>
        <p>You may use our service only for lawful purposes and in accordance with these Terms.</p>
        <p>You agree not to use the service to upload any content that is unlawful, harmful, offensive, or infringes on anyone's rights.</p>
        
        <h4 class="text-success mt-4">2. Image Processing</h4>
        <p>Our service processes photos entirely in your browser to resize and fit as full WhatsApp profile pictures.</p>
        <p>We do not store or share your uploaded images. All images are processed locally in your device.</p>
        
        <h4 class="text-success mt-4">3. Intellectual Property</h4>
        <p>All content, trademarks, and intellectual property related to WhatsApp Full DP are owned by us or our licensors.</p>
        
        <h4 class="text-success mt-4">4. Disclaimer</h4>
        <p>The service is provided "as is" without warranties of any kind. We do not guarantee that the service will be error-free or uninterrupted.</p>
        
        <h4 class="text-success mt-4">5. Contact Us</h4>
        <p>If you have questions about these Terms, please email us at:</p>
        <p><strong>📧 itstheone786@gmail.com</strong></p>
    `,
    
    howItWorks: `
        <h2 class="text-success mb-4">How It Works — WhatsApp Full DP</h2>
        
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="d-flex align-items-start">
                    <div class="bg-success text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px; min-width: 40px;">
                        <strong>1</strong>
                    </div>
                    <div>
                        <h5 class="text-success">Select Your Photo</h5>
                        <p>Click on the upload button to choose the photo you want to use as your WhatsApp profile picture. Works on all devices including mobile phones.</p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6 mb-4">
                <div class="d-flex align-items-start">
                    <div class="bg-success text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px; min-width: 40px;">
                        <strong>2</strong>
                    </div>
                    <div>
                        <h5 class="text-success">Choose the Style</h5>
                        <p>Select from 5 different processing styles that maintain your full picture without cropping. Each style offers a unique way to fit your image.</p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6 mb-4">
                <div class="d-flex align-items-start">
                    <div class="bg-success text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px; min-width: 40px;">
                        <strong>3</strong>
                    </div>
                    <div>
                        <h5 class="text-success">Instant Processing</h5>
                        <p>Your photo is processed instantly in your browser. No uploads to servers - everything happens on your device for maximum privacy.</p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6 mb-4">
                <div class="d-flex align-items-start">
                    <div class="bg-success text-white rounded-circle d-flex align-items-center justify-content-center me-3" style="width: 40px; height: 40px; min-width: 40px;">
                        <strong>4</strong>
                    </div>
                    <div>
                        <h5 class="text-success">Download and Use</h5>
                        <p>Download the processed photo directly to your device and set it as your WhatsApp DP. Perfect quality, no cropping!</p>
                    </div>
                </div>
            </div>
        </div>
    `
};

// Navigation functions
function showSection(sectionId) {
    const mainContent = document.getElementById('main-content');
    const dynamicContent = document.getElementById('dynamic-content');
    const contentArea = document.getElementById('content-area');
    
    if (sectionContent[sectionId]) {
        mainContent.classList.add('d-none');
        dynamicContent.classList.remove('d-none');
        contentArea.innerHTML = sectionContent[sectionId];
        window.scrollTo(0, 0);
    }
}

function showHome() {
    const mainContent = document.getElementById('main-content');
    const dynamicContent = document.getElementById('dynamic-content');
    
    dynamicContent.classList.add('d-none');
    mainContent.classList.remove('d-none');
    window.scrollTo(0, 0);
}

// Main Image Processor Class
class WhatsAppDPProcessor {
    constructor() {
        this.selectedOption = null;
        this.selectedColor = '#ffffff';
        this.blurIntensity = 15;
        this.currentImage = null;
        this.originalImageData = null;
        
        this.initializeEventListeners();
        this.setupDragAndDrop();
    }

    initializeEventListeners() {
        // File input handler with mobile support
        const fileInput = document.getElementById('file-input');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
            
            // Prevent default click behavior to avoid double triggers
            fileInput.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        }

        // Upload area click handler for mobile compatibility
        const uploadArea = document.getElementById('upload-area');
        if (uploadArea) {
            uploadArea.addEventListener('click', (e) => {
                if (e.target === uploadArea || e.target.closest('.upload-content')) {
                    fileInput.click();
                }
            });
        }

        // Checkbox selection handlers
        document.querySelectorAll('.option-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => this.handleCheckboxChange(e.target));
        });

        // Color selection handlers
        document.querySelectorAll('.color-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.selectColor(e.currentTarget.dataset.color));
        });

        // Blur slider handler
        const blurSlider = document.getElementById('blur-slider');
        if (blurSlider) {
            blurSlider.addEventListener('input', (e) => {
                this.blurIntensity = parseInt(e.target.value);
                if (this.currentImage && this.selectedOption === 'set-blur') {
                    this.processImage();
                }
            });
        }
    }

    setupDragAndDrop() {
        const uploadArea = document.getElementById('upload-area');
        if (!uploadArea) return;

        // Desktop drag and drop support
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, this.preventDefaults, false);
            document.body.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('drag-over');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('drag-over');
            }, false);
        });

        uploadArea.addEventListener('drop', (e) => this.handleDrop(e), false);

        // Mobile touch support
        uploadArea.addEventListener('touchstart', (e) => {
            uploadArea.classList.add('touch-active');
        });

        uploadArea.addEventListener('touchend', (e) => {
            uploadArea.classList.remove('touch-active');
        });
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleCheckboxChange(checkbox) {
        // Uncheck all other checkboxes
        document.querySelectorAll('.option-checkbox').forEach(cb => {
            if (cb !== checkbox) {
                cb.checked = false;
            }
        });

        // Set selected option
        if (checkbox.checked) {
            this.selectedOption = checkbox.closest('.option-line').dataset.option;
        } else {
            this.selectedOption = null;
        }

        this.updateColorOptionsVisibility();
        
        // Process image if one is loaded
        if (this.currentImage) {
            this.processImage();
        }
    }

    selectColor(color) {
        this.selectedColor = color;
        
        // Update visual selection
        document.querySelectorAll('.color-btn').forEach(btn => {
            btn.classList.remove('selected');
        });
        document.querySelector(`[data-color="${color}"]`).classList.add('selected');
        
        // Process image if it's color mode
        if (this.currentImage && this.selectedOption === 'crop-colors') {
            this.processImage();
        }
    }

    updateColorOptionsVisibility() {
        const colorOptions = document.querySelector('.color-options');
        const blurOptions = document.querySelector('.blur-options');
        
        if (colorOptions) {
            colorOptions.style.display = this.selectedOption === 'crop-colors' ? 'block' : 'none';
        }
        
        if (blurOptions) {
            blurOptions.style.display = this.selectedOption === 'set-blur' ? 'block' : 'none';
        }
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }

    processFile(file) {
        // Validate file type
        if (!this.isValidFileType(file)) {
            this.showError('Please select a JPG or PNG file.');
            return;
        }

        // Validate file size (16MB)
        if (file.size > 16 * 1024 * 1024) {
            this.showError('File size must be less than 16MB.');
            return;
        }

        // Show processing state
        this.showUploadProcessing();
        this.showProgress();

        // Load image
        const reader = new FileReader();
        reader.onload = (e) => {
            this.loadImage(e.target.result);
        };
        reader.readAsDataURL(file);
    }

    isValidFileType(file) {
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        return allowedTypes.includes(file.type);
    }

    loadImage(src) {
        const img = new Image();
        img.onload = () => {
            this.currentImage = img;
            this.showOriginalPreview(img);
            this.hideProgress();
            
            if (this.selectedOption) {
                this.processImage();
            } else {
                this.showError('Please select a processing style first.');
            }
        };
        img.onerror = () => {
            this.showError('Failed to load image. Please try a different file.');
            this.hideProgress();
        };
        img.src = src;
    }

    showOriginalPreview(img) {
        const originalPreview = document.getElementById('original-preview');
        if (originalPreview) {
            originalPreview.src = img.src;
        }
        
        const previewSection = document.getElementById('preview-section');
        if (previewSection) {
            previewSection.classList.remove('d-none');
        }
    }

    processImage() {
        if (!this.currentImage || !this.selectedOption) return;

        const canvas = document.getElementById('processed-canvas');
        const ctx = canvas.getContext('2d');
        
        // Set canvas size to WhatsApp DP size
        const size = 640;
        canvas.width = size;
        canvas.height = size;

        // Process based on selected option
        switch (this.selectedOption) {
            case 'full-resize':
                this.processFullResize(ctx, size);
                break;
            case 'center-left-right':
                this.processCenterLeftRight(ctx, size);
                break;
            case 'left-right-center':
                this.processLeftRightCenter(ctx, size);
                break;
            case 'crop-colors':
                this.processWithColors(ctx, size);
                break;
            case 'set-blur':
                this.processWithBlur(ctx, size);
                break;
        }
    }

    processFullResize(ctx, size) {
        // Stretch image to fill entire square
        ctx.drawImage(this.currentImage, 0, 0, size, size);
    }

    processCenterLeftRight(ctx, size) {
        // Center Same Left Right Resize: Keep 90% center, stretch 5% left and 5% right
        const img = this.currentImage;
        const imgWidth = img.width;
        const imgHeight = img.height;
        
        // Scale to fit height
        const scaleFactor = size / imgHeight;
        const scaledWidth = imgWidth * scaleFactor;
        
        if (scaledWidth <= size) {
            // If scaled image fits, center it with stretched edges
            const centerWidth = Math.floor(scaledWidth * 0.9);
            const edgeWidth = Math.floor((size - centerWidth) / 2);
            
            // Draw left edge (stretched)
            const leftEdgeSourceWidth = Math.floor(imgWidth * 0.05);
            ctx.drawImage(img, 0, 0, leftEdgeSourceWidth, imgHeight, 0, 0, edgeWidth, size);
            
            // Draw center (normal)
            const centerSourceWidth = Math.floor(imgWidth * 0.9);
            const centerSourceStart = leftEdgeSourceWidth;
            ctx.drawImage(img, centerSourceStart, 0, centerSourceWidth, imgHeight, edgeWidth, 0, centerWidth, size);
            
            // Draw right edge (stretched)
            const rightEdgeSourceWidth = imgWidth - centerSourceStart - centerSourceWidth;
            const rightEdgeSourceStart = centerSourceStart + centerSourceWidth;
            ctx.drawImage(img, rightEdgeSourceStart, 0, rightEdgeSourceWidth, imgHeight, edgeWidth + centerWidth, 0, edgeWidth, size);
        } else {
            // If too wide, crop and apply the same logic
            const cropWidth = size / scaleFactor;
            const cropStart = (imgWidth - cropWidth) / 2;
            
            const leftEdgeWidth = Math.floor(size * 0.05);
            const centerWidth = Math.floor(size * 0.9);
            const rightEdgeWidth = size - leftEdgeWidth - centerWidth;
            
            // Draw left edge
            ctx.drawImage(img, cropStart, 0, cropWidth * 0.05, imgHeight, 0, 0, leftEdgeWidth, size);
            
            // Draw center
            ctx.drawImage(img, cropStart + cropWidth * 0.05, 0, cropWidth * 0.9, imgHeight, leftEdgeWidth, 0, centerWidth, size);
            
            // Draw right edge
            ctx.drawImage(img, cropStart + cropWidth * 0.95, 0, cropWidth * 0.05, imgHeight, leftEdgeWidth + centerWidth, 0, rightEdgeWidth, size);
        }
    }

    processLeftRightCenter(ctx, size) {
        // Left Right Same Centre Resize: Keep 90% sides, stretch 10% center
        const img = this.currentImage;
        const imgWidth = img.width;
        const imgHeight = img.height;
        
        // Scale to fit height
        const scaleFactor = size / imgHeight;
        const scaledWidth = imgWidth * scaleFactor;
        
        if (scaledWidth <= size) {
            // If scaled image fits, stretch center to fill
            const sideWidth = Math.floor(scaledWidth * 0.45); // 45% each side
            const centerWidth = size - (sideWidth * 2);
            
            // Draw left side
            const leftSourceWidth = Math.floor(imgWidth * 0.45);
            ctx.drawImage(img, 0, 0, leftSourceWidth, imgHeight, 0, 0, sideWidth, size);
            
            // Draw center (stretched)
            const centerSourceWidth = Math.floor(imgWidth * 0.1);
            const centerSourceStart = leftSourceWidth;
            ctx.drawImage(img, centerSourceStart, 0, centerSourceWidth, imgHeight, sideWidth, 0, centerWidth, size);
            
            // Draw right side
            const rightSourceWidth = imgWidth - centerSourceStart - centerSourceWidth;
            const rightSourceStart = centerSourceStart + centerSourceWidth;
            ctx.drawImage(img, rightSourceStart, 0, rightSourceWidth, imgHeight, sideWidth + centerWidth, 0, sideWidth, size);
        } else {
            // If too wide, crop and apply the same logic
            const cropWidth = size / scaleFactor;
            const cropStart = (imgWidth - cropWidth) / 2;
            
            const sideWidth = Math.floor(size * 0.45);
            const centerWidth = size - (sideWidth * 2);
            
            // Draw left side
            ctx.drawImage(img, cropStart, 0, cropWidth * 0.45, imgHeight, 0, 0, sideWidth, size);
            
            // Draw center (stretched)
            ctx.drawImage(img, cropStart + cropWidth * 0.45, 0, cropWidth * 0.1, imgHeight, sideWidth, 0, centerWidth, size);
            
            // Draw right side
            ctx.drawImage(img, cropStart + cropWidth * 0.55, 0, cropWidth * 0.45, imgHeight, sideWidth + centerWidth, 0, sideWidth, size);
        }
    }

    processWithColors(ctx, size) {
        // Fit image with colored background
        const img = this.currentImage;
        const imgWidth = img.width;
        const imgHeight = img.height;
        
        // Fill background with selected color
        ctx.fillStyle = this.selectedColor;
        ctx.fillRect(0, 0, size, size);
        
        // Calculate scale to fit image
        const scale = Math.min(size / imgWidth, size / imgHeight);
        const newWidth = imgWidth * scale;
        const newHeight = imgHeight * scale;
        
        // Center the image
        const x = (size - newWidth) / 2;
        const y = (size - newHeight) / 2;
        
        ctx.drawImage(img, x, y, newWidth, newHeight);
    }

    processWithBlur(ctx, size) {
        // Create blurred background with sharp image on top
        const img = this.currentImage;
        const imgWidth = img.width;
        const imgHeight = img.height;
        
        // Draw blurred background (stretched to fill)
        ctx.filter = `blur(${this.blurIntensity}px)`;
        ctx.drawImage(img, 0, 0, size, size);
        
        // Reset filter and draw sharp image on top
        ctx.filter = 'none';
        
        // Calculate scale to fit image
        const scale = Math.min(size / imgWidth, size / imgHeight);
        const newWidth = imgWidth * scale;
        const newHeight = imgHeight * scale;
        
        // Center the sharp image
        const x = (size - newWidth) / 2;
        const y = (size - newHeight) / 2;
        
        ctx.drawImage(img, x, y, newWidth, newHeight);
    }

    async downloadImage() {
        const canvas = document.getElementById('processed-canvas');
        if (!canvas) return;
        
        const dataUrl = canvas.toDataURL('image/jpeg', 0.9);
        
        // Android/Capacitor download
        if (window.Capacitor && Filesystem) {
            try {
                const base64Data = dataUrl.split(',')[1];
                const fileName = `whatsapp-dp-${Date.now()}.jpg`;
                
                const result = await Filesystem.writeFile({
                    path: fileName,
                    data: base64Data,
                    directory: 'DOCUMENTS'
                });
                
                this.showSuccess(`Image saved to Documents/${fileName}`);
                
                // Optional: Share the image
                if (Share) {
                    await Share.share({
                        title: 'WhatsApp DP Generated',
                        text: 'Check out my new WhatsApp profile picture!',
                        url: result.uri
                    });
                }
                
                return;
            } catch (error) {
                console.error('Capacitor download failed:', error);
                // Fall back to web download
            }
        }
        
        // Web download fallback
        const link = document.createElement('a');
        link.download = 'whatsapp-dp.jpg';
        link.href = dataUrl;
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    async openCameraOrGallery() {
        if (window.Capacitor && Camera) {
            try {
                const options = {
                    quality: 90,
                    allowEditing: false,
                    resultType: 'DataUrl',
                    source: 'PROMPT' // Asks user to choose camera or gallery
                };
                
                const image = await Camera.getPhoto(options);
                this.loadImageFromDataUrl(image.dataUrl);
                
            } catch (error) {
                console.error('Camera/Gallery error:', error);
                this.showError('Could not access camera or gallery. Please try the file picker.');
            }
        } else {
            // Web fallback - trigger file input
            document.getElementById('file-input').click();
        }
    }

    loadImageFromDataUrl(dataUrl) {
        const img = new Image();
        img.onload = () => {
            this.currentImage = img;
            this.showOriginalPreview(img);
            this.hideProgress();
            
            if (this.selectedOption) {
                this.processImage();
            } else {
                this.showError('Please select a processing style first.');
            }
        };
        img.onerror = () => {
            this.showError('Failed to load image from camera.');
            this.hideProgress();
        };
        img.src = dataUrl;
    }

    showSuccess(message) {
        // Create or update success alert
        let successAlert = document.getElementById('success-alert');
        if (!successAlert) {
            successAlert = document.createElement('div');
            successAlert.id = 'success-alert';
            successAlert.className = 'alert alert-success mt-3';
            successAlert.innerHTML = '<i class="fas fa-check-circle me-2"></i><span id="success-message"></span>';
            
            const errorAlert = document.getElementById('error-alert');
            if (errorAlert) {
                errorAlert.parentNode.insertBefore(successAlert, errorAlert);
            }
        }
        
        const successMessage = document.getElementById('success-message');
        if (successMessage) {
            successMessage.textContent = message;
            successAlert.classList.remove('d-none');
            
            // Auto-hide after 3 seconds
            setTimeout(() => {
                successAlert.classList.add('d-none');
            }, 3000);
        }
    }

    showUploadProcessing() {
        const uploadProcessing = document.getElementById('upload-processing');
        const uploadArea = document.getElementById('upload-area');
        
        if (uploadProcessing && uploadArea) {
            uploadProcessing.classList.remove('d-none');
            uploadArea.style.display = 'none';
        }
    }

    showProgress() {
        const progressContainer = document.getElementById('progress-container');
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        
        if (progressContainer) {
            progressContainer.classList.remove('d-none');
            
            // Simulate progress
            let progress = 0;
            const interval = setInterval(() => {
                progress += 20;
                if (progressBar) progressBar.style.width = progress + '%';
                if (progressText) progressText.textContent = progress + '%';
                
                if (progress >= 100) {
                    clearInterval(interval);
                    setTimeout(() => this.hideProgress(), 300);
                }
            }, 100);
        }
    }

    hideProgress() {
        const progressContainer = document.getElementById('progress-container');
        if (progressContainer) {
            progressContainer.classList.add('d-none');
        }
    }

    showError(message) {
        const errorAlert = document.getElementById('error-alert');
        const errorMessage = document.getElementById('error-message');
        
        if (errorAlert && errorMessage) {
            errorMessage.textContent = message;
            errorAlert.classList.remove('d-none');
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                errorAlert.classList.add('d-none');
            }, 5000);
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.processor = new WhatsAppDPProcessor();
});

// Initialize Capacitor when available
if (window.Capacitor) {
    window.Capacitor.Plugins.StatusBar?.setStyle({ style: 'DARK' });
    window.Capacitor.Plugins.StatusBar?.setBackgroundColor({ color: '#25D366' });
}

// Global download function
function downloadImage() {
    const canvas = document.getElementById('processed-canvas');
    if (!canvas) return;
    
    const link = document.createElement('a');
    link.download = 'whatsapp-dp.jpg';
    link.href = canvas.toDataURL('image/jpeg', 0.9);
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}