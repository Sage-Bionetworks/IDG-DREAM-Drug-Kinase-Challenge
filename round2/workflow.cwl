#!/usr/bin/env cwl-runner
#
# Sample workflow
# Inputs:
#   submissionId: ID of the Synapse submission to process
#   adminUploadSynId: ID of a folder accessible only to the submission queue administrator
#   submitterUploadSynId: ID of a folder accessible to the submitter
#   workflowSynapseId:  ID of the Synapse entity containing a reference to the workflow file(s)
#   synapseConfig: ~/.synapseConfig file that has your Synapse credentials
#
cwlVersion: v1.0
class: Workflow

requirements:
- class: StepInputExpressionRequirement
- class: InlineJavascriptRequirement

inputs:
  - id: submissionId
    type: int
  - id: adminUploadSynId
    type: string
  - id: submitterUploadSynId
    type: string
  - id: workflowSynapseId
    type: string
  - id: synapseConfig
    type: File

# there are no output at the workflow engine level.  Everything is uploaded to Synapse
outputs: []

steps:
  download_submission:
    run: https://raw.githubusercontent.com/Sage-Bionetworks/ChallengeWorkflowTemplates/v1.3/download_submission_file.cwl
    in:
      - id: submissionid
        source: "#submissionId"
      - id: synapse_config
        source: "#synapseConfig"
    out:
      - id: filepath
      - id: entity
      - id: entity_type 

  download_goldstandard:
    run: https://raw.githubusercontent.com/Sage-Bionetworks/ChallengeWorkflowTemplates/v1.3/download_from_synapse.cwl
    in:
      - id: synapseid
        valueFrom: "syn18421225"
      - id: synapse_config
        source: "#synapseConfig"
    out:
      - id: filepath
      
  validation:
    run: validate.cwl
    in:
      - id: inputfile
        source: "#download_submission/filepath"
      - id: goldstandard_file
        source: "#download_goldstandard/filepath"
      - id: entity_type
        source: "#download_submission/entity_type"
    out:
      - id: results
      - id: status
      - id: invalid_reasons
  
  validation_email:
    run: https://raw.githubusercontent.com/Sage-Bionetworks/ChallengeWorkflowTemplates/v1.3/validate_email.cwl
    in:
      - id: submissionid
        source: "#submissionId"
      - id: synapse_config
        source: "#synapseConfig"
      - id: status
        source: "#validation/status"
      - id: invalid_reasons
        source: "#validation/invalid_reasons"

    out: []



  annotate_validation_with_output:
    run: https://raw.githubusercontent.com/Sage-Bionetworks/ChallengeWorkflowTemplates/v1.3/annotate_submission.cwl
    in:
      - id: submissionid
        source: "#submissionId"
      - id: annotation_values
        source: "#validation/results"
      - id: to_public
        valueFrom: "true"
      - id: force_change_annotation_acl
        valueFrom: "true"
      - id: synapse_config
        source: "#synapseConfig"
    out: []

  scoring:
    run: score.cwl
    in:
      - id: inputfile
        source: "#download_submission/filepath"
      - id: status 
        source: "#validation/status"
      - id: goldstandard_file
        source: "#download_goldstandard/filepath"
    out:
      - id: results
      
  score_email:
    run: https://raw.githubusercontent.com/Sage-Bionetworks/ChallengeWorkflowTemplates/v1.3/score_email.cwl
    in:
      - id: submissionid
        source: "#submissionId"
      - id: synapse_config
        source: "#synapseConfig"
      - id: results
        source: "#scoring/results"
      - id: private_annotations
        valueFrom: $(["average_auc", "spearman", "rmse"])
    out: []

  annotate_submission_with_output:
    run: https://raw.githubusercontent.com/Sage-Bionetworks/ChallengeWorkflowTemplates/v1.3/annotate_submission.cwl
    in:
      - id: submissionid
        source: "#submissionId"
      - id: annotation_values
        source: "#scoring/results"
      - id: to_public
        valueFrom: "true"
      - id: force_change_annotation_acl
        valueFrom: "true"
      - id: synapse_config
        source: "#synapseConfig"
    out: []
 

