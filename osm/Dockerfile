FROM postgis/postgis:12-2.5

WORKDIR /data

RUN apt update -y \
    && apt install wget -y \
    && apt install make cmake g++ libboost-dev libboost-system-dev \
        libboost-filesystem-dev libexpat1-dev zlib1g-dev \
        libbz2-dev libpq-dev libproj-dev lua5.2 liblua5.2-dev -y \
    && apt install osm2pgsql -y

RUN wget https://download.openstreetmap.fr/extracts/russia/central_federal_district/moscow.osm.pbf

COPY ./osm/1000-build.sh /docker-entrypoint-initdb.d/

RUN chmod a+x /docker-entrypoint-initdb.d/1000-build.sh