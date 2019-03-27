#!/usr/bin/env cwl-runner
#
# Authors: Andrew Lamb

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [python3, /usr/local/bin/download_current_lead_submission.py]

hints:
  DockerRequirement:
    dockerPull: quay.io/andrewelamb/python_challenge_utils

inputs:

  - id: submissionid
    type: int
    inputBinding:
      prefix: -i
      
  - id: synapse_config
    type: File
    inputBinding:
      prefix: -c

  - id: queue
    type: string
    inputBinding:
      prefix: -q
    
  - id: status
    type: string
    inputBinding:
      prefix: -s

  - id: cutoff_annotation
    type: string?
    inputBinding:
      prefix: -a
   
outputs:

  - id: output
    type: File?
    outputBinding:
      glob: "previous_submission.csv"
