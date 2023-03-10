
from config.bd import db, ma, app

class Lote(db.Model):
    __tablename__ = 'Lote'
    num_lote = db.Column(db.Integer, primary_key=True)
    nit_finca = db.Column(db.Integer, db.ForeignKey('Finca.nit'))
    nombre = db.Column(db.String(50))
    responsable = db.Column(db.Integer, db.ForeignKey('Responsable.id'))

    def __init__(self, nit_finca, nombre, responsable):
        #self.num_lote = num_lote
        self.nit_finca = nit_finca
        self.nombre = nombre
        self.responsable = responsable

with app.app_context():
    db.create_all()

class LoteSchema(ma.Schema):
    class Meta:
        fields = ('num_lote', 'nit_finca', 'nombre', 'responsable')
