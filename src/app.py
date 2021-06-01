from flask import Flask,request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util 
from bson.objectid import ObjectId
        

app = Flask(__name__)
app.config.from_pyfile('../config.py')


mongo = PyMongo(app)
 
@app.route('/user', methods=['POST'])
def createUser():
   #Receiving data 
   username = request.json['username']
   password = request.json['password']
   email = request.json['email']

   #Validate info
   if username and password and email:
       #Encrypt password
       hashed_pasword = generate_password_hash(password)
       id = mongo.db.users.insert(
           {'username': username, 'password': hashed_pasword, 'email': email}
       )
       response = {
           'id': str(id),
           'username': username,
           'password' : hashed_pasword,
           'email': email
       }
       return response
   else:
       return notFound() 
   return {'message':'received'}

@app.route('/users', methods=['GET'])
def getUsers():
   #Get list users  
   users = mongo.db.users.find()
   response = json_util.dumps(users) 
   return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def getUser(id):
   #Get only one user by id  
   user = mongo.db.users.find_one({'_id': ObjectId(id)})
   response = json_util.dumps(user)
   return Response(response, mimetype='application/json')

@app.route('/user/<id>', methods=['DELETE'])
def deleteUser(id):
   user_delete = mongo.db.users.delete_one({'_id':ObjectId(id)})
   response = jsonify({'message':'User with '+ id +  '  was erased successfully'})
   return response

@app.route('/user/<id>', methods=['PUT'])
def updateUser(id):
   #Get data of user by Id 
   username = request.json['username']
   password = request.json['password']
   email = request.json['email']
   #Validation 
   if username and password and email:
       hashed_password = generate_password_hash(password)
       user_update = mongo.db.users.update_one({'_id': ObjectId(id)},{'$set':{
           'username':username,
           'password': hashed_password,
           'email': email
       }})
       response = jsonify({'message': 'User'+id+' was update successfully'})
       return response

@app.errorhandler(404)
def notFound(error=None):
    response = jsonify({
        'message': 'Resource not found:'+ request.url,
        'status': 404
    })
    response.status_code = 404
    return response

if __name__=="__main__":
    app.run(debug=True)