# sqlacodegen_v2 mysql+pymysql://ich1:ich1_password_ilovedbs@ich-edit.edu.itcareerhub.de:3306/social_blogs --outfile sqlalchemy_lessons/social_blogs_models.py

from sqlalchemy import create_engine, select
from sqlalchemy.orm import joinedload

from lessons.sqlalchemy_lessons.lesson_2.db_connector import DBConnector

engine = create_engine(
    url="mysql+pymysql://ich1:ich1_password_ilovedbs@ich-edit.edu.itcareerhub.de:3306/social_blogs",
    echo=True,
    future=True
)


# Session = sessionmaker(bind=engine)
# session = Session()
# session.close()


with DBConnector(engine) as session:
    # CRUD operations

    # C (Create)
    # data = {"name": "NewRole"}
    #
    # new_role = Role(**data)
    # session.add(new_role)
    # session.commit()


    # R (Read)

    # Read one
    # user = session.get(User, 11)
    #
    # print(user)
    #
    # print(user.email)
    # print(user.first_name)
    # print(user.created_at)

    # Read many
    # all_authors = (  # stmt (STATEMENT)
    #     select(User)  # SELECT * FROM `user`
    #     .where(User.role_id == 3) # WHERE role_id = 3
    # )
    #
    # # по умолчанию вернётся [Row(User()), Row(User()), ..., Row(User())]
    # response = session.execute(all_authors).scalars() # -> [User(), User(), ..., User()]
    #
    # data = [
    #     {
    #         "id": user.id,
    #         "name": user.first_name,
    #         "role": user.role_id
    #     }
    #     for user in response
    # ]
    #
    #
    # print(data)

    # Получить только пользователей с рейтингом больше 5

    # v1 подход
    # res = session.query(User).filter(User.rating > 5).all()

    # v2
    # stmt = (
    #     select(User)
    #     .where(User.rating > 5)
    # )
    #
    # res = session.execute(stmt).scalars()
    #
    # for obj in res:
    #     print(obj.email, obj.rating)

    # получить только тех юзеров, чьи фамилии начинаются на `M`

    # last_name_pattern = "M%"
    #
    # stmt = (
    #     select(User)
    #     .where(User.last_name.like(last_name_pattern))
    # )
    #
    # result = session.execute(stmt).scalars()
    #
    # print(result)
    #
    # for user in result:
    #     print(user.last_name, user.role_id)


    # посмотреть пользователей с рейтингом от 2 до 5

    # stmt = (
    #     select(User)
    #     .where(User.rating.between(2, 5))
    # )
    #
    # res = session.execute(stmt).scalars()
    #
    # for user in res:
    #     print(user)
    #     # print(user.rating)

    # взять только авторов с рейтингом больше 6

    # stmt = (
    #     select(User)
    #     .where(
    #         and_(User.role_id == 3, User.rating > 6)
    #     )
    #     .order_by(desc(User.rating), User.last_name)
    # )
    #
    # res = session.execute(stmt).scalars()
    #
    # for user in res:
    #     print(user.rating, user.last_name)




    # ======================================================================

    # Aggregation && grouping

    # stmt = (
    #     select(func.avg(User.rating))  # SELECT AVG('user'.rating) FROM user;
    # )
    #
    # res = session.execute(stmt).scalar()
    #
    # print(res)

    # stmt = (
    #     select(User.role_id, func.avg(User.rating))  # SELECT user.role_id, AVG('user'.rating) FROM user GROUP BY uer.role_id;
    #     .group_by(User.role_id)
    # )
    #
    # result = session.execute(stmt).scalars()
    #
    # print(result)
    #
    # for res in result:
    #     print(res)


    # us = alias(selectable=User, name="us")
    # us = aliased(element=User, name="us")
    #
    #
    # stmt = (
    #     select(
    #         us.role_id,
    #         func.count(us.id).label("count_of_users")
    #     )
    #     .group_by(us.role_id)
    # )
    #
    # result = session.execute(stmt).all() # -> [(1, 1), (2, 4), (3, 26)]
    #
    # for group_ in result:
    #     print(f"user role: {group_.role_id}  | Count of Users: {group_.count_of_users}")


    # us = aliased(element=User, name="us")
    #
    # stmt = (
    #     select(
    #         us.role_id,
    #         func.count(us.id).label("count_of_users")
    #     )
    #     .group_by(us.role_id)
    #     .having(func.count(us.id) > 4)
    # )
    #
    # result = session.execute(stmt).all() # -> [(3, 26)]
    #
    # for group_ in result:
    #     print(f"user role: {group_.role_id}  | Count of Users: {group_.count_of_users}")

    # # Подзапрос
    # mean_rate_by_author_sbq = select(
    #     func.avg(User.rating).label("user_rating")
    # ).where(User.role_id == 3).scalar_subquery()
    #
    # # Главный зпрос
    # main_query = select(User).where(User.rating > mean_rate_by_author_sbq)
    #
    # result = session.execute(main_query).scalars()
    #
    # print(result)
    #
    # for user in result:
    #     print(user.last_name, user.rating)

    # roles = select(Role)
    #
    #
    # result = session.execute(roles).scalars()
    #
    # for role in result:
    #     print(role.name)
    #     print("User Info:")
    #     for user in role.user:
    #         print(user.last_name, user.first_name)


    # =======================================================================

    # .join() -- когда нужно провести фильтрацию \ поиск данных из таблицы А на основе значения из таблицы Б

    # .joinedload()
    # .subqueryload()
    # .selectinload()

    # взять пользователей в роли "author"

    # stmt = (
    #     select(User)
    #     # .join(Role)
    #     .join(Role, Role.id == User.role_id)
    #     # .join(User.role)
    #     .where(Role.name == 'author')
    # )
    #
    # result = session.execute(stmt).scalars()
    #
    #
    # for user in result:
    #     print(user.first_name, user.role_id)



    # получить пользователей и для каждого пользователя взять его новости

    stmt = (
        select(User)
        .join(Role, Role.id == User.role_id) # подгружается только таблица Ролей для фильтрации
        .outerjoin(User.news)  # Необязательный метод, может помочь в тех случаях, когда нужно получить только полный мэтч (Получить только тех юзеров, у которых есть хоть одна новость)
        .options(joinedload(User.news))  # подгружает непосредственно САМИ НОВОСТИ
        .where(Role.name == 'author')  # фильтруем только тех пользователей, у которых определённое имя роли
    )

    result = session.execute(stmt).unique().scalars()  # при присоединении новостей мы получаем данные в формате:
    # [User1(..., News1), User1(..., News2), User1(News3)] то есть каждая новость содержит инфо о пользователе.
    # из-за этого получаем много дубликатов. Чтобы их убрать, и запрос работал без ошибок -- добавляем к извлечению
    # данных метод .unique(). Тогда мы получаем данные в формате [User1(News1, News2, News3, News4)]


    for user in result:
        print(user.last_name, user.role_id, user.news)



# Типичная ошибка: путать joinedload() и явный JOIN
# joinedload() – это инструмент жадной загрузки (eager loading) данных для объектов отношений.
# Он НЕ влияет на условия выборки, только на то, что подгрузится в результирующие объекты.
#
# .join() и .outerjoin() явно влияют на состав запроса и фильтрацию данных.

# Когда использовать joinedload()?
# Когда нужны данные (ИМЕННО САМИ ДАННЫЕ) связанного объекта сразу после запроса:

# Преимущества:
    # 1 SQL-запрос вместо нескольких.
    # Удобно для небольших вложений.

# Недостатки:
    # При большом объёме данных или глубоких вложениях генерируются
    # большие запросы и избыток данных.


# Когда использовать явный .join() или .outerjoin() (Что собсвенно часто и путает)?
# Если нужно ЯВНО ФИЛЬТРОВАТЬ данные по связанным объектам или условиям, нужно использовать именно JOIN:
    # .join() используется в запросах именно для фильтрации данных.
    # НЕ ВЛИЯЕТ напрямую на то, как объекты связи загружаются (lazy/eager).









# ==================================================================================================

# Раписать про Annotated

# ==================================================================================================


# Обычно мы можем привязывать типы данных к каким-то переменных \ параметрам классов \ функций.
#
# Это как правило "сухой" тип данных, без интерактивностей.
#
#
#
# Annotated позволяет накинуть на нащшу переменную с типом данных (коробку) накинуть специальную наклейку.
#
# Переменная остаётся такой же, но благодаря Annotated мы маркируем на неё что-то дополнителное.
#
# "Не больше 100"
# "Только положительные числа"
# "Обязательное поле"
# "Это специальный класс с вот такими доп возможностями"
#
# И вот это дополнительное могут читать какие-то библиотеки, которые мы можем подклкючать в приложении.
#
#
# Формально выглядеть может так:
#
# from typing import Annotated
#
# Annotated[TYPE, metadata1, metadata2, ...]
#
# где TYPE -- основной тип
# а metadata -- любая дополнительная информация
#
# важно не забывать -- Annotated ничего не делает сам. Он лишь хранит информацию для инструментов.
# Если библиотека не умеет его читать -- он бесполезен.
#
#
# Благодаря этому мы можем делать что-то в таком вот стиле:
#
#
#
# from pydantic import PlainValidator
# from typing import Annotated
#
# def is_even(value: int) -> int:
#     if value % 2 != 0:
#         raise ValueError("Must be even")
#     return value
#
# EvenInt = Annotated[int, PlainValidator(is_even)]
#
#
#
# class Data(BaseModel):
#     number: EvenInt
#
#
# Использовать этот Annotated можно в случаях если:
#
# Есть runtime-инструмент (Pydantic, FastAPI)
# Нужна валидация
# Нужны расширенные метаданные для какого-то типа данных
# Есть желание \ необъодимтость создавать переиспользуемые доменные типы
#
#
# Просто ради красоты, потому что вы вот так вот выучили лучше такие инструменты не использовать
# В алхимии этот класс так же не будет помощником -- алхимия не умеет читать эти дополнительные метаданные.











