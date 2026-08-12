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
    AD Dashboard management class for monitoring and retrieving Active Directory details.

    This class provides an interface to access and manage various aspects of the AD Dashboard,
    including dashboard details, application details, configuration status, domain and tenant information,
    backup health, data distribution, and application panel data. It is designed to work with a CommCell
    object for integration with the underlying infrastructure.

    Key Features:
        - Retrieve AD dashboard details
        - Access AD applications details
        - Check if the dashboard is configured
        - Get domains and tenants information
        - Monitor backup health status
        - Analyze data distribution across AD entities
        - View application panel information
        - Properties for easy access to configuration, domains/tenants, backup health, data distribution, and application panel

    #ai-gen-doc
    """

    def __init__(self, commcell_object: object) -> None:
        """Initialize an instance of the AdDashboard class.

        Args:
            commcell_object: An instance of the Commcell class used to establish a connection 
                and interact with the Commcell environment.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> ad_dashboard = AdDashboard(commcell)
            >>> print("AdDashboard instance created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self.dashboard_response = None
        self.azure_ad_response = None
        self.apps_response = None
        self.apps_totalentities = None

    def get_ad_dashboard_details(self) -> dict:
        """Retrieve Active Directory (AD) Dashboard details from the Commcell via REST API.

        This method makes a REST API call to fetch the AD Dashboard details associated with the Commcell.
        It raises an SDKException if the response is empty or if the API call is unsuccessful.

        Returns:
            dict: A dictionary containing the AD Dashboard details.

        Raises:
            SDKException: If the API response is empty or indicates a failure.

        Example:
            >>> ad_dashboard = AdDashboard(commcell_object)
            >>> details = ad_dashboard.get_ad_dashboard_details()
            >>> print(details)
            >>> # The 'details' dictionary contains information about the AD Dashboard

        #ai-gen-doc
        """
        configured = self._services['ADDASHBOARD'] + '?slaNumberOfDays=1'
        flag, response = self._cvpysdk_object.make_request(method='GET', url=configured)
        if flag and response:
            self.dashboard_response = response.json()
        elif not flag:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))
        else:
            raise SDKException('Response', '102', self._commcell_object._update_response_(response.text))

    def get_ad_apps_details(self) -> dict:
        """Retrieve the Active Directory (AD) application listing details from the Commcell.

        This method performs a REST API call to fetch details about all AD applications configured
        in the Commcell environment.

        Returns:
            dict: A dictionary containing details of the AD applications.

        Raises:
            SDKException: If the API response is empty or indicates a failure.

        Example:
            >>> ad_dashboard = AdDashboard()
            >>> ad_apps = ad_dashboard.get_ad_apps_details()
            >>> print(f"Number of AD applications: {len(ad_apps)}")
            >>> # Access details of a specific AD application
            >>> for app_id, app_info in ad_apps.items():
            ...     print(f"App ID: {app_id}, Name: {app_info.get('name')}")

        #ai-gen-doc
        """
        configured = self._services['ADAPPS']
        flag, response = self._cvpysdk_object.make_request(method='GET', url=configured)

        if flag and response:
            self.apps_response = response.json()
        elif not flag:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))
        else:
            raise SDKException('Response', '102', self._commcell_object._update_response_(response.text))

    def _configured(self) -> dict:
        """Check if both Active Directory (AD) and Azure AD are configured.

        This method verifies the configuration status of both AD and Azure AD by retrieving
        their configuration values from the Dashboard API and Apps Listing API.

        Returns:
            dict: A dictionary containing the configuration values of AD and Azure AD.

        Example:
            >>> dashboard = AdDashboard()
            >>> config_status = dashboard._configured()
            >>> print(config_status)
            {'AD': True, 'AzureAD': False}

        #ai-gen-doc
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
    def is_configured(self) -> dict:
        """Get the configuration values of AD and Azure AD from the Dashboard API and Apps Listing API.

        Returns:
            dict: A dictionary containing the configuration status and details for Active Directory (AD) and Azure AD.

        Example:
            >>> dashboard = AdDashboard()
            >>> config = dashboard.is_configured
            >>> print(config)
            {'AD': {'configured': True}, 'AzureAD': {'configured': False}}

        #ai-gen-doc
        """
        configure_dict=self._configured()
        return configure_dict

    def _get_domains_and_tenants(self) -> dict:
        """Retrieve the number of domain controllers and tenants.

        This method fetches information from the Dashboard API and Apps Listing API,
        returning a dictionary containing the counts of domain controllers and tenants.

        Returns:
            dict: A dictionary with the number of domain controllers and tenants.

        Example:
            >>> ad_dashboard = AdDashboard()
            >>> result = ad_dashboard._get_domains_and_tenants()
            >>> print(result)
            {'domain_controllers': 5, 'tenants': 3}

        #ai-gen-doc
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
    def domains_and_tenants(self) -> dict:
        """Get the number of domain controllers and tenants from the Dashboard API and Apps Listing API.

        Returns:
            dict: A dictionary containing the count of domain controllers and tenants as retrieved from the Dashboard API and Apps Listing API.

        Example:
            >>> ad_dashboard = AdDashboard()
            >>> result = ad_dashboard.domains_and_tenants
            >>> print(result)
            {'domain_controllers': 5, 'tenants': 3}

        #ai-gen-doc
        """
        return self._get_domains_and_tenants()

    def _get_backup_health(self) -> dict:
        """Retrieve the backup health panel details.

        Returns:
            dict: A dictionary containing details about the backup health panel.

        Example:
            >>> dashboard = AdDashboard()
            >>> health_info = dashboard._get_backup_health()
            >>> print(health_info)
            >>> # Output will be a dictionary with backup health metrics

        #ai-gen-doc
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
    def backup_health(self) -> dict:
        """Get the backup health panel details as a dictionary.

        Returns:
            dict: A dictionary containing details about the backup health panel.

        Example:
            >>> dashboard = AdDashboard()
            >>> health_info = dashboard.backup_health
            >>> print(health_info)
            >>> # Output will be a dictionary with backup health details

        #ai-gen-doc
        """
        return self._get_backup_health()


    def _get_data_distribution(self) -> dict:
        """Retrieve the data distribution panel details.

        Returns:
            dict: A dictionary containing data distribution details for the dashboard.

        Example:
            >>> dashboard = AdDashboard()
            >>> data_distribution = dashboard._get_data_distribution()
            >>> print(data_distribution)
            >>> # Output will be a dictionary with data distribution information

        #ai-gen-doc
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
    def data_distribution(self) -> dict:
        """Get the data distribution details as a dictionary.

        Returns:
            dict: A dictionary containing data distribution details.

        Example:
            >>> dashboard = AdDashboard()
            >>> distribution = dashboard.data_distribution
            >>> print(distribution)
            {'region1': 120, 'region2': 340, 'region3': 210}

        #ai-gen-doc
        """
        return self._get_data_distribution()

    def _get_application_panel(self) -> dict:
        """Retrieve the application panel details for the dashboard.

        Returns:
            dict: A dictionary containing the details of the application panel.

        Example:
            >>> dashboard = AdDashboard()
            >>> panel_details = dashboard._get_application_panel()
            >>> print(panel_details)
            >>> # Output will be a dictionary with application panel information

        #ai-gen-doc
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
    def application_panel(self) -> dict:
        """Get the application panel details as a dictionary.

        Returns:
            dict: A dictionary containing details of the application panel.

        Example:
            >>> dashboard = AdDashboard()
            >>> panel_details = dashboard.application_panel
            >>> print(panel_details)
            >>> # Output will be a dictionary with application panel information

        #ai-gen-doc
        """
        return self._get_application_panel()
