from flask import Flask, request,send_file
from flask_cors import CORS
from rm import getphoto
import random

app = Flask(__name__)
CORS(app)
@app.route('/')
def home():
    return "Hello, Flask from VS Code!"

@app.route('/api', methods=['GET'])
def get_image_ready():
    img_name = request.args.get('path')
    type_photo= request.args.get('category')
    num=int(request.args.get('num'))
    size=request.args.get('size')
    str_path=getphoto(img_name,type_photo,size,num)
    return send_file(str_path, mimetype='image/jpeg')

@app.route('/api', methods=['POST'])
def upload_image(): 
    img = request.files.get('img')
    if not img:
        return "No file uploaded", 400
    name=img.filename.split(".")[0]
    extension=img.filename.split(".")[1]
    result=name+str(random.randint(0,1000))+"."+extension
    img.save(result)
    return result
    # Aquí puedes manejar la carga de imágenes
    #return f"Image name: {img_name}"
    # Aquí puedes agregar la lógica para procesar la imagen
    # Por ejemplo, llamar a la función que genera el DNI
    # y devolver la imagen generada como respuesta
if __name__ == '__main__':
    app.run(debug=True)
