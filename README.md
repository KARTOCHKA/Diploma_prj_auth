##Russian
##English
# Cервис для верификации пользователя путем отправки ему СМС кода
## Описание
* Интерфейс системы содержит следующие экраны: регистрацию пользователя по имени, паролю и номеру телефона, верификация по смс коду, домашняя страница со списком всех зарегистрированных пользователей.
* При создании нового пользователя на указанный номер телефона высылается 6-ти значный смс код с помощью Twilio.
* Права доступа к домашней страницы даются пользователю после подтверждения номера телефона.
* Использовано 2 модели, User, используемая для создания пользователя и UserVerification, которая отвечает за верификацию пользователя.
## Технологии
* Python
* Django
* DRF
* PostgreSQL
* Twilio
* nginx
* Docker
## Сущности
* Пользователь
* Верификация


### Запуск приложения в локальной сети:
_Для работы с переменными окружениями необходимо создать файл .env и заполнить его согласно файлу .env.sample:_
```

#Database
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=


#Secret_key:
SECRET_KEY=
```
_Для запуска проекта необходимо клонировать репозиторий и создать и активировать виртуальное окружение:_ 
```
python3 -m venv venv
source venv/bin/activate
```
_Установить зависимости:_
```
pip install -r requirements.txt
```
_Выполнить миграции:_
```
python3 manage.py migrate
```
_Для создания администратора запустить команду и указать данные:_
```
 python manage.py createsuperuser
```
_Для запуска приложения:_
```
python3 manage.py runserver
```

# User Verification Service via SMS Code
## Description
* The system's interface includes the following screens: user registration with name, password, and phone number, SMS code verification, and a home page with a list of all registered users.
* When creating a new user, a 6-digit SMS code is sent to the specified phone number using Twilio.
* Access rights to the home page are granted to the user after phone number confirmation.
* Two models are used: User, which is used for user creation, and UserVerification, which is responsible for user verification.
## Technologies
* Python
* Django
* Django Rest Framework (DRF)
* PostgreSQL
* Twilio
* Nginx
* Docker
## Entities
* User
* Verification


### Running the Application Locally:
_To work with environment variables, you need to create a .env file and fill it out according to the .env.sample file:_
```

#Database
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=


#Secret_key:
SECRET_KEY=
```
_To run the project, clone the repository and create/activate a virtual environment:_
```
python3 -m venv venv
source venv/bin/activate
```
_Install dependencies:_
```
pip install -r requirements.txt
```
_Run migrations:_
```
python3 manage.py migrate
```
_To create an admin user, run the following command and provide the necessary details:_
```
python manage.py createsuperuser
```
_To start the application:_
```
python3 manage.py runserver
```