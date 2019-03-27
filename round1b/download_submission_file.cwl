#!/usr/bin/env cwl-runner
#
# Download a submitted file from Synapse and return the downloaded file
#
cwlVersion: v1.0
class: CommandLineTool
baseCommand: python

inputs:
  - id: submissionid
    type: int
  - id: synapse_config
    type: File

arguments:
  - valueFrom: download_submission_file.py
  - valueFrom: $(inputs.submissionid)
    prefix: -s
  - valueFrom: results.json
    prefix: -r
  - valueFrom: $(inputs.synapse_config.path)
    prefix: -c

requirements:
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - entryname: download_submission_file.py
        entry: |
          #!/usr/bin/env python
          import synapseclient
          import argparse
          import json
          import os
          parser = argparse.ArgumentParser()
          parser.add_argument("-s", "--submissionid", required=True, help="Submission ID")
          parser.add_argument("-r", "--results",required=True, help="download results info")
          parser.add_argument("-c", "--synapse_config", required=True, help="credentials file")
          args = parser.parse_args()
          syn = synapseclient.Synapse(configPath=args.synapse_config)
          syn.login()
          sub = syn.getSubmission(args.submissionid, downloadLocation=".")
          if sub.entity.concreteType!='org.sagebionetworks.repo.model.FileEntity':
            raise Exception('Expected FileEntity type but found '+sub.entity.entityType)
          os.rename(sub.filePath, "submission-"+args.submissionid)
          result = {'entityId':sub.entity.id,'entityVersion':sub.entity.versionNumber}
          with open(args.results, 'w') as o:
            o.write(json.dumps(result))
     
outputs:
  - id: filepath
    type: File
    outputBinding:
      glob: $("submission-"+inputs.submissionid)
  - id: entity
    type:
      type: record
      fields:
      - name: id
        type: string
        outputBinding:
          glob: results.json
          loadContents: true
          outputEval: $(JSON.parse(self[0].contents)['entityId'])
      - name: version
        type: int
        outputBinding:
          glob: results.json
          loadContents: true
          outputEval: $(JSON.parse(self[0].contents)['entityVersion'])

