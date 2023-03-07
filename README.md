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
│   └──flujo-GKE.png
├── deployment.yaml
├── service.yaml
├── requirements.txt
├── Dockerfile
├── LICENSE
└── settings.py
```

Los archivos más importante son:
* `trabajojuan/to-expose.ipynb` - se toma el trabajo de juan, se intenta mejorar el modelo y luego se exportan las configuraciones del mejor modelo.
* `endpoints/atrasovuelo/resource.py` - se implementar el mejor modelo en formato adeacuado para la API.
* `app.py` - aplicación flask para inicializar y deployear api en maquina virtual se conecta a `resource.py` en la carpeta de `endpoints`.
* `deployment.yaml` - configuración para el deploy en docker en GCP.
* `service.yaml` - configuración para el service de docker en GCP.
* `Dockerfile` - script para la ejecución de Docker
* `img/` carpeta con las imagenes para este readmme

## Descripción del trabajo hecho 

En primera instancia se trabajó sobre el jupyter de de Juan en `./trabajojuan/to-expose.ipynb`. Ahi mismo, se agregaron nuevas metricas, se hizo un downsampling a la clase mayoritaria y se buscaron los mejores parametros para el modelo XGBoost. De igual manera se agregaron más variables de entrada para mejorar el perfoarmance. Desde el juputer se exportan los archivos 'XGBoost-model.joblib' con la configuración del mejor modelo y 'column-transformer.joblib' con la configuración del preprocesamiento de variables dummies para trabarlos con unseen data (data nueva o con la que no fue entrenado ni testeado). 

```python
joblib.dump(modelxgb_GridCV_balanced, 'XGBoost-model.joblib')
joblib.dump(column_transformer, 'column-transformer.joblib') 
```

Al encontrar el mejor modelo hasta ese momento, se creó y testeó el script `atrasos-vuelos.py` con data no existente . Este script creo la función que ejecuta el modelo para las variables de entrada: `prediction(opera,mes,tipovuelo)` y sera la funcion template para el endpoint de la API. El detalle del desarollo se encuentre en el notebook.

Posteriormente, se creó la estructura API Rest utilizando la herramienta Flask. Es un framework basado en pythyon para crear APIs. Esta estructura es la que se aprecia en este proyecyo y es la base del modelo entregado. Se decidió utilizar flask dado que el proyecto estaba en python. El script princial es `app.py` y es el que orquesta el resto del codigo. Se creó el endpoint `prediction`:

```python
@app.route('/prediction', methods = ['GET'])
def disp():
    mes=request.args.get('MES')
    opera=request.args.get('OPERA')
    tipo_vuelo=request.args.get('TIPOVUELO')
    response=str(prediction(opera, mes, tipo_vuelo))
 
    return  jsonify({'response': response})

```


 que recibe los parametros opera, mes, tipovuelo. Este endpoint se encuentra en la carpeta `endponts/atrasovuelo/resource.py` y sigue la estructura de `atrasos-vuelos.py`  testeada anteriormente. Cabe destacar que el modelo estructurado solo permite hacer un request de un vuelo a la vez. Se simplifico para las pruebas correspondientes

Para las pruebas cloud se decidió utilizar **GKE: Google Kubernetes Engine**. En primera instancia se escogió Google Cloud Platform dado que en mi experiencia es la mejor herramienta cloud, bien documentada y con constantes actualizaciones beneficiosas. En segundo lugar, **Kubernetes Engine** dado el hecho que el trabajar con clusters permite una flexibilidad mayor, mejor escabilidad y ademas del hecho que es open source. El hecho de utilizarlo en google tambien permite automatizar ciertos procesos y por lo menos para la creación de este proyecto, da facilidades de deploy rapido.

Se habilitó un proyecto en GPC, se habilitó GKE, a través de Cloud Console se conectó con este repositorio git. Se creó la maquina y se pudo efectuar las respectivas pruebas utilizando el repositorio [HTTP benchmarking tool](https://github.com/wg/wrk) que se recomendó en enunciado. La maquina se habilitó solamente para las pruebas dada que al estar mucho tiempo prendida poddría empezar a cobrar en GCP.





## Estructura Cloud

![Alt text](img/flujo-GKE.png?raw=true "Estructura CLoud")


## Testing

Las caracteristicas basicas del cluster son:

| Modo    | CPU totales | Memotia Total | Ubicacion |
| ------- | ----------  |  -----------  |  ---------|
| Autopilot |    0.5    |      2 gb     | us-central1|

Los resultados son mostrados a continuacion:

```
 Running 45s test @ http://34.30.84.111/prediction?MES=1&OPERA=Iberia&TIPOVUELO=I
60 threads and 550 connections
```

| Thread Stats  | Avg         |   Stdev       |   Max    | +/- Stdev |
| -------       | ----------  |  -----------  |  ---------| ---------|
|Latency       | 669.61ms    | 176.63ms      |    2.00s   |  85.59%|
|    Req/Sec |   12.26       |       9.25    |   90.00   |  80.09%|


```
23357 requests in 45.11s, 3.68MB read
Socket errors: connect 0, read 130, write 0, timeout 458
Requests/sec:    517.83
Transfer/sec:     83.44KB
```

en definitiva no se logró llegar  a los 50 000 requests en los 45 segundos y esto puede estar dado por la configuración del cluster. Iterando con la cantidad de ejecuciones paralelas en threads y las conexiones en espera la maquina no da para ese numero. Aumentando las mismas catacteristicas en gcp se podria llegar a explotar más la capacidad.

## Running 

1. Clonar repositorio.
2. pip install requirements.txt
3. Run following commands:
    1. python3 app.py


## Usage

### Users endpoint

Para trabajar desde el local, se tiene:

GET http://127.0.0.1:5000/prediction

REQUEST
```json
{
	"MES": 1,
    "OPERA": "Iberia",
    "TIPOVUELO": "I"

}
```
RESPONSE
```json
{
    "response":0
}
```

La respuesta es 0 si es que el algoritmo predice que no se va a atrasar y 1 si es que predice que se va a atrasar