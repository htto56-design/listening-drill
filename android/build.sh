#!/bin/bash
set -e
APP=/c/tmp/apk/v3/app
export JAVA_HOME='C:\tmp\android\jdk\jdk-17.0.13+11'
JAVAC=/c/tmp/android/jdk/jdk-17.0.13+11/bin/javac.exe
BT=/c/tmp/android/sdk/build-tools/34.0.0
PLAT=/c/tmp/android/sdk/platforms/android-34/android.jar
OUT="C:/刷题系统-连做版/听力刷题-连做版.apk"

cd "$APP"
rm -rf build
mkdir -p build/gen build/obj build/dex

echo "[1/6] aapt2 compile"
"$BT/aapt2.exe" compile --dir res -o build/res.zip

echo "[2/6] aapt2 link"
"$BT/aapt2.exe" link -o build/app.ap_ -I "$PLAT" --manifest AndroidManifest.xml \
  -R build/res.zip --java build/gen --auto-add-overlay -A assets

echo "[3/6] javac"
"$JAVAC" -nowarn -source 8 -target 8 -encoding UTF-8 -bootclasspath "$PLAT" \
  -d build/obj build/gen/com/listen/drill/v3/R.java src/com/listen/drill/v3/MainActivity.java

echo "[4/6] d8"
"$BT/d8.bat" --lib "$PLAT" --min-api 21 --output build/dex $(find build/obj -name "*.class" | tr '\n' ' ')

echo "[5/6] zip + zipalign"
python - <<'PY'
import zipfile, shutil
shutil.copy('build/app.ap_', 'build/unsigned.apk')
with zipfile.ZipFile('build/unsigned.apk', 'a', zipfile.ZIP_DEFLATED) as z:
    z.write('build/dex/classes.dex', 'classes.dex')
print('entries:', len(zipfile.ZipFile('build/unsigned.apk').namelist()))
PY
"$BT/zipalign.exe" -f 4 build/unsigned.apk build/aligned.apk

echo "[6/6] apksigner"
"$BT/apksigner.bat" sign --ks debug.keystore --ks-pass pass:android --key-pass pass:android \
  --out "$OUT" build/aligned.apk

"$BT/apksigner.bat" verify --print-certs "$OUT" | head -3
echo done
