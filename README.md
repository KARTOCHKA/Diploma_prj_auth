Порядок языков (language order):
* Russian
* English
# Cервис для верификации пользователя путем отправки СМС кода
## Описание
* Интерфейс системы содержит следующие экраны: регистрацию пользователя по имени, паролю и номеру телефона, верификация по смс коду, домашняя страница со списком всех зарегистрированных и верифицированных пользователей, страница пользователя где он может изменить имя и телефон, а так жн ввести инвайт код другого пользователя
* При создании нового пользователя на указанный номер телефона высылается 6-ти значный смс код с помощью Twilio.
* Права доступа к домашней страницы и профилю даются пользователю после подтверждения номера телефона.
* Использовано 2 модели, User, используемая для создания пользователя и UserVerification, которая отвечает за верификацию пользователя.
## Технологии
* Python
* Django
* DRF (Django Rest Framework)
* PostgreSQL
* Twilio
* nginx
* Docker
## Сущности
* Пользователь
* Верификация
## Эндпоинты
* Эндпоинт Регистрации Пользователя:
URL: /api/register/
Метод: POST
Описание: Регистрирует нового пользователя с автоматически сгенерированным 6-значным инвайт-кодом. Если пользователь уже существует, он будет перенаправлен на домашнюю страницу.
* Эндпоинт Профиля Пользователя:
URL: /api/profile/
Метод: GET
Описание: Позволяет пользователям просматривать свой профиль и вводить инвайт-код другого пользователя. Этот эндпоинт также отображает инвайт-код, который пользователь уже активировал.
* Эндпоинт Активации Инвайт-Кода:
URL: /api/activate-invite/
Метод: POST
Описание: Позволяет пользователям активировать инвайт-код в своем профиле. Пользователи могут активировать только один инвайт-код, и если они уже активировали один, будет отображен ранее активированный код.
* Эндпоинт Пользователей с Инвайт-Кодом:
URL: /api/users-with-invite/
Метод: GET
Описание: Список пользователей (номеров телефонов), которые ввели инвайт-код текущего пользователя.

### Запуск приложения в локальной сети:
_Для работы с переменными окружениями необходимо создать файл .env и заполнить его согласно файлу .env.sample:_
```

#Database
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=


#Secret_key:
SECRET_KEY=

# Twilio
TWILIO_ACCOUNT_SID=
YOUR_TWILIO_AUTH_TOKEN=
YOUR_TWILIO_PHONE_NUMBER=
```
Для получения TWILIO_ACCOUNT_SID, YOUR_TWILIO_AUTH_TOKEN и YOUR_TWILIO_PHONE_NUMBER необходимо зарегистрироваться и подтвердить свой номер на сайте Twilio (https://www.twilio.com/en-us). 
Далее необходимо приобрести любой номер на ваш выбор, он и будет YOUR_TWILIO_PHONE_NUMBER.

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
* The system interface contains the following screens: user registration by name, password and phone number, verification by SMS code, home page with a list of all registered and verified users, a user page where he can change his name and phone number, and also enter the invite code of another user
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
## Endpoints
* User Registration Endpoint:
URL: /api/register/
Method: POST
Description: Registers a new user with a randomly generated 6-digit invite code. If the user already exists, they will be redirected to the home page.
* User Profile Endpoint:
URL: /api/profile/
Method: GET
Description: Allows users to view their profile and enter another user's invite code. This endpoint also displays the invite code that the user has already activated.
* Activate Invite Code Endpoint:
URL: /api/activate-invite/
Method: POST
Description: Allows users to activate an invite code in their profile. Users can activate only one invite code, and if they have already activated one, the previously activated code will be displayed.
* Users with Invite Code Endpoint:
URL: /api/users-with-invite/
Method: GET
Description: Lists users (phone numbers) who entered the invite code of the current user.
### Running the Application Locally:
_To work with environment variables, you need to create a .env file and fill it out according to the .env.sample file:_
```

#Database
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=


#Secret_key:
SECRET_KEY=

# Twilio
TWILIO_ACCOUNT_SID=
YOUR_TWILIO_AUTH_TOKEN=
YOUR_TWILIO_PHONE_NUMBER=
```

To obtain the TWILIO_ACCOUNT_SID, YOUR_TWILIO_AUTH_TOKEN, and YOUR_TWILIO_PHONE_NUMBER, you need to register and verify your phone number on the Twilio website (https://www.twilio.com/en-us).
Afterward, you should purchase any phone number of your choice, and that number will become YOUR_TWILIO_PHONE_NUMBER.

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