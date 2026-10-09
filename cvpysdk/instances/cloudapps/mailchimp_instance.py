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

"""File for operating on a Mailchimp instance."""

from typing import Any, List, Optional

from ..cainstance import CloudAppsInstance


class MailchimpInstance(CloudAppsInstance):
    """Represents a Mailchimp Cloud Apps instance."""

    def restore_in_place(
            self,
            paths: Optional[List[str]] = None,
            overwrite: bool = True,
            copy_precedence: int = 0,
            **kwargs: Any
    ):
        """Submit an in-place restore job for Mailchimp content.

        Args:
            paths: Content paths to restore. Defaults to the Mailchimp root.
            overwrite: Whether to overwrite existing data. Defaults to True.
            copy_precedence: Copy precedence to use. Defaults to 0.
            **kwargs: Additional options forwarded to the restore operation.

        Returns:
            Job: A Job object representing the submitted restore job.

        #ai-gen-doc
        """
        return self._restore_in_place(
            paths=paths or ['/'],
            overwrite=overwrite,
            copy_precedence=copy_precedence,
            **kwargs
        )