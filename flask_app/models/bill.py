from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import datetime 
from dateutil.relativedelta import relativedelta

class Bill:
    DB = 'billing'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.amount = data['amount']
        self.due_day = data['due_day']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.til_due = None
    @staticmethod
    def validate_bill(bill):
        is_valid = True
        if (len(bill['name']) - (bill['name'].count(' ')) == 0) and (len(bill['amount']) - (bill['amount'].count(' ')) == 0):
            flash("All fields required", 'bill')
            is_valid = False
        elif len(bill['name']) - (bill['name'].count(' ')) == 0:
            flash("Bill name is required", 'bill')
            is_valid = False
        elif len(bill['name']) - (bill['name'].count(' ')) < 2:
            flash("Bill name requires at least 2 characters", 'bill')
            is_valid = False
        elif len(bill['name']) - (bill['name'].count(' ')) > 40:
            flash("Bill name should be less than 40 characters", 'bill')
            is_valid = False
        elif len(bill['amount']) - (bill['amount'].count(' ')) == 0:
            flash("Bill amount is required", 'bill')
            is_valid = False
        elif int(bill['amount']) < 1:
            flash("Bill amount should be a valid number", 'bill')
            is_valid = False
        return is_valid
    @classmethod
    def add_bill(cls, data):
        query = """INSERT INTO bills (name, amount, due_day, user_id, created_at, updated_at)
                VALUES (%(name)s, %(amount)s, %(due_day)s, %(user_id)s, NOW(), NOW());"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def edit_bill(cls, data):
        query = """UPDATE bills
                SET name = %(name)s,
                amount = %(amount)s,
                due_day = %(due_day)s
                WHERE id = %(id)s"""
        return connectToMySQL(cls.DB).query_db(query, data)
    @classmethod
    def get_by_id(cls, data):
        query = """SELECT * FROM bills 
                WHERE id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    @classmethod
    def scan_dates(cls):
        query = """SELECT * FROM bills
                LEFT JOIN users 
                ON users.id = bills.user_id"""
        return connectToMySQL(cls.DB).query_db(query)
    @classmethod
    def bills_for_one(cls, data):
        query = """SELECT * FROM bills
                LEFT JOIN users
                ON users.id = bills.user_id
                WHERE users.id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        all_bills = []
        for bill in results:
            this_bill = cls(bill)
            today = datetime.date.today()
            dueDay = bill['due_day']
            dayDue = datetime.date(today.year, today.month, dueDay)
            if today.day > dayDue.day:
                dueDate = dayDue + relativedelta(months=1)
            else:
                dueDate = dayDue
            daysLeft = (dueDate - today).days
            print(daysLeft)
            this_bill.til_due = daysLeft
            all_bills.append(this_bill)
        return all_bills
    @classmethod
    def delete_bill(cls, data):
        query = """DELETE FROM bills
                WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)
