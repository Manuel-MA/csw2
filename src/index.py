import sqlite3
#import easygui as eg
from flask import Flask, render_template, redirect, url_for, request, g, session
app=Flask(__name__)
app.secret_key = 'qwerty12345'

DATABASE = 'var/forum.db'

logged = '<form action="/logout" method="post"><input class="btn btn-default" type="submit" value="Logout"> </form>'
notLogged = '<form action="/login" method="post"><input type="text" placeholder="Username" name="username"><input type="password" placeholder="Password" name="password"><input class="btn btn-default" type="submit" value="Login"></form>'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def home():
	try:
		if (session['name']):
			login = logged
			return render_template('home.html',login=login),200
	except KeyError:
		pass
	login = notLogged
	return render_template('home.html',login=login),200
	
# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	db = get_db()
	cursor = db.cursor()
	login = logged
	if request.method == 'POST':
		name = (request.form['username'])
		session['name']= name
		password = (request.form['password'])
		cursor.execute('SELECT * FROM user WHERE login="%s" AND password="%s"' % (name, password))
		if cursor.fetchone() is not None:
			return render_template('home.html', name=name, login=login),200
		else:
			return render_template('invalidLogin.html', name=name),200
	return page_not_found(404)
	
@app.route('/logout', methods=['GET', 'POST'])
def logout():
	if request.method == 'POST':
		session.pop('name', None)
		login = notLogged
		return render_template('home.html', login=login),200

@app.route('/invalidLogin')
def invalidLogin():
		return render_template('invalidLogin')
	
@app.route("/display/<table>")
def showTables(table=None):
	try:
		if (session['name']):
			login = logged
	except KeyError:
		login = notLogged
		pass		
	
	tab = {'table':table}
	cursor = get_db().cursor()
	page = ""
	if table == "worker":
		sql = " SELECT rowid , * FROM worker"
		page = page + '<h1>Workers table</h1><table class="table table-striped"><thead><tr><th>Firstname</th><th>Lastname</th><th>E-mail</th><th>Date of Birth</th><th>Post</th><th>Action</th></tr></thead><tbody>'
		for row in cursor.execute(sql):
			page = page + '<tr>'
			page = page + '<td class="tdTable"> {0} </td>'.format(row[2])
			page = page + '<td class="tdTable"> {0} </td>'.format(row[3])
			page = page + '<td class="tdTable"> {0} </td>'.format(row[6])
			page = page + '<td class="tdTable"> {0} </td>'.format(row[4])
			page = page + '<td class="tdTable"> {0} </td>'.format(row[5])
			page = page + '<td> <a class="btn btn-warning" href="/display/'+table+'/edit/{0}">Edit</a>'.format(row[1])
			page = page + '<a class="btn btn-danger" href="/display/'+table+'/delete/{0}">Delete</a> </td>'.format(row[1])
	elif table == "department":
		sql = " SELECT rowid , * FROM department"
		page = page + '<h1>Departaments table</h1><table class="table table-striped"><thead><tr><th>Department</th><th>Location</th><th>Action</th></tr></thead><tbody>'
		for row in cursor.execute(sql):
			page = page + '<tr>'
			page = page + '<td class="tdTable"> {0} </td>'.format(row[2])
			page = page + '<td class="tdTable"> {0} </td>'.format(row[3])
			page = page + '<td> <a class="btn btn-warning" href="/display/'+table+'/edit/{0}">Edit</a>'.format(row[1])
			page = page + '<a class="btn btn-danger" href="/display/'+table+'/delete/{0}">Delete</a> </td>'.format(row[1])
	elif table == "intership":
		sql = " SELECT rowid , * FROM intership"
		page = page + '<h1>Interships table</h1><table class="table table-striped"><thead><tr><th>Firstname</th><th>Lastname</th><th>E-mail</th><th>Date of Birth</th><th>University</th><th>Action</th></tr></thead><tbody>'
		for row in cursor.execute(sql):
			page = page + '<tr>'
			page = page + '<td class="tdTable"> {0} </td>'.format(row[2])
			page = page + '<td class="tdTable"> {0} </td>'.format(row[3])
			page = page + '<td class="tdTable"> {0} </td>'.format(row[6])
			page = page + '<td class="tdTable"> {0} </td>'.format(row[5])
			page = page + '<td class="tdTable"> {0} </td>'.format(row[4])
			page = page + '<td> <a class="btn btn-warning" href="/display/'+table+'/edit/{0}">Edit</a>'.format(row[1])
			page = page + '<a class="btn btn-danger" href="/display/'+table+'/delete/{0}">Delete</a> </td>'.format(row[1])
	else:
		return page_not_found(404)
	page = page + '</tr>'
	page = page + '</tbody></table>'
	page = page + '<a href="/display/'+table+'/add" class="btn btn-default">Add new '+table+'</a>'
	page = page + '<a href="/" class="btn btn-default">Back</a>'

	return render_template('tables.html', page=page, login=login),200
	
	
		
@app.route("/display/<table>/add")
def displayForms(table=None):
	try:
		if(session['name']):
			tab = {'table':table}
			cursor = get_db().cursor()
			tableInput = ""
			if table == "worker":
				tableInput= "worker"
				return render_template('workerForm.html', tableInput=tableInput),200
			elif table == "department":
				tableInput= "department"
				return render_template('departmentForm.html', tableInput=tableInput),200
			elif table == "intership":
				tableInput= "intership"
				return render_template('intershipForm.html', tableInput=tableInput),200
			else:
				return page_not_found(404)
			
	except KeyError:
		pass
	return render_template('noLogin.html'),200
	
@app.route("/display/<table>/delete/<id>")
def deleteRegister(table=None, id=None):
	#eg.ynbox(msg='Are you sure that you want to delete this register?',
	#			title='Delete',
	#			choices=('Yes', 'No'),
	#			image=None)
	try:
		if(session['name']):
			tab = {'table':table}
			id1 = {'id':id}
			print table + id
			db = get_db()
			cursor = db.cursor()
			cursor.execute("DELETE FROM "+table+" WHERE id="+id)
			db.commit()
			return redirect(url_for('showTables',table=table))
	except KeyError:
		pass
	return render_template('noLogin.html'),200
	
@app.route("/new/<table>", methods=['GET', 'POST'])
def insertData(table=None):
	if request.method == "POST":
		name = (request.form['name'])
		db = get_db()
		cursor = db.cursor()
		if table == "worker":
			surname = (request.form['surname'])
			post = (request.form['post'])
			bday = (request.form['birthday'])
			mail = (request.form['email'])
			departament = (request.form['departament'])
			cursor.execute("insert into worker (name, surname, post, dateOfBirth, email, department) values (?, ?, ?, ?, ?, ?)", (name, surname, post, bday, mail, departament))
			db.commit()
			return showTables('worker')
		elif table == "department":
			location = (request.form['location'])
			cursor.execute("insert into department (name, location) values (?, ?)", (name, location))
			db.commit()
			return showTables('department')
		elif table == "intership":
			surname = (request.form['surname'])
			university = (request.form['university'])
			bday = (request.form['birthday'])
			mail = (request.form['email'])
			department = (request.form['department'])
			cursor.execute("insert into intership (name, surname, university, dateOfBirth, email, department) values (?, ?, ?, ?, ?, ?)", (name, surname, university, bday, mail, department))
			db.commit()
			return showTables('intership')
		else:
			return page_not_found(404)
			
@app.route("/edit/<table>", methods=['GET', 'POST'])
def editData(table=None):
	if request.method == "POST":
		name = (request.form['name'])
		db = get_db()
		cursor = db.cursor()
		id = (request.form['id'])
		if table == "worker":
			surname = (request.form['surname'])
			post = (request.form['post'])
			bday = (request.form['birthday'])
			mail = (request.form['email'])
			departament = (request.form['departament'])
			cursor.execute("UPDATE worker SET name = ?, surname = ?, post = ?, dateOfBirth = ?, email = ?, department = ? WHERE id = ?", (name, surname, post, bday, mail, departament, id))
			db.commit()
			return showTables('worker')
		elif table == "department":
			location = (request.form['location'])
			cursor.execute("UPDATE department SET name = ?, location = ? WHERE id = ?", (name, location, id))
			db.commit()
			return showTables('department')
		elif table == "intership":
			surname = (request.form['surname'])
			university = (request.form['university'])
			bday = (request.form['birthday'])
			mail = (request.form['email'])
			department = (request.form['department'])
			cursor.execute("UPDATE intership SET name = ?, surname = ?, university = ?, dateOfBirth = ?, email = ?, department = ? WHERE id = ?", (name, surname, university, bday, mail, departament, id))
			db.commit()
			return showTables('intership')
		else:
			return page_not_found(404)
@app.route("/display/<table>/edit/<id>")
def fillForms(table=None,id=None):
	try:
		if(session['name']):
			db = get_db()
			cursor = db.cursor()
			tab = {'table':table}
			id1 = {'id':id}
			sql = "SELECT rowid , * FROM "+table+" where id="+id
			if table == "worker":
				for row in cursor.execute(sql):
					id=row[1]
					name=row[2]
					surname=row[3]
					post=row[4]
					birthday=row[5]
					email=row[6]
					department=row[7]
				return render_template('workerFormFill.html', table=table, id=id, email=email, department=department, birthday=birthday, name=name, surname=surname, post=post),200
			elif table == "department":
				for row in cursor.execute(sql):
					id=row[1]
					name=row[2]
					location=row[3]
				return render_template('departmentFormFill.html', table=table, id=id, name=name, location=location),200
			elif table == "intership":
				for row in cursor.execute(sql):
					id=row[1]
					name=row[2]
					surname=row[3]
					university=row[4]
					birthday=row[5]
					email=row[6]
					department=row[7]
				return render_template('intershipFormFill.html', table=table, id=id, email=email, department=department, birthday=birthday, name=name, surname=surname, university=university),200
			else:
				return page_not_found(404)
	except KeyError:
		pass
	return render_template('noLogin.html'),200	
	
@app.route("/redirect", methods=['GET', 'POST'])
def redirect2():
	try:
		if (session['name']):
			login = logged
	except KeyError:
		login = notLogged
		pass
	return render_template('home.html', login=login),200


@app.errorhandler(404)
def page_not_found(error):

  form = '''
  <html>
  <head>
    <link href="../static/css/bootstrap.min.css" rel="stylesheet"/>
    <link href="../static/css/style.css" rel="stylesheet"/>
  <body>
    <div id="container">
    <h1> ERROR, the requested URL is not valid</h1>
      <div class="mainImgContainer">
        <h3> Let us take you back </h3>
        <br/><br/><br/>
        <form action="/redirect" method="post" name="form">
          <input type="submit" value="Go Home!" class="btnGo btn btn-default btn-lg">
        </form>
      </div>
    </div>
  <html><body>
  '''
  return form	
	
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)