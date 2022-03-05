from re import I
from flask import Flask,render_template,request,session, request
from flask.helpers import flash, url_for
import pymongo
from werkzeug.utils import redirect
import secrets
from bson.objectid import ObjectId
import api  
import settings

# myclient = pymongo.MongoClient('mongodb://localhost:27017/')
# mydb = myclient['mydatabase']


app = Flask(__name__)
app.secret_key='ASDASDASDASDASDSA-dsadsadsadsa'
    
    

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        err_msg = "Khong Dang Nhap Thanh Cong ! "
        username= request.form.get("username")
        password= request.form.get("password")
        if api.user.find_one({"username":username}):
            if api.mydb.user.find_one({"password":password}):
                session['user']=str(username)  
                return redirect(url_for("hello_world"))
        print(2)
        return redirect(url_for("login",err_msg = err_msg))
    return render_template("login.html")

@app.route('/register',methods=['POST','GET'])
def register(): 
    api.account.find()
    if request.method=='POST':
        first_name = request.form.get("first_name"),
        last_name = request.form.get("last_name"),
        dob = request.form.get("dob"),
        email = request.form.get("email"),
        password = request.form.get("password"),
        address = request.form.get("address"),
        phone = request.form.get("phone"),
        gender = request.form.get("gender"),
        country = request.form.get("country"),
        province = request.form.get("province")
        create_acount = {
            first_name :"first_name", 
            last_name: "last_name",
            dob:"dob",
            email:"email",
            password:"password",
            address:"address",
            phone:"phone",
            gender:"gender",
            country :"country",
            province :"province"
        }
        api.account.insert_one(create_acount)
        list_account = api.account.find()
        return render_template("register.html",list_account = list_account)
    return render_template("register.html")



@app.route('/index',methods=['POST','GET'])
def hello_world():
    if session.get("user")==None:
        return redirect(url_for("login"))
    khachhang = api.customers.find()
    if request.method == 'POST':
        add_user = {"name":request.form["Name_add"],"address":request.form["Address_add"]}
        find_delete = request.form.get('Name_add')
        find = request.args.get('search_name')
        if find:
            khachhang = api.customers.find({'name': {'$regex': '.*'+find+'.*','$options':'i'}})
        if find_delete:
            api.customers.delete_one({'name': {'$regex': '.*'+find_delete+'.*','$options':'i'}})
        api.customers.insert_one(add_user)
        # ITEMS_PER_PAGE = 8
        # filter = {
            
        # }
        # count_logs = api.account.count_documents(filter)
        # page = int(request.args.get('page', 1))
        # pagination = Pagination(
        #     page=page,
        #     total=count_logs,
        #     per_page=ITEMS_PER_PAGE,
        #     css_framework='bootstrap3')
        # recs = api.customers.find(filter).sort("created_at", pymongo.DESCENDING).skip(
        #     ITEMS_PER_PAGE * (page - 1)).limit(ITEMS_PER_PAGE)
        # pagination = pagination
    return render_template("index.html", khachhang = khachhang)

@app.route('/')
def loadPage():
    return render_template('loadpage.html')

@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/create_user',methods=['POST','GET'])
def create_user():
   data_user = api.user.find()
   if request.method == 'POST':
            create_user = {"username":request.form["name_user"],"password":request.form["password_user"]}
            api.user.insert_one(create_user)
   return render_template('user.html',data_user = data_user)

@app.route('/delete_user',methods=['POST','GET'])
def delete_user():
   data_user = api.user.find()
   if request.method == 'POST':
            delete_one_user = request.form.get('delete_user')
            if delete_one_user:
               api.user.delete_one({'username': {'$regex': '.*'+delete_one_user+'.*','$options':'i'}})
               return render_template('delete_user.html',data_user = data_user)
                     
   return render_template('delete_user.html',data_user = data_user)


@app.route('/update_user',methods=['POST','GET'])
def update_user():
    if request.method == 'POST':
        id = request.form.get('update_id')
        name = request.form["update_user"]
        password = request.form["update_password"]
        new_data = {"$set":{"username":name,"password":password}}
        api.user.update_one({'_id': ObjectId(id)},new_data)
        return 'Updated success !'
    data_user = api.user.find()
    return render_template('update_user.html',data_user = data_user)

@app.route('/search',methods=['POST','GET'])
def search():
    khachhang = api.customers.find()
    if request.method == 'POST':
        find_data = request.args.get('searchname')
        if find_data:
            khachhang = api.customers.find_one( { '$text': {' $search': find_data }})
    return render_template('abc.html',khachhang = khachhang)


@app.route('/find', methods=['POST', 'GET'])
def find():
    name = request.args.get('find_name')
    find_data = {'name': name}
    if name:
        user_list = api.list_people.find(find_data)
    else:
        user_list = api.list_people.find()
    return render_template('list_user.html', user_list=user_list)

@app.route('/employee')
def employee():
    return render_template("employee.html")

@app.route('/delete_user/<user_id>')
def delete_user_by_id(user_id):
    api.list_people.delete_one({'_id': ObjectId(user_id)})
    return redirect(url_for('list_people'))

@app.route('/list_people')
def list_people():
    data_user = api.list_people.find()
    return render_template("list_people.html",data_user = data_user)

@app.route('/list_project')
def list_project():
    list_project = api.list_project.find()
    return render_template("list_project.html",list_project =list_project)

@app.route('/list_team')
def list_team():
    list_team = api.list_team.find()
    return render_template("list_team.html",list_team =list_team)

@app.route('/log_out')
def log_out():
    session.clear()
    return redirect(url_for("login"))

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5678, debug=True)
    app.run(host='127.0.0.1', port=5000, debug=True)