#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: 
- python3
- /usr/local/bin/score.py

requirements:
- class: InlineJavascriptRequirement

hints:
  DockerRequirement:
    dockerPull: quay.io/andrewelamb/drug_target_score_2

inputs:

- id: inputfile
  type: File
  inputBinding:
    prefix: --submission_file
  
- id: goldstandard_file
  type: File
  inputBinding:
    prefix: --goldstandard_file

- id: status
  type: string
  inputBinding:
    prefix: --status

outputs:

  - id: results
    type: File
    outputBinding:
      glob: "results.json"
