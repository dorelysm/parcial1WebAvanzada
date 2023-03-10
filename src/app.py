from flask import Flask, redirect, request, jsonify, json, session, render_template

from config.bd import app, db
from modelos.Responsable import Responsable, ResponsableSchema
from modelos.Usuario import User, UsersSchema
from modelos.Finca import Finca, FincaSchema
from modelos.Lote import Lote, LoteSchema
from modelos.Cultivo import Cultivo, CultivoSchema
from modelos.Venta import Venta, VentaSchema


responsable_schema = ResponsableSchema()
responsables_schema = ResponsableSchema(many=True)

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

finca_schema = FincaSchema()
fincas_schema = FincaSchema(many=True)

lote_schema = LoteSchema()
lotes_schema = LoteSchema(many=True)

cultivo_schema = CultivoSchema()
cultivos_schema = CultivoSchema(many=True)

venta_schema = VentaSchema()
ventas_schema = VentaSchema(many=True)

@app.route('/', methods=['GET'])
def index():
    
    return render_template("login.html")

@app.route('/ingresar', methods=['POST'])
def ingresar():
    email = request.form['email']
    password = request.form['password']
    user = db.session.query(User.id).filter(User.email == email, User.password == password).all()
    resultado = users_schema.dump(user)

    if len(resultado)>0:
        session['usuario'] = email
        return redirect('/lcultivos')
    else:
        return redirect('/')

@app.route('/lcultivos', methods=['GET'])
def lcultivos():
    if 'usuario' in session:
        all_cultivos = Cultivo.query.all()
        result_cultivos = cultivos_schema.dump(all_cultivos)
        return render_template("lcultivos.html", cultivos = result_cultivos, usuario= session['usuario'])
    else:
        return redirect('/')
   
@app.route('/cerrar')
def cerrar():
    session.pop('usuario',None)
    return redirect('/')

@app.route('/guardar', methods=['POST'] )
def guardar_cultivo():
    N_lote = request.form['N_lote']
    Fruta = request.form['Fruta']
    Existencias = request.form['Existencias']
    new_cultivo = Cultivo(N_lote, Fruta, Existencias)
    db.session.add(new_cultivo)
    db.session.commit()
    return redirect('/lcultivos')

@app.route('/eliminar', methods=['GET'] )
def eliminar():
    id = request.args.get('id')
    cultivos = Cultivo.query.get(id)
    db.session.delete(cultivos)
    db.session.commit()
    return cultivo_schema.dump(cultivos)

@app.route('/cultivos', methods=['GET'] )
def cultivos():
    id = request.args.get('id')
    cultivos = Cultivo.query.get(id)
    restul_cultivos = cultivo_schema.dump(cultivos)
    return jsonify(restul_cultivos)

@app.route('/actualizar', methods=['POST'] )
def actualizar():
    id = request.form['id']
    #print('id: ', id)
    N_lote = request.form['N_lote']
    Fruta = request.form['Fruta']
    Existencias = request.form['Existencias']
    cultivo = Cultivo.query.get(id)
    cultivo.N_lote = N_lote
    cultivo.Fruta = Fruta
    cultivo.Existencias = Existencias
    db.session.commit()
    return redirect('/lcultivos')

@app.route('/consultar3tabla', methods=['GET'])
def consultar3tablas():
    datos= {}
    resultado = db.session.query(Responsable, Lote, Finca). \
        select_from(Responsable).join(Lote).join(Finca).all()
    i=0
    for responsable, lote, finca  in resultado:
        i+=1
        datos[i]={
           
                'Rname': responsable.nombre,
                'Lname': lote.nombre,
                'Fname': finca.nombre          
        }
    print(datos)
    return "Algo"

@app.route('/lfincas', methods=['GET'])
def fincas():
    if 'usuario' in session:
        all_fincas = Finca.query.all()
        result_fincas = fincas_schema.dump(all_fincas)
        return render_template("lfincas.html", fincas = result_fincas, usuario= session['usuario'])
    else:
        return redirect('/')
    
@app.route('/llotes', methods=['GET'])
def lotes():
    if 'usuario' in session:
        all_lotes = Lote.query.all()
        result_lotes = lotes_schema.dump(all_lotes)
        all_fincas = Finca.query.all()
        result_fincas = fincas_schema.dump(all_fincas)
        all_responsables = Responsable.query.all()
        result_responsables = responsables_schema.dump(all_responsables)
        return render_template("llotes.html", lotes = result_lotes, fincas = result_fincas, responsables = result_responsables, usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/lventas', methods=['GET'])
def ventas():
    if 'usuario' in session:
        all_ventas = Venta.query.all()
        result_venta = ventas_schema.dump(all_ventas)
        return render_template("lventas.html", ventas = result_venta, usuario= session['usuario'])
    else:
        return redirect('/')
    
@app.route('/guardar_finca', methods=['POST'])
def guardar_finca():
    #nit = request.form['nit']
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    contacto = request.form['contacto']
    correo = request.form['correo']
    propietario = request.form['propietario']
    new_finca = Finca(nombre, contacto, direccion, correo, propietario)
    db.session.add(new_finca)
    db.session.commit()
    return redirect('/lfincas')

@app.route('/guardar_lote', methods=['POST'])
def guardar_lote():
    nit_finca = request.form['nit_finca']
    nombre = request.form['nombre']
    responsable = request.form['id_responsable']
    
    new_lote = Lote(nit_finca, nombre, responsable)
    db.session.add(new_lote)
    db.session.commit()
    return redirect('/llotes')

@app.route('/guardar_venta', methods=['POST'])
def guardar_venta():
    id_cultivo = request.form['id_cultivo']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    
    new_venta = Venta(id_cultivo, precio, cantidad)
    db.session.add(new_venta)
    #db.session.commit()

    cultivo = Cultivo.query.get(id_cultivo)
    cultivo.Existencias = cultivo.Existencias - int(cantidad)
    db.session.commit()

    return redirect('/lventas')

if __name__ == "__main__":
    app.run(debug=True)

