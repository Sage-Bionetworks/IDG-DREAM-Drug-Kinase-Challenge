library(plyr)
library(doMC)
library(reticulate)
library(challengescoring)
library(argparse)
library(magrittr)
library(rjson)
library(tibble)
library(purrr)



parser = ArgumentParser(description = "Create directory with input files")

parser$add_argument(
    "-c",
    "--current_sub",
    type = "character",
    required = TRUE,
    help = "current submission file")

parser$add_argument(
    "-p",
    "--previous_sub",
    type = "character",
    help = "previous submission file")

parser$add_argument(
    "-g",
    "--gold_standard",
    type = "character",
    required = TRUE,
    help = "gold_standard file")

parser$add_argument(
    "-s",
    "--status",
    required = TRUE,
    type = "character",
    help = "current submission status")

parser$add_argument(
    "-v",
    "--verbose",
    action = 'store_false')

args <- parser$parse_args()

if(args$status != "VALIDATED"){
    result_json <- 
        list("prediction_file_status" = args$status) %>% 
        rjson::toJSON()
    
} else {
    
    n_cores <- parallel::detectCores()
    if(args$verbose){
        print(stringr::str_c("Number of cores: ", as.character(n_cores)))  
    } 
    
    if(is.na(n_cores) || n_cores <= 2){
        do_parallel <- F
    } else {
        do_parallel <- T
        doMC::registerDoMC(cores = n_cores -1)
    }
    
    
    
    reticulate::use_python("~/../usr/bin/python2.7")
    
    reticulate::source_python('evaluation_metrics_python2.py')
    
    spearman_py <- function(gold, pred){
        gold_py <- gold %>% np_array()
        pred_py <- pred %>% np_array()
        spearman(gold_py, pred_py)
    }
    
    pearson_py <- function(gold, pred){
        gold_py <- gold %>% np_array()
        pred_py <- pred %>% np_array()
        pearson(gold_py, pred_py)
    }
    
    rmse_py <- function(gold, pred){
        gold_py <- gold %>% np_array()
        pred_py <- pred %>% np_array()
        rmse(gold_py, pred_py)
    }
    
    auc_py <- function(gold, pred){
        gold_py <- gold %>% as.data.frame() %>% r_to_py()
        pred_py <- pred %>% as.data.frame() %>% r_to_py()
        average_AUC(gold_py, pred_py)
    }
    
    ci_py <- function(gold, pred){
        gold_py <- gold %>% np_array()
        pred_py <- pred %>% np_array()
        ci(gold_py, pred_py)
    }
    
    f1_py <- function(gold, pred){
        gold_py <- gold %>% as.data.frame() %>% r_to_py()
        pred_py <- pred %>% as.data.frame() %>% r_to_py()
        f1(gold_py, pred_py)
    }
    
    param_df <- 
        tibble::tibble(
            scoreFun = list(auc_py, spearman_py, pearson_py, ci_py, f1_py, rmse_py),
            largerIsBetter = c(rep(T, 5), F),
            predictions = args$current_sub,
            predictionColname = 'pKd_.M._pred',
            goldStandard = args$gold_standard,
            goldStandardColname = 'pKd_.M.',
            doParallel = do_parallel
        ) 
    
    if (!is.null(args$previous_sub)){
        param_df$prevPredictions <- args$previous_sub
    }
    
    
    output <- param_df %>% 
        purrr::pmap(bootLadderBoot) %>% 
        magrittr::set_names(c("auc", "spearman", "pearson", "ci", "f1", "rmse"))
    
    output_scores <- purrr::map(output, "score")
    
    met_cutoff <- output %>% 
        magrittr::extract2("spearman") %>% 
        magrittr::extract2("metBayesCutoff")
    
    if(is.na(met_cutoff)) {
        met_cutoff <- T
    }
    
    result_json <- output_scores %>% 
        magrittr::inset("met_cutoff", value = met_cutoff) %>% 
        magrittr::inset("prediction_file_status", value = "SCORED") %>% 
        rjson::toJSON()
}

write(result_json, "results.json")


