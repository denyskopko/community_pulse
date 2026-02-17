from pydantic import BaseModel, ConfigDict
from sqlalchemy import DECIMAL


class MineralOut(BaseModel):
    model_config = ConfigDict(  # эта настройка помогает задать дополнительные конфигурации модели
        from_attributes=True,  # поможет пайдантик работать с классами и их аттрибутами
        str_strip_whitespace=True,  # для всех строковых полей убирает пробелы
        extra="forbid"  # запрещает создание полей, которых нет в модели
    )

    id: int
    name: str
    color: str
    hardness: DECIMAL



# docker run --name sqlalchemy-queries -p 3306:3306 -v ${PWD}/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=qwerty -e MYSQL_DATABASE=database -e MYSQL_USER=user -e MYSQL_PASSWORD=qwerty -d mysql:8.0


# docker volume create mysql_data

# docker run --name sqlalchemy-queries -p 3306:3306 --restart unless-stopped -v mysql_data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root_password -e MYSQL_DATABASE=database -e MYSQL_USER=user -e MYSQL_PASSWORD=strong_password -d mysql:8.0
