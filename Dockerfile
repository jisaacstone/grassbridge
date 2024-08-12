FROM ubuntu:22.04

LABEL maintainer="isaac@jisaacstone.com"
LABEL version="0.1"
LABEL description="Grass API Interface Test"

ARG DEBIAN_FRONTEND=noninteractive

# apt dependancies
RUN apt update
RUN apt-get -y install software-properties-common wget unzip sqlite3
RUN add-apt-repository ppa:ubuntugis/ppa
RUN apt-get -y install grass
RUN apt clean

# setup grass env
RUN grass --config python_path > /usr/local/lib/python3.10/dist-packages/grass.pth
ENV GISBASE=/usr/lib/grass83
ENV GRASS_GUI=text
ENV PATH="$PATH:$GISBASE/bin:$GISBASE/scripts"
ENV LD_LIBRARY_PATH="$GISBASE/lib"

# download data
RUN mkdir datasets
RUN wget https://www.fhwa.dot.gov/bridge/nbi/2022/delimited/PA22.txt -O datasets/PA22.csv
# RUN wget https://www2.census.gov/geo/tiger/TIGER2022/COUNTY/tl_2022_us_county.zip
RUN wget https://www2.census.gov/geo/tiger/TIGER2022/STATE/tl_2022_us_state.zip
# RUN wget https://www2.census.gov/geo/tiger/TIGER2023/UAC/tl_2023_us_uac20.zip
RUN cd datasets && unzip ../*.zip && rm ../*.zip && cd -

# clead up data
RUN sqlite3 datasets/bridges.db '.import --csv datasets/PA22.csv bridges'
RUN sqlite3 datasets/bridges.db 'ALTER TABLE bridges ADD COLUMN latitude REAL; ALTER TABLE bridges ADD COLUMN longitude REAL; UPDATE bridges SET latitude = CAST(LAT_016 AS REAL) / 1000000, longitude = -CAST(LONG_017 AS REAL) / 1000000;'

# make grass project

RUN mkdir /grassdata
RUN grass -c epsg:4326 /grassdata/latlng -e
RUN grass -c v.in.csv input=datasets/PA22.csv output=PA22

