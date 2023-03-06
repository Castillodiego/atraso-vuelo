from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions

#importamos la
from endpoints.atrasovuelo.resource import prediction



app = Flask(__name__)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
  
        data = "Algoritmo Atraso Vuelos"
        return jsonify({'data': data})


@app.route('/home', methods = ['GET'])
def disp():
    content_type = request.headers.get('Content-Type')
    """
    if (content_type == 'application/json'):
        json = request.json
        
    else:
        return 'Content-Type not supported!'
    """

    
    mes=request.args.get('MES')
    opera=request.args.get('OPERA')
    tipo_vuelo=request.args.get('TIPOVUELO')

    response=str(prediction(opera, mes, tipo_vuelo))
    print(response)
    #entry=request.query_string()
  
    return  jsonify({'response': response})


if __name__ == '__main__':
    app.run()
