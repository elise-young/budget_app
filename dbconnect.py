import psycopg2
account_name = 'demo account'
account_type = 3
onbudget = True
user_notes = 'savings'

def add_account(account_name,user_notes,onbudget,account_type):
    cur.execute("INSERT INTO accounts (name, notes, onbudget, type) VALUES('" + account_name + "','"  + user_notes + "','" + str(onbudget) + "'," + str(account_type) + ");")
    con.commit()

def add_transaction(inflow,outflow,memo,status,payee,accountid,transferid,flag,date,category):
    string_build = "INSERT INTO accounts (inflow,outflow,memo,status,payee,accountid,transferid,flag,date,category) VALUES('"
    #cur.execute(string_build +  + "','"   + ");")
    #con.commit()

con = psycopg2.connect(
    host = "localhost",
    database="my_budget",
    user="altdev",
    password="altdev"
)


cur = con.cursor()



cur.execute("SELECT * FROM accounts")
rows = cur.fetchall()
for r in rows:
    print(r)

con.commit()
cur.close()    
con.close()