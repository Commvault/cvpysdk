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

"""Main file for performing operations on request manager App under Activate.

'Requests' & 'Request' are 2 classes defined in this file

Requests:   Class to represent all requests in the commcell

Request:    Class to represent single request in the commcell


Requests:

    __init__()                          --  initialise object of the Requests class

     _response_not_success()            --  parses through the exception response, and raises SDKException

     _get_all_requests()                --  gets all the requests from the commcell

     refresh()                          --  refresh the requests with the commcell

     has_request()                      --  checks whether request with given name exists or not

     get()                              --  returns Request object for given request name

     delete()                           --  deletes the request

     add()                              --  Add request

Request:

    __init__()                          --  initialise object of the Request class

     _response_not_success()            --  parses through the exception response, and raises SDKException

     _get_request_properties()          --  returns the properties of the request

     _get_property_value()              --  returns the property value for given property name in request

     _get_valid_projects()              --  returns valid projects for this request

     refresh()                          --  refresh the request details

     configure()                        --  configures created request with details provided

     review_stats()                     --  returns the stats of the review request

     review_document()                  --  marks review for the document

     get_document_details()             --  returns the document details for this request

     mark_review_complete()             --  marks request as review complete

     request_approval()                 --  Request approval for this review request

     give_approval()                    --  Approves the review request

Request Attributes:
--------------------

    **request_id**      --  returns the id of the request

    **review_set_id**   --  returns the request's review set id

    **request_app**     --  returns the app type for this request

    **request_name**    --  returns the name of the request

    **owner**           -- returns owner name of the request

    **request_props**   --  returns the request properties

    **reviewers**       --  returns the reviewers list

    **approvers**       --  returns the approvers list

    **criteria**        --  returns the review request criteria

    **status**          --  returns the request status

    **requestor**       --  returns the requestor mail id who requested this review

    **request_type**    --  returns the type of request

"""
import copy

from ..exception import SDKException
from ..activateapps.constants import RequestConstants, TargetApps
from ..activateapps.ediscovery_utils import EdiscoveryClientOperations


class Requests:
    """Class for representing all requests in the commcell."""

    def __init__(self, commcell_object):
        """Initializes an instance of the Requests class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

            Returns:
                object  -   instance of the Requests class

        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._requests = None
        self._API_GET_REQUESTS = self._services['EDISCOVERY_REQUESTS']
        self._API_REQ_DELETE = self._services['EDISCOVERY_REQUEST_DETAILS']
        self.refresh()

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_all_requests(self):
        """gets all the requests from the commcell

            Args:
                None

            Returns:

                dict    --  containing request details

            Raises:

                SDKException:

                    if failed to fetch requests details

         """
        flag, response = self._cvpysdk_object.make_request('GET', self._API_GET_REQUESTS)
        output = {}
        if flag:
            if response.json() and 'requests' in response.json():
                for node in response.json()['requests']:
                    if 'name' in node:
                        output[node['name'].lower()] = node
                return output
            raise SDKException('RequestManager', '103')
        self._response_not_success(response)

    def refresh(self):
        """Refresh the requests with the commcell."""
        self._requests = self._get_all_requests()

    def has_request(self, req_name):
        """Checks if a request exists in the commcell with the input name or not

            Args:
                req_name (str)  --  name of the request

            Returns:
                bool - boolean output to specify whether the request exists in the commcell or not

            Raises:
                SDKException:
                    if type of the request name argument is not string

        """
        if not isinstance(req_name, str):
            raise SDKException('RequestManager', '101')
        return self._requests and req_name.lower() in self._requests

    def get(self, req_name):
        """Returns the Instance of Request class for given request name

            Args:
                req_name (str)  --  name of the request

            Returns:
                obj --  Instance of Request class

            Raises:
                SDKException:
                    if type of the request name argument is not string

                    if failed to find request

        """
        if not self.has_request(req_name):
            raise SDKException('RequestManager', '105')
        return Request(commcell_object=self._commcell_object, req_name=req_name.lower(),
                       req_id=self._requests[req_name.lower()]['id'])

    def delete(self, req_name):
        """deletes the request for given request name

            Args:
                req_name (str)  --  name of the request

            Returns:
                None

            Raises:
                SDKException:

                    if type of the request name argument is not string

                    if failed to find request

                    if failed to delete request

        """
        if not self.has_request(req_name):
            raise SDKException('RequestManager', '105')
        flag, response = self._cvpysdk_object.make_request(
            'DELETE', self._API_REQ_DELETE % self._requests[req_name.lower()].get('id'))
        if flag:
            if response.json():
                if 'errorCode' in response.json() and response.json()['errorCode'] != 0:
                    raise SDKException(
                        'RequestManager',
                        '102',
                        f"Delete request failed with - {response.json().get('errorMessage')}")
                self.refresh()
                return
            raise SDKException('RequestManager', '106')
        self._response_not_success(response)

    def add(self, req_name, req_type, requestor, criteria, **kwargs):
        """adds request to request manager app

            Args:

                req_name            (str)       --  Name of request

                req_type            (enum)      --  Request type enum(Refer to RequestManagerConstants.RequestType)

                requestor           (str)       --  Mail id of requestor

                criteria            (dict)      --  containing criteria for request

                                                        Example : {'entity_email': [xxx@yy.com]}

                Kwargs Arguement:

                    redaction           (bool)      --  Enable redaction for export type request
                                                                Default:False

                    chaining            (bool)      --  Enable document chaining for export type request
                                                                Default:False

                    delete_backup       (bool)      --  Specifies whether to delete data from backup or not
                                                                            for delete type request
                                                                Default:False

                Returns:

                    obj --  Instance of Request class

                Raises:

                    SDKException:

                            if input is not valid

                            if failed to create request

        """
        if not isinstance(
                criteria,
                dict) or not isinstance(
                req_name,
                str) or not isinstance(
                req_type,
                RequestConstants.RequestType) or not isinstance(
                    requestor,
                str):
            raise SDKException('RequestManager', '101')
        entities = []
        for key, value in criteria.items():
            entities.append({
                'name': key,
                'values': value
            })
        req_json = {"name": req_name,
                    "type": req_type.name,
                    "deleteFromBackup": kwargs.get('delete_backup', False),
                    "enableRedaction": kwargs.get('redaction', False),
                    "enableDocumentChaining": kwargs.get('chaining', False),
                    "requestor": requestor,
                    "entities": entities}

        flag, response = self._cvpysdk_object.make_request('POST', self._API_GET_REQUESTS, req_json)
        if flag:
            if response.json():
                if 'name' in response.json():
                    self.refresh()
                    return Request(commcell_object=self._commcell_object, req_name=response.json()['name'],
                                   req_id=response.json().get('id'))
                if 'errorCode' in response.json() and response.json()['errorCode'] != 0:
                    raise SDKException(
                        'RequestManager',
                        '102',
                        f"Add request failed with - {response.json().get('errorMessage')}")
            raise SDKException('RequestManager', '107')
        self._response_not_success(response)


class Request:
    """Class to represent single request in the commcell"""

    def __init__(self, commcell_object, req_name, req_id=None):
        """Initializes an instance of the Request class.

            Args:
                commcell_object     (object)    --  instance of the commcell class

                req_name            (str)       --  Name of the request

                req_id             (int)        --  request id

            Returns:
                object  -   instance of the Request class

        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._req_name = req_name
        self._req_id = None
        self._req_props = None
        self._req_owner_id = None
        self._req_approvers = None
        self._req_reviewers = None
        self._req_criteria = None
        self._req_status = None
        self._requestor = None
        self._req_type = None
        self._req_app = None
        self._review_set_id = None
        self._req_client_type = 9515
        self._API_REQ_DETAILS = self._services['EDISCOVERY_REQUEST_DETAILS']
        self._API_VALID_PROJECTS = self._services['EDISCOVERY_REQUEST_PROJECTS']
        self._API_REQ_CONFIGURE = self._services['EDISCOVERY_REQUEST_CONFIGURE']
        self._API_REQ_FEDERATED = self._services['EDISCOVERY_REQUEST_FEDERATED']
        self._API_REQ_DYN_FEDERATED = self._services['EDISCOVERY_DYNAMIC_FEDERATED']
        if req_id:
            self._req_id = req_id
        else:
            self._req_id = self._commcell_object.activate.request_manager().get(req_name).request_id
        self.refresh()
        self._ediscovery_client_ops = EdiscoveryClientOperations(self._commcell_object, self)

    def _response_not_success(self, response):
        """Helper function to raise an exception when reponse status is not 200 (OK).

            Args:
                response    (object)    --  response class object,

                received upon running an API request, using the `requests` python package

        """
        raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_property_value(self, req_properties, prop_name):
        """parses request properties and returns value for given property name

            Args:

                prop_name       (str)       --  name of property

                req_properties  (list(dict))--  list of request properties

            Returns:

                str     -- property value
        """
        for prop in req_properties:
            if 'name' in prop and prop['name'].lower() == prop_name.lower():
                return prop['value'] if "value" in prop else prop.get('values')
        return None

    def _get_request_properties(self):
        """returns the properties of the request

            Args:

                None

            Returns:

                dict        --  Containing properties of request

            Raises:

                SDKException:

                        if failed to find request details
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._API_REQ_DETAILS % self._req_id)
        if flag:
            if response.json():
                self._req_owner_id = response.json().get('owner').get('id', 0)
                self._req_approvers = response.json().get('approvers')
                self._req_reviewers = response.json().get('reviewers')
                self._req_name = response.json().get('name')
                self._req_criteria = self._get_property_value(req_properties=response.json().get(
                    'properties', []), prop_name=RequestConstants.PROPERTY_REVIEW_CRIERIA)
                if not self._req_criteria:
                    # SDG request based on entities
                    self._req_criteria = self._get_property_value(
                        req_properties=response.json().get(
                            'properties', []), prop_name=RequestConstants.PROPERTY_ENTITIES)
                self._review_set_id = self._get_property_value(
                    req_properties=response.json().get(
                        'properties', []),
                    prop_name=RequestConstants.PROPERTY_REVIEW_SET_ID)
                if not self._review_set_id:
                    self._review_set_id = self._req_id
                self._req_status = response.json().get('status')
                self._requestor = response.json().get('requestor')
                self._req_type = response.json().get('type')
                self._req_app = response.json().get('application')
                return response.json()
            raise SDKException('RequestManager', '104')
        self._response_not_success(response)

    def _get_valid_projects(self):
        """returns list of valid projects for this request

            Args:

                None

            Returns:

                dict    --  containing valid project details

            Raises:

                SDKException:

                    if failed to get project details

        """
        output = {}
        flag, response = self._cvpysdk_object.make_request('GET', self._API_VALID_PROJECTS % self._req_id)
        if flag:
            if response.json() and 'projects' in response.json():
                projects = response.json()['projects']
                for project in projects:
                    if 'status' in project and project['status'] == 'VALID':
                        output[project['name'].lower()] = project
                return output
            raise SDKException('RequestManager', '102', "Failed to get valid project details")
        self._response_not_success(response)

    def configure(self, projects, reviewers, approvers):
        """configure created request with provided details

            Args:

                projects        (list)      --  list of project names to associate

                reviewers       (list)      --  list of reviewers user names

                approvers       (list)      --  list of approvers user names

            Returns:

                None

            Raises:

                SDKException:

                    if failed to configure request

                    if input is not valid

                    if reviewers/approvers doesn't exists
        """
        if self.status != RequestConstants.RequestStatus.TaskCreated.name:
            raise SDKException(
                'RequestManager',
                '102',
                f"Request is not in created state. Current state - {self.status}")
        if self.request_app != TargetApps.SDG.name:
            raise SDKException(
                'RequestManager',
                '102',
                f"Configuring Request is supported only for SDG App request")
        if not isinstance(projects, list) or not isinstance(reviewers, list) or not isinstance(approvers, list):
            raise SDKException('RequestManager', '101')
        valid_projects = self._get_valid_projects()
        project_ids = []
        sdg_obj = self._commcell_object.activate.sensitive_data_governance()
        for project in projects:
            if project.lower() not in valid_projects:
                raise SDKException('RequestManager', '102', f"Not a valid project {project} to associate to request")
            project_ids.append(int(sdg_obj.get(project).project_id))

        # reviewer
        reviewers_list = []
        for user in reviewers:
            if not self._commcell_object.users.has_user((user)):
                raise SDKException('RequestManager', '102', f"Unable to find reviewer user : {user}")
            user_obj = self._commcell_object.users.get(user)
            reviewers_list.append({"id": user_obj.user_id,
                                   "name": user_obj.user_name
                                   })

        # approvers
        approvers_list = []
        for user in approvers:
            if not self._commcell_object.users.has_user((user)):
                raise SDKException('RequestManager', '102', f"Unable to find approver user : {user}")
            user_obj = self._commcell_object.users.get(user)
            approvers_list.append({"id": user_obj.user_id,
                                   "name": user_obj.user_name
                                   })
        req_json = {"projectIds": project_ids,
                    "reviewers": reviewers_list,
                    "approvers": approvers_list}

        flag, response = self._cvpysdk_object.make_request('PUT', self._API_REQ_CONFIGURE % self._req_id, req_json)
        if flag:
            if response.json():
                if 'errorCode' in response.json() and response.json()['errorCode'] != 0:
                    raise SDKException(
                        'RequestManager',
                        '102',
                        f"Configure request failed with - {response.json().get('errorMessage')}")
                self.refresh()
                return
            raise SDKException('RequestManager', '108')
        self._response_not_success(response)

    def get_document_details(self, criteria=None, attr_list=None, query="*:*", start=0, rows=10):
        """Returns the document details for this request

            Args:

                criteria        (str)      --  containing criteria for query

                                                    Example :

                                                        Size:[10 TO 1024]
                                                        FileName:09_23*

                attr_list       (set)      --  Column names to be returned in results.
                                                     Acts as 'fl' in query

                start           (int)      --  Specifies start index for fetching documents

                rows            (int)      --  No of document details to fetch

                query           (str)      --   query to be performed (acts as q param in query)
                                                    default:None (Means *:*)

            Returns:

                dict        --  Containing document details

            Raises:

                SDKException:

                    if failed to perform search
        """
        if not attr_list:
            attr_list = RequestConstants.SEARCH_QUERY_SELECTION_SET
        else:
            attr_list = attr_list.union(RequestConstants.SEARCH_QUERY_SELECTION_SET)
        api = self._API_REQ_FEDERATED % (self._get_property_value(
            req_properties=self.request_props,
            prop_name=RequestConstants.PROPERTY_REQUEST_HANDLER_ID),
            self._get_property_value(
            req_properties=self.request_props,
            prop_name=RequestConstants.PROPERTY_REQUEST_HANDLER_NAME))
        if self.request_app == TargetApps.FSO.name:
            api = self._API_REQ_DYN_FEDERATED % (self._req_client_type, self._req_id)
        payload = self._ediscovery_client_ops.form_search_params(
            query=query, criteria=criteria, attr_list=attr_list, params={
                'start': f"{start}", 'rows': f"{rows}"})
        flag, response = self._cvpysdk_object.make_request('POST', api, payload)
        if flag:
            if response.json():
                if 'response' in response.json():
                    return response.json()['response']['docs']
            raise SDKException('RequestManager', '102', 'Failed to get document details for this request')
        self._response_not_success(response)

    def review_stats(self):
        """returns review statistics for this request

            Args:

                None

            Returns:

                dict    --  Containing review stats

                            Example : {
                                            'TotalDocuments': 5,
                                            'ReviewedDocuments': 5,
                                            'Non-ReviewedDocuments': 0,
                                            'AcceptedDocuments': 5,
                                            'DeclinedDocuments': 0,
                                            'RedactedDocuments': 0,
                                            'Non-RedactedDocuments': 0
                                        }

            Raises:

                SDKException:

                        if failed to get stats info
        """
        api = self._API_REQ_FEDERATED % (self._get_property_value(
            req_properties=self.request_props,
            prop_name=RequestConstants.PROPERTY_REQUEST_HANDLER_ID),
            self._get_property_value(
            req_properties=self.request_props,
            prop_name=RequestConstants.PROPERTY_REQUEST_HANDLER_NAME))
        review_set_id = self._review_set_id
        if self.request_app == TargetApps.FSO.name:
            api = self._API_REQ_DYN_FEDERATED % (self._req_client_type, self._req_id)
            review_set_id = f"FSO_{self._req_id}"  # for fso, we have prefix in consent as FSO_
        payload = copy.deepcopy(RequestConstants.REQUEST_FEDERATED_FACET_SEARCH_QUERY)
        for param in payload['searchParams']:
            param['value'] = param['value'].replace("<rsidparam>", review_set_id)
        flag, response = self._cvpysdk_object.make_request('POST', api, payload)
        output = {}
        if flag:
            if response.json():
                if 'response' in response.json():
                    output[RequestConstants.FIELD_DOC_COUNT] = response.json()['response']['numFound']
                if 'facets' in response.json():
                    facets = response.json()['facets']
                    output[RequestConstants.FIELD_REVIEWED] = facets[RequestConstants.FACET_REVIEWED %
                                                                     review_set_id][RequestConstants.FACET_COUNT]
                    output[RequestConstants.FIELD_NOT_REVIEWED] = facets[RequestConstants.FACET_NOT_REVIEWED %
                                                                         review_set_id][RequestConstants.FACET_COUNT]
                    output[RequestConstants.FIELD_ACCEPTED] = facets[RequestConstants.FACET_ACCEPTED % review_set_id][
                        RequestConstants.FACET_COUNT]
                    output[RequestConstants.FIELD_DECLINED] = facets[RequestConstants.FACET_DECLINED % review_set_id][
                        RequestConstants.FACET_COUNT]
                    if self.request_type == RequestConstants.RequestType.EXPORT.value:
                        output[RequestConstants.FIELD_REDACTED] = facets[RequestConstants.FACET_REDACTED %
                                                                         review_set_id][RequestConstants.FACET_COUNT]
                        output[RequestConstants.FIELD_NOT_REDACTED] = facets[RequestConstants.FACET_NOT_REDACTED %
                                                                             review_set_id][RequestConstants.FACET_COUNT]
                return output
            raise SDKException('RequestManager', '102', 'Failed to get review stats for this request')
        self._response_not_success(response)

    def refresh(self):
        """Refresh the request details from the commcell."""
        self._req_props = self._get_request_properties()

    def mark_review_complete(self):
        """Marks review request as review complete

            Args:
                None

            Returns:
                None

            Raises:
                SDKException:

                        if failed to mark review complete
        """
        stats = self.review_stats()
        if int(stats[RequestConstants.FIELD_DOC_COUNT]) != int(stats[RequestConstants.FIELD_REVIEWED]):
            raise SDKException('RequestManager', '109')
        task_prop = [
            {
                "attrVal": "ReviewCompleted",
                "attrName": "progress"
            }
        ]
        self._ediscovery_client_ops.configure_task(task_props=task_prop)
        self.refresh()

    def request_approval(self):
        """Invokes workflow job requesting approval for this request

            Args:
                None

            Returns:

                str --  Workflow job id

            Raises:

                SDKException:

                    if failed to invoke workflow
        """
        if self.status != RequestConstants.RequestStatus.ReviewCompleted.name:
            raise SDKException('RequestManager', '110')
        job_id = self._ediscovery_client_ops.task_workflow_operation()
        self.refresh()
        return job_id

    def review_document(self, comment, doc_id=None, ds_id=None, consent=True, redact=False):
        """does document review update for consent/comment on this request
            Args:

                doc_id          (str)       --  Document id (Mandatory in case of SDG)

                comment         (str)       --  User comment

                ds_id           (int)       --  Data SourceId (Mandatory in case of SDG)

                consent         (bool)      --  Accept or Decline (Default:True)

                redact          (bool)      --  Redact ON or OFF (only in case of export)
                                                        (Default:False)

            Returns:

                None

            Raises:

                SDKException:

                    if failed to update document

                    if input is not valid
        """
        return self._ediscovery_client_ops.do_document_task(doc_id=doc_id, comment=comment,
                                                            consent=consent, redact=redact, ds_id=ds_id)

    def give_approval(self, workflow_job_id, action="Approve"):
        """Gives approval for the review request

                Args:

                    action              (str)       --  Approval action status
                                                            Default : Approve
                                                            Supported Values : [Approve,Deny]


                    workflow_job_id     (int)       --  Workflow job id


                Returns:

                    None

                Raises:

                    SDKException:

                                if failed to give approval

                                if failed to find workflow job

        """
        if not isinstance(workflow_job_id, int):
            raise SDKException('RequestManager', '101')
        interaction_props = self._commcell_object.workflows.get_interaction_properties(
            interaction_id=None, workflow_job_id=workflow_job_id)
        self._commcell_object.workflows.submit_interaction(interaction=interaction_props, input_xml="", action=action)

    @property
    def request_id(self):
        """returns the id of the request

            Returns:

                int     --  Request id

        """
        return int(self._req_id)

    @property
    def review_set_id(self):
        """returns the id of the request's reviewset

            Returns:

                int     --  Request review set id

        """
        return int(self._review_set_id)

    @property
    def request_name(self):
        """returns the name of the request

            Returns:

                str     --  Request name

        """
        return self._req_name

    @property
    def owner(self):
        """returns the name of the request owner

            Returns:

                str     --  Request owner's name

        """
        users_obj = self._commcell_object.users
        for key, value in users_obj.all_users.items():
            if value == self._req_owner_id:
                return key

    @property
    def request_props(self):
        """returns the properties of the request

            Returns:

                list(dict)     --  Request properties

        """
        return self._req_props['properties']

    @property
    def reviewers(self):
        """returns the reviewers for this request

            Returns:

                list(dict)      --  Reviewer user details
        """
        return self._req_reviewers

    @property
    def approvers(self):
        """returns the approvers for this request

            Returns:

                list(dict)      --  Approver user details
        """
        return self._req_approvers

    @property
    def criteria(self):
        """returns the criteria value for this request

            Returns:

                str --  Request criteria

        """
        return self._req_criteria

    @property
    def status(self):
        """returns the status for this request

            Returns:

                str --  Request status

        """
        return self._req_status

    @property
    def request_app(self):
        """returns the app used for this request

            Returns:

                str --  Activate app name

        """
        return self._req_app

    @property
    def request_type(self):
        """returns the type for this request

            Returns:

                str --  Request type

        """
        return self._req_type

    @property
    def requestor(self):
        """returns the requestor mail id for this request

            Returns:

                str --  Requestor mail id

        """
        return self._requestor
