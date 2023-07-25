from flask import Flask,render_template,request,redirect,jsonify
from flask_mail import Mail
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_URI"] = # enter your mongo db atlas uri here
mongo = PyMongo(app)

app.secret_key ='super-secret-key'
app.config['MAIL_SERVER'] ='smtp.gmail.com'
app.config['MAIL_PORT' ]= 465
app.config['MAIL_USE_TLS' ]= False
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USERNAME'] = 'mail@gmail.com'
app.config['MAIL_PASSWORD'] ='' #password




mail = Mail(app)

@app.route("/",methods=['GET','POST'])
def hello_world():
    if "name" in request.form and request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        massage=request.form.get('massage')
        mail.send_message("the mail from mirza",
        sender="mirzadanish7218@gmail.com",
        recipients=["mail@gmail.com"],
        body = f"the name of user is {name} \nthe email of user is {email} \nthe massage from the user is {massage}")
        

    if "checkin" in request.form and request.method=='POST':
        checkin=request.form.get("checkin")
        checkout=request.form.get("check-out")
        adults=request.form.get("adults")
        kids=request.form.get("kids")
        mylist={"checkin":checkin ,"checkout":checkout,"adults":adults,"kids":kids}
        mongo.db.Users.insert_one(mylist) 
    
       



    return render_template("index.html")

@app.route("/todo",methods=['GET','POST'])
def todo():
    if request.method=="POST":
        title=request.form.get("title")
        # sno=mongo.db.todo.create_index('No', unique = True)
        mongo.db.todo.insert_one({"title":title})
        alltodo=mongo.db.todo.find()
       
    alltodo=mongo.db.todo.find()    
    return render_template("todo.html",alltodo=alltodo)
  


@app.route("/delete/<id>")
def delete(id):
      
        mongo.db.todo.delete_one({'_id':ObjectId(id)})
       
        return redirect("/todo")

@app.route("/update/<id>",methods=["POST",'GET'] )
def update(id):
    if request.method=="POST":
      print("print hoja")
    # geting the title from todo to update ends
    #   new=request.form.get("new")
      

    #   mongo.db.todo.insert_one(new)
      return redirect("/todo")
    update_todo= mongo.db.todo.find_one({'_id':ObjectId(id)})
    # alltodo=mongo.db.todo.find()   
    return render_template("update.html",update_todo=update_todo) 
    



app.run(debug=True)
    
