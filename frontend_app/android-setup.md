# Android App Setup Guide

## Prerequisites
- Node.js 16+ installed
- Android Studio installed
- Java 11+ installed
- Android SDK installed

## Setup Steps

### 1. Install Dependencies
```bash
npm install
```

### 2. Add Android Platform
```bash
npx cap add android
```

### 3. Sync Web Code
```bash
npx cap sync
```

### 4. Open in Android Studio
```bash
npx cap open android
```

## Android Studio Configuration

### Required Permissions (automatically added):
- `android.permission.CAMERA`
- `android.permission.READ_EXTERNAL_STORAGE` 
- `android.permission.WRITE_EXTERNAL_STORAGE`
- `android.permission.ACCESS_MEDIA_LOCATION`

### Build Configuration:
- **Target SDK**: 34
- **Min SDK**: 24
- **Compile SDK**: 34

### Gradle Dependencies (auto-configured):
- Capacitor Core
- Capacitor Camera
- Capacitor Filesystem
- Capacitor Share

## Testing

### Development Mode:
```bash
npm run android:dev
```

### Production Build:
```bash
npm run android:build
```

## APK Generation

1. Open Android Studio
2. Go to **Build > Generate Signed Bundle/APK**
3. Choose **APK** 
4. Create/select keystore
5. Build APK

## AAB Generation (Google Play)

1. Open Android Studio
2. Go to **Build > Generate Signed Bundle/AAB**
3. Choose **Android App Bundle**
4. Create/select keystore
5. Build AAB for Play Store

## Features Enabled

✅ **Camera Integration**: Direct camera access
✅ **Gallery Access**: Photo library access  
✅ **File Downloads**: Save processed images
✅ **Share Functionality**: Share processed images
✅ **Offline Support**: Works without internet
✅ **Native Performance**: Optimized for mobile

## Troubleshooting

### File Picker Not Visible:
- Ensure permissions are granted
- Check Android version compatibility
- Verify WebView is updated

### Camera Not Working:
- Grant camera permissions
- Test on physical device (not emulator)
- Check AndroidManifest.xml permissions

### Build Errors:
- Update Android Studio
- Sync project with Gradle files
- Clean and rebuild project