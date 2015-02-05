from flask import Flask, request, url_for, redirect
import sqlite3
app = Flask(__name__)
dbFile = 'db1.db'
conn = None
#tasks = []
def get_conn():
    global conn
    if conn is None:
        conn = sqlite3.connect(dbFile)
        conn.row_factory = sqlite3.Row
    return conn

@app.teardown_appcontext
def close_connection(exception):
    global conn
    if conn is not None:
        conn.close()
        conn = None

def query_db(query, args=(), one=False):
    cur = get_conn().cursor()
    cur.execute(query, args)
    r = cur.fetchall()
    cur.close()
    return (r[0] if r else None) if one else r 

def add_task(category, priority, description):
    task = query_db('insert into tasks(category, priority, description)  values(?,?,?)', [category, priority, description], one=True)
    get_conn().commit()
    
    
@app.route('/')
def welcome():
    return '<h1>Welcome to Flask lab!<h1>'    

@app.route('/task', methods = ['GET', 'POST'])
def task():
    #POST:
    if request.method == 'POST':
        category = request.form['category']
        priority = request.form['priority']
        description = request.form['description']
        add_task(category, priority, description)        
        #priority = request.form['priority']
        #tasks.append({'priority':priority})
        #return redirect('/task1')
        return redirect(url_for('task'))
    
    #GET:
    resp = '''
    <form action="" method = post>
    <p>Category: <input type='text' name='category'></p>
    <p>Priority: <input type='text' name='priority'></p>
    <p>Description: <input type='text' name='description'></p>
    <p><input type='submit' value='Add'></p>
    </form>
    
    '''
    
    resp = resp + '''
    <table border="1" cellpadding="3">
    <body>
         <tr>
             <td>Category</td>
             <td>Priority</td>
             <td>Description</td>
               </tr>
    '''
    for task in query_db('select * from tasks'):
        resp = resp + "<tr><td>%s</td>" %(task['category']) + "<td>%s</td>" %(task['priority']) + "<td>%s</td></tr>" %(task['description'])
    resp = resp + '</tbody></table>'
    return resp

if __name__ == '__main__':
    app.debug = True
    app.run()
    #query_db('delete from tasks')
    #print_tasks()
    #add_task('CMPUT410')
    #add_task('Shopping')
    #add_task('Coding')
    #print_tasks()