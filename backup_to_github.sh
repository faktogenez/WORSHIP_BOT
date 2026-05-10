#!/bin/bash
# Скрипт полного бэкапа проекта на GitHub

cd /home/ubuntu/radio_bot

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}📦 БЭКАП ПРОЕКТА НА GITHUB${NC}"
echo -e "${GREEN}========================================${NC}"

# Получаем дату и время
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Проверяем, есть ли изменения
if git status --porcelain | grep -q .; then
    echo -e "${YELLOW}📝 Найдены изменения:${NC}"
    git status --short
    
    # Добавляем все файлы
    git add .
    
    # Создаём коммит с датой
    git commit -m "Backup: $DATE"
    
    # Отправляем на GitHub
    echo -e "${YELLOW}🚀 Отправка на GitHub...${NC}"
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Бэкап успешно создан и отправлен!${NC}"
    else
        echo -e "${RED}❌ Ошибка при отправке на GitHub${NC}"
    fi
else
    echo -e "${GREEN}✅ Нет изменений для бэкапа${NC}"
fi

echo -e "${GREEN}========================================${NC}"
