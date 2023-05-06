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
    def validate_income(daily):
        is_valid = True
        if len(daily['name'] - (daily['name'].count(' '))) == 0:
            flash("Daily reminder name is required")
            is_valid = False
        elif len(daily['name'] - (daily['name'].count(' '))) < 2:
            flash("Daily reminder name requires at least 2 characters")
            is_valid = False
        elif len(daily['name'] - (daily['name'].count(' '))) > 150:
            flash("Daily reminder name should be less than 150 characters")
            is_valid = False
        return is_valid
    @classmethod
    def add_daily(cls, data):
        query = """INSERT INTO dailies (name, category, priority, user_id, created_at, updated_at)
                VALUES (%(name)s, %(category)s, %(priority)s, %(user_id)s, NOW(), NOW());"""
        return connectToMySQL(cls.DB).query_db(query, data)
