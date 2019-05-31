import datetime
import os
import uuid
from contextlib import contextmanager

from flask_login import UserMixin
from psycopg2 import pool

db = pool.ThreadedConnectionPool(2, 100, host=os.environ["DB_ADDRESS"],
                                 dbname=os.environ["DB_NAME"],
                                 user=os.environ["DB_USER"],
                                 password=os.environ["DB_PASSWORD"],
                                 port=os.environ["DB_PORT"])


@contextmanager
def get_connection():
    con = db.getconn()
    try:
        yield con
    finally:
        db.putconn(con)


def get_top_tags(top_number):
    query = """
    select tag_name 
    from cocktails.tags
    group by tag_name
    order by count(tag_name) desc
    LIMIT {}
    """.format(top_number)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def get_tags(is_ingredient, ids):
    where_ddl = ""
    predicates = []
    if is_ingredient is not None:
        predicates.append("is_ingredient = {}".format(is_ingredient))
    if ids is not None and ids:
        predicates.append("id in ({})".format(','.join("'{}'".format(id) for id in ids)))
    if predicates:
        where_ddl = "WHERE " + ' and '.join(predicates)
    query = """
    select DISTINCT tag_name, is_ingredient
    from cocktails.tags
    {}
    """.format(where_ddl)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def get_article_db(guid):
    query = """
        SELECT a.id, a.title, a.body, a.is_cocktail, a.creation_time, a.user_id, a.cocktail_name FROM 
        cocktails.articles a
        where a.id = '{}'
        """.format(guid)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def get_cocktails():
    query = """
        select a.id, a.cocktail_name, t.tag_name from cocktails.articles a 
        join cocktails.tags t on a.id = t.id
        where t.is_main_ingredient = True
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def get_articles(size, offset, search, cocktails_only, with_tag):
    where_ddl = ""
    predicates = []
    if search is not None:
        predicates.append("title ilike '%{}%'".format(search))
    if cocktails_only is not None:
        predicates.append("is_cocktail = {}".format(cocktails_only))
    if with_tag is not None:
        predicates.append("id in (select id from cocktails.tags where tag_name='{}')".format(with_tag))
    if predicates:
        where_ddl = "WHERE " + ' and '.join(predicates)
    query = """
    SELECT a.id, a.title, a.body, a.is_cocktail, a.creation_time, 
    a.user_id, a.cocktail_name FROM 
    cocktails.articles a
    {}
    order by a.creation_time desc
    offset {} limit {}
    """.format(where_ddl, offset, size)
    if int(offset) <= 0:
        has_prev = False
    else:
        has_prev = True
    query_next = """
    SELECT EXISTS(SELECT * FROM cocktails.articles a
    {}
    order by a.creation_time desc
    offset {})
    """.format(where_ddl, int(offset) + int(size))
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        res_data = cursor.fetchall()
        cursor.execute(query_next)
        has_next = cursor.fetchone()[0]
    return res_data, has_prev, has_next



def write_article_with_tags(data):
    with get_connection() as conn:
        conn.autocommit = False
        cursor = conn.cursor()
        if "id" in data:
            cursor.execute("DELETE FROM cocktails.articles where id = {}".format(data["id"]))
        new_id = str(uuid.uuid4())
        cursor.execute("""INSERT INTO cocktails.articles (id, title, body, is_cocktail, creation_time, user_id, cocktail_name) 
                        VALUES('{}', '{}', '{}', {}, '{}', {}, '{}')""".format(new_id,
                                                                         data["title"].replace("'", r"''"),
                                                                         data["body"].replace("'", r"''", ),
                                                                         data["is_cocktail"],
                                                                         datetime.datetime.now().isoformat(),
                                                                         data["user_id"],
                                                                         data.get("cocktail_name")))

        all_tags = generate_tag_data(data, new_id, "tags")
        all_ingr = generate_tag_data(data, new_id, "ingredients")
        all_ingr[0][3] = True
        all_tags.extend(all_ingr)
        all_tags = ["('{}', '{}', {}, {})".format(tg[0], tg[1], tg[2], tg[3]) for tg in all_tags]
        cursor.execute("""
            INSERT INTO cocktails.tags (id, tag_name, is_ingredient, is_main_ingredient)
            VALUES {}
        """.format(', '.join(all_tags)))
        conn.commit()


def generate_tag_data(data, new_id, param_name):
    return [[new_id, tg.replace("'", "''"), False, False] for tg in data[param_name]]


class User(UserMixin):
    def __init__(self, id, name, password, is_active):
        self.id = id
        self.name = name
        self.password = password

def get_user_by_name(user_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, "name", password, is_active from cocktails.users where "name" = \'{}\''.format(user_name))
        return User(*cursor.fetchone())

def get_user_by_id(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, "name", password, is_active from cocktails.users where "id" = \'{}\''.format(user_id))
        return User(*cursor.fetchone())
