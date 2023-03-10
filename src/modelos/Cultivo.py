
from config.bd import db, ma, app

class Cultivo(db.Model):
    __tablename__ = 'Cultivo'
    id = db.Column(db.Integer, primary_key=True)
    N_lote = db.Column(db.Integer, db.ForeignKey('Lote.num_lote'))
    Fruta = db.Column(db.String(50))
    Existencias = db.Column(db.Integer)

    def __init__(self, N_lote, Fruta, Existencias):
        #self.id = id
        self.N_lote = N_lote
        self.Fruta = Fruta
        self.Existencias = Existencias

with app.app_context():
    db.create_all()

class CultivoSchema(ma.Schema):
    class Meta:
        fields = ('id','N_lote', 'Fruta', 'Existencias')
