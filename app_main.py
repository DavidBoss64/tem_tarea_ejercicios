from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#Simularemos la base de datos con una lista de productos

carrito = [
    {
        'nombre':'Producto 1',
        'precio':10.0,
        'cantidad':2,
        'subtotal':20.0

    }
]

@app.route('/')
def index():
    #calcularemos el total sumando el subtotal de cada producto
    total_compra = sum(item['precio']*item['cantidad'] for item in carrito)

    #renderizamos la plantilla enviando la lista y el total
    return render_template('index.html', carrito=carrito, total = total_compra)


#en flask manejamos el metodo POST para enciar datos al servidor
@app.route('/agregar', methods = ['POST'])
def agregar():
    #Recuperaremos los datos del formulario usando request.form
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    cantidad = int(request.form['cantidad'])

    #Agregamos el nuevo producto al carrito

    carrito.append({
        'nombre':nombre,
        'precio':precio,
        'cantidad':cantidad,
        'subtotal':precio*cantidad
    })

    #Redirigimos al usuario de vuelta a la pagina principal
    return redirect(url_for('index'))


contactos = []
contador_id = 1


@app.route('/contact')
def contact():
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
    return redirect(url_for('contact'))

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
        return redirect(url_for('contact'))

    #Si es metodo GET, mostraremos el formulario con los datos actuales    
    return render_template('editar.html',contacto=contacto_actual)

#DELETE: Eliminar un contacto
@app.route('/eliminar/<int:id_contacto>')
def eliminar(id_contacto):
    global contactos
    contactos = [c for c in contactos if c['id']!=id_contacto]
    return redirect(url_for('contact',mensaje='Contacto eliminado'))


if __name__ =='__main__':
    app.run(debug=True)