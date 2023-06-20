a=[]
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime, date
import pandas as pd

today = str(date.today()).replace("-", "_")

mydb = mysql.connector.connect(host='localhost', user='root', password='NewOne', database='attendance_db')
cursor = mydb.cursor()

cursor.execute(f"SHOW COLUMNS FROM Student_Attendance_8 LIKE '{today}'")
result=cursor.fetchone()

if result:
    q0=f'ALTER TABLE Student_Attendance_8 DROP COLUMN {today}'
    cursor.execute(q0)

# q1 = 'CREATE TABLE Student_Attendance_8(Roll_Number int, Name varchar(100))'
# q2 = 'INSERT INTO Student_Attendance_8 VALUES (1, "Ishaan Gupta"), (2, "Jihan Chheda"),' \
#    '(3, "Shrikar Gaikar"), (4, "Sahil Gupta"), (5, "Jayant Nag Sai Vasa"),' \
#    '(6, "Bhavya Jain"),(7, "Kunal Pawar"), (8, "Ishan Naik"),' \
#    '(9, "Kartik Prajapati"), (10, "Akshay Vennikal")'
# cursor.execute(q1)
# cursor.execute(q2)

q3=f'ALTER TABLE Student_Attendance_8 ADD {today} INT'
cursor.execute(q3)

@auth.route('/')
def root():
    return render_template('login.html', user=None)

@auth.route('/view')
def see():
    cursor.execute("DESCRIBE Student_Attendance_8")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("SELECT * FROM Student_Attendance_8")
    data = cursor.fetchall()
    return render_template('attendance.html', columns=columns, data=data)

@auth.route('/todo')
def serve_todo():
    return render_template('todo.html')
        
@auth.route('/view_notice')
def view_notice():
    q_all = 'SELECT * FROM NOTICE ORDER BY n_id DESC '
    cursor.execute(q_all)
    data=cursor.fetchall()
    return render_template('viewnotice.html', data=data)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
 
        user = User.query.filter_by(email=email).first()
        if user:
            a.append(user.email)
            if user.email == 'tcet@gmail.com':
                if check_password_hash(user.password, password):
                    # flash('Logged in successfully!', category='success')
                    login_user(user, remember=False)
                    cursor.execute('SELECT * FROM Student_Attendance_8')
                    students = cursor.fetchall()   
                    return render_template('teacher.html', students=students)
                else:
                    flash('Incorrect password, try again.', category='error')
            elif user :
                if check_password_hash(user.password, password):
                    # flash('Logged in successfully!', category='success')
                    login_user(user, remember=False)

                    return render_template('index.html')
                else:
                    flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/home')
def home():
    if a[-1] == 'tcet@gmail.com':
        return render_template('teacher.html')
    else:
        return render_template('index.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/att')
def index():
    return render_template('index2.html')    

@auth.route('/attend', methods=['POST'])
def attend():
    attendance_list = []
    for i in range(1, 11):  # assuming there are 10 students in the table
        attendance_checkbox = request.form.get(f'attendance_checkbox_{i}')
        if attendance_checkbox == 'on':
            attendance_list.append(1)
        else:
            attendance_list.append(0)

        new_q = f"UPDATE Student_Attendance_8 SET {today}={attendance_list[i-1]} WHERE Roll_Number={i}"
        cursor.execute(new_q)

    mydb.commit()

    return redirect(url_for('auth.success'))

@auth.route('/success')
def success():
    return render_template('success.html')

@auth.route('/addnotice')
def addnotice():
    return render_template('notice.html')


@auth.route('/notice', methods=['POST'])
def notice():
    qn='SELECT * From notice ORDER BY n_id DESC LIMIT 1'
    cursor.execute(qn)
    res=cursor.fetchone()
    n=res[2]
    title=request.form.get('title')
    text=request.form.get('text')
    q19='INSERT INTO NOTICE values(%s, %s, %s)'
    cursor.execute(q19, (title, text, n+1))
    mydb.commit()
    return redirect(url_for('auth.success'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        contact_number = request.form.get('contact_number')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            a.append(email)
            new_user = User(email=email, first_name=first_name, contact_number=contact_number, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/addtimetable')
def addtimetable():
    return render_template("timetable.html")

@auth.route('/timetable', methods=['POST'])
def timetable():   
    times = request.form.getlist('time')
    mondays = request.form.getlist('monday')
    tuesdays = request.form.getlist('tuesday')
    wednesdays = request.form.getlist('wednesday')
    thursdays = request.form.getlist('thursday')
    fridays = request.form.getlist('friday') 

    q28='SELECT * FROM TIMETABLE'
    cursor.execute(q28)
    res=cursor.fetchall()
    if res:
        q32='TRUNCATE TABLE TIMETABLE'
        cursor.execute(q32)
        mydb.commit()

    for i in range(len(times)):
        sql = "INSERT INTO timetable (time, monday, tuesday, wednesday, thursday, friday) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (times[i], mondays[i], tuesdays[i], wednesdays[i], thursdays[i], fridays[i])
        cursor.execute(sql, values)
              
    mydb.commit()

    return redirect(url_for('auth.success'))

@auth.route('/viewtimetable')
def viewtimetable():
    cursor.execute("DESCRIBE timetable")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("SELECT * FROM timetable")
    data = cursor.fetchall()
    return render_template('viewtimetable.html', columns=columns, data=data) 

@auth.route('/addresult')
def addresult():
    return render_template("result.html")

@auth.route("/result", methods=['POST'])
def result():
    roll_nos = request.form.getlist('rollNo')
    names = request.form.getlist('name')
    subject1s = request.form.getlist('subject1')
    subject2s = request.form.getlist('subject2')
    subject3s = request.form.getlist('subject3')
    subject4s = request.form.getlist('subject4')
    subject5s = request.form.getlist('subject5')    

    for i in range(len(roll_nos)):
        sql = "INSERT INTO result (roll_no, name, sdm, dsa, bai, dmbi, python) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (roll_nos[i], names[i], subject1s[i], subject2s[i], subject3s[i], subject4s[i], subject5s[i])
        cursor.execute(sql, values)
              
    mydb.commit()

    return redirect(url_for('auth.success'))
    

@auth.route('/viewresult')
def viewresult():
    cursor.execute("DESCRIBE result")
    columns = [column[0] for column in cursor.fetchall()]
    cursor.execute("SELECT * FROM result")
    data = cursor.fetchall()
    return render_template('viewresult.html', columns=columns, data=data)    

   
