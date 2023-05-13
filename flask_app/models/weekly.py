from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Weekly:
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
    def validate_weekly(weekly):
        is_valid = True
        if len(weekly['name']) - (weekly['name'].count(' ')) == 0:
            flash("Weekly name is required", 'weekly')
            is_valid = False
        elif len(weekly['name']) - (weekly['name'].count(' ')) < 2:
            flash("Weekly name requires at least 2 characters", 'weekly')
            is_valid = False
        elif len(weekly['name']) > 25:
            flash("Weekly name should be less than 25 characters", 'weekly')
            is_valid = False
        return is_valid
    @classmethod
    def add_weekly(cls, data):
        query = """INSERT INTO weeklies (name, category, priority, user_id, created_at, updated_at)
                VALUES (%(name)s, %(category)s, %(priority)s, %(user_id)s, NOW(), NOW());"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def complete_weekly(cls, data):
        query = """UPDATE weeklies
                SET category = %(category)s
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def revert_weekly(cls, data):
        query = """UPDATE weeklies
                SET category = %(category)s
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def all_for_one(cls, data):
        query = """SELECT * FROM weeklies 
                LEFT JOIN users
                ON weeklies.user_id = users.id
                WHERE users.id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        all_weeklies = []
        for daily in results:
            one_weekly = cls(daily)
            all_weeklies.append(one_weekly)
        return all_weeklies
    @classmethod
    def delete_weekly(cls, data):
        query = """DELETE FROM weeklies
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)
