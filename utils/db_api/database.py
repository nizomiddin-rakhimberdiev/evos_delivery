import sqlite3


class Database:
    def __init__(self):
        self.con = sqlite3.connect('evos.db')
        self.cursor = self.con.cursor()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            lang VARCHAR(3),
            contact VARCHAR(20)
        )
        ''')
        self.con.commit()
        # self.con.close()

    def insert_user(self, chat_id):
        self.cursor.execute('INSERT INTO users (chat_id,lang) VALUES (?, ?)', (chat_id,"ru"))
        self.con.commit()
        # self.con.close()

    def get_contact(self, chat_id):
        self.cursor.execute('SELECT contact FROM users WHERE chat_id = ?', (chat_id,))
        contact = self.cursor.fetchone()
        # self.con.close()
        if contact:
            return contact[0]
        return None
    

    def update_user(self, chat_id, contact):
        self.cursor.execute('UPDATE users SET contact = ? WHERE chat_id =?', (contact, chat_id))
        self.con.commit()
        # self.con.close()

    def all_chat_id(self):
        self.cursor.execute('SELECT chat_id FROM users')
        chat_id = [i[0] for i in self.cursor.fetchall()]
        # self.con.close()
        return chat_id

    def change_lng(self, user_id,lng):
        self.cursor.execute('UPDATE users SET lang = ? WHERE chat_id= ?',(lng,user_id,))
        self.con.commit()
        # self.con.close()

    def get_lng(self, user_id):
        self.cursor.execute('SELECT lang from users WHERE chat_id = ?',(user_id,))
        result = self.cursor.fetchone()
        print(result)
        # self.con.close()
        return result[0]



    