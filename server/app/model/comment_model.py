import pymysql

db_host = 'localhost'
db_port = 3306
db_user = 'root'
db_password = '2013'
db_name = 'web_fuzzing'

def connect_db():
    db = pymysql.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return db

# comment 테이블에 댓글 추가
def add_comment(user_uuid, post_uuid, comment_content):
    db = connect_db()
    sql = """
        INSERT INTO comment(user_uuid, post_uuid, comment_content)
        VALUES (%s, %s, %s);
    """ % user_uuid, post_uuid, comment_content
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    db.commit()


# comment 테이블에서 댓글 읽기 (post_uuid)
# 반환하는 열은 모든 열 (comment_uuid, user_uuid, post_uuid, comment_content, create_time, update_time)
# 정상 처리시 데이터를 딕셔너리들을 담은 배열로 반환, 오류 발생시 Error 반환
def get_comment(post_uuid):
    db = connect_db()
    sql = """
        SELECT comment_uuid, user_uuid, post_uuid, comment_content, create_time, update_time 
        FROM comment
        WHERE post_uuid = %s;
    """ % post_uuid
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except pymysql.Error as e:
        print(f'데이터베이스에서 댓글을 불러오는 중 오류 발생 -> {e}')
        return e