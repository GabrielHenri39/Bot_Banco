import sqlite3

class PlayerAccount:
    def __init__(self, name):
        self.name = name
        self.bronze = 0
        self.silver = 0
        self.gold = 0
        self.platinum = 0

    def save(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?)', 
            (self.name, self.bronze, self.silver, self.gold, self.platinum))
        conn.commit()
        conn.close()

class AccountDAO:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS accounts
                    (name text primary key, bronze integer, silver integer, gold integer, platinum integer)''')
        self.conn.commit()

    def add_account(self, name):
        account = PlayerAccount(name)
        account.save()

    def get_account(self, name):
        self.c.execute('SELECT * FROM accounts WHERE name = ?', (name,))
        row = self.c.fetchone()
        if row is None:
            return None
        account = PlayerAccount(row[0])
        account.bronze = row[1]
        account.silver = row[2]
        account.gold = row[3]
        account.platinum = row[4]
        return account

    def update_account(self, account):
        account.save()

    def delete_account(self, name):
        self.c.execute('DELETE FROM accounts WHERE name = ?', (name,))
        self.conn.commit()

    def close(self):
        self.conn.close()


class Account:
    def __init__(self, bronze=0, plata=0, ouro=0, platinha=0):
        self.bronze = bronze
        self.plata = plata
        self.ouro = ouro
        self.platinha = platinha

    def deposit(self, amount, currency):
        if currency == 'bronze':
            self.bronze += amount
        elif currency == 'plata':
            self.plata += amount
        elif currency == 'ouro':
            self.ouro += amount
        elif currency == 'platinha':
            self.platinha += amount

    def withdraw(self, amount, currency):
        if currency == 'bronze':
            if amount > self.bronze:
                return False
            else:
                self.bronze -= amount
                return True
        elif currency == 'plata':
            if amount > self.plata:
                return False
            else:
                self.plata -= amount
                return True
        elif currency == 'ouro':
            if amount > self.ouro:
                return False
            else:
                self.ouro -= amount
                return True
        elif currency == 'platinha':
            if amount > self.platinha:
                return False
            else:
                self.platinha -= amount
                return True

    def get_balance(self, currency):
        if currency == 'bronze':
            return self.bronze
        elif currency == 'plata':
            return self.plata + self.bronze * 50
        elif currency == 'ouro':
            return self.ouro + self.plata * 500 + self.bronze * 50 * 500
        elif currency == 'platinha':
            return self.platinha + self.ouro * 5000 + self.plata * 500 * 5000 + self.bronze * 50 * 500 * 5000
    def total_balance(self):
        return self.bronze + self.silver*50 + self.gold*500 + self.platinum*5000