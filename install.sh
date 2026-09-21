#!/data/data/com.termux/files/usr/bin/bash
# STAR Plus — Fast Installer (แก้ค้างตอนอัปเดต)
# Repo: Markx755/Starplustool

set -e

REPO="Markx755/Starplustool"
ASSET_NAME="star_plus.zip"
MAIN_FILE="star_plus.py"
LATEST_API="https://api.github.com/repos/$REPO/releases/latest"
DIR="$HOME/star-tool"

echo "════════════════════════════════════════"
echo "  ⭐ STAR Plus · Auto Rejoin · Installer"
echo "════════════════════════════════════════"

# 1) เปลี่ยนแหล่งโปรแกรมให้เร็วขึ้น + ติดตั้งโดยไม่ค้าง
echo "[1/5] ตรวจสอบแพ็กเกจ..."
pkg update -y --quiet 2>/dev/null || true

echo "[2/5] ติดตั้งเครื่องมือ..."
pkg install -y python python-pip curl jq unzip --quiet 2>/dev/null

echo "[3/5] ติดตั้งไลบรารี Python..."
pip install requests --quiet

# 2) ดาวน์โหลด
echo "[4/5] ดาวน์โหลดไฟล์..."
DOWNLOAD_URL=$(curl -sL "$LATEST_API" | jq -r --arg name "$ASSET_NAME" \
    '.assets[] | select(.name==$name) | .browser_download_url')

if [ -z "$DOWNLOAD_URL" ] || [ "$DOWNLOAD_URL" = "null" ]; then
    echo "❌ ไม่พบไฟล์ $ASSET_NAME"
    exit 1
fi

mkdir -p "$DIR"
cd "$DIR"
curl -sL "$DOWNLOAD_URL" -o "$ASSET_NAME"

echo "[5/5] แตกไฟล์..."
unzip -o "$ASSET_NAME" >/dev/null
rm -f "$ASSET_NAME"
chmod +x "$MAIN_FILE" 2>/dev/null || true

echo ""
echo "✅ ติดตั้งเสร็จ!"
echo "════════════════════════════════════════"
echo "  เปิดใช้งาน:"
echo "  cd ~/star-tool && python star_plus.py"
echo "════════════════════════════════════════"