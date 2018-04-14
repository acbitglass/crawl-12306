import pymysql
from AnhuiGov import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

db = pymysql.connect(MYSQL_HOSTS, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, charset="utf8")
cursor = db.cursor()


class Sql:
    @classmethod
    def insert_data(cls, title, content, source_publish_time, info_source, source_url):
        sql = 'insert into AnhuiGov (`title`, `content`, `source_publish_time`, `info_source`, `source_url`) values ' \
              '(%(title)s, %(content)s, %(source_publish_time)s, %(info_source)s, %(source_url)s)'
        value = {
            'title': title,
            'content': content,
            'source_publish_time': source_publish_time,
            'info_source': info_source,
            'source_url': source_url
        }
        try:
            cursor.execute(sql, value)
            db.commit()
        except Exception as e:
            print('fer_native error:', e.message)
            db.rollback()

    @classmethod
    def duplicate(cls, source_url):
        sql = 'select exists(select 1 from AnhuiGov where source_url = %(source_url)s)'
        value = {
            'source_url': source_url
        }
        cursor.execute(sql, value)
        rows = cursor.fetchall()[0][0]
        return rows

