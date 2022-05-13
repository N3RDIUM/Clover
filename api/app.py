from flask import Flask, flash, request, jsonify
import firebase_admin

firebaseConfig = {
'apiKey': "AIzaSyA-2IcM6hvaGqJ-gvugZtjmOMcySAzvEgA",
'authDomain': "clover-66a65.firebaseapp.com",
'projectId': "clover-66a65",
'storageBucket': "clover-66a65.appspot.com",
'messagingSenderId': "280821316151",
'appId': "1:280821316151:web:3ba6433cb9d31d95425db2",
'measurementId': "G-9708NBV1J6"
}

app = Flask(__name__)

@app.route('/')
def api_status():
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
