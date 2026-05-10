#!/bin/bash
cd /home/ubuntu/radio_bot
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ -z "$1" ]; then
    COMMIT_MSG="Auto-save: $(date '+%Y-%m-%d %H:%M:%S')"
else
    COMMIT_MSG="$1"
fi

echo -e "${YELLOW}📝 Сообщение: ${COMMIT_MSG}${NC}"
git add .
git commit -m "$COMMIT_MSG"
git push origin main
echo -e "${GREEN}✅ Сохранено на GitHub${NC}"
