from config.bd import db, ma, app

class Venta(db.Model):
    __tablename__ = 'Venta'
    id = db.Column(db.Integer, primary_key=True)
    id_cultivo = db.Column(db.Integer, db.ForeignKey('Cultivo.id'))
    precio = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)

    def __init__(self, id_cultivo, precio, cantidad):
        #self.id = id
        self.id_cultivo = id_cultivo
        self.precio = precio
        self.cantidad = cantidad

with app.app_context():
    db.create_all()

class VentaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_cultivo', 'precio','cantidad')