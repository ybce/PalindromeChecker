from app import get_conn

def create_all():
    c = get_conn()
    c.execute("CREATE TABLE `messages` ( "
              "`message_id` INTEGER PRIMARY KEY AUTOINCREMENT, "
              "`message` TEXT NOT NULL, "
              "`palindrome` INTEGER DEFAULT -1 );")

    c.commit()
    c.close()

def drop_all():
    c = get_conn()
    c.execute("DROP TABLE `messages`");
    c.commit()
    c.close()