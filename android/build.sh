#!/bin/bash
# 手工打包 apk（不依赖 Gradle）。
# 依赖：JDK 17+、Android SDK（build-tools 34.0.0、platform 34）、python
#
#   export ANDROID_SDK=/path/to/android-sdk
#   bash build.sh
#
# 产物默认输出到仓库根目录的 听力刷题-连做版.apk，可用 OUT 覆盖。
set -e

APP="$(cd "$(dirname "$0")" && pwd)"
: "${ANDROID_SDK:?请先设置 ANDROID_SDK 环境变量}"
BT="$ANDROID_SDK/build-tools/34.0.0"
PLAT="$ANDROID_SDK/platforms/android-34/android.jar"
OUT="${OUT:-$APP/../听力刷题-连做版.apk}"

[ -f "$APP/assets/index.html" ] || {
  echo "缺少 assets/index.html —— 先把根目录的 html 复制进来："
  echo "  cp \"$APP/../听力刷题-连做版.html\" \"$APP/assets/index.html\""
  exit 1
}

cd "$APP"
rm -rf build
mkdir -p build/gen build/obj build/dex

echo "[1/6] aapt2 compile"
"$BT/aapt2" compile --dir res -o build/res.zip

echo "[2/6] aapt2 link"
"$BT/aapt2" link -o build/app.ap_ -I "$PLAT" --manifest AndroidManifest.xml \
  -R build/res.zip --java build/gen --auto-add-overlay -A assets

echo "[3/6] javac"
javac -nowarn -source 8 -target 8 -encoding UTF-8 -bootclasspath "$PLAT" \
  -d build/obj build/gen/com/listen/drill/v3/R.java src/com/listen/drill/v3/MainActivity.java

echo "[4/6] d8"
"$BT/d8" --lib "$PLAT" --min-api 21 --output build/dex $(find build/obj -name "*.class" | tr '\n' ' ')

echo "[5/6] zip + zipalign"
python - <<'PY'
import zipfile, shutil
shutil.copy('build/app.ap_', 'build/unsigned.apk')
with zipfile.ZipFile('build/unsigned.apk', 'a', zipfile.ZIP_DEFLATED) as z:
    z.write('build/dex/classes.dex', 'classes.dex')
print('entries:', len(zipfile.ZipFile('build/unsigned.apk').namelist()))
PY
"$BT/zipalign" -f 4 build/unsigned.apk build/aligned.apk

echo "[6/6] apksigner"
"$BT/apksigner" sign --ks debug.keystore --ks-pass pass:android --key-pass pass:android \
  --out "$OUT" build/aligned.apk
"$BT/apksigner" verify --print-certs "$OUT" | head -3
echo "done -> $OUT"
