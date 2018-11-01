FROM sgoblin/python3.5
#davidjfelix/python3.5
MAINTAINER Sandro Melo
LABEL vendor=weather:dev \
      com.example.is-beta= \
      com.example.is-production="" \
      com.example.version="0.0.1-beta" \
      com.example.release-date="2018-10-30"
WORKDIR /bin
COPY getweather.py /bin
RUN chmod +x /bin/getweather.py
RUN pip3 install --upgrade pip 
RUN pip3 install pyowm 
