# WhatsApp Full DP - Flask Web Application

A modern Flask web application that allows users to create perfect WhatsApp profile pictures without cropping. The app offers 5 different processing styles to maintain the full image while fitting WhatsApp's square format requirements.

## Features

- **5 Processing Styles:**
  1. Set Full DP As It Is
  2. Centre Same Left Right Resize
  3. Left Right Same Centre Resize
  4. Set DP With Colors (custom background)
  5. Set DP With Blur (blurred background)

- **Modern UI:** Bootstrap-based responsive design with WhatsApp green theme
- **Fast Processing:** Optimized image processing with PIL/Pillow
- **Mobile Responsive:** Works perfectly on all devices
- **Navigation Pages:** Privacy Policy, Terms of Service, About Us, Contact Us, How It Works

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd whatsapp-full-dp
```

2. Install dependencies:
```bash
pip install -r requirements_export.txt
```

3. Run the application:
```bash
python main.py
```

The app will be available at `http://localhost:5000`

## Deployment

### For Render.com:
1. Connect your GitHub repository to Render
2. Set build command: `pip install -r requirements_export.txt`
3. Set start command: `gunicorn --bind 0.0.0.0:$PORT --reuse-port --reload main:app`
4. Environment: Python 3

### For Heroku:
1. Create a `Procfile` with: `web: gunicorn --bind 0.0.0.0:$PORT --reuse-port --reload main:app`
2. Push to Heroku

## File Structure

```
whatsapp-full-dp/
├── app.py                 # Main Flask application
├── main.py               # Application entry point
├── requirements_export.txt # Dependencies
├── templates/            # HTML templates
│   └── index.html       # Main template
├── static/              # Static files
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── images/         # Static images
├── uploads/            # User uploaded images (temporary)
└── processed/          # Processed images (temporary)
```

## Technical Details

- **Backend:** Flask with PIL/Pillow for image processing
- **Frontend:** Bootstrap 5 with custom CSS and JavaScript
- **Image Processing:** Multiple algorithms for different DP styles
- **File Handling:** Secure file upload with validation
- **Performance:** Optimized for fast processing

## License

All rights reserved. Made for perfect WhatsApp profile pictures.