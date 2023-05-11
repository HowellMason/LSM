from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Daily:
    DB = 'billing'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.category = data['category']
        self.priority = data['priority']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @staticmethod
    def validate_daily(daily):
        is_valid = True
        if len(daily['name']) - (daily['name'].count(' ')) == 0:
            flash("Daily name is required", "daily")
            is_valid = False
        elif len(daily['name']) - (daily['name'].count(' ')) < 2:
            flash("Daily name requires at least 2 characters", "daily")
            is_valid = False
        elif len(daily['name']) > 25:
            flash("Daily name should be less than 25 characters", "daily")
            is_valid = False
        return is_valid
    @classmethod
    def add_daily(cls, data):
        query = """INSERT INTO dailies (name, category, priority, user_id, created_at, updated_at)
                VALUES (%(name)s, %(category)s, %(priority)s, %(user_id)s, NOW(), NOW());"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def revert_daily(cls, data):
        query = """UPDATE dailies
                SET category = %(category)s
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def complete_daily(cls, data):
        query = """UPDATE dailies
                SET category = %(category)s
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def all_for_one(cls, data):
        query = """SELECT * FROM dailies 
                LEFT JOIN users
                ON dailies.user_id = users.id
                WHERE users.id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        all_dailies = []
        for daily in results:
            one_daily = cls(daily)
            all_dailies.append(one_daily)
        return all_dailies
    @classmethod
    def delete_daily(cls, data):
        query = """DELETE FROM dailies
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)
