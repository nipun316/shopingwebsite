from flask import Flask,render_template,url_for,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json
import os

app=Flask(__name__)
app.secret_key="196137"
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/shoppingwebsite'
db=SQLAlchemy(app)
APP_ROOT=os.path.dirname(os.path.abspath(__file__))


class Userdetails(db.Model):
	email= db.Column(db.String(120), unique=True, nullable=False)
	sno= db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=False, nullable=False)
	role= db.Column(db.String(80), unique=False, nullable=False)
	password= db.Column(db.String(120), unique=False, nullable=False)
	date= db.Column(db.String(12), unique=False, nullable=True)

class Products(db.Model):
	
	sno= db.Column(db.Integer, primary_key=True)
	productname= db.Column(db.String(120), unique=False, nullable=False)
	price= db.Column(db.Integer,unique=False,nullable=False)
	quantity= db.Column(db.Integer,unique=False,nullable=False)
	description= db.Column(db.String(120), unique=False, nullable=False)
	image= db.Column(db.String(120), unique=False, nullable=False)
	date= db.Column(db.String(12), unique=False, nullable=True)
	selleremail= db.Column(db.String(120), unique=False, nullable=False)

class Cart(db.Model):
	
	sno= db.Column(db.Integer, primary_key=True)
	productname= db.Column(db.String(120), unique=False, nullable=False)
	productprice= db.Column(db.Integer,unique=False,nullable=False)
	quantity= db.Column(db.Integer,unique=False,nullable=False)
	description= db.Column(db.String(120), unique=False, nullable=False)
	image= db.Column(db.String(120), unique=False, nullable=False)
	date= db.Column(db.String(12), unique=False, nullable=True)
	seller= db.Column(db.String(120), unique=False, nullable=False)
	buyer= db.Column(db.String(120), unique=False, nullable=False)

class Purchased(db.Model):
	sno= db.Column(db.Integer, primary_key=True)
	productname= db.Column(db.String(120), unique=False, nullable=False)
	price= db.Column(db.Integer,unique=False,nullable=False)
	quantity= db.Column(db.Integer,unique=False,nullable=False)
	description= db.Column(db.String(120), unique=False, nullable=False)
	image= db.Column(db.String(120), unique=False, nullable=False)
	date= db.Column(db.String(12), unique=False, nullable=True)
	seller= db.Column(db.String(120), unique=False, nullable=False)
	buyer= db.Column(db.String(120), unique=False, nullable=False)




@app.route('/')
def hello():
	return render_template('createaccount.html')


@app.route('/login.html')
def getintry():
	return render_template('login.html')

@app.route('/createaccount.html')
def nice():
	return render_template('createaccount.html')

@app.route('/alreadytaken.html')
def goo():
	return render_template('alreadytaken.html')

@app.route('/<string:pagename>')
def pagename(pagename):
	if "email" in session:
		try:
			return render_template(pagename)
		except:
			if(session["role"]==buyer):
				purchasedgoods=Purchased.query.filter_by(buyer=session["email"]).all()
				productsavailable=Products.query.filter_by().all()
				return render_template('shopingsite.html',productsavailable=productsavailable,purchasedgoods=purchasedgoods)
			else:
				customers=Purchased.query.filter_by(seller=session["email"])
				sellerproducts=Products.query.filter_by(selleremail=session["email"]).all()
				return render_template('sellersinterface.html',yourproducts=sellerproducts,customers=customers)

	else:
		return redirect(url_for('checker'))
	
	


def namecheck(name):
	num=Userdetails.query.filter_by(email=name).count()
	if num>0:
		return False
	else:
		return True


def save(data):
	username=data["username"]
	password=data["password"]
	email=data['email']
	role=data['role']
	entry=Userdetails(email=email,role=role, username=username,password=password,date=datetime.now())
	db.session.add(entry)
	db.session.commit()

def passcheck(peru,passu):
	val=Userdetails.query.filter_by(email=peru).first()
	if(val.password==passu):
		return True
	else:
		return False

def saveproduct(product,imagename):
	productname=product["nameofproduct"]
	quantity=product["number"]
	price=product["price"]
	description=product["description"]
	selleremail=session["email"]
	image="static/images/"+imagename
	productsaver=Products(selleremail=selleremail,productname=productname,price=price,quantity=quantity,description=description,image=image,date=datetime.now()
	)
	db.session.add(productsaver)
	db.session.commit()

def cartsaver(cartitem):
	buyer=session["email"]
	productname=cartitem["productname"]
	seller=cartitem["selleremail"]
	productprice=cartitem["price"]
	quantity=cartitem["quantity"]
	description=cartitem["description"]
	image=cartitem["image"]
	cartstuff=Cart(buyer=buyer,seller=seller,productname=productname,productprice=productprice,quantity=quantity,description=description,image=image,date=datetime.now())
	db.session.add(cartstuff)
	db.session.commit()
	
def purchasedstuff(bought):
	buyer=session["email"]
	productname=bought["productname"]
	seller=bought["selleremail"]
	price=bought["price"]
	quantity=bought["quantity"]
	description=bought["description"]
	image=bought["image"]
	sold=Purchased(buyer=buyer,seller=seller,productname=productname,price=price,quantity=quantity,description=description,image=image,date=datetime.now())
	db.session.add(sold)
	db.session.commit()




@app.route('/login',methods=['POST','GET'])
def login():
	if(request.method=='POST'):
		data=request.form.to_dict()
		if(namecheck(data["email"])):
			if data["check"]==data["password"]:
				save(data)
				return redirect('login.html')
			else:
			    return redirect('createaccount.html')
		else:
			return redirect('alreadytaken.html')

@app.route('/checklogin',methods=['POST','GET'])
def checker():
	if(request.method=='POST'):
		data1=request.form.to_dict()
		if(namecheck(data1["email"])):
			return render_template('createagain.html')
		else:
			if(passcheck(data1["email"],data1["password"])):
				session["email"]=data1["email"]
				person=Userdetails.query.filter_by(email=session["email"]).first()
				session["role"]=person.role
				
				if(person.role=="seller"):
					return redirect(url_for("seller"))
				else:
					return redirect(url_for('buyer'))
			else:
				return render_template('createagain.html')


@app.route('/shopyourgoods')
def buyer():
	if('email' in session and session["role"]=='buyer'):
		purchasedgoods=Purchased.query.filter_by(buyer=session["email"]).all()
		productsavailable=Products.query.filter_by().all()
		return render_template('shopingsite.html',productsavailable=productsavailable,purchasedgoods=purchasedgoods)
	else:
		return render_template('login.html')

@app.route('/addedtocart',methods=['POST','GET'])
def cart():
	if(request.method=='POST'):
		cartitem=request.form.to_dict()
		cartsaver(cartitem)
		productsavailable=Products.query.filter_by().all()
		purchasedgoods=Purchased.query.filter_by(buyer=session["email"]).all()
		return render_template('shopingsite.html',productsavailable=productsavailable,purchasedgoods=purchasedgoods)
	else:
		if('email' in session and session["role"]=='buyer'):
			return redirect('buyer')
		else:
			return redirect('checker')

@app.route('/searchgoods',methods=['POST','GET'])
def search():
	if(request.method=='POST'):
		searchproducts=request.form.to_dict()
		searched=Products.query.filter_by(productname=searchproducts["searched"]).all()
		purchasedgoods=Purchased.query.filter_by(buyer=session["email"]).all()
		productsavailable=Products.query.filter_by().all()
		return render_template('search.html',productsavailable=productsavailable,searched=searched,purchasedgoods=purchasedgoods)
	else:
		if('email' in session and session["role"]=='buyer'):
			return redirect('buyer')
		else:
			return redirect('checker')




@app.route('/incart')
def gocart():
	if('email' in session and session["role"]=='buyer'):
		person=Cart.query.filter_by(buyer=session['email']).all()
		return render_template('cart.html',person=person)
	else:
		return redirect('checker')

@app.route('/purchased',methods=['POST','GET'])
def purchase():
	if(request.method=='POST'):
		bought=request.form.to_dict()
		purchasedstuff(bought)
		Cart.query.filter_by(seller=bought["selleremail"],buyer=session["email"],productname=bought["productname"],productprice=bought["price"]).delete()
		db.session.commit()
		update=Products.query.filter_by(image=bought["image"]).first()
		if(update.quantity>0):
			update.quantity-=1
		else:
			update.quantity==0
		db.session.commit()
		person=Cart.query.filter_by(buyer=session['email']).all()
		return render_template('cart.html',person=person)
	else:
		if('email' in session and session["role"]=='buyer'):
			return redirect('gocart')
		else:
			return redirect('checker')

@app.route('/yourproducts')
def seller():
	if('email' in session and session["role"]=='seller'):
		customers=Purchased.query.filter_by(seller=session["email"])
		sellerproducts=Products.query.filter_by(selleremail=session["email"]).all()
		return render_template('sellersinterface.html',yourproducts=sellerproducts,customers=customers)
	else:
		return redirect('checker')


@app.route('/uploaded',methods=['POST','GET'])
def upload():
	if(request.method=='POST'):
		target= os.path.join(APP_ROOT,'static/images/')
		product=request.form.to_dict()
		for file in request.files.getlist("file"):
			filename=file.filename
			saveproduct(product,filename)
			destination="/".join([target,filename])
			file.save(destination)
		return redirect(url_for("seller"))
	else:
		if('email' in session and session["role"]=='seller'):
			return redirect('seller')
		else:
			return redirect('checker')




app.run(debug=True)	

