FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copia todos los archivos
COPY . . 

# si no encuentra la base de datos, crea una base de datos de ejemplo
RUN if [ ! -f /db/table.db ]; then python ./scripts/init_db.py; fi

CMD [ "python", "./your-daemon-or-script.py" ]
