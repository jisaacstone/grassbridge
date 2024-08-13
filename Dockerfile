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
RUN wget https://www2.census.gov/geo/tiger/TIGER2022/COUNTY/tl_2022_us_county.zip
# RUN wget https://www2.census.gov/geo/tiger/TIGER2022/STATE/tl_2022_us_state.zip
RUN wget https://www2.census.gov/geo/tiger/TIGER2022/UAC/tl_2022_us_uac20.zip
RUN cd datasets && unzip ../tl_2022_us_county.zip
RUN cd datasets && unzip ../tl_2022_us_uac20.zip

# clean up data bridge data (decimal lat/lng)
ADD clean_bridge_data.sql /
RUN sqlite3 -init clean_bridge_data.sql datasets/bridges.db .quit

# make grass project
RUN mkdir /grassdata
RUN grass -c epsg:4269 /grassdata/latlng -e
ADD import_data.py /
RUN python3 import_data.py

# server setup
ADD https://bootstrap.pypa.io/get-pip.py /
RUN python3 get-pip.py
ADD setup.cfg pyproject.toml /
ADD grassbridge grassbridge
RUN pip3 install --ignore-installed -e .
EXPOSE 5000

CMD flask --app grassbridge.app run --host 0.0.0.0 --port 5000 --debug
