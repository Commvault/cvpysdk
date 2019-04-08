# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
# Copyright Commvault Systems, Inc.
# See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Module for performing operations on a Backupset for the **Virtual Server** Agent.

VSBackupset is the only class defined in this file.

VSBackupset:

    browse()                        -- browse the content of the backupset
    _process_browse_response()      -- retrieves the items from browse response
"""

from __future__ import unicode_literals

import time

from ..backupset import Backupset
from ..exception import SDKException

class VSBackupset(Backupset):
    """Derived class from Backupset Base class, representing a vs backupset,
            and to perform operations on that backupset."""



    def browse(self, *args, **kwargs):
        """Browses the content of the Backupset.

            Args:
                Dictionary of browse options:
                    Example:

                        browse({
                            'path': 'c:\\\\hello',

                            'show_deleted': True,

                            'from_time': '2014-04-20 12:00:00',

                            'to_time': '2016-04-21 12:00:00'
                        })

            Kwargs:
                Keyword argument of browse options:
                    Example:

                        browse(
                            path='c:\\hello',

                            show_deleted=True,

                            from_time='2014-04-20 12:00:00',

                            to_time='2016-04-21 12:00:00'
                        )

            Returns:
                (list, dict)
                    list    -   List of only the file, folder paths from the browse response

                    dict    -   Dictionary of all the paths with additional metadata retrieved
                    from browse operation
        """
        if args and isinstance(args[0], dict):
            options = args[0]
        else:
            options = kwargs

        options['operation'] = 'browse'
        options['retry_count'] = 0
        return self._do_browse(options)


    def  _process_browse_response(self, flag, response, options):
        """Retrieves the items from browse response.

                Args:
                    flag        (bool)  --  boolean, whether the response was success or not

                    response    (dict)  --  JSON response received for the request from the Server

                    options     (dict)  --  The browse options dictionary

                Returns:
                    list - List of only the file / folder paths from the browse response

                    dict - Dictionary of all the paths with additional metadata retrieved from browse

                Raises:
                    SDKException:
                        if failed to browse/search for content

                        if response is empty

                        if response is not success
                """
        paths_dict = {}
        paths = []
        result_set = None
        browse_result = None
        error_message = None
        options['retry_count'] = options['retry_count'] + 1

        if flag:
            response_json = response.json()
            if response_json and 'browseResponses' in response_json:
                _browse_responses = response_json['browseResponses']
                for browse_response in _browse_responses:
                    resp_type = browse_response['respType']
                    if 'messages' in browse_response:
                        message = browse_response['messages'][0]
                        error_message = message['errorMessage']
                        if resp_type == 2 or resp_type == 3 and 'No items found in the index, possibly index is being rebuilt' in \
                                error_message:
                            if options['retry_count'] <= 3:
                                time.sleep(180)
                                return self._do_browse(options)
                            else:
                                err = "Maximum browse attemps exhausted. Browse did not give full results"
                                raise Exception(err)
                    if "browseResult" in browse_response:
                        browse_result = browse_response['browseResult']
                        if 'dataResultSet' in browse_result:
                            result_set = browse_result['dataResultSet']
                            break
                if not browse_result:
                    if 'messages' in response_json['browseResponses'][0]:
                        message = response_json['browseResponses'][0]['messages'][0]
                        error_message = message['errorMessage']
                        raise SDKException('Backupset', '102', str(error_message))

                    else:
                        return [], {}

                if not result_set:
                    raise SDKException('Backupset', '110', "Failed to browse for subclient backup content")

                if 'all_versions' in options['operation']:
                    return self._process_browse_all_versions_response(result_set)

                for result in result_set:
                    name = result.get('displayName')
                    snap_display_name = result.get('name')

                    if 'path' in result:
                        path = result['path']
                    else:
                        path = '\\'.join([options['path'], name])

                    if 'modificationTime' in result and result['modificationTime'] > 0:
                        mod_time = time.localtime(result['modificationTime'])
                        mod_time = time.strftime('%d/%m/%Y %H:%M:%S', mod_time)
                    else:
                        mod_time = None

                    if 'file' in result['flags']:
                        if result['flags']['file'] is True:
                            file_or_folder = 'File'
                        else:
                            file_or_folder = 'Folder'
                    else:
                        file_or_folder = 'Folder'

                    if 'size' in result:
                        size = result['size']
                    else:
                        size = None

                    paths_dict[path] = {
                        'name': name,
                        'snap_display_name': snap_display_name,
                        'size': size,
                        'modified_time': mod_time,
                        'type': file_or_folder,
                        'advanced_data': result['advancedData']
                    }

                    paths.append(path)

                return paths, paths_dict


        else:
            raise SDKException('Response', '101', self._update_response_(response.text))
