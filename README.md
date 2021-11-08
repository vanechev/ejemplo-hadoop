# Ejemplo de Hadoop en Google Cloud Platform
En este ejemplo, ejecutaremos un job de mapreduce utilizando un cluster de GCP.

## 1. Crear un bucket (Data storage) 
Esto nos sirve para leer los datos que van a a ser procesados y escribir los resultados del job mapreduce. Sin este bucket, al momento de borrar el cluster perdemos todos los datos.

Los datos han sido cargados a un GCS bucket con la siguiente estructura:

Archivos de lectura CSV
`- input/NYCbikerides/`

Scripts de python mapper y reducer
`- NYCbikerides/`

También definimos una carpeta donde se alojarán el resultado
`- output/`

Tomar en cuenta que en este ejemplo, como usamos DataProc de GCP no necesitamos HDFS puesto que esto ya usa HDFS
https://cloud.google.com/dataproc/docs/concepts/dataproc-hdfs

## 2. Crear cluster en CCP
Vamos a crear un cluster con 1 master node y 4 worker nodes (standard n2)

Para visualizar nuestro cluster, nodos, job y demás procesos:
- Instalar gcloud (Cloud SDK) https://cloud.google.com/sdk/docs/install

- Crear tunel ssh que nos permita conectar remotamente (1080 es el puerto que vamos a abrir). 
Para esto:
  - Click en el cluster creado.
  - Click en web interfaces.
  - Click en create SSH tunnel. 
  - Copiar el código
  - Abrir consola de su computadora personal
  - Ejecutar el siguiente codigo en la ruta donde se encuentra el Cloud SDK

`- ./google-cloud-sdk/bin/gcloud  compute ssh hadoop-example-m \
  --project=warm-dynamics-331320 \
  --zone=us-central1-f -- -D 1080 -N`

  - Abrir otra pestaña en la consola para ejecutar Chrome con un proxy apuntando al node master y al puerto abierto. El puerto 8088 es para ver los procesos de Hadoop.

`- "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "http://hadoop-example-m:8088"\
	--proxy-server="socks5://localhost:1080" \
	--user-data-dir=/tmp/hadoop-example-m`

## 3. Ejecutar el proceso de hadoop map-reduce en el master node.
### 3.1 Contar palabras en un archivo de texto.
Ejecutar en la consola del master node:

`- hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
	-files gs://us-central1-hadoop-demo-58952bde-bucket/wordcount/mapper.py,gs://us-central1-hadoop-demo-58952bde-bucket/wordcount/reducer.py \
	-mapper mapper.py \
	-reducer reducer.py \
	-input gs://us-central1-hadoop-demo-58952bde-bucket/input/rose.txt \
	-output gs://us-central1-hadoop-demo-58952bde-bucket/output/wordcount`
  
Consultar los resultados:

`- hdfs dfs -cat gs://us-central1-hadoop-demo-58952bde-bucket/output/wordcount/part* | sort -n -k 2 -r `

### 3.2 Contar palabras de varios archivos de texto.
Ejecutar en la consola del master node:

`- hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
	-files gs://us-central1-hadoop-demo-58952bde-bucket/wordcount/mapper.py,gs://us-central1-hadoop-demo-58952bde-bucket/wordcount/reducer.py \
	-mapper mapper.py \
	-reducer reducer.py \
	-input gs://us-central1-hadoop-demo-58952bde-bucket/input/*.txt \
	-output gs://us-central1-hadoop-demo-58952bde-bucket/output/wordcount2`
  
Consultar los resultados:

`- hdfs dfs -cat gs://us-central1-hadoop-demo-58952bde-bucket/output/wordcount/part* | sort -n -k 2 -r `

### 3.3 Listar las estaciones de bicicletas de la ciudad de New York y su concurrencia.
Ejecutar en la consola del master node:

`- hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
	-files gs://us-central1-hadoop-demo-58952bde-bucket/NYCbikerides/mapper.py,gs://us-central1-hadoop-demo-58952bde-bucket/NYCbikerides/reducer.py \
	-mapper mapper.py \
	-reducer reducer.py \
	-input gs://us-central1-hadoop-demo-58952bde-bucket/input/rides/* \
	-output gs://us-central1-hadoop-demo-58952bde-bucket/output/NYCbikerides`

Consultar los resultados:

`- hdfs dfs -cat gs://us-central1-hadoop-demo-58952bde-bucket/output/NYCbikerides/part* | sort -t$'\t' -k 2 -n -r `

### 3.4 Listar las 10 estaciones más concurridas.
Ejecutar en la consola del master node:

hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
	-files gs://us-central1-hadoop-demo-58952bde-bucket/NYCbikerides/mapper.py,gs://us-central1-hadoop-demo-58952bde-bucket/NYCbikerides/reducer2.py \
	-mapper mapper.py \
	-reducer reducer2.py \
	-input gs://us-central1-hadoop-demo-58952bde-bucket/input/rides/* \
	-output gs://us-central1-hadoop-demo-58952bde-bucket/output/NYCbikerides_top10

Consultar los resultados:

`- hdfs dfs -cat gs://us-central1-hadoop-demo-58952bde-bucket/output/NYCbikerides_top10/part* | sort -t$'\t' -k 2 -n -r | head -n10 `



	
