#!/data/data/com.termux/files/usr/bin/bash
# STAR Plus v4.3 — Installer from GitHub Releases
# Repo: Markx755/Starplustool

set -e

REPO="Markx755/Starplustool"
ASSET_NAME="star_plus.zip"
LATEST_API="https://api.github.com/repos/$REPO/releases/latest"
DIR="$HOME/star-tool"

echo "════════════════════════════════════════"
echo "  ⭐ STAR Plus v4.3 · Auto Rejoin · Installer"
echo "  ดาวน์โหลดจาก GitHub Releases (ZIP)"
echo "════════════════════════════════════════"

# 1) ติดตั้งพื้นฐาน
echo "[1/5] อัปเดตระบบ..."
pkg update -y >/dev/null 2>&1
pkg upgrade -y >/dev/null 2>&1

echo "[2/5] ติดตั้ง Python & เครื่องมือ..."
pkg install -y python python-pip curl jq unzip >/dev/null 2>&1

echo "[3/5] ติดตั้งไลบรารี..."
pip install requests --quiet

# 2) หาลิงก์ไฟล์
echo "[4/5] ค้นหาเวอร์ชันล่าสุด..."
DOWNLOAD_URL=$(curl -sL "$LATEST_API" | jq -r --arg name "$ASSET_NAME" \
    '.assets[] | select(.name==$name) | .browser_download_url')

if [ -z "$DOWNLOAD_URL" ] || [ "$DOWNLOAD_URL" = "null" ]; then
    echo "❌ ไม่พบไฟล์ $ASSET_NAME ใน Releases!"
    echo "ตรวจสอบ: ชื่อไฟล์ต้องตรงเป๊ะ — star_plus.zip"
    exit 1
fi

echo "✅ พบไฟล์ — กำลังดาวน์โหลด..."
mkdir -p "$DIR"
cd "$DIR"
curl -sL "$DOWNLOAD_URL" -o "$ASSET_NAME"

# 3) แตกไฟล์ ZIP
echo "[5/5] กำลังแตกไฟล์..."
unzip -o "$ASSET_NAME"
rm -f "$ASSET_NAME"

chmod +x star_plus.py 2>/dev/null || true

echo ""
echo "✅ ติดตั้งเสร็จสิ้น!"
echo "════════════════════════════════════════"
echo "  เปิดใช้งาน:"
echo "  cd ~/star-tool && python star_plus.py"
echo ""
echo "  เข้าโหมดแอดมิน:"
echo "  cd ~/star-tool && python star_plus.py admin"
echo "════════════════════════════════════════"