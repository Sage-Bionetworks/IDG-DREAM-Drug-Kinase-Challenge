FROM tailordev/pandas

RUN pip3 install --upgrade pip
RUN pip3 install argparse pandas numpy scipy sklearn

COPY bin/*.py /usr/local/bin/
RUN chmod a+x /usr/local/bin/*
