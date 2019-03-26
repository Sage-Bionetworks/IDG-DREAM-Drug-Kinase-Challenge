FROM rocker/tidyverse:3.5.0

RUN mkdir home/dream

COPY demo_predict.R home/dream/demo_predict.R
COPY round_2_template.csv home/dream/template.csv

CMD ["R", "home/dream/demo_predict.R", "template.csv"]