# Android Export Setup

This project now includes a base Android export preset in `export_presets.cfg`.
The repository also includes CI/CD support in `.github/workflows/`.

## Project-ready settings

- Base resolution: `1280x720`
- Stretch mode: `canvas_items`
- Aspect: `expand`
- Orientation: landscape in `project.godot`
- Android export path preset: `builds/android/FoodballGo.apk`
- Target architecture: `arm64-v8a`
- Android package name: `com.ferfranky.foodballgo`
- Version name preset: `1.0.8`
- Launcher app visibility: enabled
- Compile and target SDK: Android 16 / API 36

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
- Set **Target SDK** to `36`.
- internet permission enabled for rewarded AdMob ads

## Recommended first export

- Export format: APK
- Architecture: `arm64-v8a`
- Debug build first
- Test on a real landscape Android phone
- Validate the generated APK with `aapt dump badging`; it must report `targetSdkVersion:'36'`.

## CI/CD references

- CI/CD overview: [android_cicd.md](android_cicd.md)
- Permission posture: [android_permission_posture.md](android_permission_posture.md)
- Signing and secrets: [android_signing_and_release.md](android_signing_and_release.md)
- AdMob configuration: [admob_setup.md](admob_setup.md)
- Release smoke checklist: [android_release_checklist.md](android_release_checklist.md)

## Notes

- If the orientation is not respected, confirm it again in:
  - `Project Settings > Display > Window > Handheld > Orientation`
- If touch feels wrong on device, test with:
  - `Display > Window > Stretch > Aspect = expand`
  - UI safe margins in your scene layout
