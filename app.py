from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#Simularemos nuestra tabla de base de datos

contactos = []
contador_id = 1

#READ: Leer nuestra tabla de base de datos
@app.route('/')
def index():
    return render_template('contactos.html',contactos=contactos)

#CREATE: Agregar un nuevo contacto a nuestra tabla de contactos
@app.route('/crear', methods = ['POST'])
def crear():
    global contador_id
    contactos.append({
        'id':contador_id,
        'nombre':request.form['nombre'],
        'correo':request.form['correo'],
        'celular':request.form['celular']
    })
    contador_id +=1
    return redirect(url_for('index'))

#UPDATE: Actualizar un contacto existente
@app.route('/actualizar/<int:id_contacto>', methods = ['GET','POST'])
def editar(id_contacto):
    #Buscaremos el cotacto por su id
    contacto_actual = next((c for c in contactos if c['id']==id_contacto),None)

    if request.method ==  'POST':
        # Si envian el formulario, actualizaremos los datos
        if contacto_actual:
            contacto_actual['nombre']=request.form['nombre']
            contacto_actual['correo']=request.form['correo']
            contacto_actual['celular']=request.form['celular']
        return redirect(url_for('index'))

    #Si es metodo GET, mostraremos el formulario con los datos actuales    
    return render_template('editar.html',contacto=contacto_actual)

#DELETE: Eliminar un contacto
@app.route('/eliminar/<int:id_contacto>')
def eliminar(id_contacto):
    global contactos
    contactos = [c for c in contactos if c['id']!=id_contacto]
    return redirect(url_for('index',mensaje='Contacto eliminado'))

if __name__ =='__main__':
    app.run(debug=True)