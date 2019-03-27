#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: 
- python3
- /usr/local/bin/validate.py

requirements:
- class: InlineJavascriptRequirement

hints:
  DockerRequirement:
    dockerPull: quay.io/andrewelamb/drug_target_validate_2
    
inputs:

- id: inputfile
  type: File?
  inputBinding:
    prefix: --submission_file
  
- id: goldstandard_file
  type: File
  inputBinding:
    prefix: --goldstandard_file

- id: entity_type
  type: string
  inputBinding:
    prefix: --entity_type

outputs:

- id: results
  type: File
  outputBinding:
    glob: "results.json"
      
- id: status
  type: string
  outputBinding:
    glob: "results.json"
    loadContents: true
    outputEval: $(JSON.parse(self[0].contents)['prediction_file_status'])

- id: invalid_reasons
  type: string
  outputBinding:
    glob: "results.json"
    loadContents: true
    outputEval: $(JSON.parse(self[0].contents)['prediction_file_errors'])
