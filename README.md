# Flask-RESTful API project for Neural Work

Este es el challenge de Neural Work realizado por Diego Castillo para el cargo de machine learning enginner

El proyecto tiene varias partes y se detallará lo más importante por aqui. Las herramientas utilizadas fueron

1. Flask - framework para realizar apis en python
2. GKE - Herramientas de Google Cloud Platform para desarollar contenedores Docker


Project structure:
```
.
├── README.md
├── app.py
├── endpoints
│   ├── __init__.py
│   └── atrasovuelo
│       ├── __init__.py
│       └── resource.py
├── trabajojuan
│   ├── atrasos-vuelos.py
│   ├── dataset_SCL.csv
│   ├── synthetic_features.csv
│   └── to-expose.ipynb
├── img
│   ├── flujo-GKE.png

├── deployment.yaml
├── service.yaml
├── requirements.txt
└── settings.py
```

Los archivos más importante son:
* trabajojuan/to-expose.ipynb - se toma el trabajo de juan, se intenta mejorar el modelo y luego se exportan las configuraciones del mejor modelo.
* endpoints/atrasovuelo/resource.py - se implementar el mejor modelo en formato adeacuado para la API.
* app.py - aplicación flask para inicializar y deployear api en maquina virtual.
* deployment.yaml - configuración para el deploy en docker en GCP.
* service.yaml - configuración para el service de docker en GCP.
* settings.py - configuración de variables de entorno (no se usa pero puede servir a futuro)
* manage.py - script for managing application (migrations, server execution, etc.)
* img/ carpeta con las imagenes para este readmme

## Resumen del trabajo hecho

En primera instancia se trabajó sobre el jupyter de de Juan en ./trabajojuan/to-expose.ipynb. Ahi mismo, se agregaron nuevas metricas, se hizo un downsampling a la clase mayoritaria y se buscaron los mejores parametros para el modelo XGBoost. De igual manera se agregaron más variables de entrada para mejorar el perfoarmance. Desde el juputer se exportan los archivos 'XGBoost-model.joblib' con la configuración del mejor modelo y 'column-transformer.joblib' con la configuración del preprocesamiento de variables dummies para trabarlos con unseen data. Al encontrar el mejor modelo hasta ese momento, se creó y testeó el script 'atrasos-vuelos.py' con data no existente. Este script creo la función que ejecuta el modelo para las variables de entrada: prediction(opera,mes,tipovuelo) y sera la funcion template para el endpoint de la API. El detalle del desarollo se encuentre en el notebook.

Posteriormente, se creó la estructura API Rest utilizando la herramienta Flask. Es un framework basado en pythyon para crear APIs. Esta estructura es la que se aprecia en este proyecyo y es la base del modelo entregado. Se decidió utilizar flask dado que el proyecto estaba en python. El script princial es app.py y es el que orquesta el resto del codigo. Se creó el endpoint 'prediction' que recibe los parametros opera, mes, tipovuelo, siglades, dianom. Este endpoint se encuentra en la carpeta 'endponts/atrasovuelo/resource.py' y sigue la estructura de 'atrasos-vuelos.py'. Cabe destacar que el modelo estructurado solo permite hacer un request de un vuelo a la vez.

El proyecto esta disponible en Github y se desarrollaba en la rama develop para probar las funcionalidades para hacer merge con la rama main.

Para las pruebas cloud se decidió utilizar GKE: Google Kubernetes Engine. En primera instancia Google Cloud Platform dado que en mi experiencia en la mejor herramienta cloud, bien documentada y con constantes actualizaciones beneficiosas. Kubernetes Engine dado el hecho que el trabajar con clusters permite una flexibilidad mayor, mejor escabilidad y ademas del hecho que es open source. El hecho de utilizarlo en google tambien permite automatizar ciertos procesos y por lo menos para la creación de este proyecto, da facilidades de deploy rapido.

Se habilitó un proyecto en GPC, se habilitó GKE y se creó



## Estructura 

![Alt text](img/flujo-GKE.png?raw=true "Estructura CLoud")


## Running 

1. Clonar repositorio.
2. pip install requirements.txt
3. Run following commands:
    1. python3 app.py


## Usage

### Users endpoint
POST http://127.0.0.1:5000/api/users

REQUEST
```json
{
	"name": "John John"
}
```
RESPONSE
```json
{
    "id": 1,
    "name": "John John",
    "todos": []
}
```
PUT http://127.0.0.1:5000/api/users/1

REQUEST
```json
{
	"name": "Smith Smith"
}
```
RESPONSE
```json
{
    "id": 1,
    "name": "Smith Smith",
    "todos": []
}
```
DELETE http://127.0.0.1:5000/api/users/1

RESPONSE
```json
{
    "id": 3,
    "name": "Tom Tom",
    "todos": []
}
```
GET http://127.0.0.1:5000/api/users

RESPONSE
```json
{
    "count": 2,
    "users": [
        {
            "id": 1,
            "name": "John John",
            "todos": [
                {
                    "id": 1,
                    "name": "First task",
                    "description": "First task description"
                },
                {
                    "id": 2,
                    "name": "Second task",
                    "description": "Second task description"
                }
            ]
        },
        {
            "id": 2,
            "name": "Smith Smith",
            "todos": []
        }
    ]
}
```
GET http://127.0.0.1:5000/api/users/2
```json
{
    "id": 2,
    "name": "Smith Smith",
    "todos": []
}
```
GET http://127.0.0.1:5000/api/users?name=John John
```json
{
    "count": 1,
    "users": [
        {
            "id": 1,
            "name": "John John",
            "todos": [
                {
                    "id": 1,
                    "name": "First task",
                    "description": "First task description"
                },
                {
                    "id": 2,
                    "name": "Second task",
                    "description": "Second task description"
                }
            ]
        }
    ]
}
```
GET http://127.0.0.1:5000/api/users?limit=1&offset=1
```json
{
    "count": 1,
    "users": [
        {
            "id": 2,
            "name": "Smith Smith",
            "todos": []
        }
    ]
}
```

Todo endpoint is similar to Users endpoint.