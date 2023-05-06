from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class Income:
    DB = 'billing'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.amount = data['amount']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @staticmethod
    def validate_income(income):
        is_valid = True
        if (len(income['name']) - (income['name'].count(' ')) == 0) and (len(income['amount']) - (income['amount'].count(' ')) == 0):
            flash("All fields required", 'income')
            is_valid = False
        elif len(income['name']) - (income['name'].count(' ')) == 0:
            flash("Income name is required", 'income')
            is_valid = False
        elif len(income['name']) - (income['name'].count(' ')) < 2:
            flash("Income name requires at least 2 characters", 'income')
            is_valid = False
        elif len(income['name']) - (income['name'].count(' ')) > 75:
            flash("Income name should be less than 75 characters", 'income')
            is_valid = False
        elif len(income['amount']) - (income['amount'].count(' ')) == 0:
            flash("Income amount is required", 'income')
            is_valid = False
        elif int(income['amount']) < 1:
            flash("Income amount should be a valid number", 'income')
            is_valid = False
        return is_valid
    @classmethod
    def add_income(cls, data):
        query = """INSERT INTO incomes(name, amount, user_id, created_at, updated_at)
                VALUES (%(name)s, %(amount)s, %(user_id)s, NOW(), NOW());"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def incomes_for_one(cls, data):
        query = """SELECT * FROM incomes
                LEFT JOIN users
                ON users.id = incomes.user_id
                WHERE users.id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        all_incomes = []
        for income in results:
            all_incomes.append(income)
            print(income)
        return all_incomes


