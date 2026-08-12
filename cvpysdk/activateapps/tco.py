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

"""Utilities class for Cost Assessment

CostAssessment:  Class for cost assessment related operations support

CostAssessment
============

    __init__()                          --  Initializes the CostAssessment class

    _response_not_success()             --  Helper method to raise exception when response is not 200 (ok)

    _get_discovery_criteria()            -- Get discovery criteria to run assessment

    run_assessment()                    -- Run Cost Assessment

    delete_credential()                 -- Delete credential from credential manager

    get_workload_details()              -- Get workload details for assessment

    _get_actual_cost_and_storage_details() -- Get actual cost and storage

    delete_assessment()                 -- Delete assessment

    get_workload_details()              -- Get workload details for assessment

"""

from cvpysdk.exception import SDKException
import cvpysdk.constants as cs


class CostAssessment:
    """Class for Cost assessment related operations support"""

    def __init__(self, commcell):
        """Initializes the Cost assessment utility class"""
        self._commcell = commcell
        self._index_servers = commcell.index_servers
        self._cvpysdk_object = commcell._cvpysdk_object
        self._services = commcell._services
        self._update_response_ = commcell._update_response_
        self._assessment_detail = self._services["ASSESSMENT_DETAILS"]
        self._assessment_criteria = self._services["ASSESSMENT_DISCOVERY_CRITERIA"]

    def _response_not_success(self, response):
        """Helper method to raise exception when response is not 200 (ok)

            Raises:
                SDKException:
                    Response was not success
        """
        raise SDKException(
            'Response',
            '101',
            self._update_response_(
                response.text))

    def _get_discovery_criteria(self, credential_id, vendor_type):
        """Get discovery criteria for given credential

                Args:
                    credential_id(str)  -- Credential id
                    vendor_type(str)      -- Vendor type (i.e. Azure, AWS)
                Return:
                    (dict)        -- Dict of discovery criteria
                                        i.e {
                                                 "criteria": "SUBSCRIPTIONS" | "Regions",
                                                 "details":[]
                                            }

                """
        if vendor_type == 'AWS':
            cloud_connector = 1
        elif vendor_type == 'AZURE':
            cloud_connector = 0
        else:
            raise SDKException("CostAssessment", "103")
        url = self._services['ASSESSMENT_DISCOVERY_CRITERIA'] % (credential_id, cloud_connector)
        flag, response = self._cvpysdk_object.make_request('GET', url=url)
        if flag:
            if response.json():
                if not response.json().get('errorMessage', None):
                    if response.json().get('discoveryCriteria', {}):
                        return response.json().get('discoveryCriteria')
                    else:
                        raise SDKException("CostAssessment", "101")
            raise SDKException('Response', '102')
        else:
            self._response_not_success(response)

    def run_assessment(self, assessment_name, credential_id, resource_scope, vendor_type):
        """
        Run Cost Assessment
        Args:
           assessment_name(str)         -- Assessment name
           credential_id(int)           -- Credential id
           resource_scope(str)          -- Resource scope (i.e. SubscriptionName, Region name)
           vendor_type(str)             -- vendor type (i.e. Azure, AWS)



        Return:
            (int)                       -- Assessment id
        """
        discovery_criteria = self._get_discovery_criteria(credential_id, vendor_type)
        discovery_criteria['details'] = [
            {**item, 'selected': True}
            for item in discovery_criteria.get('details', [])
            if item.get('name') == resource_scope
        ]
        if vendor_type == 'AWS':
            cloud_connector = 1
        elif vendor_type == 'AZURE':
            cloud_connector = 0
        else:
            raise SDKException("CostAssessment", "103")

        assessment_config = cs.cost_assessment_config

        requests_json = {
            "assessmentName": assessment_name,
            "assessmentProperties": {
                "cloudConnector": cloud_connector,
                "credentialId": credential_id,
                "authType": 1,
                "discoveryCriteria": discovery_criteria,
                "assessmentConfig": assessment_config
            }
        }

        request = self._services['RUN_ASSESSMENT']
        flag, response = self._cvpysdk_object.make_request(
            'POST', request, requests_json
        )
        if flag:
            if response.json():
                if 'assessmentId' in response.json():
                    return response.json().get('assessmentId')
                else:
                    raise SDKException("CostAssessment", "102", )
            raise SDKException('Response', '102')
        else:
            self._response_not_success(response)

    def get_workload_details(self, assessment_id):
        """Method to get workload details

            Args:
                assessment_id         (str)   -   Assessment id

            Returns:
                (list)  -   Workload details
                             i.e       [
                                        {
                                            "costdetails": [],
                                            "discoveredCount": 1,
                                            "discoveredSize": 1,
                                            "resourceDetails": [],
                                            "workloadtype": "VM"
                                        }
                                    ]

            Raises:
                    SDKException:
                        Response was not success

        """

        url = self._services['ASSESSMENT_DETAILS'] % assessment_id
        flag, response = self._cvpysdk_object.make_request('GET', url=url)
        if flag:
            if response.json():
                if "Assessments" in response.json():
                    assessments = response.json().get('Assessments', [])
                    if assessments:
                        tco_properties = assessments[0].get('tcoAssessmentProperties', {})
                        if tco_properties:
                            if 'commvaultCost' in tco_properties and 'workloadDetails' in tco_properties:
                                commvault_cost = tco_properties.get('commvaultCost')
                                workload_details = tco_properties.get('workloadDetails')
                                year1_details, year3_details = self._get_actual_cost_and_storage_details(commvault_cost,
                                                                                                         workload_details)
                                return year1_details, year3_details, self._format_workload_data(workload_details)
                return []
            raise SDKException('Response', '102')
        else:
            self._response_not_success(response)

    def _get_actual_cost_and_storage_details(self, commvault_cost, workload_details):
        """
        Get cost and storage details
        Args:
            commvault_cost(dict)    -- commvault cost for workloads
            workload_details(list)  -- workload details
        Returns:
            (dict)  -   Dict of year one and year three cost and storage
        """
        year1_agp_primary = 0
        year3_agp_primary = 0
        year1_agp_secondary = 0
        year3_agp_secondary = 0
        year1_license_cost = 0
        year3_license_cost = 0

        primary_y1_cost = commvault_cost.get('primaryCloudStorageUsedCost', 0)
        primary_y3_cost = commvault_cost.get('primaryCloudStorageUsed3YCost', 0)
        secondary_y1_cost = commvault_cost.get('secondaryCloudStorageUsedCost', 0)
        secondary_y3_cost = commvault_cost.get('secondaryCloudStorageUsed3YCost', 0)

        for workload in workload_details:
            costdetails = workload.get('costdetails', [])
            for costdetail in costdetails:
                if not isinstance(costdetail, dict):
                    continue
                name = costdetail.get('name')
                value = costdetail.get('value')
                if not name or value is None:
                    continue
                value = float(value)
                if name == 'StorageEstimateOneYearAGPPrimary':
                    year1_agp_primary += value
                if name == 'StorageEstimateThreeYearAGPPrimary':
                    year3_agp_primary += value
                if name == 'StorageEstimateOneYearAGPSecondary':
                    year1_agp_secondary += value
                if name == 'StorageEstimateThreeYearAGPSecondary':
                    year3_agp_secondary += value
                if name == 'LicenseCostOneYear':
                    year1_license_cost += value
                if name == 'LicenseCostThreeYear':
                    year3_license_cost += value

        year1_agp_primary_in_tb = cs.convert_bytes_to_tb(year1_agp_primary)
        year3_agp_primary_in_tb = cs.convert_bytes_to_tb(year3_agp_primary)
        year1_agp_secondary_in_tb = cs.convert_bytes_to_tb(year1_agp_secondary)
        year3_agp_secondary_in_tb = cs.convert_bytes_to_tb(year3_agp_secondary)

        year_one_dashboard = {}
        year_three_dashboard = {}
        year_one_dashboard["AGP Frequent (Primary)"] = [primary_y1_cost, year1_agp_primary_in_tb]
        year_one_dashboard["AGP Infrequent (Replication)"] = [secondary_y1_cost, year1_agp_secondary_in_tb]
        year_one_dashboard["Total storage"] = [year1_agp_primary_in_tb + year1_agp_secondary_in_tb]
        year_one_dashboard["Total cost"] = [primary_y1_cost + secondary_y1_cost + year1_license_cost]

        year_three_dashboard["AGP Frequent (Primary)"] = [primary_y3_cost, year3_agp_primary_in_tb]
        year_three_dashboard["AGP Infrequent (Replication)"] = [secondary_y3_cost, year3_agp_secondary_in_tb]
        year_three_dashboard["Total storage"] = [year3_agp_primary_in_tb + year3_agp_secondary_in_tb]
        year_three_dashboard["Total cost"] = [primary_y3_cost + secondary_y3_cost + year3_license_cost]

        return year_one_dashboard, year_three_dashboard

    def delete_assessment(self, assessment_id):
        """Method to delete an assessment with the provided assessment id

            Args:
                assessment_id         (str)   -   Assessment id

            Raises:
                    SDKException:
                        Response was not success

        """

        url = self._services['ASSESSMENT_DETAILS'] % assessment_id
        flag, response = self._cvpysdk_object.make_request('DELETE', url=url)

        if response.status_code != 200 or not flag:
            self._response_not_success(response)

    def _format_workload_data(self, workloads):
        """
        Format the resource data into the required format
        Args:
           workloads(dict)      --Workload data
        Returns:
            (dict)              -- Formatted data for workload
        """
        formatted_resources = {}

        for resource in workloads:
            workload = cs.workload_mapping.get(resource['workloadtype'], resource['workloadtype'])
            count = resource['discoveredCount']
            storage_size = cs.convert_bytes_to_tb(resource['discoveredSize'])

            formatted_resources[workload] = [count, storage_size]
        return formatted_resources
