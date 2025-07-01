#!/usr/bin/env python3
"""
Environment setup script for WhatsApp DP application
Handles wheel build issues and dependency conflicts
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors gracefully"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"⚠️ {description} - Warning: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python version compatible")
        return True
    else:
        print("❌ Python 3.8+ required for optimal wheel support")
        return False

def install_build_dependencies():
    """Install essential build dependencies"""
    
    # Core build tools
    core_packages = [
        "pip>=23.0",
        "setuptools>=65.0", 
        "wheel>=0.38.0",
        "build>=0.10.0",
        "cython>=0.29.0"
    ]
    
    print("📦 Installing core build tools...")
    for package in core_packages:
        run_command(f"python -m pip install --upgrade '{package}'", f"Installing {package}")
    
    # Image processing packages with specific versions known to have wheels
    image_packages = [
        "Pillow>=9.0.0,<11.0.0",  # Version range with reliable wheels
        "numpy>=1.21.0,<2.0.0",   # Stable numpy version
    ]
    
    print("🖼️ Installing image processing packages...")
    for package in image_packages:
        # Try to install pre-compiled wheels first
        success = run_command(
            f"python -m pip install --only-binary=all --no-cache-dir '{package}'",
            f"Installing {package} (wheel only)"
        )
        
        if not success:
            print(f"⚠️ Wheel not available for {package}, trying source build...")
            run_command(
                f"python -m pip install --no-cache-dir '{package}'",
                f"Installing {package} (from source)"
            )

def install_flask_dependencies():
    """Install Flask and web dependencies"""
    
    flask_packages = [
        "Flask>=2.3.0,<3.0.0",
        "Werkzeug>=2.3.0,<3.0.0", 
        "Gunicorn>=20.0.0",
        "flask-cors>=4.0.0"
    ]
    
    print("🌐 Installing Flask dependencies...")
    for package in flask_packages:
        run_command(
            f"python -m pip install --prefer-binary '{package}'",
            f"Installing {package}"
        )

def verify_installations():
    """Verify all critical packages are working"""
    
    test_imports = [
        ("PIL", "Pillow image processing"),
        ("numpy", "NumPy array processing"),
        ("flask", "Flask web framework"),
        ("wheel", "Wheel packaging"),
        ("setuptools", "Python packaging tools"),
        ("build", "Build system")
    ]
    
    print("🧪 Verifying installations...")
    all_success = True
    
    for module, description in test_imports:
        try:
            __import__(module)
            print(f"✅ {description}: OK")
        except ImportError as e:
            print(f"❌ {description}: Failed - {e}")
            all_success = False
    
    return all_success

def create_pip_conf():
    """Create pip configuration to prefer wheels"""
    
    pip_conf_content = """[global]
prefer-binary = true
only-binary = :all:
no-cache-dir = true
timeout = 300

[install]
find-links = https://download.pytorch.org/whl/cpu
trusted-host = pypi.org
               pypi.python.org
               files.pythonhosted.org
               download.pytorch.org
"""
    
    # Create pip config directory
    if platform.system() == "Windows":
        config_dir = os.path.expanduser("~/pip")
        config_file = os.path.join(config_dir, "pip.ini")
    else:
        config_dir = os.path.expanduser("~/.config/pip")
        config_file = os.path.join(config_dir, "pip.conf")
    
    try:
        os.makedirs(config_dir, exist_ok=True)
        with open(config_file, 'w') as f:
            f.write(pip_conf_content)
        print(f"✅ Created pip configuration: {config_file}")
    except Exception as e:
        print(f"⚠️ Could not create pip config: {e}")

def main():
    """Main setup function"""
    print("🚀 WhatsApp DP Environment Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        print("❌ Setup aborted due to Python version incompatibility")
        return False
    
    # Create pip configuration for better wheel handling
    create_pip_conf()
    
    # Install dependencies in order
    install_build_dependencies()
    install_flask_dependencies()
    
    # Verify everything works
    if verify_installations():
        print("\n✅ Environment setup complete!")
        print("🚀 Ready to run WhatsApp DP application")
        return True
    else:
        print("\n❌ Some packages failed to install")
        print("💡 Try running the script again or check system dependencies")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)