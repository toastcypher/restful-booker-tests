Автотесты для Restful Booker API.

Описание:
Проект содержит автотесты для Restful-Booker API.
Реализован минимальный тестовый фреймворк с разделением на слои:
* API Client слой (транспортный уровень)
* Fixtures / Data слой (генерация и подготовка тестовых данных)
* Asserts слой (логика проверок)

Тесты написаны с использованием pytest.

Структура проекта:
* clients/
  * base_api_client.py
  * restful_booker_client.py
* data/
  * booking_payloads.py
* asserts/
  * response_asserts.py
  * booking_asserts.py
* tests/
  * test_auth.py
  * test_booking.py
  * test_negative.py
  * test_booking_filters.py
* config.py
* pytest.ini
* requirements.txt

Установка:
1. [ ] Создание виртуального окружения:
   2. [ ] python -m venv venv
   3. [ ] source venv/bin/activate
4. [ ] Установка зависимостей:
   5. [ ] pip install -r requirements.txt

Переменные окружения:
* export BASE_URL=https://restful-booker.herokuapp.com
* export AUTH_USERNAME=admin
* export AUTH_PASSWORD=password123

Запуск тестов:
* pytest или pytest -q

Покрытие тестами

Реализованы проверки для:
* Авторизации (POST /auth)
* Создания бронирования (POST /booking)
* Получения списка бронирований (GET /booking)
* Фильтрации по имени и датам
* Обновления бронирования (PUT /booking/{id})
* Удаления бронирования (DELETE /booking/{id})
* Негативных сценариев:
  * отсутствие обязательных полей
  * некорректный JSON
  * неверный Content-Type
  * несуществующий id

Особенности API:
* API выполняет “мягкий” (lenient) парсинг дат.
* Невалидные строки даты могут быть автоматически преобразованы сервером.
* База данных сервиса сбрасывается примерно каждые 10 минут.
* В ряде случаев сервер может возвращать 500 вместо 400 при ошибочных данных.