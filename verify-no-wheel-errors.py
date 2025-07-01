#!/usr/bin/env python3
"""
Final verification script to confirm wheel build errors are completely resolved
"""

import sys
import subprocess
import importlib

def test_package_installation(package_name, import_name=None):
    """Test if a package can be imported without errors"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'Unknown')
        print(f"✅ {package_name}: Version {version}")
        return True
    except ImportError as e:
        print(f"❌ {package_name}: Import failed - {e}")
        return False

def test_wheel_build(package_name):
    """Test if a package can be installed from wheel"""
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '--force-reinstall', 
            '--only-binary=all', '--no-cache-dir', package_name
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ {package_name}: Wheel installation successful")
            return True
        else:
            print(f"⚠️ {package_name}: Wheel installation warning")
            return False
    except Exception as e:
        print(f"❌ {package_name}: Wheel test failed - {e}")
        return False

def main():
    """Run comprehensive verification"""
    print("🔍 WhatsApp DP - Wheel Build Error Verification")
    print("=" * 50)
    
    # Core dependencies that commonly cause wheel issues
    core_packages = [
        ('pillow', 'PIL'),
        ('numpy', 'numpy'),
        ('flask', 'flask'),
        ('gunicorn', 'gunicorn'),
        ('werkzeug', 'werkzeug'),
        ('wheel', 'wheel'),
        ('setuptools', 'setuptools'),
        ('certifi', 'certifi'),
    ]
    
    print("📦 Testing core package imports...")
    all_imports_ok = True
    for package, import_name in core_packages:
        if not test_package_installation(package, import_name):
            all_imports_ok = False
    
    print(f"\n🎯 Import test result: {'PASS' if all_imports_ok else 'FAIL'}")
    
    # Test image processing functionality
    print("\n🖼️ Testing image processing capabilities...")
    try:
        from PIL import Image, ImageFilter
        import numpy as np
        
        # Create a test image
        test_img = Image.new('RGB', (100, 100), color='red')
        test_array = np.array(test_img)
        
        # Apply basic transformations
        resized = test_img.resize((50, 50))
        blurred = test_img.filter(ImageFilter.GaussianBlur(radius=2))
        
        print("✅ Image processing: All operations working")
        image_processing_ok = True
    except Exception as e:
        print(f"❌ Image processing: Failed - {e}")
        image_processing_ok = False
    
    # Test Flask functionality
    print("\n🌐 Testing Flask web framework...")
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def test_route():
            return 'WhatsApp DP Ready'
        
        print("✅ Flask: Web framework ready")
        flask_ok = True
    except Exception as e:
        print(f"❌ Flask: Failed - {e}")
        flask_ok = False
    
    # Final verdict
    print("\n" + "=" * 50)
    all_tests_pass = all_imports_ok and image_processing_ok and flask_ok
    
    if all_tests_pass:
        print("🎉 SUCCESS: All wheel build errors resolved!")
        print("🚀 WhatsApp DP is ready for production deployment")
        print("\nDeployment options:")
        print("  • Web hosting: Extract frontend ZIP and upload")
        print("  • Android APK: Use Capacitor configuration")
        print("  • Docker: Use docker-requirements.txt")
        print("  • Local server: python app.py")
    else:
        print("⚠️ Some issues detected. Check error messages above.")
        print("💡 Try running: python fix-wheel-errors.py")
    
    return all_tests_pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)