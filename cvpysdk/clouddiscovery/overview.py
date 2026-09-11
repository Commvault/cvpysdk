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
Module for Cloud Discovery overview API interactions.

Classes
-------
CloudDiscoveryOverview
    Thin wrapper around the Commvault cloud-discovery REST APIs that:

    * Fetches the Overview page resource summary (counts + byte sizes by
      protection status and workload type) from ``Asset/Search``.
    * Calls the ``Asset/TCO`` API to get the server-side monthly cost estimate.

Usage::

    from cvpysdk.clouddiscovery.overview import CloudDiscoveryOverview

    overview = CloudDiscoveryOverview(commcell)

    # Fetch live resource summary
    summary = overview.get_resource_summary(provider=1)

    # Fetch monthly cost estimate
    cost = overview.get_monthly_cost_estimate(discovered_sizes, provider="AZURE")
"""

import copy
import json
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .constants import (
    ASSET_SEARCH_PAYLOAD,
    ASSET_TCO_PAYLOAD,
    AssetCVProtectionStatus,
    CV_TOTAL,
    FACET_JSON,
    KUBERNETES_WORKLOAD,
    NATIVE_TOTAL,
    PROTECTION_STATUS_COUNT_MAP,
    PROTECTION_STATUS_SIZE_CONFIGURED,
    PROTECTION_STATUS_SIZE_MANAGED,
    PROTECTION_STATUS_SIZE_NOT_PROTECTED,
    PROTECTION_STATUS_SIZE_PROTECTED,
    PROVIDER_PROTECTED_BY_MAP,
    SAVINGS_AMOUNT,
    SAVINGS_PERCENT,
    TOTAL_SIZE,
    VM_WORKLOAD_WITHOUT_KUBERNETES,
    WORKLOAD_TYPE_MAP,
)
from ..exception import SDKException

if TYPE_CHECKING:
    from ..commcell import Commcell


class CloudDiscoveryOverview:
    """Wrapper around the Commvault cloud-discovery overview REST APIs.

    Provides methods to fetch the Overview page resource summary from
    ``Asset/Search`` and to retrieve the server-side monthly cost estimate
    from ``Asset/TCO``.

    This class is intentionally stateless between calls — each method issues
    a fresh API request so results always reflect the current server state.

    Parameters
    ----------
    commcell:
        A connected :class:`~cvpysdk.commcell.Commcell` (or tenant commcell)
        object used for all REST requests.

    Example::

        from cvpysdk.clouddiscovery.overview import CloudDiscoveryOverview

        overview = CloudDiscoveryOverview(commcell)
        summary = overview.get_resource_summary(provider=1)
        cost    = overview.get_monthly_cost_estimate(discovered_sizes)
    """

    def __init__(self, commcell: 'Commcell') -> None:
        """Initialize the CloudDiscoveryOverview object.

        Args:
            commcell: Commcell object used to make API requests.

        Returns:
            None

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('webconsole_hostname', 'username', 'password')
            >>> overview = CloudDiscoveryOverview(commcell)
        """
        self._commcell = commcell
        self._cvpysdk_object = commcell._cvpysdk_object
        self._services = commcell._services
        self._update_response_ = commcell._update_response_

    # ------------------------------------------------------------------
    # Public API methods
    # ------------------------------------------------------------------

    def get_resource_summary(
        self,
        provider: int = 1,
        cloud_connection_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fetch the Overview resource summary from the ``Asset/Search`` API.

        Issues a POST to ``Asset/Search`` with ``rows=0`` so only the facets
        are returned, then extracts the protection-status and workload-type
        breakdowns.

        Args:
            provider: Integer provider enum value used for the ``Provider`` fq
                filter. Defaults to ``1`` (Azure).
            cloud_connection_name: Optional cloud connection name. When provided,
                an additional ``CloudConnectionName`` fq filter is applied so
                the summary is scoped to a single connection.

        Returns:
            Dict with the following keys:

            * ``"Total_Size"``                          — total count + byte sum
            * ``"ProtectionStatusSize_Protected"``      — Commvault-protected
            * ``"ProtectionStatusSize_Managed"``        — natively protected
            * ``"ProtectionStatusSize_NotProtected"``
            * ``"ProtectionStatusSize_Configured"``
            * ``"_protection_status_count"``            — ``{status_int: count}``
            * ``"WorkloadType"``                        — per-workload counts + sizes

        Raises:
            SDKException: If the API request fails or returns an error.

        Example::

            summary = overview.get_resource_summary(provider=2)
            total_count = (summary.get("Total_Size") or {}).get("count", 0)
        """
        url = self._services['GET_RESOURCES']
        payload = copy.deepcopy(ASSET_SEARCH_PAYLOAD)
        payload["searchParams"].append({"key": "fq", "value": f"Provider:{provider}"})

        if cloud_connection_name:
            payload["searchParams"].append(
                {"key": "fq", "value": f'CloudConnectionName:"{cloud_connection_name}"'}
            )

        facet = copy.deepcopy(FACET_JSON)
        ps_configured = AssetCVProtectionStatus.PROTECTION_CONFIGURED_COMMVAULT
        ps_protected = AssetCVProtectionStatus.PROTECTED
        facet["ProtectionStatusSize_Managed"]["q"] = (
            f"(ProtectionStatus:{ps_configured} OR ProtectionStatus:{ps_protected})"
            f" AND ProtectedBy:{PROVIDER_PROTECTED_BY_MAP.get(provider, provider)}"
        )
        payload["searchParams"].append({"key": "json.facet", "value": json.dumps(facet)})

        flag, response = self._cvpysdk_object.make_request('POST', url=url, payload=payload)

        if flag:
            if response.json():
                error_message = response.json().get('errorMessage')
                if error_message:
                    raise SDKException('Response', '102', error_message)
                facets = response.json().get('facets')
                if not isinstance(facets, dict):
                    raise SDKException('Response', '102')
                workload_facet = facets.get(WORKLOAD_TYPE_MAP) or {}
                return {
                    TOTAL_SIZE:                           facets.get(TOTAL_SIZE) or {},
                    PROTECTION_STATUS_SIZE_PROTECTED:     facets.get(PROTECTION_STATUS_SIZE_PROTECTED) or {},
                    PROTECTION_STATUS_SIZE_MANAGED:       facets.get(PROTECTION_STATUS_SIZE_MANAGED) or {},
                    PROTECTION_STATUS_SIZE_NOT_PROTECTED: facets.get(PROTECTION_STATUS_SIZE_NOT_PROTECTED) or {},
                    PROTECTION_STATUS_SIZE_CONFIGURED:    facets.get(PROTECTION_STATUS_SIZE_CONFIGURED) or {},
                    PROTECTION_STATUS_COUNT_MAP:          self._protection_status_count_map(facets),
                    WORKLOAD_TYPE_MAP:                    {
                        **workload_facet,
                        KUBERNETES_WORKLOAD:            facets.get(KUBERNETES_WORKLOAD) or {},
                        VM_WORKLOAD_WITHOUT_KUBERNETES: facets.get(VM_WORKLOAD_WITHOUT_KUBERNETES) or {},
                    },
                }
            raise SDKException('Response', '102')
        raise SDKException('Response', '101', self._update_response_(response.text))

    def get_monthly_cost_estimate(
        self,
        discovered_sizes: Optional[List[Dict[str, Any]]] = None,
        provider: Optional[str] = None,
    ) -> Dict[str, float]:
        """Get the monthly cost estimate from the ``Asset/TCO`` API.

        Args:
            discovered_sizes: Pre-built list in the format expected by the
                ``Asset/TCO`` endpoint::

                    [{"workloadType": "COMPUTE", "sizeInTB": 14.33}, ...]

                If ``None``, the API is called with an empty ``discoveredSizes``
                list (server uses its own discovered data).
            provider: Cloud provider string for the ``Asset/TCO`` payload (e.g.
                ``"AZURE"``, ``"AWS"``).  When ``None`` (default) the value from
                :data:`ASSET_TCO_PAYLOAD` is used (``"AZURE"``).

        Returns:
            Dict with keys ``native_total``, ``cv_total``, ``savings_amount``,
            ``savings_percent`` — all as floats.

        Raises:
            SDKException: If the API request fails or returns an error.

        Example::

            sizes = [{"workloadType": "COMPUTE", "sizeInTB": 14.33}]
            cost  = overview.get_monthly_cost_estimate(sizes, provider="AWS")
            print(cost["cv_total"])
        """
        url = self._services['GET_RESOURCE_TCO']

        payload = copy.deepcopy(ASSET_TCO_PAYLOAD)
        if discovered_sizes is not None:
            payload['discoveredSizes'] = discovered_sizes
        if provider is not None:
            payload['provider'] = provider

        flag, response = self._cvpysdk_object.make_request('POST', url=url, payload=payload)

        if flag:
            if response.json():
                error_message = response.json().get('errorMessage')
                if error_message:
                    raise SDKException('Response', '102', error_message)
                response_json = response.json()
                savings = response_json.get('savings') or {}
                return {
                    NATIVE_TOTAL:    float((response_json.get('nativeCost') or {}).get('total', 0.0)),
                    CV_TOTAL:        float((response_json.get('cvCost') or {}).get('total', 0.0)),
                    SAVINGS_AMOUNT:  float(savings.get('amount', 0.0)),
                    SAVINGS_PERCENT: float(savings.get('percent', 0.0)),
                }
            raise SDKException('Response', '102')
        raise SDKException('Response', '101', self._update_response_(response.text))

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _protection_status_count_map(facets: Dict[str, Any]) -> Dict[int, Dict[int, int]]:
        """Extract a ``{protection_status: {protected_by: count}}`` mapping from the facets dict.

        Categorisation rules:

        * PS 6, PB 6   → Protection Configured (Commvault)
        * PS 4/6, PB 1 → Azure Managed
        * PS 4/6, PB 2 → AWS Managed
        * PS 4, PB 6   → Protected (Commvault)

        Args:
            facets: The ``facets`` sub-dict from the ``Asset/Search`` response.

        Returns:
            Nested dict ``{protection_status_int: {protected_by_int: count}}``.
            When no ``ProtectedBy`` breakdown is present for a bucket, the
            protected_by key defaults to ``0``.
        """
        buckets = (facets.get("ProtectionStatus") or {}).get("buckets") or []
        mapping: Dict[int, Dict[int, int]] = {}
        for bucket in buckets:
            try:
                ps = int(bucket.get("val"))
            except (TypeError, ValueError):
                continue
            pb_buckets = (bucket.get("ProtectedBy") or {}).get("buckets") or []
            if pb_buckets:
                pb_map: Dict[int, int] = {}
                for pb_bucket in pb_buckets:
                    try:
                        pb_map[int(pb_bucket.get("val"))] = int(pb_bucket.get("count", 0))
                    except (TypeError, ValueError):
                        continue
                mapping[ps] = pb_map
            else:
                mapping[ps] = {0: int(bucket.get("count", 0))}
        return mapping
