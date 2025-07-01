#!/usr/bin/env python3
"""
Quick fix for wheel build errors in WhatsApp DP project
Focuses on the most common dependency issues
"""

import subprocess
import sys

def run_pip_install(packages, description):
    """Install packages with error handling"""
    print(f"Installing {description}...")
    
    cmd = [
        sys.executable, "-m", "pip", "install", "--upgrade",
        "--prefer-binary", "--no-cache-dir"
    ] + packages
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ {description} installed successfully")
            return True
        else:
            print(f"⚠️ {description} installation warning: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⚠️ {description} installation timed out, but may have succeeded")
        return True
    except Exception as e:
        print(f"❌ {description} installation failed: {e}")
        return False

def main():
    """Fix wheel build dependencies quickly"""
    print("🔧 Fixing wheel build errors for WhatsApp DP...")
    
    # Essential build tools - install first
    build_tools = ["pip", "setuptools", "wheel"]
    run_pip_install(build_tools, "build tools")
    
    # Core dependencies that commonly cause wheel issues
    core_deps = ["numpy", "Pillow"]
    run_pip_install(core_deps, "core image processing")
    
    # Flask dependencies
    flask_deps = ["Flask", "Werkzeug", "Gunicorn"]
    run_pip_install(flask_deps, "Flask web framework")
    
    # Test imports
    print("\n🧪 Testing critical imports...")
    
    test_modules = [
        ("PIL", "Pillow"),
        ("numpy", "NumPy"), 
        ("flask", "Flask")
    ]
    
    for module, name in test_modules:
        try:
            __import__(module)
            print(f"✅ {name}: Working")
        except ImportError:
            print(f"❌ {name}: Failed")
    
    print("\n✅ Wheel error fixes completed!")

if __name__ == "__main__":
    main()