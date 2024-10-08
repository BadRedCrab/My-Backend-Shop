# Мой проект: Backend сайта магазина

## Стек технологий:

- **Django**  
- **Django REST Framework**  
- **Django-Rest-Knox**  
- **Celery**  
- **Redis**  
- **PostgreSQL**

## Описание:

Этот проект реализует backend для сайта магазина с функциями регистрации, авторизации по токену, подтверждения электронной почты и многими другими возможностями, такими как:


- **Создание и запрос товаров**  
- **Редактирование товаров**  
- **Добавление товаров в корзину**  
- **Оставление комментариев и оценка продуктов**

Сайт состоит из двух основных приложений для управления пользователями и магазином: `account` и `shop`.  

## API эндпоинты:

### Приложение: `shop`

- **`/api-products/`**  
  - **GET**: Получение списка товаров  
  - **POST**: Создание нового товара  
- **`/api-product/<str:slug>/`**  
  - **GET**: Получение конкретного продукта  
  - **PATCH**: Редактирование продукта  
- **`/api-comments/<str:slug>/`**  
  - **GET**: Получение списка комментариев о продукте  
  - **POST**: Создание нового комментария  
- **`/api-cart/`**  
  - **GET**: Получение списка товаров в корзине  
  - **POST**: Добавление товара в корзину  
  - **DELETE**: Удаление товара из корзины  

### Приложение: `account`

- **`/account/api-register/`**  
  - **POST**: Регистрация пользователя и получение токена  
- **`/account/api-login/`**  
  - **POST**: Авторизация и получение токена  
- **`/account/api-update/`**  
  - **PATCH**: Обновление данных пользователя  
- **`/account/api-recreate-token/`**  
  - **GET**: Переполучение токена авторизованным пользователям  
- **`/account/api-confirm-email/`**  
  - **GET**: Отправка кода подтверждения на электронную почту  
- **`/account/api-confirm-email/<str:key>`**  
  - **POST**: Подтверждение адреса электронной почты  
- **`/account/api-profile/`**  
  - **GET**: Получение информации о пользователе  
- **`/account/api-change-password/`**  
  - **PATCH**: Смена пароля  

## Основные команды:

### Запуск сервера Django:

```bash
python3 manage.py runserver
```

### Запуск Celery:  
```bash
celery -A MySite worker --loglevel=info
```


