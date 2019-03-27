#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [Rscript, /usr/local/bin/score.R]

hints:
  DockerRequirement:
    dockerPull: quay.io/andrewelamb/drug_target_score_1b
    
requirements:
  - class: InlineJavascriptRequirement

inputs:

  current_submission_file:
    type: File
    inputBinding:
      prefix: --current_sub
  
  goldstandard:
    type: File
    inputBinding:
      prefix: --gold_standard
 
  previous_submission_file:
    type: File?
    inputBinding:
      prefix: --previous_sub

  status:
    type: string
    inputBinding:
      prefix: --status

  n_bootstraps:
    type: int?
    inputBinding:
      prefix: --n_bootstraps

outputs:

  - id: results
    type: File
    outputBinding:
      glob: "results.json"
