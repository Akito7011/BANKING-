#importing sql module
import mysql.connector as mysql
#importing date from datetime to keep a record of all entries
from datetime import date
#connecting to the server
sql=mysql.connect(host="localhost",user="root",passwd="DASHINGFIST",database="BANK")
#checking whether system is online or not
if sql.is_connected()== True:
    print("systems online")
    cr=sql.cursor()
else :
    print("connection not established")
def front_page():
    print('ASCII BANK')
    input('ENTER TO GO TO MENU')
    menu()
#menu design
def menu():
    print('''    1:- CREATE ACCOUNT
    2:- LOGIN ACCOUNT
    3:- EXIT''')
    call()
# a call function to use menu items
def call():
    try:
        x=eval(input("press the code for the desired function: "))
        if x==1:
            Create()
        elif x==2:
            login()
        else:
            cr.close()
            sql.close()
            print('server terminated')
    except SyntaxError:
        print()
# a create function : used to create an account in bank
def Create():
    s=0
    t_id=0
    cr.execute('select Max(ID) from ACCOUNT')
    code=cr.fetchall()
    for i in code:#a check loop to determine if their is any data in server's database
        for j in i:
            print(j)
            if j==None:
                s=1204000
            else:
                s=int(j)+1
    F_name=input("enter  First_name: ")
    S_name=input("enter Second_name: ")
    DOB=input("enter enter Date Of Birth: ")
    State=input("enter State: ")
    City=input("enter City: ")
    Address=input('enter address line: ')
    P_no=eval(input('enter phone number: '))
    ACC_type=eval(input('Enter ACC tyep you want :1: share account, :2: individual account'))
    Pass=input('Enter Your Password: ')
    cr.execute('INSERT INTO ACCOUNT VALUES("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(F_name,S_name,DOB,State,City,Address,P_no,ACC_type,Pass,s))
    sql.commit()
    print('account created successfully: ')
    print('your bank ID is :',s)
    cr.execute('select Max(Trans_ID) from transaction')
    trans=cr.fetchall()
    for i in trans:
        for j in i:
            if j==None:
                t_id=1
            else:
                t_id=j+1
    today = date.today()
    cr.execute('insert into transaction values({},"{}","{}","{}","{}","{}")'.format(t_id,today,s,'deposit','via bank',int(input(':DEPOSIT MINIMUN OF 1000 INR:'))))
    sql.commit()
    print('transaction completed')
    menu()
#when user logs in .....this menu is shown
def log():
    print('''    1:- Withdraw
    2:- Deposit
    3:- transfer
    4:- Modify Details
    5:- logout''')
    x=eval(input('Enter your choice'))
    if x==1:
        withdraw()
    elif x==2:
        Deposit()
    elif x==3:
        transfer()
    elif x==4:
        modify()
    else: 
        print("Logout successfully")
        menu()
def login():#login function 
    global Id
    Id=int(input('enter you id'))
    Pass=input('enter your password')
    cr.execute("select password from account where id={}".format(Id))
    data=cr.fetchall()
    for i in data:
        for j in i:
            if j==Pass:
                print('login successful')
                input('press enter to continue')
                log()
            else:
                print(''''
                      password is wrong
                      :Returning to login page:
                      ''')
                login()
def withdraw():
    balance=0
    t_id=0
    s=input('Withdraw Medium: ')
    withdraw=eval(input('enter amount to withdraw: '))
    cr.execute('select Max(Trans_ID) from transaction ')
    trans=cr.fetchall()
    for i in trans:
        for j in i:
            if j==None:
                t_id=1
            else:
                t_id=j+1
    today = date.today()
    cr.execute(' select max(trans_id),balance from transaction where id={} group by balance order by trans_id desc'.format(Id))
    x=cr.fetchall()
    balance=int(x[0][1])
    if withdraw<balance:
        cr.execute("insert into transaction values({},'{}',{},'{}','{}',{})".format(t_id,today,Id,'withdraw',s,balance-withdraw))
        sql.commit()
        print("transaction completed")
    else:
        print(':funds not suuficient:')
        print("returning to account screen")
        log()
def Deposit():
    balance=0
    t_id=0
    s=input(':Deposit Medium: ')
    deposit=eval(input('enter amount to deposit: '))
    cr.execute('select Max(Trans_ID) from transaction ')
    trans=cr.fetchall()
    for i in trans:
        for j in i:
            if j==None:
                t_id=1
            else:
                t_id=j+1
    today = date.today()
    cr.execute(' select max(trans_id),balance from transaction where id={} group by balance order by trans_id desc'.format(Id))
    x=cr.fetchall()
    balance=int(x[0][1])
    if deposit>0:
        cr.execute("insert into transaction values({},'{}',{},'{}','{}',{})".format(t_id,today,Id,'deposit',s,balance+deposit))
        sql.commit()
        print('Transaction Successful')
        log()
    else:
        print(':invalid input:')
        print("returning to account screen")
        log()
def transfer():#it keeps a check on transactions
    balance1=0
    balance2=0
    t_id=0
    s=input('transfer Medium: ')
    tansfer=eval(input('enter amount to tansfer: '))
    ID=int(input("Enter account ID to tansfer money to it: "))
    cr.execute('select Max(Trans_ID) from transaction')
    trans=cr.fetchall()
    for i in trans:
        for j in i:
            if j==None:
                t_id=1
            else:
                t_id=j+1
    today = date.today()
    cr.execute(' select max(trans_id),balance from transaction where id={} group by balance order by trans_id desc'.format(Id))
    x=cr.fetchall()
    balance1=int(x[0][1])
    print(balance1)
    cr.execute(' select max(trans_id),balance from transaction where id={} group by balance order by trans_id desc'.format(ID))
    y=cr.fetchall()
    balance2=int(y[0][1])
    if tansfer<balance1:
        cr.execute("insert into transaction values('{}','{}','{}','{}','{}','{}')".format(t_id,today,Id,'tranfer_out',s,balance1-tansfer))
        sql.commit()
        cr.execute("insert into transaction values('{}','{}','{}','{}','{}','{}')".format(t_id+1,today,ID,'tranfer_in',s,balance2+tansfer))
        sql.commit()
        print('transaction done')
        log()
    else:
        print(':funds not suuficient:')
        print("returning to account screen")
        log()
def modify():#it helpes the user to modify data
    try:
        print(':USE THE FIELD GIVEN BELOW AS REFERNCE:')
        print(''': | State    |
                   | City     |
                   | Address  |
                   | Phone_NO |
                   | Password :''')
        mod=input("enter field name as shown above to modify: ")
        modify=input('enter updated data')
        if mod=='Phone_NO':
            cr.execute('update account set {}="{}" where ID={}'.format(mod,int(modify),Id))
            sql.commit()
            log()
        elif mod=='State'or'city'or'address'or'password':
            cr.execute('update account set {}="{}" where ID={}'.format(mod,modify,Id))
            sql.commit
            log()
    except:
        print('invalid data .returning to home screen')
        menu()
front_page() 