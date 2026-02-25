from colorama import init, Fore, Style
from getpass import getpass
from tabulate import tabulate
import mysql.connector
import os
import time

def get_Seat():
    while True:
        try:
            seat=int(input("Enter the ID number of the student : "))
            return seat
        except ValueError:
            print(Fore.YELLOW + Style.BRIGHT+"⚠️⚠️...ONLY Integer values, pls."+Style.RESET_ALL)
def get_Name():
    while True:
        name=input("Enter the name of the Student : ")
        if name.replace(" ", "").isalpha():
            break
        else:
            print(Fore.YELLOW + Style.BRIGHT+"Alphabets are only allowed"+Style.RESET_ALL)
    return name

def Marks():
    subject=["Eng","Maths","Che","Bio","Phy"]
    values={}
    for sub in subject:
        while True:
            try:
                values[sub]=float(input(f"Enter the marks for {sub}: "))
                if 0<= values[sub] <=100:
                    break
                else:
                    print(Fore.YELLOW + Style.BRIGHT+"marks is allowed in 0-100 range only."+Style.RESET_ALL)
            except ValueError:
                print(Fore.YELLOW + Style.BRIGHT+"Enter only numberical values.."+Style.RESET_ALL)
    Mark=sum(values.values())
    total=len(subject)*100
    Per=round((Mark/total)*100,2)
    return Mark,Per

def grade(p):
    if p >= 90:
        return "A+"
    elif p >= 80:
        return "A"
    elif p >= 70:
        return "B+"
    elif p >= 60:
        return "B"
    elif p >= 50:
        return "C+"
    elif p >= 40:
        return "D"
    elif p >= 34:
        return "E"
    elif p >= 0:
        return "F"
    else:
        return "-"
def Insert(con,cur,s):
    seat=s
    name=get_Name()
    marks,per=Marks()
    gra=grade(per)
    query="insert into SMS(seat, name, Tmarks, Percentage, grade) values(%s, %s, %s, %s, %s)"
    data=[seat,name,marks,per,gra]
    cur.execute(query, data)
    con.commit()

def delete_record(con,cur,se):
    seat=se
    query="delete from SMS where seat=%s"
    cur.execute(query,(seat,))
    con.commit()

def update(con,cur,sw):
    seat=sw
    name=get_Name()
    Tmarks,per=Marks()
    gra=grade(per)
    query="update SMS set name=%s, Tmarks=%s, Percentage=%s, grade=%s where seat=%s"
    data=[name,Tmarks,per,gra,seat]
    cur.execute(query,data)
    con.commit()

def display(cur,query="select * from SMS"):
    cur.execute(query)
    res=cur.fetchall()
    if not res:
        print("No records found!!")
        return
    headers=[i[0] for i in cur.description]
    print(tabulate(res,headers=headers,tablefmt="grid"))

def search(cur):
    seat=get_Seat()
    query="select * from SMS where seat=%s"
    cur.execute(query,(seat,))
    res=cur.fetchall()
    if res:
        headers = [i[0] for i in cur.description]
        print(tabulate(res, headers=headers, tablefmt="grid"))
    else:
        print(" Records Not Found. Please ENTER RIGHT ID NUMBER......")

def loading(msg="Loading"):
    print(msg, end="")
    for _ in range(3):
        print(".", end="",flush=True)
        time.sleep(0.5)
    print("fetching data...")

def login(cur):
    for _ in range(3):
        user = input("Enter username: ")
        pwd = getpass("Enter password: ")
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pwd))
        if cur.fetchone():
            print(" Login successful!")
            return True
        else:
            print(" Invalid credentials.")
    print(" Too many failed attempts. Exiting...")
    return False
def clear_load():
    os.system('cls' if os.name == 'nt' else 'clear')
    loading()
    os.system('cls' if os.name == 'nt' else 'clear')

def record_checking(cur):
    while True:
        try:
            seat = int(input("Enter the seat number : "))
            if seat <= 0:
                print("Pls enter a positive number")
                continue
            break
        except ValueError:
            print("Pls enter numerical value...")
    cur.execute("select 1 from SMS where seat=%s",(seat,))
    return (True, seat) if cur.fetchone() else (False, seat)
def main():
    init(autoreset=True)
    con=None
    cur=None
    try:
        con=mysql.connector.connect(host="localhost", user="root", password="<Your_MYSQL_Password>", database="<Your_database_Name>")
        cur=con.cursor()

        if login(cur):
            while True:
                print("----------------------------------------------------------------------------")
                print(Fore.BLUE + Style.BRIGHT+"WELCOME TO STUDENT MANAGEMENT SYSTEM"+Style.RESET_ALL)
                print("----------------------------------------------------------------------------")
                print("\n1.Add Records\n2.Display Records\n3. Search Record\n4. Delete Record\n5. Update Record\n6. Toppers\n7. Exit")
                print("----------------------------------------------------------------------------")
                try:
                    ch=int(input("Choose an option : "))
                except ValueError:
                    print("Invalid entry. Pls enter in numerical value and upto the given range..")
                    continue
                if ch==1:
                    clear_load()
                    r,s = record_checking(cur)
                    if r==True:
                        print("Record already exist of this seat number!!")
                    else:
                        Insert(con,cur,s)
                        print( Fore.GREEN + Style.BRIGHT+"Records Added Successfully"+Style.RESET_ALL)
                elif ch==2:
                    clear_load()
                    display(cur,"select * from SMS order by seat ASC")
                elif ch==3:
                    clear_load()
                    search(cur)
                elif ch==4:
                    clear_load()
                    r,s = record_checking(cur)
                    if r==True:
                        delete_record(con,cur,s)
                    else:
                        print("Record don't exist of this ID, pls varify by checking the records manually.")
                elif ch==5:
                    clear_load()
                    r,s = record_checking(cur)
                    if r==True:
                        update(con,cur,s)
                    else:
                        print("record don't found to update!!")
                elif ch==6:
                    clear_load()
                    display(cur,"select * from SMS order by Percentage DESC")
                elif ch==7:
                    break
                else:
                    print(Fore.RED+Style.BRIGHT+"Invalid Choice...⚠️⚠️⚠️"+Style.RESET_ALL)
        else:
            print("Exiting system....")
    except mysql.connector.Error as e:
        print("Database connection failed ",e)
    finally:
        if cur:
            cur.close()
        if con:
            con.close()
if __name__ =="__main__":
    main()
