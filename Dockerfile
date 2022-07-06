FROM python:3.6.7


WORKDIR /app
#Optional

# install FreeTDS and dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install dialog apt-utils -y \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install freetds-dev -y \
 && apt-get install freetds-bin -y \
 && apt-get install tdsodbc -y \
 && apt-get install --reinstall build-essential -y
# populate "ocbcinst.ini" as this is where ODBC driver config sits
RUN echo "[FreeTDS]\n\
Description = FreeTDS Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

RUN apt-get install tdsodbc -y
# By copying over requirements first, we make sure that Docker will cache
# our installed requirements rather than reinstall them on every build
COPY requirements.txt /app/requirements.txt
COPY odbcinst.ini /app/odbcinst.ini
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
RUN odbcinst -i -d -f /app/odbcinst.ini
# Now copy in our code, and run it
COPY . /app/
EXPOSE 80
#ENTRYPOINT ["tail", "-f", "/dev/null"]
#ENTRYPOINT python /app/manage.py runserver 0.0.0.0:80