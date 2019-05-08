import datetime
import os
import uuid
from contextlib import contextmanager

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
    SELECT a.id, a.title, a.body, a.is_cocktail, a.creation_time, a.user_id FROM 
    cocktails.articles a
    {}
    order by a.creation_time desc
    offset {} limit {}
    """.format(where_ddl, offset, size)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def write_article_with_tags(data):
    with get_connection() as conn:
        conn.autocommit = False
        cursor = conn.cursor()
        if "id" in data:
            cursor.execute("DELETE FROM cocktails.articles where id = {}".format(data["id"]))
        new_id = str(uuid.uuid4())
        cursor.execute("""INSERT INTO cocktails.articles (id, title, body, is_cocktail, creation_time, user_id) 
                        VALUES('{}', '{}', '{}', {}, '{}', {})""".format(new_id,
                                                                    data["title"].replace("'", r"''"),
                                                                   data["body"].replace("'", r"''", ),
                                                                   data["is_cocktail"],
                                                                   datetime.datetime.now().isoformat(),
                                                                   data["user_id"]))

        all_tags = ["('{}', '{}', {})".format(new_id, tg.replace("'", "''"), False) for tg in data["tags"]]
        all_tags.extend(["('{}', '{}', {})".format(new_id, tg.replace("'", "''"), True) for tg in data["ingredients"]])
        cursor.execute("""
            INSERT INTO cocktails.tags (id, tag_name, is_ingredient)
            VALUES {}
        """.format(', '.join(all_tags)))
        conn.commit()
