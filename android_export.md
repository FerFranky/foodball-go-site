# Android Export Setup

This project now includes a base Android export preset in `export_presets.cfg`.

## Project-ready settings

- Base resolution: `1280x720`
- Stretch mode: `canvas_items`
- Aspect: `expand`
- Orientation: landscape in `project.godot`
- Android export path preset: `builds/android/FoodballGo.apk`
- Target architecture: `arm64-v8a`

## Still required in your local Godot editor

These values are machine-specific and should be configured on your PC:

1. Install Android export dependencies from Godot:
   - Android SDK
   - Android build template
   - JDK
2. Open:
   - `Editor > Editor Settings > Export > Android`
3. Set:
   - `adb`
   - `jarsigner`
   - `debug_keystore`
   - `android_sdk_path`
4. Open:
   - `Project > Export > Android`
5. Verify:
   - package name
   - version code
   - version name
   - permissions if later needed

## Recommended first export

- Export format: APK
- Architecture: `arm64-v8a`
- Debug build first
- Test on a real landscape Android phone

## Notes

- If the orientation is not respected, confirm it again in:
  - `Project Settings > Display > Window > Handheld > Orientation`
- If touch feels wrong on device, test with:
  - `Display > Window > Stretch > Aspect = expand`
  - UI safe margins in your scene layout
