#all the imports
import sqlite3
from flask import Flask,g,request





#configfile
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'



app=Flask(__name__)
app.config.from_object(__name__)

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])
def get_db():
  if not hasattr(g,'sqlite_db'):
    g.sqlite_db=connect_db()
  return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
  if hasattr(g,'sqlite_db'):
    g.sqlite_db.close()

def init_db():
  with app.app_context():
    db = get_db()
    with app.open_resource('./schema.sql',mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

@app.route('/')
def show_entries():
  cur = g.db.excute('select title,text from entries order by id desc')
  entries = [dict(title=row[0],text=row[1]) for row in cur.fetchall()]
  return render_templates('show_entries.html',entries=entries)

if __name__=='__main__':
  app.run()

