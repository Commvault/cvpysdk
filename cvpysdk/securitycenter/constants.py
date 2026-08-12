FQ_PARAMETERS = {"THREAT_DETECTION" :"fq=groups.clientGroup.clientGroupName%3Aneq%3AIndex+Servers&fq=groups.configurationGroupType%3Aeq%3A1"}
FL_PARAMETERS = {"THREAT_DETECTION" : "&fl=groups.clientGroup,groups.discoverRulesInfo,groups.groupAssocType,groups.Id,groups.name,groups.isCompanySmartClientGroup,groups.description,groups.clientCount,groups.tiPlan&hardRefresh=true"}

UPDATE_TI_PLAN_JSON ={
          "clientGroupOperationType": "Update",
          "clientGroupDetail": {
            "configurationGroupType": 1,
            "tiPlan": {
              "planName": "",
              "planId": 0
            }
          }
        }

RESOURCE_GROUP_PAYLOAD_MANUAL = {
                "name": "",
                "serverGroupType": "MANUAL",
                "manualAssociation": {
                "associatedservers": [

                ]
              }
            }

RESOURCE_GROUP_PAYLOAD_MANUAL_UPDATE = {
    "serverGroup":{"id":0,"name":""},
    "serverGroupType":"MANUAL",
    "manualAssociation":{
        "associatedservers":[
            ]
            }
            }

RESOURCE_GROUP_PAYLOAD_AUTOMATIC = {
    "name": "",
    "serverGroupType": "AUTOMATIC",
    "automaticAssociation": {
        "clientScope": {
            "clientScopeType": "COMMCELL"
        },
        "serverGroupRule": {}
    }
}