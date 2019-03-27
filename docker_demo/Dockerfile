FROM rocker/r-ver

RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > ~/.Rprofile
RUN Rscript -e "install.packages('readr')"

RUN mkdir test
RUN mkdir io

COPY demo_prediction.R /test/demo_prediction.R
COPY round_2_template.csv /io/template.csv

CMD Rscript /test/demo_prediction.R

