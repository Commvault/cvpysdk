# -*- coding: utf-8 -*-
# pylint: disable=R1705, R0205
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
File for performing Ad agent dashboard operation.

AdDashboard class is defined in this file.

AdDashboard:    Class for performing Ad agent dashboard operation.

Class:
    AdDashboard :

        __init__(self,commcell_object)         --    initialize object of AdDashboard class associated with the commcell.

        get_ad_dashboard_details               --    get the dashboard details from Dashboard API.

        get_ad_apps_details                    --    get the app listing details from App Listing API.

        configured                          --    return whether both AD and Azure AD are configured or not from Dashboard API and App Listing API.

        _get_domains_and_tenants                    --    return number of domains and tenants from Dashboard API and App Listing API.

        _get_backup_health                          --    return backup health panel details from Dashboard API and App Listing API.

        _get_data_distribution                      --    return data distribution panel details from Dashboard API and App Listing API.

        _get_application_panel                      --    return application panel details from Dashboard API and App Listing API.

AdDashboard Attributes
----------------------
    **configure_dict**                          --      returns a dictionary indicating whether AD and Azure AD are configured with the commcell.

    **domains_and_tenants_dict**                --      returns a dictionary containing the number of domain controllers and tenants in the commcell.

    **backup_health_dict**                      --      returns a dictionary with information about the backup health panel of the AD Dashboard, including SLA met and SLA not met.

    **data_distribution_dict**                  --      returns a dictionary with information about the data distribution panel of the AD Dashboard, such as backup size and backed-up objects.

    **application_panel_dict**                  --      returns a dictionary with information about the application panel of the AD Dashboard, including Azure AD backup size and AD backup size.
"""

from cvpysdk.exception import SDKException

class AdDashboard(object):
    """
    Class for AD Dashboard Details
    """

    def __init__(self,commcell_object):
        """Initialize object of the Clients class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

            Returns:
                object - instance of the Clients class
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self.dashboard_response = None
        self.azure_ad_response = None
        self.apps_response = None
        self.apps_totalentities = None

    def get_ad_dashboard_details(self):
        """
        REST API call to get AD Dashboard details in the commcell
        Raises:
            SDKException:

                if response is empty

                if response is not success
        """
        configured = self._services['ADDASHBOARD'] + '?slaNumberOfDays=1'
        flag, response = self._cvpysdk_object.make_request(method='GET', url=configured)
        if flag and response:
            self.dashboard_response = response.json()
        elif not flag:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))
        else:
            raise SDKException('Response', '102', self._commcell_object._update_response_(response.text))

    def get_ad_apps_details(self):
        """
        REST API call to get AD APP Listing details in the commcell
        Raises:
            SDKException:

                if response is empty

                if response is not success
        """
        configured = self._services['ADAPPS']
        flag, response = self._cvpysdk_object.make_request(method='GET', url=configured)

        if flag and response:
            self.apps_response = response.json()
        elif not flag:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))
        else:
            raise SDKException('Response', '102', self._commcell_object._update_response_(response.text))

    def _configured(self):
        """
        Function check both AD and Azure AD are configured
        Returns:
            configure_dict    --  Configuration value of AD and Azure AD from Dashboard API and Apps Listing API as dict
        """
        configure_dict = {"adconfigure": self.dashboard_response.get('agentSummary', [{}])[0].get('isConfigured', None),
                          "aadconfigure": self.dashboard_response.get('agentSummary', [{}])[1].get('isConfigured',None),
                          "apps_adconfigure": False,
                          "apps_aadconfigure": False}
        for i in range(self.apps_response.get('totalADClients', None)):
            if self.apps_response.get('adClients', [{}])[i].get('isConfigured') and \
                    self.apps_response.get('adClients', [{}])[i].get('appTypeId') == 41:
                configure_dict["apps_adconfigure"] = True
                break

        for i in range(self.apps_response.get('totalADClients', None)):
            if self.apps_response.get('adClients', [{}])[i].get('isConfigured') and \
                    self.apps_response.get('adClients', [{}])[i].get('appTypeId') == 139:
                configure_dict["apps_aadconfigure"] = True
                break

        return configure_dict

    @property
    def is_configured(self):
        """
        Returns:
            configure_dict    --  Configuration value of AD and Azure AD from Dashboard API and Apps Listing API as dict
        """
        configure_dict=self._configured()
        return configure_dict

    def _get_domains_and_tenants(self):
        """
        Function to get number of domains and tenants
        Returns:
            domains_and_tenants_dict    --  Number of domain controllers and tenants from Dashboard API and Apps Listing API as dict
        """
        domains_and_tenants_dict = {
            "total_entities": self.dashboard_response.get('solutionSummary', {}).get('slaSummary', {}).get(
                'totalEntities'),
            "domain_controllers": self.dashboard_response.get('agentSummary', [{}])[0].get('slaSummary', {}).get(
                'totalEntities'),
            "tenants": self.dashboard_response.get('agentSummary', [{}])[1].get('slaSummary', {}).get('totalEntities'),
            "apps_totalentities": 0,
            "apps_domain_controllers": 0,
            "apps_tenants": 0
            }
        for i in range(len(self.apps_response['adClients'])):
            if self.apps_response.get('adClients', [])[i].get('appTypeId') == 41 and \
                    self.apps_response.get('adClients', [])[i].get('slaStatus') != "EXCLUDED_SLA":
                domains_and_tenants_dict["apps_domain_controllers"] += 1
            if self.apps_response.get('adClients', [])[i].get('appTypeId') == 139 and \
                    self.apps_response.get('adClients', [])[i].get('slaStatus') != "EXCLUDED_SLA":
                domains_and_tenants_dict["apps_tenants"] += 1
            if self.apps_response.get('adClients', [])[i].get('slaStatus') != "EXCLUDED_SLA":
                domains_and_tenants_dict["apps_totalentities"] += 1
        return domains_and_tenants_dict

    @property
    def domains_and_tenants(self):
        """
        Returns:
            domains_and_tenants_dict    --  Number of domain controllers and tenants from Dashboard API and Apps Listing API as dict
        """
        return self._get_domains_and_tenants()

    def _get_backup_health(self):
        """
        Function to get backup health panel details
        Returns:
            backup_health_dict    --  Backup health panel details as dict
        """
        backup_health_dict = {
            "recently_backedup": self.dashboard_response.get('solutionSummary', {}).get('slaSummary', {}).get(
                'totalEntities', 0) - self.dashboard_response.get('solutionSummary', {}).get('slaSummary', {}).get(
                'slaNotMetEntities', 0),
            "recently_backedup_per": self.dashboard_response.get('solutionSummary', {}).get('slaSummary', {}).get(
                'slaMetPercentage', 0),
            "recently_not_backedup": self.dashboard_response.get('solutionSummary', {}).get('slaSummary', {}).get(
                'slaNotMetEntities', 0) - self.dashboard_response.get('solutionSummary', {}).get('slaSummary', {}).get(
                'neverBackedupEntities', 0),
            "recently_not_backedup_per": self.dashboard_response.get('solutionSummary', {}).get('slaSummary', {}).get(
                'slaNotMetProcessedAtleastOncePercentage', 0),
            "never_backedup": self.dashboard_response.get('solutionSummary', {}).get('slaSummary', {}).get(
                'neverBackedupEntities', 0),
            "never_backedup_per": self.dashboard_response.get('solutionSummary', {}).get('slaSummary', {}).get(
                'neverBackedupPercentage', 0),
            "apps_recently_backedup": 0,
            "apps_recently_not_backedup": 0,
            "apps_never_backedup": 0,
            "apps_totalentities": 0,
            "apps_recently_backedup_per": 0,
            "apps_recently_not_backedup_per": 0,
            "apps_never_backedup_per": 0
            }
        for i in range(len(self.apps_response['adClients'])):
            if self.apps_response.get('adClients', [])[i].get('slaStatus') == "MET_SLA":
                backup_health_dict["apps_recently_backedup"] += 1
            if self.apps_response.get('adClients', [])[i].get('slaStatus') == "MISSED_SLA" and \
                    self.apps_response.get('adClients', [])[i].get('numberOfItems') != 0:
                backup_health_dict["apps_recently_not_backedup"] += 1
            if self.apps_response.get('adClients', [])[i].get('slaStatus') == "MISSED_SLA" and \
                    self.apps_response.get('adClients', [])[i].get('numberOfItems') == 0:
                backup_health_dict["apps_never_backedup"] += 1
            if self.apps_response.get('adClients', [])[i].get('slaStatus') != "EXCLUDED_SLA":
                backup_health_dict["apps_totalentities"] += 1

        backup_health_dict["apps_recently_backedup_per"] = (
            round(((backup_health_dict["apps_recently_backedup"] / backup_health_dict["apps_totalentities"]) * 100), 2))
        backup_health_dict["apps_recently_not_backedup_per"] = (
            round(((backup_health_dict["apps_recently_not_backedup"] / backup_health_dict["apps_totalentities"]) * 100),
                  2))
        backup_health_dict["apps_never_backedup_per"] = (
            round(((backup_health_dict["apps_never_backedup"] / backup_health_dict["apps_totalentities"]) * 100), 2))

        return backup_health_dict

    @property
    def backup_health(self):
        """
        Returns:
            backup_health_dict    --  Backup health panel details as dict
        """
        return self._get_backup_health()


    def _get_data_distribution(self):
        """
        Function to get data distribution panel details
        Returns:
            data_distribution_dict    --  Data distribution details data as dict
        """
        data_distribution_dict = {"backup_size": round((((self.dashboard_response.get('agentSummary', [{}])[0].get('applicationSize', 0) +
                                                          self.dashboard_response.get('agentSummary', [{}])[1].get('applicationSize',0))
                                                         / 1024) / 1024), 2),
                                  "backup_obj": (
                                              self.dashboard_response.get('agentSummary', [{}])[0].get('numberOfItems', 0) +
                                              self.dashboard_response.get('agentSummary', [{}])[1].get('numberOfItems',0)),
                                  "apps_backup_size": 0,
                                  "apps_backup_obj": 0,
                                  }

        for i in range(len(self.apps_response['adClients'])):
            data_distribution_dict["apps_backup_size"] += self.apps_response.get('adClients', [{}])[i].get('applicationSize', None)

        data_distribution_dict["apps_backup_size"] = round(((data_distribution_dict["apps_backup_size"] / 1024) / 1024), 2)

        for i in range(len(self.apps_response['adClients'])):
            data_distribution_dict["apps_backup_obj"] += self.apps_response.get('adClients', [{}])[i].get('numberOfItems', None)

        return data_distribution_dict

    @property
    def data_distribution(self):
        """
        Returns:
            data_distribution_dict    --  Data distribution details data as dict
        """
        return self._get_data_distribution()

    def _get_application_panel(self):
        """
        Function to get application panel details
        Returns:
            application_panel_dict    --  Application panel details as dict
        """
        application_panel_dict = {
            "aad_tenant": self.dashboard_response.get('agentSummary', [{}])[1].get('slaSummary', {}).get('totalEntities'),
            "aad_backup_size": round((((self.dashboard_response.get('agentSummary', [{}])[1].get('applicationSize')) / 1024) / 1024), 2),
            "aad_backup_obj": self.dashboard_response.get('agentSummary', [{}])[1].get('numberOfItems'),
            "aad_sla_per": self.dashboard_response.get('agentSummary', [{}])[1].get('slaSummary', {}).get('slaMetPercentage'),
            "aad_not_sla_per": self.dashboard_response.get('agentSummary', [{}])[1].get('slaSummary', {}).get('slaNotMetProcessedAtleastOncePercentage'),

            "ad_domains": self.dashboard_response.get('agentSummary', [{}])[0].get('slaSummary', {}).get('totalEntities'),
            "ad_backup_size": round((((self.dashboard_response.get('agentSummary', [{}])[0].get('applicationSize')) / 1024) / 1024), 2),
            "ad_backup_obj": self.dashboard_response.get('agentSummary', [{}])[0].get('numberOfItems'),
            "ad_sla_per": self.dashboard_response.get('agentSummary', [{}])[0].get('slaSummary', {}).get('slaMetPercentage'),
            "ad_not_sla_per": self.dashboard_response.get('agentSummary', [{}])[0].get('slaSummary', {}).get('slaNotMetProcessedAtleastOncePercentage'),

            "apps_aad_tenant": 0, "apps_aad_backup_size": 0, "apps_aad_backup_obj": 0,
            "apps_aad_sla_per": 0,"apps_aad_not_sla_per": 0,
            "apps_ad_domains": 0, "apps_ad_backup_size": 0, "apps_ad_backup_obj": 0,
            "apps_ad_sla_per": 0,"apps_ad_not_sla_per": 0,
            "apps_aad_sla": 0, "apps_ad_sla": 0}

        for i in range(len(self.apps_response['adClients'])):
            if self.apps_response.get('adClients', [])[i].get('appTypeId') == 139 and \
                    self.apps_response.get('adClients', [])[i].get('slaStatus') != "EXCLUDED_SLA":
                application_panel_dict["apps_aad_tenant"] += 1

            if self.apps_response.get('adClients', [])[i].get('appTypeId') == 139:
                application_panel_dict["apps_aad_backup_size"] += self.apps_response.get('adClients', [{}])[i].get(
                    'applicationSize')
                application_panel_dict["apps_aad_backup_obj"] += self.apps_response.get('adClients', [{}])[i].get(
                    'numberOfItems')

            if self.apps_response.get('adClients', [])[i].get('appTypeId') == 41 and \
                    self.apps_response.get('adClients', [])[i].get('slaStatus') != "EXCLUDED_SLA":
                application_panel_dict["apps_ad_domains"] += 1

            if self.apps_response.get('adClients', [])[i].get('appTypeId') == 41:
                application_panel_dict["apps_ad_backup_size"] += self.apps_response.get('adClients', [{}])[i].get(
                    'applicationSize')
                application_panel_dict["apps_ad_backup_obj"] += self.apps_response.get('adClients', [{}])[i].get(
                    'numberOfItems')

            if self.apps_response.get('adClients', [])[i].get('appTypeId') == 139 and \
                    self.apps_response.get('adClients', [])[i].get('slaStatus') == "MET_SLA":
                application_panel_dict["apps_aad_sla"] += 1

            if self.apps_response.get('adClients', [])[i].get('appTypeId') == 41 and \
                    self.apps_response.get('adClients', [])[i].get('slaStatus') == "MET_SLA":
                application_panel_dict["apps_ad_sla"] += 1

        application_panel_dict["apps_aad_backup_size"] = round(
            ((application_panel_dict["apps_aad_backup_size"] / 1024) / 1024), 2)
        application_panel_dict["apps_ad_backup_size"] = round(
            ((application_panel_dict["apps_ad_backup_size"] / 1024) / 1024), 2)

        application_panel_dict["apps_aad_sla_per"] = (
            round(((application_panel_dict["apps_aad_sla"] / application_panel_dict["apps_aad_tenant"]) * 100), 2))
        application_panel_dict["apps_ad_sla_per"] = (
            round(((application_panel_dict["apps_ad_sla"] / application_panel_dict["apps_ad_domains"]) * 100), 2))

        application_panel_dict["apps_aad_not_sla_per"] = (round((((application_panel_dict["apps_aad_tenant"] -
                                                                   application_panel_dict["apps_aad_sla"]) /
                                                                  application_panel_dict["apps_aad_tenant"]) * 100), 2))
        application_panel_dict["apps_ad_not_sla_per"] = (round((((application_panel_dict["apps_ad_domains"] -
                                                                  application_panel_dict["apps_ad_sla"]) /
                                                                 application_panel_dict["apps_ad_domains"]) * 100), 2))

        return application_panel_dict

    @property
    def application_panel(self):
        """
        Returns:
            application_panel_dict    --  Application panel details as dict
        """
        return self._get_application_panel()