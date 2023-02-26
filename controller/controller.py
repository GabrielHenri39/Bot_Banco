from model.models import Account , AccountDAO
import sqlite3


class AccountController:
    def __init__(self):
        self.dao = AccountDAO()

    def get_account(self, name):
        return self.dao.get_account(name)

    def add_account(self, name):
        account = Account(name)
        self.dao.insert_account(account)

    def convert(self, account, from_type, to_type, amount):
        if from_type == to_type:
            return False

        if from_type == 'bronze' and to_type == 'silver':
            if account.bronze < amount:
                return False
            account.bronze -= amount
            account.silver += amount * 50
        elif from_type == 'silver' and to_type == 'gold':
            if account.silver < amount:
                return False
            account.silver -= amount
            account.gold += amount * 500
        elif from_type == 'gold' and to_type == 'platinum':
            if account.gold < amount:
                return False
            account.gold -= amount
            account.platinum += amount * 5000
        else:
            return False

        self.dao.update_account(account)
        return True
    
    def transfer(self, sender, receiver, amount):
        if sender == receiver:
            return False

        sender_account = self.dao.get_account(sender)
        receiver_account = self.dao.get_account(receiver)

        if sender_account is None or receiver_account is None:
            return False

        if sender_account.bronze < amount:
            return False

        sender_account.bronze -= amount
        receiver_account.bronze += amount

        self.dao.update_account(sender_account)
        self.dao.update_account(receiver_account)

        return True
