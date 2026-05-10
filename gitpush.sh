#!/bin/bash
cd /home/ubuntu/radio_bot
git add .
git commit -m "Update: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
echo "✅ Сохранено на GitHub"
