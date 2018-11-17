## SUBD_RK

#### Рубежные контрольные работы по предмету "Системы управления базами данных".
Материалы для подготовки: html-файлы с вопросами для самопроверки.  
Университет ИТМО, кафедра ВТ, семестр 7, период обучения 17/18 года.

### Установка
```bash
cd SUBD_RK
python3 -m venv subd_venv
source subd_venv/bin/activate
python3 -m pip install -r requirements.txt
```
### Использование
Справка по доступным опциям:
```bash
python3 subd_parser.py -h
```
Создать файлы **без номера** вопроса на странице:
```bash
python3 subd_parser.py -i rk1_questions.txt -d rk1 --no-title
python3 subd_parser.py -i rk2_questions.txt -d rk2 --no-title
```
Создать файлы **с номером** вопроса на странице:
```bash
python3 subd_parser.py -i rk1_questions.txt -d rk1
python3 subd_parser.py -i rk2_questions.txt -d rk2
```
