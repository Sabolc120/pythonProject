from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#Adatbázishoz SQLAlchemyt használtunk, MQSQL-t.
app = Flask(__name__)

#Ha ezt nem adnánk hozzá amiatt error lenne.
app.secret_key = "megoldando"

#Adatbázis csatlakozás 1.Felhasználonév, 2. Jelszo, ami ez esetben semmi mivel nem kellet., 3. A tábla neve amit használjon.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/pythoncrud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Lényegében ez itt a model, ez arra kell, hogy automatikus létrejöjjön a tábla, milyen adattipusokat akarunk használni, mint mikor egy táblát készitünk MqSQL-ben.
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    position = db.Column(db.String(100))

    def __init__(self, name, email, phone, position):
        self.name = name
        self.email = email
        self.phone = phone
        self.position = position

#Ez lesz a kezdöoldal, ha uresen hagyjuk akkor mindig mikor meglátogatjuk az URLT, ezt fogja elöször feldobni
@app.route("/")
def index():
    all_data = Data.query.all()

    #Itt az láthato hogy milyen html fált szeretnénk hogy betöltsön abban az esetben ha meglátogatjuk az oldalt.
    return render_template("index.html", employees=all_data)


#Ez itt a delete route, a deletehez szükséges az ID, annak az elemnek az ID-ja amit ki akarunk törölni, különben nem fogja tudni mit töröljön.
@app.route("/delete/<id>", methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id) #Itt vonjuk ki az ID-t az URL-bol. mert ez valojában igy néz ki: (address)/delete/1
    db.session.delete(my_data) #Az ORM felismeri mit akarunk tenni, bármiféle query irás nélkül. ORM: Object-relational mapping
    db.session.commit()

    #Ha sikeres volt a müvelet, ide dobjon vissza.
    return redirect(url_for('index'))


#Ez itt az update route
@app.route("/update", methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id')) #Megint csak egy beépitett funkcio SQLAlchemyben.

        my_data.name = request.form['name'] #Kinyerjük a formba irt adatokat mikor updatelünk.
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.position = request.form['position']

        db.session.commit()

        return redirect(url_for('index'))


#Hozzáadás metodus
@app.route("/insert", methods=["POST"]) #Mindig mikor hozzáadunk az egy POST metodus lesz.
def insert():
    if request.method == 'POST':
        name = request.form['name'] #Megint csak kinyerjük az adatokat a formbol
        email = request.form['email']
        phone = request.form['phone']
        position = request.form['position']

        my_data = Data(name, email, phone, position) #Majd pedig azt beillesztjük a model segitségével.
        db.session.add(my_data)
        db.session.commit()

        return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all() #Enélkül hibára futna, mert elöbb lére kell hozni a táblát bármi elött.
        app.run(debug=True)
