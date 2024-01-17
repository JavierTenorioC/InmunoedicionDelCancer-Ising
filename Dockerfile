# Usa la imagen base oficial de Python
FROM python:3.8

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala Vim
RUN apt-get update && \
    apt-get install -y vim && \
    rm -rf /var/lib/apt/lists/*

# Copia el archivo de requerimientos (si es necesario)
COPY requirements.txt requirements.txt

# Instala las dependencias del programa
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia el código actual al contenedor en /app
COPY . .

# Especifica el comando a ejecutar al iniciar el contenedor
CMD ["bash"]


