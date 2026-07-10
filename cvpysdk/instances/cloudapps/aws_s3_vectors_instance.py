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

"""File for operating on an AWS S3 Vectors Instance.

AwsS3VectorsInstance is the only class defined in this file.

AwsS3VectorsInstance: Derived class from CloudAppsInstance Base class, representing an
AWS S3 Vectors Cloud Apps instance, and to perform operations on that instance

AwsS3VectorsInstance:

    _get_instance_properties()  --  Instance class method overwritten to add AWS S3 Vectors-specific
                                    properties

    restore_in_place()          --  Submits an in-place restore job for the given paths

AwsS3VectorsInstance Attributes:

    Common properties inherited from CloudAppsInstance:

    ca_instance_type    --  Returns the cloud apps instance type
    credential_name     --  Returns the credential name used for authentication
    credential_id       --  Returns the credential ID used for authentication
    plan_name           --  Returns the plan name associated with this instance
    account_name        --  Returns the account name (client name)
    proxy_client        --  Returns the proxy client name

"""
from typing import List, Optional

from ..cainstance import CloudAppsInstance


class AwsS3VectorsInstance(CloudAppsInstance):
    """
    Represents an instance of the AWS S3 Vectors Cloud Apps service.

    Common cloud apps properties (instance type, credentials, plan, account, proxy client)
    are inherited from CloudAppsInstance. This class adds the restore_in_place method
    for AWS S3 Vectors data.
    """

    def __init__(self, agent_object: object, instance_name: str, instance_id: str = None) -> None:
        """Initialize a new AwsS3VectorsInstance object.

        Args:
            agent_object: Instance of the Agent class associated with this AWS S3 Vectors instance.
            instance_name: The name of the AWS S3 Vectors instance.
            instance_id: Optional; the unique identifier for the instance.
        """
        super(AwsS3VectorsInstance, self).__init__(
            agent_object,
            instance_name,
            instance_id
        )

    def _get_instance_properties(self) -> None:
        """Retrieve AWS S3 Vectors-specific instance properties.

        Common properties (instance type, credential name/id, plan, account, proxy client)
        are parsed by the parent CloudAppsInstance._get_instance_properties().
        """
        super(AwsS3VectorsInstance, self)._get_instance_properties()

    def restore_in_place(
            self,
            paths: List[str],
            overwrite: bool = True,
            copy_precedence: int = 0,
            **kwargs
    ):
        """Submit an in-place restore job for the specified AWS S3 Vectors paths.

        Args:
            paths: List of region/bucket paths to restore, e.g. ["/us-east-1"].
            overwrite: Whether to overwrite existing data during restore. Defaults to True.
            copy_precedence: The copy precedence to use. Defaults to 0 (latest backup).
            **kwargs: Additional keyword arguments forwarded to _restore_in_place.

        Returns:
            Job: A Job object representing the submitted restore job.

        Raises:
            SDKException: If the restore operation fails or parameters are invalid.

        #ai-gen-doc
        """
        return self._restore_in_place(
            paths=paths,
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )
