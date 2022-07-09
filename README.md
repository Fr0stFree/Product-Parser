### Hi there, I'm Danila!
[![codewars](https://www.codewars.com/users/FrostFree/badges/large)](https://www.codewars.com/users/FrostFree)
#### Python backend developer student from Russia 🇷🇺

---
### Парсер Продуктов

Данная программа создавалась с целью сбора информации о товарах с сайта [MiShop](https://mi-shop.com/ru/).
Требования, стоящие перед разработчиком программы - интуитивно понятный интерфейс, простая логика, устойчивость к ~неадекватному поведению пользователя~ ошибкам.

Работа программы начинается с получения html-страницы. Страницу можно загрузить двумя путями: локально из памяти компьютера указав путь к странице (кнопка Open), или загрузив  из интернета по указанному в поле ввода адресу (кнопка Request). При необходимости можно загрузить сразу несколько страниц изменив в поле "pages:1" число на необходимое количество страниц.

Второй этап работы заключается в поиске объектов с карточками товаров (кнопка Find All). Для поиска необходимо указать корректный CSS-селектор объекта карточки.

Третим этапом является парсинг каждой найденной карточки на параметры (например: цена, название, скидка, отзывы), соответствующие указанным CSS-селекторам. Можно указать до пяти параметров. При успешном парсинге карточек предложит сохранить полученные данные в формате .json или .xlsx (кнопки Save json и Save xlsx соответственно)


### Использованные технологии
- [Python](https://github.com/python)
- [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)
- [requests](https://pypi.org/project/requests/)
- [openpyxl](https://pypi.org/project/openpyxl/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)

---
### Запуск проекта
- Клонировать репозиторий
```
git clone https://github.com/Fr0stFree/Product-parser
```
- Установить и активировать виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate (Windows OS)
с
source venv/bin/activate (Unix OS)
```
- Установить необходимые зависимости
```
pip install -r requirements.txt
или
python -m pip install -r requirements.txt
```
- Запустить проект из главной директории
```
python main.py
```
![alt text](https://github.com/Fr0stFree/Product-parser/blob/main/screenshot.jpg?raw=true)
