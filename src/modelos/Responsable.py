from config.bd import db, ma, app

class Responsable(db.Model):
    __tablename__ = 'Responsable'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    celular = db.Column(db.String(50))
    correo = db.Column(db.String(50))

    def __init__(self, nit, nombre, celular, correo):
        self.id = id
        self.nombre = nombre
        self.celular = celular
        self.correo = correo

with app.app_context():
    db.create_all()

class ResponsableSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'celular', 'correo')