# Ejemplo de Hadoop en Google Cloud Platform
En este ejemplo, ejecutaremos un job de mapreduce utilizando un cluster de GCP.

## Datos
Para el ejemplo de wordcount:
https://drive.google.com/drive/folders/1RYLe6IyOUGKgwX6fUyZxVechr9KdlQWL?usp=sharing

Para el ejemplo de NYC bike rides:

https://drive.google.com/drive/folders/1R6se32EtNNdOMSHD8sW-enuk2ff7l48W?usp=sharing 

## 1. Crear un bucket (Data storage) 
Esto nos sirve para leer los datos que van a a ser procesados y escribir los resultados del job mapreduce. Sin este bucket, al momento de borrar el cluster perdemos todos los datos.

Los datos han sido cargados a un GCS bucket con la siguiente estructura:

Archivos de lectura 
`input/wordcount/`

`input/rides/`


Scripts de python mapper y reducer

`wordcount/`

`NYCbikerides/`

También definimos una carpeta donde se alojarán el resultado
`output/`

<img width="1275" alt="Screen Shot 2021-11-08 at 13 21 24" src="https://user-images.githubusercontent.com/7211600/140800004-6e18c2a0-debb-4a5b-9bf5-cdbed6733b6a.png">

Tomar en cuenta que en este ejemplo, como usamos DataProc de GCP no necesitamos HDFS puesto que esto ya usa HDFS

https://cloud.google.com/dataproc/docs/concepts/dataproc-hdfs

## 2. Crear cluster en CCP
Vamos a crear un cluster con 1 master node y 4 worker nodes (standard n2)
<img width="1275" alt="Screen Shot 2021-11-08 at 08 06 19" src="https://user-images.githubusercontent.com/7211600/140800086-3d182505-c868-4a6c-9dc4-82b8b5c77ebb.png">
<img width="1275" alt="Screen Shot 2021-11-08 at 08 07 04" src="https://user-images.githubusercontent.com/7211600/140800103-670b9257-d057-4846-9dc1-02226b9271a8.png">
<img width="1275" alt="Screen Shot 2021-11-08 at 08 07 12" src="https://user-images.githubusercontent.com/7211600/140800116-aa837baa-b6b8-4c20-93d0-c2fe5f409352.png">
<img width="1275" alt="Screen Shot 2021-11-08 at 08 07 19" src="https://user-images.githubusercontent.com/7211600/140800128-6df90544-a9ba-488e-837a-04193810c5fd.png">
<img width="1275" alt="Screen Shot 2021-11-08 at 08 07 45" src="https://user-images.githubusercontent.com/7211600/140800151-5a7a58e9-451c-4128-a14c-d111d9701064.png">
<img width="1275" alt="Screen Shot 2021-11-08 at 08 07 49" src="https://user-images.githubusercontent.com/7211600/140800172-0dd60de8-c15c-43ca-b28e-4d043e4fbb9f.png">
<img width="1275" alt="Screen Shot 2021-11-08 at 08 18 37" src="https://user-images.githubusercontent.com/7211600/140800237-5ecd772b-1991-4998-9bb8-569867e31193.png">

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

`./google-cloud-sdk/bin/gcloud  compute ssh hadoop-example-m \
  --project=warm-dynamics-331320 \
  --zone=us-central1-f -- -D 1080 -N`

  - Abrir otra pestaña en la consola para ejecutar Chrome con un proxy apuntando al node master y al puerto abierto. El puerto 8088 es para ver los procesos de Hadoop.

`"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "http://hadoop-example-m:8088"\
	--proxy-server="socks5://localhost:1080" \
	--user-data-dir=/tmp/hadoop-example-m`

<img width="1275" alt="Screen Shot 2021-11-08 at 08 18 12" src="https://user-images.githubusercontent.com/7211600/140800205-1c3bf4aa-05f1-4681-9061-fec008b75b0a.png">

## 3. Ejecutar el proceso de hadoop map-reduce en el master node.
### 3.1 Contar palabras en un archivo de texto.
Ejecutar en la consola del master node:

`hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
	-files gs://us-central1-hadoop-demo-58952bde-bucket/wordcount/mapper.py,gs://us-central1-hadoop-demo-58952bde-bucket/wordcount/reducer.py \
	-mapper mapper.py \
	-reducer reducer.py \
	-input gs://us-central1-hadoop-demo-58952bde-bucket/input/wordcount/rose.txt \
	-output gs://us-central1-hadoop-demo-58952bde-bucket/output/wordcount`

Si refrescamos el browser, veremos la aplicación que se está ejecutando:
<img width="1275" alt="Screen Shot 2021-11-08 at 08 21 25" src="https://user-images.githubusercontent.com/7211600/140800306-c03c85d8-5e64-4d50-879d-b4a0218ad405.png">

Si le damos click a la aplicación ejecutándose, veremos los nodos y sus tareas ejecutándose.
<img width="1275" alt="Screen Shot 2021-11-08 at 08 21 52" src="https://user-images.githubusercontent.com/7211600/140800510-cc6b4838-7720-4886-8e61-04c98edf9583.png">

Consultar los resultados del job:

`hdfs dfs -cat gs://us-central1-hadoop-demo-58952bde-bucket/output/wordcount/part* | sort -n -k 2 -r `

### 3.2 Contar palabras de varios archivos de texto.
Ejecutar en la consola del master node:

`hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
	-files gs://us-central1-hadoop-demo-58952bde-bucket/wordcount/mapper.py,gs://us-central1-hadoop-demo-58952bde-bucket/wordcount/reducer.py \
	-mapper mapper.py \
	-reducer reducer.py \
	-input gs://us-central1-hadoop-demo-58952bde-bucket/input/wordcount/*.txt \
	-output gs://us-central1-hadoop-demo-58952bde-bucket/output/wordcount2`
  
Consultar los resultados:

`hdfs dfs -cat gs://us-central1-hadoop-demo-58952bde-bucket/output/wordcount2/part* | sort -n -k 2 -r `

### 3.3 Listar las estaciones de bicicletas de la ciudad de New York y su concurrencia.
Ejecutar en la consola del master node:

`hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
	-files gs://us-central1-hadoop-demo-58952bde-bucket/NYCbikerides/mapper.py,gs://us-central1-hadoop-demo-58952bde-bucket/NYCbikerides/reducer.py \
	-mapper mapper.py \
	-reducer reducer.py \
	-input gs://us-central1-hadoop-demo-58952bde-bucket/input/rides/* \
	-output gs://us-central1-hadoop-demo-58952bde-bucket/output/NYCbikerides`

Consultar los resultados:

`hdfs dfs -cat gs://us-central1-hadoop-demo-58952bde-bucket/output/NYCbikerides/part* | sort -t$'\t' -k 2 -n -r `

### 3.4 Listar las 10 estaciones más concurridas.
Ejecutar en la consola del master node:

`hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
	-files gs://us-central1-hadoop-demo-58952bde-bucket/NYCbikerides/mapper.py,gs://us-central1-hadoop-demo-58952bde-bucket/NYCbikerides/reducer2.py \
	-mapper mapper.py \
	-reducer reducer2.py \
	-input gs://us-central1-hadoop-demo-58952bde-bucket/input/rides/* \
	-output gs://us-central1-hadoop-demo-58952bde-bucket/output/NYCbikerides_top10`

Consultar los resultados:

`hdfs dfs -cat gs://us-central1-hadoop-demo-58952bde-bucket/output/NYCbikerides_top10/part* | sort -t$'\t' -k 2 -n -r | head -n10`



	
