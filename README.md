# Установка
1. Скачать проект с github
   
        $ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
        $ cd YOUR-REPOSITORY

2. Создать файл с настройками inosatiot_cfg.json. Шаблон находится в setup/inosatiot_cfg.json_template.

3. Добавить в переменные среды путь к файлу inosatiot_cfg.json
   
        $ sudo nano /etc/environment
        
   Дописать в файл inosatiot_cfg="PATH-TO-CONFIG-FILE"

4. Установка библиотек python в файле setup/setup.sh
   
        $ chmod +x setup/setup.sh
        $ setup/setup.sh

5. После установки можно запустить на выполнение через systemd
   
        $ sudo systemctl start inosatiot_report.service  // запустить
        $ sudo systemctl stop inosatiot_report.service  // остановить
        $ sudo systemctl restart inosatiot_report.service  // перезапустить
        $ sudo systemctl status inosatiot_report.service  // просмотреть статус

# После установки
- Синхронизировать проект с github (локальные изменения теряются)
   
        $ git fetch origin && git reset --hard origin/master && git clean -f -d

