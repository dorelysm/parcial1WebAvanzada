
from config.bd import db, ma, app

class Finca(db.Model):
    __tablename__ = 'Finca'
    nit = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contacto = db.Column(db.String(50))
    direccion = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    propietario = db.Column(db.String(50))

    def __init__(self, nombre, contacto, direccion, correo, propietario):
        #self.nit = nit
        self.nombre = nombre
        self.contacto = contacto
        self.direccion = direccion
        self.correo = correo
        self.propietario = propietario

with app.app_context():
    db.create_all()

class FincaSchema(ma.Schema):
    class Meta:
        fields = ('nit', 'nombre', 'contacto', 'direccion', 'correo', 'propietario')
