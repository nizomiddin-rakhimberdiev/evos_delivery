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
       
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            name VARCHAR(255),
            latitude REAL,
            longitude REAL,
            FOREIGN KEY(chat_id) REFERENCES users(chat_id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) UNIQUE
            )
                            ''')
        

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) UNIQUE,
            price INTEGER,
            description TEXT,
            image TEXT,
            category_id INTEGER, 
            FOREIGN KEY(category_id) REFERENCES categories(id)
                            )''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            products VARCHAR(255),
            total_price INTEGER,
            user_id INTEGER,
            phone_number VARCHAR(15),
            address VARCHAR(255)
                            )
        ''')

        self.con.commit()



    
        # self.con.close()

    def add_product(self, name, price, description, image, category_id):
        self.cursor.execute('INSERT INTO products (name, price, description, image, category_id) VALUES (?,?,?,?,?)', (name, price, description, image, category_id))
        self.con.commit()
        # self.con.close()


    def add_category(self, category):
        self.cursor.execute('INSERT INTO categories (name) VALUES (?)', (category,))
        self.con.commit()
        # self.con.close()    

    def get_categories(self):
        self.cursor.execute('SELECT * FROM categories')
        categories = self.cursor.fetchall()
        # self.con.close()
        return categories

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


    def add_address(self, user_id, name, latitude, longitude):
        self.cursor.execute('INSERT INTO addresses (chat_id, name, latitude, longitude) VALUES (?,?,?,?)',(user_id, name, latitude, longitude))
        self.con.commit()
        # self.con.close()

    def get_addresses(self, user_id):
        self.cursor.execute('SELECT name, latitude, longitude FROM addresses WHERE chat_id =?',(user_id,))
        addresses = self.cursor.fetchall()
        # self.con.close()
        return addresses
    

    def check_language(self, chat_id):
        self.cursor.execute("SELECT lang FROM users WHERE chat_id = ?", (chat_id,))
        result = self.cursor.fetchone()
        # print(result)
        return result[0] if result else None


    def get_products(self, category_name):
        self.cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
        category_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT name FROM products WHERE category_id = ?", (category_id,))
        products = self.cursor.fetchall()
        return products

    def get_product(self, name):
        self.cursor.execute("SELECT * FROM products WHERE name = ?", (name,))
        product = self.cursor.fetchall()
        # self.con.close()
        return product


    def delete_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS products')
        self.con.commit()
        # self.con.close()