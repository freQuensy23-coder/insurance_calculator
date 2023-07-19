# О проекте 
Это заготовка небольшого API, созданного для расчета стоимости страховки заказов. Используется **postgres** для хранения тарифов для разных типов грузов, дат итп. **Fastapi** для обработки запросов. Валидации пользовательских данных используется **pydantic**, в качестве ORM - tortoise,  а для логирования - **loguru**. Для развертывания - **docker**.

### Немного важных технических деталей
* Так как при работе с финансами неточность расчета floating point значений может быть критична, для хранения финансовых чисел используется Decimal. Так что все итоговые цены, будут округлсяться по стандартным правилам банковского округления. 
* Все даты в API передаются в формате yyyy-mm-dd
* Порт подключения к серверу - 8000. Эта система поднята на моем удаленном сервере, вы можете ее опробывать, не поднимая локально.
# Инструкция по развертыванию 
1) Установить docker + docker compose. Используйте свой менеджер пакетов, для arch - `pacman -S docker docker-compose`
2) Запустите демон докера используя systemctl или другой менеджер сервисов. Для systemd based arch - `systemctl start docker`
3) Выполните `docker-compose up -d` в корне проекта. При первом запуске из интернета будут подтянуты все необходимые образы, по этому необходимо подключение к сети.
4) Для остановки - `docker-compose down`.

# Что еще можно сделать
- [ ] Добавить систему контроля API ключей
- [ ] Добавить настройку часовых поясов. Наше API довольно сильно завязано на серверное время. Нужно или отказаться от этого (и требовать клиента явно указывать дату при каждом запросе) или сделать работу с часовыми поясами более гибкой, а не просто брать системное время.
- [ ] Если число типов грузов фиксировано, то их хорошо бы вынести в отдельную таблицу, а в rates просто хранить id типа груза. Это намного лучше чем представление типа груза в виде строки. 

# API Endpoints
## 1. GET /calculate_cost

This endpoint is used to calculate the cost of insurance for a given cargo.

### Parameters:

- `cargo_type` (string, required): The type of the cargo for which the insurance cost is to be calculated.
- `cost` (string, required): The cost of the cargo.
- `date` (dateformat-string, optional): The date of delivery. If not provided, the current date will be used.

### Return:

It returns a JSON with the calculated cost of the insurance for the given cargo. If the rate for the given date and cargo type is not established, it raises a HTTP 404 error.

### Example:

```
GET /calculate_cost?cargo_type=Glass&cost=1222
```
```JSON
{
    "status":"ok"
    "cost": 61.1
}
```


---

## 2. POST /set_rates

This endpoint is used to set the rates for different cargo types.

### Parameters:

- `rates` (list of Rate_pydantic objects, required): A list of rates to be set. Each Rate_pydantic object should have the following structure:
  - `date`: The date for which the rate is set.
  - `cargo_type`: The type of cargo for which the rate is set.
  - `rate`: The rate to be set.

### Return:

It returns a JSON with the status of the operation and a list of warnings if any of the rates are outdated (i.e., the date for the rate is before the current date).
Warn if the rate is outdated (i.e., the date for the rate is before the current date).
### Example:

```
POST /set_rates 
BDOY [{"cargo_type":"Glass", "rate":"0.05", "date":"2023-07-19"}]
```
```JSON
{
    "status": "ok",
    "warnings": []
}
```



---

## 3. GET /rates

This endpoint is used to get the rates for a given day.

### Parameters:

- `day` (string, optional): The date for which the rates are requested. If not provided, the current date will be used.

### Return:

It returns a JSON with the status of the operation and the list of rates for the given day. If there are no rates for the given day, it returns an empty list.

### Example:

```
GET /rates
```
```JSON
{
    "status": "ok",
    "result": [
        {
            "date": "2023-07-19",
            "cargo_type": "Glass",
            "id": 1,
            "rate": 0.05
        }
    ]
}
```
