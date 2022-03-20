from flask import Flask, redirect, url_for, render_template, request, flash
from datetime import date
import pyrebase
import qrcode
import json
import time
import io
import base64

BASE_URL = 'http://127.0.0.1:5000'

# Connect to Firebase Realtime Database
config = {
  "apiKey": "AIzaSyBGRn-c9Cl6kbROuWu44w5besGDNxsDM5I",
  "authDomain": "retro-c0350.firebaseapp.com",
  "projectId": "retro-c0350",
  "databaseURL": "https://retro-c0350-default-rtdb.firebaseio.com/",
  "storageBucket": "retro-c0350.appspot.com",
  "messagingSenderId": "112454151211",
  "appId": "1:112454151211:web:abd98d22947b2b37ba0e6e"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

USER = {"idToken": None, "localId": None, "mapVerified": False}

app = Flask(__name__)

# Views
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["password"]
        name = result["name"]
        date_of_birth = result["date_of_birth"]
        sex = result["sex"]

        # date of birth
        today = date.today()

        yr = int(date_of_birth[:4])

        age = today.year - yr
        
        if email is None or password is None or name is None or date_of_birth is None or sex is None:
            return {'message': 'Error missing information'}, 400
        try:
            auth.create_user_with_email_and_password(email, password)
            user = auth.sign_in_with_email_and_password(email, password)
            id = user['localId']
            url = f'{BASE_URL}/portal/{id}'

            # Firebase Realtime Database
            data = {
                "id": id,
                "name": name,
                "email": email,
                "date_of_birth": date_of_birth,
                "url": url,
                "sex": sex,
                "height": "N/A",
                "weight": "N/A",
                "blood_type": "N/A",
                "emergency_phone": "N/A",
                "emergency_email": "N/A",
                "past_conditions": {
                    "initial": "N/A",
                },
                "treatments": {
                    "initial": {
                        "hospital": "N/A",
                        "treatment": "N/A"
                    }
                },
                "blood_tests": "N/A",
                "age": age,
                "files": {
                    "initial": True,
                },
            }
            db.child("users").child(id).set(data)

            USER["idToken"] = user['idToken']
            USER["localId"] = user['localId']

            return redirect(url_for('personal_portal'))
        except:
            print('error creating user')
            return {'message': 'Error creating user'}, 400
    else:
        return render_template('signup.html')


@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["password"]
        if email is None or password is None:
            return {'message': 'Error missing information'}, 400
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            USER["idToken"] = user['idToken']
            USER["localId"] = user['localId']

            return redirect(url_for('personal_portal'))
        except:
            return {'message': 'Error logging in'}, 400
    else:
        return render_template('login.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/personal-portal')
def personal_portal():
    db = firebase.database()
    if USER["idToken"] != None and USER["localId"] != None and USER["mapVerified"] == False:
        USER["mapVerified"] = True
        return redirect(url_for('map'))
    elif USER["idToken"] != None and USER["localId"] != None and USER["mapVerified"] == True:
        id = USER["localId"]
        user = db.child("users").child(id).get()
        user_data = user.val()
        name = user_data["name"]
        date_of_birth = user_data["date_of_birth"]
        email = user_data["email"]
        url = user_data["url"]
        sex = user_data["sex"]
        height = user_data["height"]
        weight = user_data["weight"]
        blood_type = user_data["blood_type"]
        age = user_data["age"]
        past_conditions = user_data["past_conditions"]
        treatments = user_data["treatments"]
        blood_tests = user_data["blood_tests"]
        emergency_phone = user_data["emergency_phone"]
        emergency_email = user_data["emergency_email"]

 

        data = io.BytesIO()
        img = getQRCode(id)
        img.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())

        return render_template('dashboard/pages/dashboard.html', img_data=encoded_img_data.decode('utf-8'), name=name, email=email, url=url, id=id, age=age, sex=sex, height=height, weight=weight, blood_type=blood_type, past_conditions=past_conditions, treatments=treatments, blood_tests=blood_tests, emergency_phone=emergency_phone, emergency_email=emergency_email)
    else:
        return redirect(url_for('login'))


@app.route('/portal/<id>')
def portal(id):
    db = firebase.database()
    user = db.child("users").child(id).get()
    user_data = user.val()

    id = user_data["id"]
    name = user_data["name"]
    date_of_birth = user_data["date_of_birth"]
    email = user_data["email"]
    url = user_data["url"]
    sex = user_data["sex"]
    height = user_data["height"]
    weight = user_data["weight"]
    blood_type = user_data["blood_type"]
    age = user_data["age"]
    past_conditions = user_data["past_conditions"]
    treatments = user_data["treatments"]
    blood_tests = user_data["blood_tests"]
    emergency_phone = user_data["emergency_phone"]
    emergency_email = user_data["emergency_email"]
    

    data = io.BytesIO()
    img = getQRCode(id)
    img.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return render_template('dashboard/pages/dashboard.html', img_data=encoded_img_data.decode('utf-8'), name=name, email=email, url=url, id=id, age=age, sex=sex, height=height, weight=weight, blood_type=blood_type, past_conditions=past_conditions, treatments=treatments, blood_tests=blood_tests, emergency_phone=emergency_phone, emergency_email=emergency_email)


@app.route('/add-entry', methods = ["POST", "GET"])
def add_entry():


    if request.method == "POST":
        result = request.form
        height = result["height"]
        weight = result["weight"]
        blood_type = result["blood_type"]
        blood_tests = result["blood_tests"]
        emergency_phone = result["emergency_phone"]
        emergency_email = result["emergency_email"]
        if height is None or weight is None or blood_type is None or blood_tests is None or emergency_phone is None or emergency_email is None:
            return {'message': 'Error missing information'}, 400
        try:
            id = USER['localId']

            # Firebase Realtime Database
            data = {
                "height": height,
                "weight": weight,
                "blood_type": blood_type,
                "blood_tests": blood_tests,
                "emergency_phone": emergency_phone,
                "emergency_email": emergency_email
            }
            db.child("users").child(id).update(data)


            return redirect(url_for('personal_portal'))
        except:
            print('error updating user')
            return {'message': 'Error updating user'}, 400
    else:
        return render_template('add_entry.html')



@app.route('/add-file', methods = ["POST", "GET"])
def add_file():
    db = firebase.database()
    id = USER["localId"]
    if id == None:
        return redirect(url_for('login'))

    if request.method == "POST":
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return {'message': 'Error missing information'}, 400
        # UPLOAD
        storage_rel_url = f"files/{id}/{time.time()}.pdf"
        storage.child(storage_rel_url).put(file)

        timestamp = str(time.time())[:9]
        
        try:

            # Firebase Realtime Database
            data = {
                timestamp: f"{storage_rel_url}",
            }

            if db.child("users").child(id).child("files").child("initial").get() == None:
                print('hi')
                db.child("users").child(id).child("files").child("initial").remove()
                db.child("users").child(id).child("files").set(data)
            else:
                db.child("users").child(id).child("files").update(data)

            return redirect(url_for('personal_portal'))
        except Exception as e:
            print(e)
            print('error updating user')
            return {'message': 'Error updating user'}, 400
    else:
        return render_template('add_file.html')


@app.route('/view-file')
def view_file():
    db = firebase.database()
    id = USER["localId"]
    if id == None:
        return redirect(url_for('login'))

    user = db.child("users").child(id).get()
    user_data = user.val()

    file_urls = user_data["files"]
    display_urls = []

    for key, url in file_urls.items():
        full_url = storage.child(url).get_url(USER["idToken"])
        display_urls.append(full_url)
    
    data = io.BytesIO()
    img = getQRCode(id)
    img.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return render_template('view-pdfs.html', urls=display_urls, img_data=encoded_img_data.decode('utf-8'))
    

def getQRCode(id):
    img = qrcode.make('{}/portal/{}'.format(BASE_URL, id))
    return img

if __name__ == '__main__':
    app.run(debug=True)