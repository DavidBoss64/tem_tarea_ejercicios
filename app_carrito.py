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

if __name__ =='__main__':
    app.run(debug=True)