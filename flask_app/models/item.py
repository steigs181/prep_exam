from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import User
class Item:
    DB = "prep_exam_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.price = data['price']
        self.img_url = data['img_url']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO items (name, description,img_url, price, user_id)
        VALUES (%(name)s, %(description)s, %(img_url)s, %(price)s, 1 );"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM items
        LEFT JOIN users on items.user_id = user_id
        ;"""
        results = connectToMySQL(cls.DB).query_db(query)
        if not results:
            return []
        items = []
        for item in results:
            this_item = cls(item)
            data = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                "last_name": item ['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at']
            }
            this_item.owner = User(data)
            items.append(cls(item))
        return items
    
    @classmethod
    def get_one(cls, item_id):
        query  = "SELECT * FROM items WHERE id = %(id)s;"
        data = {'id': item_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return None
        return cls(results[0])


    @classmethod
    def update(cls,data):
        query = """UPDATE items 
                SET name %(name)s, description = %(description)s , img_url = %(img_url)s ,price = %(price)s  
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls, id):
        query  = "DELETE FROM items WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL(cls.DB).query_db(query, data)