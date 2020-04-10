from flask import Flask,jsonify,request,Response
from flask_mysqldb import MySQL
from  werkzeug.security import generate_password_hash, check_password_hash

app =  Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_PASSWORD']='Admin_09'
app.config['MYSQL_USER']='root'
app.config['MYSQL_DB']='pythondb'

app.secret_key='secrect_key'

mysql = MySQL(app) 


@app.route('/users', methods=['GET'])
def getusers():
    pool = mysql.connection.cursor()
    pool.execute('SELECT * FROM users')
    users = pool.fetchall()
    return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def getOneUser(id):
    pool = mysql.connection.cursor()
    pool.execute('SELECT * FROM users WHERE id=%s',id)
    user = pool.fetchall()
    return jsonify(user)

@app.route('/users', methods=['POST'])
def createUser():
    username= request.json['username']
    password = request.json['password']
    email = request.json['email']
    hash_password = generate_password_hash(password)
    pool = mysql.connection.cursor()
    pool.execute('INSERT INTO users (username, password, email) VALUES (%s,%s,%s)',(username, hash_password, email) )
    mysql.connection.commit()
    return Response('user created', mimetype='applcation/json')

@app.route('/users/<id>',methods=['DELETE'])
def deleteUser(id):
    pool = mysql.connection.cursor()
    pool.execute('DELETE FROM users WHERE id=%s', id)
    mysql.connection.commit()

    return jsonify({
        "message":"user deleted"
    })
   

@app.route('/users/<id>', methods=['PUT'])
def updateusers(id):
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    pool = mysql.connection.cursor()
    hash_password = generate_password_hash(password)
    pool.execute('UPDATE users SET username=%s, password=%s, email=%s WHERE id=%s',(
        username, hash_password, email, id
    ))
    mysql.connection.commit()
    return jsonify({
        "message":"users updated"
    })

@app.errorhandler(404)
def erro_found(error=None):
    response = jsonify({
        "message":"page not found "+ request.url,
        "status":'404'
    })
    response.status_code = 404
    return response

if __name__=='__main__':
    app.run(debug=True, port=4000)