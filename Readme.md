Проект собирается через Docker.

Для корректной работы необходимо создать файл .env внутри проекта
(Пример данных для .env файла можно найти в env.example)

Далее необходимо перейти в корневую директорию проекта и ввести следующую команду:
docker-compose up --build или docker compose up --build, если первая команда выдаст ошибку

После успешного билда вы можете зайти в swager и посмотреть функционал.
Документацию по проекту можно найти по адресу: 127.0.0.1:8000/docs