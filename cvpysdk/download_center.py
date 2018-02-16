# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""File for doing operations on Download Center.

DownloadCenter is the class defined in this module for doing operations on the Download Center.

Following Operations can be performed on the Download Center:

    1.  Add a new category to Download Center

    2.  Add a new sub category to the specified category to Download Center

    3.  Upload a package to Download Center

    4.  Download a package from Download Center

    5.  Delete a sub category from the specified category on Download Center

    6.  Delete a category from Download Center

    7.  Delete a package from Download Center

    8.  Update the category information

    9.  Update the sub category information for the specified category


DownloadCenter:

    __init__(commcell_object)   --  initializes a connection to the download center

    __repr__()                  --  returns the string representation of an instance of this class

    _get_properties()           --  get the properties of the download center

    _get_packages()             --  get the packages available at download center

    _process_category_request() --  executes the request on the server, and parses the response

    _process_sub_category_request() --  executes the request on the server, and parses the response

    sub_categories()            --  returns the sub categories available for the given category

    get_package_details()       --  returns the details of the package specified

    add_category()              --  adds a new category to the download center

    update_category()           --  updates the category details at the download center

    delete_category()           --  deletes the given category from the download center

    add_sub_category()          --  adds a new sub category to the specified category

    update_sub_category()       --  updates the sub category details for the given catetory
    at the download center

    delete_sub_category()       --  deletes the specified sub category for the given category
    from the download center

    upload_package()            --  uploads the given package to download center

    download_package()          --  downloads the given package from download center

    delete_package()            --  deletes the given package from download center

    refresh()                   --  refresh the properties of the download center class instance


Attributes:

    Following attributes are available for an instance of the Download Center class:

        **product_versions**    --  returns list of product versions supported on Download Center

        **servers_for_browse**  --  returns the list of servers available for browse on DC

        **error_detail**        --  errors returned while getting the Download Center attributes

        **users_and_groups**    --  returns the list of users and user groups available at DC

        **categories**          --  returns the list of categories available at Download Center

        **download_types**      --  returns the list of supported download types for packages

        **vendors**             --  returns the list of vendors available at Download Center

        **platforms**           --  returns the list of supported platforms for DC packages

        **packages**            --  returns the list of packages available at Download Center


# TODO: implement update method for updating details of a package

# TODO: add a PS script to be called via commcell client, to check if the location is valid,
and get the size of the file


"""

from xml.parsers.expat import ExpatError

import os
import time
import xmltodict

from .exception import SDKException


class DownloadCenter(object):
    """Class for doing operations on Download Center like upload or download product."""

    def __init__(self, commcell_object):
        """Initializes an instance of the DownloadCenter class.

            Args:
                commcell_object     (object)    --  instance of the Commcell class

            Returns:
                object  -   instance of the DownloadCenter class

        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_

        self._response = None
        self.refresh()

    def __repr__(self):
        """Returns the string representation of an instance of this class."""
        return "DownloadCenter class instance for Commcell: '{0}'".format(
            self._commcell_object.commserv_name
        )

    def _get_properties(self):
        """Get the properties of the download center."""

        request_xml = """
        <App_DCGetDataToCreatePackageReq getListOfUsers="1"
            getListOfGroups="1" getCategories="1" getSubCategories="1"
            getPlatforms="1" getDownloadTypes="1" getProductVersions="1"
            getRecutNumbers="1" getVendors="1" getDownloadedPackageUsers="1"
            packageId="1" getServerTypes="1"/>
        """

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['GET_DC_DATA'], request_xml
        )

        if flag:
            try:
                self._response = xmltodict.parse(response.text)['App_DCGetDataToCreatePackageResp']
            except ExpatError:
                raise SDKException('DownloadCenter', '101', response.text)
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _get_packages(self):
        """Gets the list of all the Active packages available at the download center."""

        request_xml = """
        <DM2ContentIndexing_CVSearchReq mode="2">
            <searchProcessingInfo pageSize="1000000">
                <queryParams param="ENABLE_DOWNLOADCENTER" value="true"/>
                <queryParams param="GROUP_RESULTS_BY" value="PKG_ID"/>
                <queryParams param="GROUP_LIMIT" value="50"/>
                <queryParams param="GROUP_FACETS" value="true"/>
                <queryParams param="GROUP_FLAT_RESULTS" value="false"/>
                <queryParams param="SORTFIELD" value="VALID_FROM"/>
            </searchProcessingInfo>
            <advSearchGrp />
            <facetRequests>
                <facetRequest count="1" name="PKG_STATUS">
                    <stringParameter selected="1" name="0"/>
                </facetRequest>
            </facetRequests>
        </DM2ContentIndexing_CVSearchReq>
        """

        root = 'DM2ContentIndexing_CVDownloadCenterResp'

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['SEARCH_PACKAGES'], request_xml
        )

        if flag:
            try:
                packages = xmltodict.parse(response.text)[root]['searchResult']['packages']

                if isinstance(packages, dict):
                    packages = [packages]

                for package in packages:
                    name = package['@name'].lower()

                    self._packages[name] = {
                        'id': package['@packageId'],
                        'description': package['@description'],
                        'platforms': {}
                    }

                    platforms = package['platforms']

                    if isinstance(platforms, dict):
                        platforms = [platforms]

                    for platform in platforms:
                        platform_name = platform['@name']
                        platform_id = platform['@id']
                        download_type = platform['downloadType']['@name']

                        if platform_name not in self._packages[name]['platforms']:
                            self._packages[name]['platforms'][platform_name] = {
                                'id': platform_id,
                                'download_type': [download_type]
                            }
                        else:
                            self._packages[name]['platforms'][platform_name][
                                'download_type'].append(download_type)
            except ExpatError:
                raise SDKException('DownloadCenter', '101', response.text)
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _process_category_request(self, operation, name, description=None, new_name=None):
        """Executes the request on the server, and process the response received from the server.

            Args:
                operation       (str)   --  type of operation to be performed on the server

                    e.g:
                        add     -   to add a new category

                        delete  -   to delete an existing category

                        update  -   to update the details of an existing category


                name            (str)   --  name of the category to perform the operation on

                description     (str)   --  description for the category

                    default: None

                new_name        (str)   --  new name to be set for the category

                    in case of ``update`` operation

                    default: None


            Returns:
                None    -   if the operation was performed successfully

            Raises:
                SDKException:
                    if failed to process the request

                    if failed to parse the response

        """
        operations = {
            'service': 'DC_ENTITY',
            'root': 'App_DCSaveLookupEntityResp',
            'error': 'Failed to %s the category.\nError: "{0}"' % (operation)
        }

        if operation == 'add':
            operation_type = '1'
            category_id = ''
        elif operation == 'delete':
            operation_type = '2'
            category_id = self._categories[name]['id']
        elif operation == 'update':
            operation_type = '3'
            category_id = self._categories[name]['id']
            name = new_name
        else:
            raise SDKException('DownloadCenter', '102', 'Invalid Operation')

        if description is None:
            description = ''

        request_xml = """
        <App_DCSaveLookupEntityReq operation="{0}">
            <entitiesToSave entityType="0" id="{1}" name="{2}" description="{3}"/>
        </App_DCSaveLookupEntityReq>
        """.format(operation_type, category_id, name, description)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services[operations['service']], request_xml
        )

        if flag:
            try:
                response = xmltodict.parse(response.text)[operations['root']]
                result = response['@result']

                try:
                    category_id = response['entitiesToSave']['@id']
                    error_code = response['entitiesToSave']['errorDetail']['@errorCode']
                    error_message = response['entitiesToSave']['errorDetail']['@errorMessage']
                except KeyError:
                    # for delete category request,
                    # entitiesToSave key is not returned in the response
                    # so initialize these values to None
                    category_id = error_code = error_message = None

                if result == '3' and error_code != '0':
                    error_message = operations['error'].format(error_message)
                    raise SDKException('DownloadCenter', '102', error_message)

                self.refresh()
            except ExpatError:
                raise SDKException('DownloadCenter', '101', response.text)
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def _process_sub_category_request(
            self,
            operation,
            name,
            category,
            description=None,
            new_name=None):
        """Executes the request on the server, and process the response received from the server.

            Args:
                operation       (str)   --  type of operation to be performed on the server

                    e.g:
                        add     -   to add a new sub category

                        delete  -   to delete an existing sub category from the specified category

                        update  -   to update the details of an existing sub category


                name            (str)   --  name of the sub category to perform the operation on

                category        (str)   --  category for the sub category

                description     (str)   --  description for the sub category

                    default: None

                new_name        (str)   --  new name to be set for the sub category

                    in case of ``update`` operation

                    default: None


            Returns:
                None    -   if the operation was performed successfully

            Raises:
                SDKException:
                    if failed to process the request

                    if failed to parse the response

        """
        operations = {
            'service': 'DC_SUB_CATEGORY',
            'root': 'App_DCSaveSubCategoriesMsg',
            'error': 'Failed to %s the sub category.\nError: "{0}"' % (operation)
        }

        if operation == 'add':
            operation_type = '1'
            sub_category_id = ''
        elif operation == 'delete':
            operation_type = '2'
            sub_category_id = self._categories[category]['sub_categories'][name]['id']
        elif operation == 'update':
            operation_type = '3'
            sub_category_id = self._categories[category]['sub_categories'][name]['id']
            name = new_name
        else:
            raise SDKException('DownloadCenter', '102', 'Invalid Operation')

        if description is None:
            description = ''

        request_xml = """
        <App_DCSaveSubCategoriesMsg operation="{0}">
            <subCategories id="{1}" name="{2}" description="{3}" categoryId="{4}"/>
        </App_DCSaveSubCategoriesMsg>
        """.format(
            operation_type, sub_category_id, name, description, self._categories[category]['id']
        )

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services[operations['service']], request_xml
        )

        if flag:
            try:
                response = xmltodict.parse(response.text)[operations['root']]

                result = response['@result']
                sub_category_id = response['subCategories']['@id']
                error_code = response['subCategories']['errorDetail']['@errorCode']
                error_message = response['subCategories']['errorDetail']['@errorMessage']

                if result == '3' and error_code != '0':
                    error_message = operations['error'].format(error_message)
                    raise SDKException('DownloadCenter', '102', error_message)

                self.refresh()
            except ExpatError:
                raise SDKException('DownloadCenter', '101', response.text)
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def product_versions(self):
        """Return the versions of product available at Download Center."""
        if not self._product_versions:
            product_versions = self._response['productVersions']

            if isinstance(product_versions, dict):
                product_versions = [product_versions]

            for product_version in product_versions:
                self._product_versions[product_version['@name']] = {
                    'id': product_version['@id'],
                    'entity_type': product_version['@entityType']
                }

        return list(self._product_versions.keys())

    @property
    def servers_for_browse(self):
        """Returns the servers available for browse at Download Center."""
        if not self._servers_for_browse:
            servers_for_browse = self._response['serversForBrowse']

            if isinstance(servers_for_browse, dict):
                servers_for_browse = [servers_for_browse]

            for server_for_browse in servers_for_browse:
                self._servers_for_browse[server_for_browse['@name']] = {
                    'id': server_for_browse['@id'],
                    'internal_name': server_for_browse['@internalName'],
                    'entity_type': server_for_browse['@entityType'],
                    'attribute': server_for_browse['@attribute']
                }

        return list(self._servers_for_browse.keys())

    @property
    def error_detail(self):
        """Returns the error details."""
        return self._response['errorDetail']

    @property
    def users_and_groups(self):
        """Returns the Users and User Groups available at Download Center."""
        if not self._users_and_groups:
            users_and_groups = self._response['usersAndGroups']

            if isinstance(users_and_groups, dict):
                users_and_groups = [users_and_groups]

            for user_and_group in self._response['usersAndGroups']:
                self._users_and_groups[user_and_group['@name']] = {
                    'id': user_and_group['@id'],
                    'provider_id': user_and_group['@providerId'],
                    'guid': user_and_group['@guid'],
                    'type': user_and_group['@type'],
                    'service_type': user_and_group['@serviceType']
                }

        return list(self._users_and_groups.keys())

    @property
    def categories(self):
        """Returns the categories of products available at Download Center."""
        if not self._categories:
            categories = self._response['categories']

            if isinstance(categories, dict):
                categories = [categories]

            for category in categories:
                category_id = category['@id']
                temp = {}

                sub_categories = self._response['subCategories']

                if isinstance(sub_categories, dict):
                    sub_categories = [sub_categories]

                for sub_category in sub_categories:
                    cat_id = sub_category['@categoryId']

                    if cat_id == category_id:
                        temp[sub_category['@name']] = {
                            'id': sub_category['@id'],
                            'description': sub_category['@description'],
                            'entity_type': sub_category['@entityType'],
                            'attribute': sub_category['@attribute']
                        }

                self._categories[category['@name']] = {
                    'id': category_id,
                    'description': category['@description'],
                    'entity_type': category['@entityType'],
                    'attribute': category['@attribute'],
                    'sub_categories': temp
                }

        return list(self._categories)

    @property
    def download_types(self):
        """Returns the types of packages available for download at Download Center."""
        if not self._download_types:
            download_types = self._response['downloadTypes']

            if isinstance(download_types, dict):
                download_types = [download_types]

            for download_type in download_types:
                self._download_types[download_type['@name']] = {
                    'id': download_type['@id'],
                    'entity_type': download_type['@entityType']
                }

        return list(self._download_types.keys())

    @property
    def vendors(self):
        """Returns the vendors available at Download Center."""
        if not self._vendors:
            vendors = self._response['vendors']

            if isinstance(vendors, dict):
                vendors = [vendors]

            for vendor in vendors:
                self._vendors[vendor['@name']] = {
                    'id': vendor['@id'],
                    'entity_type': vendor['@entityType']
                }

        return list(self._vendors.keys())

    @property
    def platforms(self):
        """Returns the platforms supported for packages at Download Center."""
        if not self._platforms:
            platforms = self._response['platforms']

            if isinstance(platforms, dict):
                platforms = [platforms]

            for platform in platforms:
                self._platforms[platform['@name']] = {
                    'id': platform['@id'],
                    'entity_type': platform['@entityType'],
                    'architecture': platform['@architectureName']
                }

        return list(self._platforms.keys())

    @property
    def packages(self):
        """Returns the packages available for download at Download Center."""
        if not self._packages:
            self._get_packages()

        return list(self._packages.keys())

    def has_package(self, package):
        """Checks if a package with the given name already exists at Download Center or not.

            Args:
                package     (str)   --  name of the package to check

            Returns:
                bool    -   boolean specifying whether the package exists or not

        """
        return self.packages and package.lower() in self.packages

    def sub_categories(self, category):
        """Returns the sub categories available for the specified category.

            Args:
                category    (str)   --  name of the category to get the sub categories of

            Returns:
                list    -   list of sub categories available for the given category

            Raises:
                SDKException:
                    if category does not exist

        """
        if category not in self.categories:
            raise SDKException('DownloadCenter', '103')

        return list(self._categories[category]['sub_categories'].keys())

    def get_package_details(self, package):
        """Returns the details of the package, like the package description, platforms, etc.

            Args:
                package     (str)   --  name of the package to get the details of

            Returns:
                dict    -   dictionary consisting of the details of the package

            Raises:
                SDKException:
                    if package does not exist

        """
        if not self.has_package(package):
            raise SDKException('DownloadCenter', '106')

        package = package.lower()
        package_detail = self._packages[package]

        output = {
            'name': package,
            'description': package_detail['description'],
            'platforms': {}
        }

        platforms = package_detail['platforms']

        for platform in platforms:
            output['platforms'][platform] = platforms[platform]['download_type']

        return output

    def add_category(self, name, description=None):
        """Adds a new category with the given name, and description.

            Args:
                name            (str)   --  name of the category to add

                description     (str)   --  description for the category (optional)
                    default: None

            Returns:
                None    -   if the category was added successfully

            Raises:
                SDKException:
                    if category already exists

                    if failed to add the category

        """
        if name in self.categories:
            raise SDKException('DownloadCenter', '104')

        self._process_category_request('add', name, description)

    def update_category(self, name, new_name, description=None):
        """Updates the name and description of the category with the given name.

            Args:
                name            (str)   --  name of the existing category to update

                new_name        (str)   --  new name for the category

                description     (str)   --  description for the category (optional)

                    default: None


            Returns:
                None    -   if the category information was updated successfully

            Raises:
                SDKException:
                    if no category exists with the given name

                    if category already exists with the new name specified

                    if failed to update the category

        """
        if name not in self.categories:
            raise SDKException('DownloadCenter', '108')

        if new_name in self.categories:
            raise SDKException('DownloadCenter', '104')

        self._process_category_request('update', name, description, new_name)

    def delete_category(self, name):
        """Deletes the category with the given name.

            Args:
                name            (str)   --  name of the category to delete

            Returns:
                None    -   if the category was deleted successfully

            Raises:
                SDKException:
                    if category does not exists

                    if failed to delete the category

        """
        if name not in self.categories:
            raise SDKException('DownloadCenter', '108')

        self._process_category_request('delete', name)

    def add_sub_category(self, name, category, description=None):
        """Adds a new sub category with the given name, and description to the specified category.

            Args:
                name            (str)   --  name of the sub category to add

                category        (str)   --  name of the category to add the sub category to

                description     (str)   --  description for the sub category (optional)
                    default: None

            Returns:
                None    -   if the sub category was added successfully

            Raises:
                SDKException:
                    if category does not exist

                    if sub category already exists

                    if failed to add the sub category

        """
        if name in self.sub_categories(category):
            raise SDKException('DownloadCenter', '105')

        self._process_sub_category_request('add', name, category, description)

    def update_sub_category(self, name, category, new_name, description=None):
        """Updates the name and description of the sub category with the given name and category.

            Args:
                name            (str)   --  name of the sub category to update the details of

                category        (str)   --  name of the category to update the sub category of

                new_name        (str)   --  new name for the sub category

                description     (str)   --  description for the sub category (optional)

                    default: None


            Returns:
                None    -   if the sub category information was updated successfully

            Raises:
                SDKException:
                    if no sub category exists with the given name

                    if sub category already exists with the new name specified

                    if failed to update the sub category

        """
        if name not in self.sub_categories(category):
            raise SDKException('DownloadCenter', '109')

        if new_name in self.sub_categories(category):
            raise SDKException('DownloadCenter', '105')

        self._process_sub_category_request('update', name, category, description, new_name)

    def delete_sub_category(self, name, category):
        """Deletes the sub category from the category with the given name.

            Args:
                name            (str)   --  name of the sub category to delete

                category        (str)   --  name of the category to delete the sub category from

            Returns:
                None    -   if the sub category was deleted successfully

            Raises:
                SDKException:
                    if sub category does not exist

                    if failed to delete the sub category

        """
        if name not in self.sub_categories(category):
            raise SDKException('DownloadCenter', '109')

        self._process_sub_category_request('delete', name, category)

    def upload_package(self, package, category, version, platform_download_locations, **kwargs):
        """Uploads the given package to Download Center.

            Args:
                package                         (str)   --  name of the package to upload

                category                        (str)   --  category to upload the package for

                version                         (str)   --  product version for package to upload

                platform_download_locations     (list)  --  list consisting of dictionaries

                    where each dictionary contains the values for the platform, download type, and
                    location of the file

                    e.g.:
                        [
                            {
                                'platform': 'Windows-x64',

                                'download_type': 'Exe',

                                'location': 'C:\\location1'
                            }, {
                                'platform': 'Windows-x64',

                                'download_type': 'Script',

                                'location': 'C:\\location2'
                            }, {
                                'platform': 'Windows-x86',

                                'download_type': 'Exe',

                                'location': 'C:\\location3'
                            }, {
                                'platform': 'Windows-x86',

                                'download_type': 'Script',

                                'location': 'C:\\location4'
                            }
                        ]


                **kwargs:

                    valid_from          (str)   --  date from which the package should be valid

                        if the value is not specified, then current date is taken as it's value

                        format:     DD/MM/YYYY


                    description         (str)   --  description of the package

                    readme_location     (str)   --  location of the readme file

                        readme file should have one of the following extensions

                            [**.txt**, **.pdf**, **.doc**, **.docx**]


                    sub_category        (str)   --  sub category to associate the package with

                    vendor              (str)   --  vendor / distributor of the package

                    valid_to            (str)   --  date till which the package should be valid

                        format:     DD/MM/YYYY


                    repository          (str)   --  name of the repository to add the package to

                        if this value is not defined, the first repository will be taken by default


                    visible_to          (list)  --  list of users, the package should be visible to

                    not_visible_to      (list)  --  users, the package should not be visible to

                    early_preview_users (list)  --  list of users, the package should be
                    visible to before release


            Returns:
                None    -   if the package was uploaded successfully to Download Center


            Raises:
                SDKException:
                    if package with given name already exists

                    if category does not exists at Download Center

                    if version is not supported at Download Center

                    if platform is not supported at Download Center

                    if download type is not supported at Download Center

                    if sub category not present for the given category

                    if failed to upload the package

                    if error returned by the server

                    if response was not success

        """
        if self.has_package(package):
            raise SDKException('DownloadCenter', '114')

        if category not in self.categories:
            raise SDKException(
                'DownloadCenter', '103', 'Available categories: {0}'.format(self.categories)
            )

        if version not in self.product_versions:
            raise SDKException(
                'DownloadCenter', '115', 'Available versions: {0}'.format(self.product_versions)
            )

        platforms = []

        readme_location = kwargs.get('readme_location', '')
        readme_file_extensions = ['.txt', '.pdf', '.doc', '.docx']

        if readme_location:
            if os.path.splitext(readme_location)[1] not in readme_file_extensions:
                raise SDKException('DownloadCenter', '118')

        del readme_file_extensions

        for platform_dl_loc in platform_download_locations:
            platform = platform_dl_loc['platform']
            download_type = platform_dl_loc['download_type']
            location = platform_dl_loc['location']

            if platform not in self.platforms:
                raise SDKException(
                    'DownloadCenter', '116', 'Available platforms: {0}'.format(self.platforms)
                )

            if download_type not in self.download_types:
                raise SDKException(
                    'DownloadCenter',
                    '117',
                    'Available download types: {0}'.format(self.download_types)
                )

            package_repository = kwargs.get('repository', self.servers_for_browse[0])
            package_repository_id = self._servers_for_browse[package_repository]['id']
            package_repository_name = self._servers_for_browse[package_repository]['internal_name']

            temp = {
                "@name": platform,
                "@readMeLocation": readme_location,
                "@location": location,
                "@id": self._platforms[platform]['id'],
                "downloadType": {
                    "@name": download_type,
                    "@id": self._download_types[download_type]['id']
                },
                'pkgRepository': {
                    '@repositoryId': package_repository_id,
                    '@respositoryName': package_repository_name
                },
                '@size': 186646528
            }

            platforms.append(temp)

        del platform
        del download_type
        del location
        del temp
        del platform_download_locations

        valid_from = kwargs.get('valid_from', time.strftime('%d/%m/%Y', time.localtime()))
        valid_from = int(time.mktime(time.strptime(valid_from, '%d/%m/%Y')))

        valid_to = kwargs.get('valid_to', '')
        if valid_to:
            valid_to = int(time.mktime(time.strptime(valid_from, '%d/%m/%Y')))

        sub_category = {
            "@entityType": 1,
            "@categoryId": self._categories[category]['id']
        }

        if 'sub_category' in kwargs:
            sub_category_name = kwargs['sub_category']
            sub_categories = self.sub_categories(category)

            if sub_category_name in sub_categories:
                sub_category["@id"] = self._categories[category][
                    'sub_categories'][sub_category_name]['id']
            else:
                raise SDKException(
                    'DownloadCenter', '109', 'Available Sub Categories: {0}'.format(sub_categories)
                )

            del sub_categories

        vendor = kwargs.get('vendor', '')

        if vendor and vendor in self.vendors:
            vendor = self._vendors[vendor]['id']

        visible_to = []
        not_visible_to = []
        early_preview_users = []

        for user in kwargs.get('visible_to', []):
            if user in self.users_and_groups:
                temp = {
                    '@name': user,
                    '@guid': self._users_and_groups[user]['guid'],
                    '@type': self._users_and_groups[user]['type']
                }
                visible_to.append(temp)

        for user in kwargs.get('not_visible_to', []):
            if user in self.users_and_groups:
                temp = {
                    '@name': user,
                    '@guid': self._users_and_groups[user]['guid'],
                    '@type': self._users_and_groups[user]['type']
                }
                not_visible_to.append(temp)

        for user in kwargs.get('early_preview_users', []):
            if user in self.users_and_groups:
                temp = {
                    '@name': user,
                    '@guid': self._users_and_groups[user]['guid'],
                    '@type': self._users_and_groups[user]['type']
                }
                early_preview_users.append(temp)

        request_json = {
            "App_DCPackage": {
                "@name": package,
                "@description": kwargs.get('description', ''),
                "@validFrom": valid_from,
                "@validTo": valid_to,
                "@rank": kwargs.get('rank', 0),
                "category": {
                    "@entityType": 0,
                    "@id": self._categories[category]['id']
                },
                "subCategory": sub_category,
                "platforms": platforms,
                "productVersion": {
                    "entityType": 3,
                    "id": self._product_versions[version]['id']
                },
                "vendor": {
                    "entityType": 6,
                    "id": vendor
                },
                "recutNumber": {
                    "entityType": 4
                },
                "visibleTo": visible_to,
                "notVisibleTo": not_visible_to,
                "earlyPreviewUsers": early_preview_users,
            }
        }

        xml = xmltodict.unparse(request_json)
        xml = xml[xml.find('<App_'):]

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['UPLOAD_PACKAGE'], xml
        )

        self.refresh()

        if flag:
            response = xmltodict.parse(response.text)['App_DCPackage']
            error_code = response['errorDetail']['@errorCode']

            if error_code != '0':
                error_message = response['errorDetail']['@errorMessage']

                raise SDKException('DownloadCenter', '119', 'Error: {0}'.format(error_message))
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def download_package(self, package, download_location, platform=None, download_type=None):
        """Downloads the given package from Download Center to the path specified.

            Args:
                package             (str)   --  name of the pacakge to be downloaded

                download_location   (str)   --  path on local machine to download the package at

                platform            (str)   --  platform to download the package for

                    to be provided only if the package is added for multiple platforms

                    default: None

                download_type       (str)   --  type of package to be downloaded

                    to be provided only if multiple download types are present for single platform

                    default: None

            Returns:
                str     -   path on local machine where the file has been downloaded

            Raises:
                SDKException:
                    if package does not exist

                    if platform not given:
                        in case of multiple platforms

                    if platform given does not exists in the list of supported platforms

                    if download type is not specified:
                        if case of multiple download types for the selected platform

                    if download type given does not exists in the list of download types available

                    if error returned by the server

                    if response was not success

        """

        # get the id of the package, if it is a valid package
        if not self.has_package(package):
            raise SDKException('DownloadCenter', '106')
        else:
            package = package.lower()
            package_id = self._packages[package]['id']

        def get_platform_id(package, platform):
            """Checks if the platform is valid or not, and returns the platform id.

                If platform is set to None, gets the platform from the list of platforms,
                and the platform id.

                Args:
                    package     (str)   --  name of the package to check the platform for

                    platform    (str)   --  name of the platform to get the id of

                Returns:
                    (str, str)  -   tuple consisting of the platform name as the first,
                                        and platform id as the second value

                Raises:
                    SDKException:
                        if platform is not given, and multiple platforms exists for the package

                        if platform specified is not supported for the package

            """
            platforms = self._packages[package]['platforms']
            # check if the package has a single platform only, in case platform is not given
            if platform is None:

                # raise exception if multiple platforms exist for the package
                if len(platforms.keys()) > 1:
                    raise SDKException('DownloadCenter', '110')

                # get the platform name and id, if it's a single platform
                else:
                    platform = list(platforms.keys())[0]
                    platform_id = platforms[platform]['id']

            # raise exception if the platform does not exists in the list of supported platforms,
            # when it is given
            elif platform not in platforms:
                raise SDKException('DownloadCenter', '112')

            # get the id of the platform,
            # when it's given and exists in the list of supported platforms
            else:
                platform_id = platforms[platform]['id']

            return platform, platform_id

        def get_download_type(package, platform, download_type):
            """Checks if the download type for the given package and platform is valid or not.

                If download type is set to None, gets the download type from the list of download
                types availalble for the given package and platform.

                Args:
                    package         (str)   --  name of the package to get the download type for

                    platform        (str)   --  name of the platform to get the download type of

                    download_type   (str)   --  download type to be validated

                Returns:
                    str     -   name of the download type

                Raises:
                    SDKException:
                        if download type is not given, and multiple download types exists

                        if download type specified is not available for the package

            """
            download_types = self._packages[package]['platforms'][platform]['download_type']
            # check if the package has a single download type only,
            # in case download type is not given
            if download_type is None:

                # raise exception if multiple download types exist for the package and the platform
                if len(download_types) > 1:
                    raise SDKException('DownloadCenter', '111')

                # get the download type name, if it's a single download type for the given platform
                else:
                    download_type = download_types[0]

            # raise exception if the download type does not exists in the list, when it is given
            elif download_type not in download_types:
                raise SDKException('DownloadCenter', '113')

            # use the download type given by the user
            else:
                pass

            return download_type

        platform, platform_id = get_platform_id(package, platform)
        download_type = get_download_type(package, platform, download_type)

        if not os.path.exists(download_location):
            try:
                os.makedirs(download_location)
            except FileExistsError:
                pass

        request_id = ''
        file_name = None

        # ID: 3 is static for Download Center, and has the value "Package"
        # ID: 2, needs to provide the package id as the value for "name"
        # ID: 9, needs to provide the platform id as the value for "name"
        # ID: 11, needs to provide the download tyoe as the value for "name"
        # ID: 10 is static for Streamed downloads
        request_xml = '''
        <DM2ContentIndexing_OpenFileReq requestId="{3}">
            <fileParams id="3" name="Package"/>
            <fileParams id="2" name="{0}"/>
            <fileParams id="9" name="{1}"/>
            <fileParams id="11" name="{2}"/>
            <fileParams id="10" name="Streamed"/>
        </DM2ContentIndexing_OpenFileReq>
        '''

        # execute the request to get the details like file name, and request id
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['DOWNLOAD_PACKAGE'], request_xml.format(
                package_id, platform_id, download_type, request_id
            )
        )

        if flag:
            error_list = response.json()['errList']
            file_content = response.json()['fileContent']

            if error_list:
                raise SDKException('DownloadCenter', '107', 'Error: {0}'.format(error_list))

            file_name = file_content.get('fileName', file_name)
            request_id = file_content['requestId']

            # full path of the file on local machine to be downloaded
            download_path = os.path.join(download_location, file_name)

            # execute request to get the stream of content
            # using request id returned in the previous response
            flag1, response1 = self._cvpysdk_object.make_request(
                'POST',
                self._services['DOWNLOAD_VIA_STREAM'],
                request_xml.format(package_id, platform_id, download_type, request_id),
                stream=True
            )

            # download chunks of 1MB each
            chunk_size = 1024 ** 2

            if flag1:
                with open(download_path, "wb") as file_pointer:
                    for content in response1.iter_content(chunk_size=chunk_size):
                        file_pointer.write(content)
            else:
                response_string = self._update_response_(response1.text)
                raise SDKException('Response', '101', response_string)
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        return download_path

    def delete_package(self, package):
        """Deletes the package from Download Center.

            Args:
                package     (str)   --  name of the package to be deleted

            Returns:
                None    -   if the package was deleted successfully

            Raises:
                SDKException:
                    if no package exists with the given name

                    if failed to delete the package

                    if response is not success

        """
        if not self.has_package(package):
            raise SDKException('DownloadCenter', '106')
        else:
            package = package.lower()
            package_id = self._packages[package]['id']

        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['DELETE_PACKAGE'] % package_id
        )

        self.refresh()

        if flag:
            response = xmltodict.parse(response.text)['DM2ContentIndexing_CVDownloadCenterResp']

            if 'errList' in response:
                error_code = response['errList']['@errorCode']

                if error_code != '0':
                    error_message = response['errList']['@errLogMessage']

                    raise SDKException('DownloadCenter', '119', 'Error: {0}'.format(error_message))
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def refresh(self):
        """Refresh the properties of the DownloadCenter."""
        self._get_properties()

        self._product_versions = {}
        self._servers_for_browse = {}
        self._users_and_groups = {}
        self._categories = {}
        self._download_types = {}
        self._vendors = {}
        self._platforms = {}
        self._packages = {}

        self._get_packages()
