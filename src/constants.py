API_ANSWERS = [{"id": 102, "description": "обработать входящие данные из внешнего источника goida.com", "priority": 3, "status": "CREATED"},
               {"id": 103, "description": "проверить состояние ресурса MAI", "priority": 2, "status": "DONE"},
               {"id": 104, "description": "обработать заказ с идентификатором 404", "priority": 5,"status": "IN_PROCESS"},
               {"id": 105, "description": "отправить уведомление пользователю EMAKS", "priority": 1, "status": "IN_PROCESS"}]
TASK_PURPOSES = ["обработать входящие данные из внешнего источника", "проверить состояние ресурса",
                "отправить уведомление пользователю", "проверить состояние сервиса", "перераспределить ресурсы на",
                "ожидать ответа от"]
TASK_DESTINATIONS = ["mai.ru", "goida.com", "recroll.en", "NIICHAVO.su", "eeva.team", "EMAKS"]
POSSIBLE_STATUSES = ["CREATED", "IN_PROCESS", "DONE"]
