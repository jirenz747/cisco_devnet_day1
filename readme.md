
Как установить:
1. git clone https://github.com/jirenz747/cisco_devnet_day1
2. cd cisco_devnet_day1
3. python3 -m venv venv
4. source venv/bin/activate
5. pip install -r requirements.txt 

Редактируем файл cisco_devnet_day1/app/hosts.yaml

Запускаем локально flask
export FLASK_APP=devnet_day_one.py
flask run

После чего заходим http://127.0.0.1:5000/


Тестировалось на CSRv

![Иллюстрация к проекту](https://github.com/jirenz747/cisco_devnet_day1/raw/master/img/devices.png)


