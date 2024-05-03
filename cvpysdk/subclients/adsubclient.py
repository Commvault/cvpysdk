# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------
"""
File for Ad agent sublcient replated operation

Class:
    ADSubclient :

        _get_subclient_properties()    --    Method to get subclinet properites

        _get_subclient_properties_json --    Method to generate subclinet properties in json format

        content                        --    Properties of AD objects in subclient

        compare_id                     --    Method returns AD compare id

        trigger_compare_job            --    Method to trigger AD compare job

        checkcompare_result_generated  --    Method to check AD compare report generated

        generate_compare_report        --    Method to generate AD compare report

        restore_job                    --    Method to do AD point in time restore
ADSubclient:
    content() -- method to get AD agent subclient content

Function:
"""

from __future__ import unicode_literals

from ..exception import SDKException
from ..subclient import Subclient
import time

class ADSubclient(Subclient):
    """Class for AD agent related subclient """

    def _get_subclient_properties(self):
        """Gets the subclient  related properties of File System subclient.
        """
        super()._get_subclient_properties()
        if 'impersonateUser' in self._subclient_properties:
            self._impersonateUser = self._subclient_properties['impersonateUser']
        if 'content' in self._subclient_properties:
            self._content = self._subclient_properties['content']

    def _get_subclient_properties_json(self):
        """get the all subclient related properties of this subclient.
           Returns:
                dict - all subclient properties put inside a dict
        """
        subclient_json = {
            "subClientProperties":
                {
                    "impersonateUser": self._impersonateUser,
                    "proxyClient": self._proxyClient,
                    "subClientEntity": self._subClientEntity,
                    "content": self._content,
                    "commonProperties": self._commonProperties,
                    "contentOperationType": 1
                }
        }
        return subclient_json

    @property
    def content(self):
        """ Get AD agent subclient content"""
        contents = []
        if "content" in self._subclient_properties:
            subclient_content = self._subclient_properties['content']
        else:
            subclient_content = []
        if len(subclient_content) > 0:
            for entry in subclient_content:
                if len(entry['path'].split(',')) > 1:
                    contents.append(",".join(entry['path'].split(',')[1:]))
                else:
                    raise SDKException('Subclient', "101",
                                       "subclient content is not valid")
        else:
            raise SDKException('Subclient', '101',
                               "subclient content return empty result")

        return contents

    def cv_contents(self, contents, entrypoint=None):
        """Commvault subclient content convert to AD format
            Args:
                content    (list)    subclient content
                entrypoint    (string)    ad object entry point
            Return:
                (list)    ad format content
            Exception:
                None
        """
        content_ad = []
        for content in contents:
            contententry = ",".join(list(reversed(content.split(","))))
            if entrypoint is not None:
                shortdn = contententry.split(",{0}".format(entrypoint))[0]
            else:
                shortdn = None
            content_ad.append((contententry, shortdn))
        return content_ad

    def compare_id(self,left_set_time,right_set_time,
                   source_item,comparison_name):
        """
        Generate Commvault AD Compare Comparison id
        Args:
             left_set_time  (int)      End Time of the first backup for comparison
             right_set_time (int)      End Time of the second backup for comparison
             source_item    (string)   sourceItem for comparison
             comparison_name(string)   name of the comparison
        Return:
            (int) Comparison ID
        Exception:
                Response was not a success
        """
        client_id=int(self._client_object.client_id)
        subclient_id=int(self.subclient_id)

        payload = {
            "adCompareOptions": {"adCompareType": 0, "comparisonName": comparison_name,
                                 "subClientId": (subclient_id),
                                 "appTypeId": 41, "clientId": (client_id),
                                 "nodeClientId": (client_id),
                                 "leftSetTime": (left_set_time),
                                 "rightSetTime": (right_set_time), "status": 0,
                                 "adComparisonJobType": 0,
                                 "selectedItems": {"sourceItem": [source_item]},
                                 "includeUnchangedItems": False,
                                 "excludeFrequentlyChanged": True}}
        generate_comparison_id = self._services['ADCOMPAREID'] % (subclient_id)

        flag, response = self._cvpysdk_object.make_request(
           method= 'POST',url= generate_comparison_id,payload= payload
        )

        if flag:
            response_dict=response.json()
            comp_id = response_dict['adCompareDetails'][0]['comparisonId']


        else:

            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

        return comp_id

    def trigger_compare_job(self,left_set_time,
                            right_set_time,
                            display_name,client_name,
                            comp_id,source_item,comparison_name):
        """
        Triggers Commvault AD compare job
        Args:
              left_set_time (int) End Time of the first backup for comparison
              right_set_time(int) End Time of the second backup for comparison
              display_name(str) displayName of the client
              client_name(str) name of the client
              comp_id(int) the comparison id for AD compare
              source_item(str)  sourceItem for comparison
              comparison_name(str) name of the comparison
        Return:
            None
        Exception:
                Response was not a success
        """
        client_id = int(self._client_object.client_id)
        backupset_id=int(self._backupset_object._get_backupset_id())

        subclient_id = int(self.subclient_id)

        trigger_compare_job=self._services['CREATE_TASK']
        request_time=int(time.time())
        payload = {"taskInfo": {"associations": [
            {"subclientId": (subclient_id), "displayName":
                display_name, "clientId": (client_id),
             "applicationId": 41, "clientName":
                 client_name, "backupsetId": (backupset_id),
             "_type_": "SUBCLIENT_ENTITY"}],
            "task": {"taskType": 1}, "subTasks": [
            {"subTask": {"subTaskType": 1, "operationType": 4025},
             "options": {"backupOpts": {},
                         "commonOpts": {"notifyUserOnJobCompletion": False},
                         "adComparisonOption": {"adCompareType": 0,
                                                "comparisonName": comparison_name,
                                                "subClientId": (subclient_id),
                                                "appTypeId": 41,
                                                "clientId": (client_id),
                                                "nodeClientId": (client_id),
                                                "leftSetTime": left_set_time,
                                                "rightSetTime": right_set_time,
                                                "status": 0,
                                                "adComparisonJobType": 0,
                                                "selectedItems": {"sourceItem": [source_item]},
                                                "includeUnchangedItems": False,
                                                "excludeFrequentlyChanged": True,
                                                "comparisonId": (comp_id),
                                                "requestTime":request_time ,
                            "selectionHash": "D51A0DDBBFF582EEFA23A750DB90F1A46F6E90CE"}}}]}}


        flag, response = self._cvpysdk_object.make_request(method='POST',
                                                                   url=trigger_compare_job,
                                                                     payload=payload)

        if not flag:
            raise SDKException('Response', '101',
                               self._commcell_object._update_response_(response.text))

    def checkcompare_result_generated(self,comp_id):
        """
        Function to check AD comparison result generated and returns comparison cache path
        Args:
             comp_id(int): comparison id of AD compare operation
        Return:
            (string) comparisonCachePath
        Exception:
                Response was not a success
        """
        compare_result = self._services['ADCOMPARESTATUSCHECK'] % (comp_id)

        while True:

            flag, response = self._cvpysdk_object.make_request(method='GET',
                                                                       url=compare_result)

            if flag:

                response_dict = response.json()
                error_message = response_dict['adCompareDetails'][0]['errorMessage']
                status = response_dict['adCompareDetails'][0]['status']
                comparison_cache_path = response_dict['adCompareDetails'][0]['sqlLiteDBCachePath']

                if (error_message == "" and status == 0 and comparison_cache_path != ""):
                    return comparison_cache_path
                if error_message != "":

                    raise SDKException('Response', '101',
                                       self._commcell_objectj._update_response_(response.text))

                time.sleep(30)
            else:
                raise SDKException('Response', '101',
                                   self._commcell_object._update_response_(response.text))

    def generate_compare_report(self,comp_id,comparison_cache_path,op_type=2):
        """
        Return AD Compare report
            Args:
                comp_id (int) the comparison id generate
                comparison_cache_path (str) local directory where we write the comparison file
            Return:
                (json) AD Compare Report
            Exception:
                    Response was not a success
        """
        client_id = int(self._client_object.client_id)
        subclient_id = int(self.subclient_id)
        ad_comp_url = self._services['ADCOMPAREVIEWRESULTS']
        payload = {"isEnterprise": True, "discoverySentTypes": [24],
                     "subclientDetails": {"subclientId": (subclient_id), "appTypeId": 41,
                                          "clientId": (client_id)},
                     "adComparisonBrowseReq": {"pageNumber": 0, "comparisonId": comp_id,
                                               "opType": op_type, "browseItemId": 0,
                                               "pageSize": 15, "comparisonCachePath":
                                                   comparison_cache_path,
                                               "searches":[{"masks":["2","1","0"],"searchType":2}]}}


        flag, response = self._cvpysdk_object.make_request(method='POST', url=ad_comp_url,
                                                                       payload=payload)

        if not flag:
            raise SDKException('Response', '101',
                               self._commcell_object._update_response_(response.text))

        return response.json()

    def restore_job(self,display_name,client_name,subclient_name,to_time,restore_path):
        """
        Triggers AD restore job and waits for its completion
        Args:
              display_name(str) displayName of the client
              client_name(str) name of the client
              subclient_name(str) name of the subclient
              to_time(int) time from where to restore
              restore_path(str)  restore path
        Return:
             None
        Exception:
             Response was not a success
        """
        client_id = int(self._client_object.client_id)
        subclient_id = int(self.subclient_id)
        backupset_id = int(self._backupset_object._get_backupset_id())
        client_guid=self._client_object.client_guid
        commcell_id=int(self._commcell_object.commcell_id)
        instance_id=int(self._instance_object.instance_id)

        payload={"taskInfo":{"associations":[{"subclientId":subclient_id,
                                              "displayName":display_name,
                                              "clientId":client_id,
                                              "entityInfo":{"companyId":0,"companyName":""},
                                              "instanceName":"DefaultInstanceName",
                                              "applicationId":41,
                                              "clientName":client_name,
                                              "backupsetId":backupset_id,
                                              "instanceId":instance_id,
                                              "clientGUID":client_guid,
                                              "subclientName":subclient_name,
                                              "backupsetName":"defaultBackupSet","_type_":7}],
                                              "task":{"taskType":1,"initiatedFrom":1},
                                              "subTasks":[{"subTask":
                                              {"subTaskType":3,"operationType":1001},
                                              "options":{"commonOpts":{
                                              "notifyUserOnJobCompletion":False,
                                              "jobMetadata":[{"selectedItems":
                                              [{"itemName":"","itemType":""}],
                                              "jobOptionItems":[]}]},
                                              "restoreOptions":{"browseOption":
                                              {"commCellId":commcell_id,
                                              "noImage":False,"useExactIndex":False,
                                              "listMedia":False,"backupset":
                                              {"backupsetId":backupset_id,
                                              "clientId":client_id},
                                              "timeRange":{"toTime":to_time},
                                              "mediaOption":{"copyPrecedence":
                                              {"copyPrecedenceApplicable":False}}},
                                              "destination":{"inPlace":True,"destClient":
                                              {"clientId":client_id,"clientName":client_name}},
                                              "fileOption":{"sourceItem":[restore_path]},
                                              "activeDirectoryRstOption":{},
                                              "commonOptions":{"detectRegularExpression":True,
                                              "preserveLevel":1,"restoreACLs":True}}}}]}}

        trigger_response=self._services['CREATE_TASK']
        flag, response =self._cvpysdk_object.make_request(method='POST', url=trigger_response,
                                                                   payload=payload)
        if not flag:
            raise SDKException('Response', '101',
                               self._commcell_object._update_response_(response.text))
        if not response:
            raise SDKException('Response', '101',
                               self._commcell_object._update_response_(response.text))
        response = response.json()
        if "errorCode" in response:
            raise SDKException('Response', '101',
                               self._commcell_object._update_response_(response.text))
        # get restore job and wait for its completion
        job_id = response["jobIds"][0]
        job = self._commcell_object.job_controller.get(job_id)
        job.wait_for_completion()
