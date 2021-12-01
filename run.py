from flask import Flask,  render_template,  session, redirect, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker




app = Flask(__name__)
app.secret_key = b'.'




engine = create_engine('postgres://')


Base = declarative_base()

class Mydata(Base):
    __tablename__ = "mydata"  # テーブル名を指定
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    mail = Column(String(255))
    age = Column(Integer)

    def __init__(self,  name, mail, age):
        self.name = name
        self.mail = mail
        self.age = age






Base.metadata.create_all(engine)





@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def form():
    name = request.form.get('name')
    mail = request.form.get('mail')
    age = int(request.form.get('age'))
    mydata = Mydata(name=name, mail=mail, age=age)
    Session = sessionmaker(bind=engine)
    ses = Session()
    ses.add(mydata)
    ses.commit()
    datas = ses.query(Mydata).all()
    ses.close()



    return render_template('index.html', post=True, name=name, mail=mail, age=age, datas=datas)



@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html')


@app.route('/search', methods=['POST'])
def find():
    find = request.form.get('find')

    Session = sessionmaker(bind=engine)
    ses = Session()
    result = ses.query(Mydata).filter(Mydata.name == find).all()
    noinfo = ("まだ登録されていません。/ No registration.")
    ses.close()

    if result:
        res = False
    else:
        res = True

    return render_template('search.html', search=True, result=result,  noinfo = noinfo, res=res)









if __name__ == '__main__':
    app.run(debug=True)