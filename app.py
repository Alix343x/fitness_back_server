#from first_app import app , db
from flask import Flask, render_template , request, redirect, make_response, session, url_for, jsonify
from flask_cors import CORS, cross_origin
import os
import sqlite3
import time
from datetime import datetime,timedelta
import json

#path = os.path.join("imagesdb")

def d_empty(d):
    if d != None and d != "" and d != "null":
        return False
    else : return True

def d_in_w(d1,d2,d3,d4,d5,d6,d7):
    days = 0
    if d_empty(d1) == False:
        days = days + 1
    if d_empty(d2) == False:
        days = days + 1
    if d_empty(d3) == False:
        days = days + 1
    if d_empty(d4) == False:
        days = days + 1
    if d_empty(d5) == False:
        days = days + 1
    if d_empty(d6) == False:
        days = days + 1
    if d_empty(d7) == False:
        days = days + 1
    return days

def exer_number(d1,d2,d3,d4,d5,d6,d7):
    exer_num = 0
    if d_empty(d1) != False:
        exer_num = len(d1) + exer_num
    if d_empty(d2) == False:
        exer_num = len(d2) + exer_num
    if d_empty(d3) == False:
        dexer_num = len(d3) + exer_num
    if d_empty(d4) == False:
        exer_num = len(d4) + exer_num
    if d_empty(d5) == False:
        exer_num = len(d5) + exer_num
    if d_empty(d6) == False:
        exer_num = len(d6) + exer_num
    if d_empty(d7) == False:
        exer_num = len(d7) + exer_num
    return exer_num


def id_gen(id,Table):
    cursor.execute(f"SELECT MAX({id}) FROM {Table}")
    max_id = cursor.fetchone()[0]
    if max_id == None : 
        id = 1 
        return id
    else: 
        id = max_id + 1
        return id

def edit_input(data):
    set_value = ""
    for value in data.items():
        if value[1] != "" and value[1] != "null" and type(value[1]) == str:
            set_value = set_value + f', {value[0]} = \'{value[1]}\''
        elif value[1] != "" and value[1] != "null" and type(value[1]) == int:
            set_value = set_value + f', {value[0]} = {value[1]}'
    set_value = set_value[2:]
    return set_value

def duplicate(tablename,columnname,value):
    if type(value) == str:
        cursor.execute(f'''SELECT COUNT(*) FROM {tablename} WHERE {columnname}='{value}' ''')
    elif type(value) == int:
        cursor.execute(f'''SELECT COUNT(*) FROM {tablename} WHERE {columnname}={value} ''')
    rep_value = cursor.fetchone()[0]
    if rep_value == 1 : return 1
    return 0

def logged():
    if 'user_id' in session:
        return
    else :
        return 0
def logged_trainee():
    check = session["type"]
    if check == "T":
        return
    else:
        return 0
def logged_coach():
    check = session["type"]
    if check == "C":
        return
    else:
        return 0


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/Downloads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#SecretKey
app.secret_key = "applejuice"
#Database Creation
DATABASE_FILE = 'app.db'
connection = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id BIGINT PRIMARY KEY,
        account_type TEXT,
        password TEXT,
        full_name TEXT,
        phone_number TEXT,
        pimage text,
        favorite_exers text,
        favorite_plans text,
        email TEXT
        
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS trainee (
        tid int,
        height int,
        weight int,
        desired_weight int,
        gender text,
        pref_time text,
        like_tags text,
	    ssplan_id int,
	    csplan_id int,
        FOREIGN KEY (tid) REFERENCES users(id),
        FOREIGN KEY (ssplan_id) REFERENCES _plan(id),
        FOREIGN KEY (csplan_id) REFERENCES _plan(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS coach (
        cid int not null,
	    speciality TEXT,
        experience int,
        price int,
        avalaible text,
        pref_tags text,
        description text,
        FOREIGN KEY (cid) REFERENCES users(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS coach_trainee (
        tid int not null,
        cid int not null,
        startdate text,
        enddate text,
        setpid int,
        payid int,
        FOREIGN KEY (tid) REFERENCES users(id),
        FOREIGN KEY (cid) REFERENCES users(id),
        FOREIGN KEY (payid) REFERENCES payment(payid)
    )
''')
"""
cursor.execute('''
    CREATE TABLE IF NOT EXISTS payment (
        payid int not null PRIMARY KEY,
        _dateTime datetime,
        amount int
    )
''')
"""
cursor.execute('''  
    CREATE TABLE IF NOT EXISTS _plan (
        pid INTEGER PRIMARY KEY,
        creator_id int ,
        title TEXT,
	    difficulty int,
        tags TEXT,
        Sat_excs TEXT,
	    Sun_excs TEXT,
	    Mon_excs TEXT,
	    Tue_excs TEXT,
	    Wed_excs TEXT,
	    Thr_excs TEXT,
	    Fri_excs TEXT,
        pimage_address TEXT,
        days_in_week int,
	    exercise_number int,
        FOREIGN KEY (creator_id) REFERENCES users(id)
    )
''')

cursor.execute('''  
    CREATE TABLE IF NOT EXISTS _plans_days (
        pid int,
        day text,
        excs TEXT,
        sets text,
        FOREIGN KEY (pid) REFERENCES _plans(pid)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercise (
	    eid int PRIMARY KEY,
        creator_id int,
	    title TEXT,
        difficulty int,
	    main_muscles TEXT,
	    sub_muscles TEXT,
        stages TEXT,	    
        main_muscles_eimage_address TEXT,
        sub_muscles_eimage_address TEXT,
        summary TEXT,
	    weight_numbers_males TEXT,
        weight_numbers_females TEXT,
        ispublic TEXT,
        FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE RESTRICT
    )
''')

connection.commit()


@app.route("/")
@cross_origin(origin='*')
def FirstPage():
    if session.get("user_name") and session.get("password"):
        if session.get("type"):    
            if session.get("type") == 'T':
                return redirect('/trainee_panel')
            elif session.get("type") == 'C':
                return redirect('/coach_panel')
            else:
                return "oh oh"
    else:
        return "Home"

from werkzeug.utils import secure_filename

#upload must be checked
@app.route('/api/upload', methods=['POST', 'GET'])
# API to upload file
def fileUpload():
    if request.method == 'POST':
        file = request.files.getlist('file')
        for f in file:
            filename = secure_filename(f.filename)
            if allowedFile(filename):
                f.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                return jsonify({'message': 'File type not allowed'}), 400
        return jsonify({"name": filename, "status": "success"})
    else:
        return jsonify({"status": "failed"})

@app.route('/api/upload/profileimage', methods=['POST', 'GET'])
# API to upload file
def pimageUpload():
    if request.method == 'POST':
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        if allowedFile(filename):
            des = os.path.join(UPLOAD_FOLDER, filename)
            file.save(des)
            cursor.execute(f'''UPDATE users (pimage)
                           VALUES ('{des}') ''')
            return jsonify({"name": filename, "status": "success"})
        
        else:
            return jsonify({'message': 'File type not allowed'}), 400
    else:
        return jsonify({"status": "failed"})

@app.route('/api/upload/exerimage', methods=['POST', 'GET'])
# API to upload file
def eimageUpload():
    if request.method == 'POST':
        file = request.files.getlist('file')
        for f in file:
            filename = secure_filename(f.filename)
            if allowedFile(filename):
                f.save(os.path.join(UPLOAD_FOLDER, filename))
            else:
                return jsonify({'message': 'File type not allowed'}), 400
        return jsonify({"name": filename, "status": "success"})
    else:
        return jsonify({"status": "failed"})

@app.route("/api/signup-control" , methods=["POST","OPTIONS"]) #changed only needs sending image func
@cross_origin(origin='*')
def signup_control():
    id = request.json.get("id")
    account_type = request.json.get("account_type")
    password = request.json.get("password")
    repassword = request.json.get("repassword")
    if password != repassword : return jsonify({"error": "differ on pass and repass"})
    full_name = request.json.get("full_name")
    phone_number = request.json.get("phone_number")
    email = request.json.get("email")
    try:
        if duplicate("users","id",id) == 1 : return jsonify({"error": "id duplicate"})
        if duplicate("users","phone_number",phone_number) == 1 : return jsonify({"error": "phone duplicate"})
        if duplicate("users","email",email) == 1 : return jsonify({"error": "email duplicate"})
        cursor.execute(f"""INSERT INTO users (id, account_type, password, full_name, phone_number, email,favorite_plans, favorite_exers) 
                       VALUES ({id}, "{account_type}", "{password}", "{full_name}", "{phone_number}", "{email}","null","null")""")
        connection.commit()
        if account_type == "T":
            tid = id
            height = request.json.get("height")
            weight = request.json.get("weight")
            desired_weight = request.json.get("desired_weight")
            
            gender = request.json.get("gender")
            pref_time = request.json.get("pref_time")
            like_tags = request.json.get("like_tags")

            pref_time = json.dumps(pref_time)
            like_tags = json.dumps(like_tags)

            cursor.execute(f'''INSERT INTO trainee (tid,height,weight,desired_weight,gender,pref_time,like_tags)
                           VALUES({tid},{height},{weight},{desired_weight},'{gender}','{pref_time}','{like_tags}')''')
            connection.commit()
            
            #login after sign up
            
            session["user_id"] = id
            session["type"] = account_type

            cursor.execute(f'''SELECT * FROM trainee WHERE tid={id}''')
            trainee_result = cursor.fetchone()

            height = trainee_result[1]
            weight = trainee_result[2]
            desired_weight = trainee_result[3]
            gender = trainee_result[4]

            pref_time = trainee_result[5]
            pref_time = json.loads(pref_time)

            like_tags = trainee_result[6]
            like_tags = json.loads(like_tags)

            return jsonify({"msg" : "trainee sign up sucess",
                            "panel" : "trainee",
                            "id" : id,
                            "account_type" : account_type,
                            "full_name" : full_name,
                            "phone_number" : phone_number,
                            "email" : email,
                            "height" : height,
                            "weight" : weight,
                            "desired_weight" : desired_weight,
                            "gender" : gender,
                            "like_tags" : like_tags,
                            "pref_time" : pref_time})

        elif account_type == "C":
            cid = id
            speciality = request.json.get("speciality")
            experience = request.json.get("experience")
            price = request.json.get("price")
            avalaible = request.json.get("avalaible")
            pref_tags = request.json.get("pref_tags")
            description = request.json.get("description")

            pref_tags = json.dumps(pref_tags)

            cursor.execute(f'''INSERT INTO coach (cid,speciality,experience,price,avalaible,pref_tags,description)
                           VALUES({cid},'{speciality}',{experience},{price},'{avalaible}','{pref_tags}','{description}')''')
            connection.commit()

            #login after sign up

            session["user_id"] = id
            session["type"] = account_type

            cursor.execute(f'''SELECT * FROM coach WHERE cid={id}''')
            coach_result = cursor.fetchone()

            speciality = coach_result[1]
            experience = coach_result[2]
            price = coach_result[3]
            available = coach_result[4]

            pref_tags = coach_result[5]
            pref_tags = json.loads(pref_tags)
            
            description = coach_result[6]


            return jsonify({"msg" : "coach sign up sucess",
                            "panel" : "coach",
                            "id" : id,
                            "account_type" : account_type,
                            "full_name" : full_name,
                            "phone_number" : phone_number,
                            "email" : email,
                            "speciality" : speciality,
                            "experience" : experience,
                            "price" : price,
                            "available" : available,
                            "pref_tags" : pref_tags,
                            "description" : description})

    except Exception as ex:
        error = str(ex)
        return jsonify({"error": {error}})

        
'''
    thefile = request.files["file"]
    path = os.path.join("Profilepics")
    #add file path to db
    if checkfileformat(thefile.filename):
        try:
            goal_path = os.path.join(path, thefile.filename)
            thefile.save(goal_path)
        except Exception as ex:
            ex = str(ex)
            return jsonify({"error": {ex}})
    else:
        return jsonify({"error": "not allowed format"})
'''
@app.route("/api/signin-control" , methods=["POST"])
def signin_control():

    id = request.json.get("id")
    password = request.json.get("password")

    cursor.execute(f'''SELECT COUNT(*) 
                       FROM users 
                       WHERE id={id} AND password='{password}' ''')
    count = cursor.fetchone()[0]
    if count == 1:
        cursor.execute(f'''SELECT * 
                           FROM users 
                           WHERE id='{id}' AND password='{password}' ''')
        user_result = cursor.fetchone()
        id = user_result[0]
        _type = user_result[1]

        session["user_id"] = id
        session["type"] = _type

        id = id
        account_type = _type
        full_name = user_result[3]
        phone_number =  user_result[4]
        email = user_result[6]

        if _type == "T":
            cursor.execute(f'''SELECT * FROM trainee WHERE tid={id}''')
            trainee_result = cursor.fetchone()

            height = trainee_result[1]
            weight = trainee_result[2]
            desired_weight = trainee_result[3]
            gender = trainee_result[4]

            pref_time = trainee_result[5]
            pref_time = json.loads(pref_time)

            like_tags = trainee_result[6]
            like_tags = json.loads(like_tags)

            return jsonify({"panel" : "trainee",
                            "id" : id,
                            "account_type" : account_type,
                            "full_name" : full_name,
                            "phone_number" : phone_number,
                            "email" : email,
                            "height" : height,
                            "weight" : weight,
                            "desired_weight" : desired_weight,
                            "gender" : gender,
                            "like_tags" : like_tags,
                            "pref_time" : pref_time})
        elif _type == "C":
            cursor.execute(f'''SELECT * FROM coach WHERE cid={id}''')
            coach_result = cursor.fetchone()

            speciality = coach_result[1]
            experience = coach_result[2]
            price = coach_result[3]
            available = coach_result[4]

            pref_tags = coach_result[5]
            pref_tags = json.loads(pref_tags)
            
            description = coach_result[6]


            return jsonify({"panel" : "coach",
                            "id" : id,
                            "account_type" : account_type,
                            "full_name" : full_name,
                            "phone_number" : phone_number,
                            "email" : email,
                            "speciality" : speciality,
                            "experience" : experience,
                            "price" : price,
                            "available" : available,
                            "pref_tags" : pref_tags,
                            "description" : description})
        else :
            return jsonify({"error": "no type account"})
    else:
        return jsonify({"error": "the account doesn't exist"})

@app.route("/api/logout-control")
def logout_control():
    session.clear()
    return jsonify({"msg" : "session cleard",
                    "logout" : True})

#-----------------profile--------------------

@app.route('/api/profile') #KINDA COMPLETE
def user_panel_profile():
    if logged() == 0:return jsonify({"error": "not logged in"})
    id = session["user_id"]
    cursor.execute(f'''SELECT * 
                        FROM users 
                        WHERE id='{id}' ''')
    user_result = cursor.fetchone()
    id = user_result[0]
    _type = user_result[1]

    id = id
    account_type = _type
    full_name = user_result[3]
    phone_number =  user_result[4]
    email = user_result[6]

    if _type == "T":
        cursor.execute(f'''SELECT * FROM trainee WHERE tid={id}''')
        trainee_result = cursor.fetchone()

        height = trainee_result[1]
        weight = trainee_result[2]
        desired_weight = trainee_result[3]
        gender = trainee_result[4]

        pref_time = trainee_result[5]
        pref_time = json.loads(pref_time)

        like_tags = trainee_result[6]
        like_tags = json.loads(like_tags)

        return jsonify({"panel" : "trainee",
                        "id" : id,
                        "account_type" : account_type,
                        "full_name" : full_name,
                        "phone_number" : phone_number,
                        "email" : email,
                        "height" : height,
                        "weight" : weight,
                        "desired_weight" : desired_weight,
                        "gender" : gender,
                        "like_tags" : like_tags,
                        "pref_time" : pref_time})
    elif _type == "C":
        cursor.execute(f'''SELECT * FROM coach WHERE cid={id}''')
        coach_result = cursor.fetchone()

        speciality = coach_result[1]
        experience = coach_result[2]
        price = coach_result[3]
        available = coach_result[4]

        pref_tags = coach_result[5]
        pref_tags = json.loads(pref_tags)
        
        description = coach_result[6]


        return jsonify({"panel" : "coach",
                        "id" : id,
                        "account_type" : account_type,
                        "full_name" : full_name,
                        "phone_number" : phone_number,
                        "email" : email,
                        "speciality" : speciality,
                        "experience" : experience,
                        "price" : price,
                        "available" : available,
                        "pref_tags" : pref_tags,
                        "description" : description})
    else :
        return jsonify({"error": "no type account"})

@app.route('/api/profile/trainee/edit' , methods=["POST"]) #KINDA COMPLETE
def user_panel_profile_edit():
    try:    
        
        id = session['user_id']
        password = request.json.get("password")
        full_name = request.json.get("full_name")
        phone_number = request.json.get("phone_number")
        email = request.json.get("email")
        height = request.json.get("height")
        weight = request.json.get("weight")
        desired_weight = request.json.get("desired_weight")
        gender = request.json.get("gender")
        pref_time = request.json.get("pref_time")
        like_tags = request.json.get("like_tags")
        pref_time = json.dumps(pref_time)
        like_tags = json.dumps(like_tags)
        if phone_number != None and phone_number != "":
            if duplicate("users","phone_number",phone_number) == 1 : return jsonify({"error": "duplicate phone number"})
        if email != None and email != "":
            if duplicate("users","email",email) == 1 : return jsonify({"error": "duplicate email"})

        data_user = {}
        data_trainee = {}
        data_user["password"] = password
        data_user["full_name"] = full_name
        data_user["phone_number"] = phone_number
        data_user["email"] = email

        
        data_trainee["height"] = height
        data_trainee["weight"] = weight
        data_trainee["desired_weight"] = desired_weight
        data_trainee["gender"] = gender
        data_trainee["pref_time"] = pref_time
        data_trainee["like_tags"] = like_tags
        
        einput_user = edit_input(data_user)
        einput_trainee = edit_input(data_trainee)
        print(einput_user)
        print(einput_trainee)
        if einput_user != "":
            cursor.execute(f'''UPDATE users SET {einput_user} WHERE id={id} ''')
            connection.commit()
        if einput_trainee != "" :
            cursor.execute(f'''UPDATE trainee SET {einput_trainee} WHERE tid={id} ''')
            connection.commit()
        
        #check data
        cursor.execute(f'''SELECT * 
                        FROM users 
                        WHERE id='{id}' ''')
        user_result = cursor.fetchone()
        id = user_result[0]
        _type = user_result[1]

        id = id
        account_type = _type
        full_name = user_result[3]
        phone_number =  user_result[4]
        email = user_result[6]

        cursor.execute(f'''SELECT * FROM trainee WHERE tid={id}''')
        trainee_result = cursor.fetchone()

        height = trainee_result[1]
        weight = trainee_result[2]
        desired_weight = trainee_result[3]
        gender = trainee_result[4]

        pref_time = trainee_result[5]
        pref_time = json.loads(pref_time)

        like_tags = trainee_result[6]
        like_tags = json.loads(like_tags)


        return jsonify({"panel" : "trainee",
                        "id" : id,
                        "account_type" : account_type,
                        "full_name" : full_name,
                        "phone_number" : phone_number,
                        "email" : email,
                        "height" : height,
                        "weight" : weight,
                        "desired_weight" : desired_weight,
                        "gender" : gender,
                        "like_tags" : like_tags,
                        "pref_time" : pref_time})
    except Exception as ex:
        return "متاسفانه انجام نشد" + "<br>" + str(ex)

@app.route('/api/profile/coach/edit' , methods=["POST"]) #KINDA COMPLETE
def coach_profile_edit():
    try:    
        
        id = session['user_id']
        password = request.json.get("password")
        full_name = request.json.get("full_name")
        phone_number = request.json.get("phone_number")
        email = request.json.get("email")
        speciality = request.json.get("speciality")
        experience = request.json.get("experience")
        price = request.json.get("price")
        avalaible = request.json.get("avalaible")
        pref_tags = request.json.get("pref_tags")
        description = request.json.get("description")
        pref_tags = json.dumps(pref_tags)

        if phone_number != None and phone_number != "":
            if duplicate("users","phone_number",phone_number) == 1 : return jsonify({"error": "duplicate phone number"})
        if email != None and email != "":
            if duplicate("users","email",email) == 1 : return jsonify({"error": "duplicate email"})

        data_user = {}
        data_coach = {}
        data_user["password"] = password
        data_user["full_name"] = full_name
        data_user["phone_number"] = phone_number
        data_user["email"] = email

        
        data_coach["speciality"] = speciality
        data_coach["experience"] = experience
        data_coach["price"] = price
        data_coach["avalaible"] = avalaible
        data_coach["pref_tags"] = pref_tags
        data_coach["description"] = description
        einput_user = edit_input(data_user)
        einput_coach = edit_input(data_coach)

        if einput_user != "":
            cursor.execute(f'''UPDATE users SET {einput_user} WHERE id={id} ''')
            connection.commit()
        if einput_coach != "":
            cursor.execute(f'''UPDATE coach SET {einput_coach} WHERE cid={id} ''')
            connection.commit()

        #check data
        cursor.execute(f'''SELECT * 
                        FROM users 
                        WHERE id='{id}' ''')
        user_result = cursor.fetchone()
        id = user_result[0]
        _type = user_result[1]

        id = id
        account_type = _type
        full_name = user_result[3]
        phone_number =  user_result[4]
        email = user_result[6]

        cursor.execute(f'''SELECT * 
                            FROM coach 
                            WHERE cid={id}''')
        coach_result = cursor.fetchone()

        speciality = coach_result[1]
        experience = coach_result[2]
        price = coach_result[3]
        available = coach_result[4]

        pref_tags = coach_result[5]
        pref_tags = json.loads(pref_tags)
        
        description = coach_result[6]


        return jsonify({"msg" : "coach sign up sucess",
                        "panel" : "coach",
                        "id" : id,
                        "account_type" : account_type,
                        "full_name" : full_name,
                        "phone_number" : phone_number,
                        "email" : email,
                        "speciality" : speciality,
                        "experience" : experience,
                        "price" : price,
                        "available" : available,
                        "pref_tags" : pref_tags,
                        "description" : description})
    except Exception as ex:
        return "متاسفانه انجام نشد" + "<br>" + str(ex)

#--------------exercise--------------

@app.route('/api/exercises' , methods=["POST"]) #not COMPELETE
def user_panel_exercises():
    if request.json.get("id") == None:
        if 'user_id' in session:
            id = session['user_id']
        else : return jsonify({"error" : "idk why but user is notlogged in"})
    else : id = request.json.get("id")
    cursor.execute(f'''SELECT * FROM exercise 
                    WHERE creator_id={id} OR ispublic='T' ''')
    exer = cursor.fetchall()
    exer_result = {}
    for items in exer:
        main_muscles = json.loads(items[4])
        sub_muscles = json.loads(items[5])
        weight_numbers_males = json.loads(items[10])
        weight_numbers_females = json.loads(items[11])
        exer_result[items[0]] = {"eid" : items[0],
                                 "creator_id" : items[1],
                                 "title" : items[2],
                                 "difficulty" : items[3],
                                 "main_muscles" : main_muscles,
                                 "sub_muscles" : sub_muscles,
                                 "stages" : items[6],
                                 "summary" : items[9],
                                 "weight_numbers_males" : weight_numbers_males,
                                 "weight_numbers_females" : weight_numbers_females,
                                 "public" : items[12]
                                 }

    return jsonify(exer_result)

@app.route('/api/exercises/add' , methods=["POST"]) #KINDA COMPELETE
def user_panel_exercises_add():
    if request.json.get("id") == None:
        if 'user_id' in session:
            id = session['user_id']
        else : return jsonify({"error" : "idk why but user is notlogged in"})
    else : id = request.json.get("id")

    eid = id_gen("eid", "exercise")
    creator_id = id
    title = request.json.get("title")
    difficulty = request.json.get("difficulty")
    main_muscles = request.json.get("main_muscles")
    main_muscles = json.dumps(main_muscles)
    sub_muscles = request.json.get("sub_muscles")
    sub_muscles = json.dumps(sub_muscles)
    stages = request.json.get("stages")
    summary = request.json.get("summary")
    weight_numbers_males = request.json.get("weight_numbers_males")
    weight_numbers_males = json.dumps(weight_numbers_males)
    weight_numbers_females = request.json.get("weight_numbers_females")
    weight_numbers_females = json.dumps(weight_numbers_females)

    cursor.execute(f'''INSERT INTO exercise (eid, creator_id, title, difficulty, main_muscles, sub_muscles, stages, summary, weight_numbers_males, weight_numbers_females)
                   VALUES({eid},{creator_id},'{title}',{difficulty},'{main_muscles}','{sub_muscles}','{stages}','{summary}','{weight_numbers_males}','{weight_numbers_females}') ''')
    connection.commit()
    #return jsonify({"msg": "add exercise success"})
    cursor.execute(f'''SELECT * FROM exercise 
                    WHERE creator_id={id} OR ispublic='T' ''')
    exer = cursor.fetchall()
    exer_result = {}
    for items in exer:
        main_muscles = json.loads(items[4])
        sub_muscles = json.loads(items[5])
        weight_numbers_males = json.loads(items[10])
        weight_numbers_females = json.loads(items[11])
        exer_result[items[0]] = {"eid" : items[0],
                                 "creator_id" : items[1],
                                 "title" : items[2],
                                 "difficulty" : items[3],
                                 "main_muscles" : main_muscles,
                                 "sub_muscles" : sub_muscles,
                                 "stages" : items[6],
                                 "summary" : items[9],
                                 "weight_numbers_males" : weight_numbers_males,
                                 "weight_numbers_females" : weight_numbers_females,
                                 "public" : items[12]
                                 }

    return jsonify(exer_result)

@app.route('/api/exercises/edit' , methods=["POST"]) #no log in check
def user_panel_exercises_edit():
    if request.json.get("id") == None:
        if 'user_id' in session:
            id = session['user_id']
        else : return jsonify({"error" : "idk why but user is notlogged in"})
    else : id = request.json.get("id")

    eid = request.json.get("eid")
    if eid == None or eid == "":
        return jsonify({"error" : "i need the exrcise id"})

    title = request.json.get("title")
    difficulty = request.json.get("difficulty")
    main_muscles = request.json.get("main_muscles")
    main_muscles = json.dumps(main_muscles)
    sub_muscles = request.json.get("sub_muscles")
    sub_muscles = json.dumps(sub_muscles)
    stages = request.json.get("stages")
    summary = request.json.get("summary")
    weight_numbers_males = request.json.get("weight_numbers_males")
    weight_numbers_males = json.dumps(weight_numbers_males)
    weight_numbers_females = request.json.get("weight_numbers_females")
    weight_numbers_females = json.dumps(weight_numbers_females)

    data_exer = {}
    data_exer["title"] = title
    data_exer["difficulty"] = difficulty
    data_exer["main_muscles"] = main_muscles
    data_exer["sub_muscles"] = sub_muscles
    data_exer["stages"] = stages
    data_exer["summary"] = summary
    data_exer["weight_numbers_males"] = weight_numbers_males
    data_exer["weight_numbers_females"] = weight_numbers_females

    einput_exer = edit_input(data_exer)

    if einput_exer != "":
        cursor.execute(f'''UPDATE exercise SET {einput_exer} WHERE eid={eid} AND creator_id={id} ''')
        connection.commit()
    
    #check data
    
    #return jsonify({"msg" : "exercise edit success"})
    cursor.execute(f'''SELECT * FROM exercise 
                    WHERE creator_id={id} OR ispublic='T' ''')
    exer = cursor.fetchall()
    exer_result = {}
    for items in exer:
        main_muscles = json.loads(items[4])
        sub_muscles = json.loads(items[5])
        weight_numbers_males = json.loads(items[10])
        weight_numbers_females = json.loads(items[11])
        exer_result[items[0]] = {"eid" : items[0],
                                 "creator_id" : items[1],
                                 "title" : items[2],
                                 "difficulty" : items[3],
                                 "main_muscles" : main_muscles,
                                 "sub_muscles" : sub_muscles,
                                 "stages" : items[6],
                                 "summary" : items[9],
                                 "weight_numbers_males" : weight_numbers_males,
                                 "weight_numbers_females" : weight_numbers_females,
                                 "public" : items[12]
                                 }

    return jsonify(exer_result)
    


@app.route('/api/exercises/delete' , methods=["POST"]) #no log in check
def user_panel_exercises_delete():
    if request.json.get("id") == None:
        if 'user_id' in session:
            id = session['user_id']
        else : return jsonify({"error" : "idk why but user is notlogged in"})
    else : id = request.json.get("id")

    eid = request.json.get("eid")
    if eid == None or eid == "":
        return jsonify({"error" : "i need the exrcise id"})
    
    cursor.execute(f"DELETE FROM exercise WHERE eid={eid} AND creator_id={id}")
    connection.commit()

    #return jsonify({"msg" : "exercise delete success"})
    cursor.execute(f'''SELECT * FROM exercise 
                    WHERE creator_id={id} OR ispublic='T' ''')
    exer = cursor.fetchall()
    exer_result = {}
    for items in exer:
        main_muscles = json.loads(items[4])
        sub_muscles = json.loads(items[5])
        weight_numbers_males = json.loads(items[10])
        weight_numbers_females = json.loads(items[11])
        exer_result[items[0]] = {"eid" : items[0],
                                 "creator_id" : items[1],
                                 "title" : items[2],
                                 "difficulty" : items[3],
                                 "main_muscles" : main_muscles,
                                 "sub_muscles" : sub_muscles,
                                 "stages" : items[6],
                                 "summary" : items[9],
                                 "weight_numbers_males" : weight_numbers_males,
                                 "weight_numbers_females" : weight_numbers_females,
                                 "public" : items[12]
                                 }

    return jsonify(exer_result)
#-----------------------------plan-----------------------------
@app.route('/api/plans/add' , methods=["POST"]) #KINDA COMPELETE
def user_panel_plans_add():
    if request.json.get("id") == None:
        if 'user_id' in session:
            id = session['user_id']
        else : return jsonify({"error" : "idk why but user is notlogged in"})
    else : id = request.json.get("id")

    pid = id_gen("pid", "_plan")
    creator_id = id
    title = request.json.get("title")
    tags = request.json.get("tags")
    if d_empty(tags) == False: tags = json.dumps(tags)
    else : tags = "null"
    Sat_excs = request.json.get("Sat_excs")
    if d_empty(Sat_excs) == False: Sat_excs = json.dumps(Sat_excs)
    else : Sat_excs = "null"
    Sun_excs = request.json.get("Sun_excs")
    if d_empty(Sun_excs) == False: Sun_excs = json.dumps(Sun_excs)
    else : Sun_excs = "null"
    Mon_excs = request.json.get("Mon_excs")
    if d_empty(Mon_excs) == False: Mon_excs = json.dumps(Mon_excs)
    else : Mon_excs = "null"
    Tue_excs = request.json.get("Tue_excs")
    if d_empty(Tue_excs) == False: Tue_excs = json.dumps(Tue_excs)
    else : Tue_excs = "null"
    Wed_excs = request.json.get("Wed_excs")
    if d_empty(Wed_excs) == False: Wed_excs = json.dumps(Wed_excs)
    else : Wed_excs = "null"
    Thr_excs = request.json.get("Thr_excs")
    if d_empty(Thr_excs) == False: Thr_excs = json.dumps(Thr_excs)
    else : Thr_excs = "null"
    Fri_excs = request.json.get("Fri_excs")
    if d_empty(Fri_excs) == False: Fri_excs = json.dumps(Fri_excs)
    else : Fri_excs = "null"

    cursor.execute(f'''INSERT INTO _plan (pid, creator_id, title, tags, Sat_excs, Sun_excs, Mon_excs, Tue_excs, Wed_excs, Thr_excs, Fri_excs)
                   VALUES({pid},{creator_id},'{title}','{tags}','{Sat_excs}','{Sun_excs}','{Mon_excs}','{Tue_excs}','{Wed_excs}','{Thr_excs}','{Fri_excs}') ''')
    connection.commit()
    return jsonify({"msg": "add plans success"})

@app.route('/api/plans' , methods=["POST"]) #not COMPELETE
def user_panel_plans():
    if request.json.get("id") == None:
        if 'user_id' in session:
            id = session['user_id']
        else : return jsonify({"error" : "idk why but user is notlogged in"})
    else : id = request.json.get("id")
    
    cursor.execute(f'''SELECT favorite_plans FROM users 
                    WHERE id={id}''')
    favorite_plans = cursor.fetchone()

    if d_empty(favorite_plans[0]) == False:
        favorite_plans = json.loads(favorite_plans[0])
    else:
        favorite_plans = []
    

    cursor.execute(f'''SELECT * FROM _plan 
                    WHERE creator_id={id}''')
    plans = cursor.fetchall()
    if plans == None: return jsonify({"msg" : "no plans"})
    plans_result = {}
    for plan in plans:
        
        if plan[0] in favorite_plans:
            favorite = "y"
        else:
            favorite = "n"

        exercise_number = 0
        tags = json.loads(plan[4])
        Sat_excs = json.loads(plan[5])
        Sun_excs = json.loads(plan[6])
        Mon_excs = json.loads(plan[7])
        Tue_excs = json.loads(plan[8])
        Wed_excs = json.loads(plan[9])
        Thr_excs = json.loads(plan[10])
        Fri_excs = json.loads(plan[11])
        days_in_week = d_in_w(Sat_excs,Sun_excs,Mon_excs,
                              Tue_excs,Wed_excs,Thr_excs,
                              Fri_excs)
        exercise_number = exer_number(Sat_excs,Sun_excs,Mon_excs,
                              Tue_excs,Wed_excs,Thr_excs,
                              Fri_excs)
        plans_result[plan[0]] = {"pid" : plan[0],
                                 "creator_id" : plan[1],
                                 "title" : plan[2],
                                 "difficulty" : plan[3],
                                 "tags" : tags,
                                 "Sat_excs" : Sat_excs,
                                 "Sun_excs" : Sun_excs,
                                 "Mon_excs" : Mon_excs,
                                 "Tue_excs" : Tue_excs,
                                 "Wed_excs" : Wed_excs,
                                 "Thr_excs" : Thr_excs,
                                 "Fri_excs" : Fri_excs,
                                 "days_in_week" : days_in_week,
                                 "exercise_number" : exercise_number,
                                 "favorite" : favorite
                                 }

    return jsonify(plans_result)

@app.route('/api/plans/delete' , methods=["POST"]) #no log in check
def user_panel_plans_delete():
    if request.json.get("id") == None:
        if 'user_id' in session:
            id = session['user_id']
        else : return jsonify({"error" : "idk why but user is notlogged in"})
    else : id = request.json.get("id")

    pid = request.json.get("pid")
    if pid == None or pid == "":
        return jsonify({"error" : "i need the exrcise id"})
    
    cursor.execute(f"DELETE FROM _plan WHERE pid={pid} AND creator_id={id}")
    connection.commit()
    return jsonify({"msg" : "delete success"})

@app.route('/api/plans/favorite' , methods=["POST"]) #no log in check
def user_panel_plans_favorite():
    if request.json.get("id") == None:
        if 'user_id' in session:
            id = session['user_id']
        else : return jsonify({"error" : "idk why but user is notlogged in"})
    else : id = request.json.get("id")

    pid = request.json.get("pid")
    if pid == None or pid == "":
        return jsonify({"error" : "i need the plan id"})

    cursor.execute(f'''SELECT favorite_plans FROM users WHERE id={id}''')
    fav_plan_result = cursor.fetchone()
    if d_empty(fav_plan_result[0]) == False:
        fav_plan_result = json.loads(fav_plan_result[0])
    else:
        fav_plan_result = []
    fav_plan_result.append(pid)
    fav_plan_result = json.dumps(fav_plan_result)
    print(fav_plan_result)
    cursor.execute(f'''UPDATE users SET favorite_plans='{fav_plan_result}' WHERE id={id}''')
    connection.commit()
    return jsonify({"msg" : "favorite success"})

@app.route('/api/plans/unfavorite' , methods=["POST"]) #no log in check
def user_panel_plans_unfavorite():
    if request.json.get("id") == None:
        if 'user_id' in session:
            id = session['user_id']
        else : return jsonify({"error" : "idk why but user is notlogged in"})
    else : id = request.json.get("id")

    pid = request.json.get("pid")
    if pid == None or pid == "":
        return jsonify({"error" : "i need the plan id"})
    
    cursor.execute(f'''SELECT favorite_plans FROM users WHERE id={id}''')
    fav_plan_result = cursor.fetchone()
    if d_empty(fav_plan_result[0]) == False:
        fav_plan_result = json.loads(fav_plan_result[0])
    else:
        fav_plan_result = []
    if pid in fav_plan_result:
        fav_plan_result.remove(pid)
    fav_plan_result = json.dumps(fav_plan_result)
    cursor.execute(f'''UPDATE users SET favorite_plans='{fav_plan_result}' WHERE id={id}''')
    connection.commit()
    return jsonify({"msg" : "unfavorite success"})

@app.route('/api/trainees/coach', methods=["POST"]) #kinda COMPELETE
def user_panel_coach():
    if request.json.get("id") == None:
        if 'user_id' in session:
            id = session['user_id']
        else : return jsonify({"error" : "idk why but user is notlogged in"})
    else : id = request.json.get("id")
    
    coach_list = {}
    tid = id
    cursor.execute(f"""SELECT cid 
                        FROM coach_trainee 
                        WHERE tid = {tid}""")
    result = cursor.fetchone()
    if result == None:
        coach_list[0] = "null"
    else:
        cid = result[0]
        coach_list[0] = cid

    cursor.execute(f"""SELECT * 
                        FROM coach""")
    
    result = cursor.fetchall()
    if result == None:
        return "no coach?How?!"
    for coaches in result:
        cid = coaches[0]
        cursor.execute(f'''SELECT * FROM users WHERE id={cid} ''')
        coach_user = cursor.fetchone()
        pref_tags = json.loads(coaches[5])
        coach_list[coaches[0]]={"cid" : coaches[0],
                                "full_name" : coach_user[3],
                                "phone_number" : coach_user[4],
                                "email" : coach_user[6],
                                "speciality" : coaches[1],
                                "experience" : coaches[2],
                                "price" : coaches[3],
                                "avalaible" : coaches[4],
                                "pref_tags" : pref_tags,
                                "description" : coaches[6]
                                }
    return coach_list
        
@app.route('/api/trainees/coach/choose', methods=["POST"])
def user_panel_coach_choose(): 
    if request.json.get("id") == None:
        if 'user_id' in session:
            id = session['user_id']
        else : return jsonify({"error" : "idk why but user is notlogged in"})
    else : id = request.json.get("id")

    tid = id

    cid = request.json.get("cid")
    if cid == None or cid == "":
        return jsonify({"error" : "i need the coach id"})

    startdate = datetime.now()
    enddate = startdate + timedelta(days=30)
    formatted_start_date = startdate.strftime('%Y-%m-%d')
    formatted_end_date = enddate.strftime('%Y-%m-%d')
    cursor.execute(f'''INSERT INTO coach_trainee (tid, cid, startdate, enddate)
                   VALUES ({tid},{cid},"{formatted_start_date}","{formatted_end_date}")''')
    connection.commit()
    #return jsonify({"error" : "i need the coach id"})
    coach_list = {}
    tid = id
    cursor.execute(f"""SELECT cid 
                        FROM coach_trainee 
                        WHERE tid = {tid}""")
    result = cursor.fetchone()
    if result == None:
        coach_list[0] = "null"
    else:
        cid = result[0]
        coach_list[0] = cid

    cursor.execute(f"""SELECT * 
                        FROM coach""")
    
    result = cursor.fetchall()
    if result == None:
        return "no coach?How?!"

    for coaches in result:
        cid = coaches[0]
        cursor.execute(f'''SELECT * FROM users WHERE id={cid} ''')
        coach_user = cursor.fetchone()
        pref_tags = json.loads(coaches[5])
        coach_list[coaches[0]]={"cid" : coaches[0],
                                "full_name" : coach_user[3],
                                "phone_number" : coach_user[4],
                                "email" : coach_user[6],
                                "speciality" : coaches[1],
                                "experience" : coaches[2],
                                "price" : coaches[3],
                                "avalaible" : coaches[4],
                                "pref_tags" : pref_tags,
                                "description" : coaches[6]
                                }
    return coach_list

@app.route('/api/coachs/trainees', methods=["POST"]) #kinda COMPLETE
def coach_profile_trainees():
    if request.json.get("id") == None:
        if 'user_id' in session:
            id = session['user_id']
        else : return jsonify({"error" : "idk why but user is notlogged in"})
    else : id = request.json.get("id")

    cid = id

    cursor.execute(f'''SELECT * 
                        FROM coach_trainee 
                        WHERE cid={cid}''')
    coach_trainees = cursor.fetchall()
    if coach_trainees == None : return jsonify({"msg" : "no trainees"})
    trainees_info = {}
    for trainees in coach_trainees:
        i = trainees[0]
        cursor.execute(f'''SELECT * 
                        FROM users 
                        WHERE id={i}''')
        trainee_user = cursor.fetchone()
        trainees_info[trainees[0]]={"tid" : trainees[0],
                                    "startdate" : trainees[2],
                                    "enddate" : trainees[3],
                                    "setpid" : trainees[4],
                                    "payid" : trainees[5],
                                    "full_name" : trainee_user[3],
                                    "phone_number" : trainee_user[4]}
        return jsonify(trainees_info)

#must check
@app.route('/api/coachs/trainees/setplan/commit', methods=["POST"]) #kinda COMPLETE #post
def coach_profile_trainees_set_plan():
    
    if request.json.get("id") == None:
        if 'user_id' in session:
            id = session['user_id']
        else : return jsonify({"error" : "idk why but user is notlogged in"})
    else : id = request.json.get("id")

    cid = id
    pid = request.json.get("pid")
    tid = request.json.get("tid")

    cursor.execute(f'''UPDATE trainee
                        SET csplan_id={pid}
                        WHERE tid={tid}''')
    cursor.execute(f'''UPDATE coach_trainee
                        SET setpid={pid}
                        WHERE tid={tid}''')
    connection.commit()
    return jsonify({"msg" : "setplan success"})


if __name__ == "__main__":
    app.run(debug=True)
