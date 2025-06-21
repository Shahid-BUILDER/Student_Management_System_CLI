from colorama import init, Fore, Style
from tabulate import tabulate
import mysql.connector
import os
import time
init(autoreset=True)
con=mysql.connector.connect(host="localhost", user="root", password="<Your_MYSQL_Password", database="shahid")
print(con)
cur=con.cursor()

def Get():
    seat=int(input("Enter the ID Number of Student : "))
    name=input("Enter the name of the Student : ")
    return seat,name

def Marks():
    Eng=float(input("Enter the marks of English : "))
    Maths=float(input("Enter the Marks of Maths : "))
    Che=float(input("Enter the Marks of Chemistry : "))
    Bio=float(input("Enter the Marks of Biology : "))
    Phy=float(input("Enter the Marks of Physics : "))
    Marks=float(Eng+Maths+Che+Phy+Bio)
    Per=float((Marks/500)*100)
    return Marks,Per
def grade(p):
    if p>=89 and p<=100:
        gra="A+"
    elif p>=80 and p<=89:
        gra="A"
    elif p>=70 and p<=79:
        gra="B+"
    elif p>=60 and p<=69:
        gra="B"
    elif p>=50 and p<=59:
        gra="C+"
    elif p>=40 and p<=49:
        gra="D"
    elif p>=34 and p<=39:
        gra="E"
    elif p>=0 and p<=33:
        gra="F"
    else:
        print(Fore.YELLOW + Style.BRIGHT+"Percentage is not valid!!⚠️⚠️"+Style.RESET_ALL)
    return gra
def Insert():
    seat,name=Get()
    marks,per=Marks()
    gra=grade(per)
    query="insert into SMS(seat, name, Tmarks, Percentage, grade) values(%s, %s, %s, %s, %s)"
    data=[seat,name,marks,per,gra]
    cur.execute(query, data)
    con.commit()

def del01():
    seat,_=Get()
    query="delete from SMS where seat=%s"
    cur.execute(query,(seat,))
    con.commit()

def update():
    seat,name= Get()
    Tmarks,per=Marks()
    gra=grade(per)
    query="update SMS set name=%s, Tmarks=%s, Percentage=%s, grade=%s where seat=%s"
    data=[name,Tmarks,per,gra,seat]
    cur.execute(query,data)
    con.commit()
def display(query="select * from SMS"):
    cur.execute(query)
    res=cur.fetchall()
    headers=[i[0] for i in cur.description]
    print(tabulate(res,headers=headers,tablefmt="grid"))
def search():
    seat,_=Get()
    query="select * from SMS where seat=%s"
    cur.execute(query,(seat,))
    res=cur.fetchall()
    if res:
        for i in res:
            print(i)
    else:
        print(" Records Not Found. Please ENTER RIGHT ID NUMBER......")
def loading(msg="Loading"):
    print(msg, end="")
    for _ in range(3):
        print(".", end="",flush=True)
        time.sleep(0.5)
    print("fetching data...")
def login():
    for _ in range(3):
        user = input("Enter username: ")
        pwd = input("Enter password: ")
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pwd))
        if cur.fetchone():
            print(" Login successful!")
            return True
        else:
            print(" Invalid credentials.")
    print(" Too many failed attempts. Exiting...")
    return False
if login():
    while(True):
        print("----------------------------------------------------------------------------")
        print(Fore.BLUE + Style.BRIGHT+"WELCOME TO STUDENT MANAGEMENT SYSTEM"+Style.RESET_ALL)
        print("----------------------------------------------------------------------------")
        print("\n1.Add Records\n2.Display Records\n3. Search Record\n4. Delete Record\n5. Update Record\n6. Toppers\n7. Exit")
        print("----------------------------------------------------------------------------")
        ch=int(input("Choose an option : "))
        if ch==1:
            os.system("cls")
            loading()
            os.system("cls")
            Insert()
            print( Fore.GREEN + Style.BRIGHT+"Records Added Successfully"+Style.RESET_ALL)
        elif ch==2:
            os.system("cls")
            loading()
            os.system("cls")
            display("select * from SMS order by seat ASC")
        elif ch==3:
            os.system("cls")
            loading()
            os.system("cls")
            search()
        elif ch==4:
            os.system("cls")
            loading()
            os.system("cls")
            del01()
        elif ch==5:
            os.system("cls")
            loading()
            os.system("cls")
            update()
        elif ch==6:
            os.system("cls")
            loading()
            os.system("cls")
            display("select * from SMS order by Percentage DESC")
        elif ch==7:
            break
        else:
            print(Fore.RED+Style.BRIGHT+"Invalid Choice...⚠️⚠️⚠️"+Style.RESET_ALL)
else:
    exit()
