# AdMob rewarded ads

Foodball Go includes Android rewarded ads for the `Ver anuncio x2` action. The player receives the coin bonus only after the Google Mobile Ads SDK confirms the reward callback.

## Development and QA

`debug` and `dev` builds are hard-wired to Google's official rewarded test ad unit. Do not replace it and do not click live production ads while testing.

The Android package is `com.ferfranky.foodballgo`. An Android build needs internet access; no storage or runtime permission is requested by this integration.

## Production registration

1. Create or access the Google AdMob account that owns Foodball Go.
2. Register an Android app with the package ID `com.ferfranky.foodballgo`.
3. Create a **Rewarded** ad unit for that app.
4. Copy `android/admob.properties.example` to `android/admob.properties`.
5. Replace the values in `android/admob.properties` with the **AdMob App ID** and the **Rewarded Ad Unit ID** from the AdMob console.
6. Build a signed `release` APK or AAB. Only the release variant reads those production IDs.

`android/admob.properties` is ignored by Git. The two IDs are client identifiers, not secrets, but keeping them local prevents accidentally publishing an unfinished production configuration. Never add a Google account password, service account JSON, private key, or Play signing key to this file or to the repository.

Before release, publish the privacy policy URL in AdMob/Play Console and configure Google UMP consent messaging for the countries where it applies. Payment and account verification are completed inside AdMob and are not part of the app build.

## Verification

1. Install a debug APK on Android.
2. Finish a match and tap `COBRAR BONUS X2`.
3. Confirm a test ad appears.
4. Complete it and confirm the coin balance increases once.
5. Close or fail an ad and confirm the balance does not change and the player can retry or continue.
