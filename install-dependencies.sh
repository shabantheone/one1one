#!/bin/bash
# Complete dependency installation script for WhatsApp DP app
# Prevents wheel build errors by installing all necessary system libraries

echo "🔧 Installing system dependencies for image processing..."

# System packages (using available package manager)
if command -v apt-get &> /dev/null; then
    echo "Using apt-get package manager..."
    sudo apt-get update
    sudo apt-get install -y \
        build-essential \
        python3-dev \
        python3-pip \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libffi-dev \
        libssl-dev \
        zlib1g-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libwebp-dev \
        libharfbuzz-dev \
        libfribidi-dev \
        libxcb1-dev \
        pkg-config
elif command -v yum &> /dev/null; then
    echo "Using yum package manager..."
    sudo yum groupinstall -y "Development Tools"
    sudo yum install -y \
        python3-devel \
        libjpeg-turbo-devel \
        libpng-devel \
        libtiff-devel \
        libffi-devel \
        openssl-devel \
        zlib-devel \
        freetype-devel \
        lcms2-devel \
        libwebp-devel \
        pkgconfig
elif command -v nix-env &> /dev/null; then
    echo "Using Nix package manager (Replit environment)..."
    # Nix packages are already configured in the environment
    echo "Nix packages available through replit.nix configuration"
else
    echo "⚠️ Package manager not detected. Manual installation may be required."
fi

echo "🐍 Upgrading Python build tools..."
python -m pip install --upgrade pip setuptools wheel

echo "📦 Installing Python packages with pre-compiled wheels..."
python -m pip install --only-binary=all --no-cache-dir -r requirements-full.txt

echo "🧪 Testing installations..."
python -c "
import sys
print(f'Python version: {sys.version}')

try:
    import PIL
    print('✅ Pillow: OK')
except ImportError as e:
    print(f'❌ Pillow: {e}')

try:
    import numpy
    print(f'✅ NumPy: OK (version {numpy.__version__})')
except ImportError as e:
    print(f'❌ NumPy: {e}')

try:
    import flask
    print('✅ Flask: OK')
except ImportError as e:
    print(f'❌ Flask: {e}')

try:
    import wheel, setuptools, build
    print('✅ Build tools: OK')
except ImportError as e:
    print(f'❌ Build tools: {e}')
"

echo "✅ Dependency installation complete!"
echo "🚀 Ready to run WhatsApp DP application"