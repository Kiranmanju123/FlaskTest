from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from flask import request
from flask.json import jsonify
import json
from flask_cors import CORS
from flask_marshmallow import Marshmallow


app= Flask(__name__) 

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class AdminInfo(db.Model):
	admin_id=db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(50),nullable=False)
	password = db.Column(db.String(50),nullable=False)
	created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

	def __str__(self):
		return self.username

class Employee(db.Model):
	employee_id = db.Column(db.Integer,primary_key=True)
	employee_name = db.Column(db.String(50),nullable=False)
	employee_address = db.Column(db.String(50),nullable=False)
	employee_position = db.Column(db.String(50),nullable=False)
	employee_department = db.Column(db.String(50),nullable=False)
	employee_salary = db.Column(db.Integer, nullable=True)
	is_employee_full_time = db.Column(db.Boolean, default=True)
	projects = db.relationship("Project",backref="employee")
	created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

	def __str__(self):
		return self.employee_name


class Project(db.Model):
	project_id = db.Column(db.Integer,primary_key=True)
	project_name = db.Column(db.String(50),nullable=False)
	project_description = db.Column(db.String(50),nullable=False)
	employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
	created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)


admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(AdminInfo, db.session))
admin.add_view(ModelView(Employee, db.session))
admin.add_view(ModelView(Project, db.session))


@app.route("/")
def home():
	return "HEllo"


@app.route("/createAdmin",methods=['POST'])
def createAdmin():
	data = request.get_json()
	adminInfo=AdminInfo(username=data['username'],password=data['password'])
	db.session.add(adminInfo)
	db.session.commit()
	return jsonify({"info":"created"})


@app.route("/login",methods=['POST'])
def adminLogin():
	data = request.get_json()
	if not data:
		return jsonify({"info":"Data Required"})
	login = AdminInfo.query.filter(AdminInfo.username==data["username"]).filter(AdminInfo.password==data["password"]).first()
	if login:
		return jsonify({"info":"Login Success","status":"success"})
	else:
		return jsonify({"info":"Wrong Crenditials","status":"failure"})


@app.route("/createEmployee",methods=['POST'])
def createEmployee():
	data = request.get_json()
	if not data:
		return jsonify({"info":"Data Required"}),400
	employee = Employee(**data)
	db.session.add(employee)
	db.session.commit()
	return jsonify({"info":"created","status":"success"})

class EmployeeSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model=Employee
		load_instance = True

@app.route("/getAllEmployee",methods=['GET'])
def getAllEmployee():
	employee_schema = EmployeeSchema(many=True)
	data = Employee.query.all()
	print(data)
	serialized_data =  employee_schema.dump(data)
	return jsonify({"info":serialized_data})

@app.route("/getSingleEmployee",methods=['GET'])
def getSingleEmployee():
	employee_id = request.args.get('employee_id')
	employee_schema = EmployeeSchema(many=True)
	data = Employee.query.filter_by(employee_id=employee_id)
	serialized_data =  employee_schema.dump(data)
	return jsonify({"info":serialized_data})



@app.route("/deleteEmployee",methods=['DELETE'])
def deleteEmployee():
	employee_id = request.args.get('employee_id')
	if not employee_id:
		return jsonify({"info":"Employee Id Required"}),400
	employee = Employee.query.filter_by(employee_id=employee_id)
	employee.delete()
	db.session.commit()
	return jsonify({"info":"deleted"})

@app.route("/updateEmployee",methods=['PUT'])
def updateEmployee():
	data = request.get_json()
	if not data:
		return jsonify({"info":"Data Required"}),400
	employee_id = request.args.get('employee_id')
	if not employee_id:
		return jsonify({"info":"Employee Id Required"}),400
	employee = Employee.query.filter_by(employee_id=employee_id)
	if not employee.first():
		return jsonify({'error': 'employee not found'})
	employee.update(data)
	db.session.commit()
	return jsonify({"updated":data})
