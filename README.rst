=======
CVPySDK
=======

CVPySDK is a Python Package for Commvault Software.

CVPySDK uses Commvault REST API to perform operations on a Commcell.


------------
Requirements
------------

- Python 2.7 or above
- **requests** Python package (https://pypi.python.org/pypi/requests/)
- **future** Python package (https://pypi.python.org/pypi/future)
- **xmltodict** Python package (https://pypi.python.org/pypi/xmltodict)
- Commvault Software v11 SP7 or later release with WebConsole installed


------------------
Installing CVPySDK
------------------

CVPySDK is available on GitHub (https://github.com/CommvaultEngg/cvpysdk).

It can be installed from source. After downloading, from within the ``cvpysdk`` directory, execute::

    python setup.py install


-------------
Using CVPySDK
-------------

Login to Commcell:
    >>> from cvpysdk.commcell import Commcell
    >>> commcell = Commcell(webconsole_hostname, commcell_username, commcell_password)

Print all clients:
    >>> print(commcell.clients)

Get a client:
	>>> client = commcell.clients.get(client_name)

Get an agent:
	>>> agent = client.agents.get(agent_name)

Get a backupset:
	>>> backupset = agent.backupsets.get(backupset_name)

Get a subclient:
	>>> subclient = backupset.subclients.get(subclient_name)

Run backup for a backupset:
	>>> job = backupset.backup()

Run backup for a subclient:
	>>> job = subclient.backup(backup_level, incremental_backup, incremental_level)

Browsing content of a subclient:
	>>> paths, dictionary = subclient.browse(path, show_deleted_files, vm_file_browse, vm_disk_browse)

Browsing content of a subclient in a specific time range:
	>>> paths, dictionary = subclient.browse_in_time(path, show_deleted_files, restore_index, from_date, to_date)

Searching a file in subclient backup content:
	>>> paths, dictionary = subclient.find(file_or_folder_name, show_deleted_files, restore_index)

Run restore in place job for a subclient:
	>>> job = subclient.restore_in_place(paths, overwrite, restore_data_and_acl)

Run restore out of place job for a subclient:
	>>> job = subclient.restore_out_of_place(client, destination_path, paths, overwrite, restore_data_and_acl)

Job Operations:
	>>> job.pause()		    # Suspends the Job
	>>> job.resume()	    # Resumes the Job
	>>> job.kill()		    # Kills the Job
	>>> job.status		    # Current Status the Job  --  Completed / Pending / Failed / .... / etc.
	>>> job.finished	    # Job finished or not     --  True / False
	>>> job.delay_reason	    # Job delay reason (if any)
	>>> job.pending_reason	    # Job pending reason (if any)


------------
Uninstalling
------------

On Windows, if CVPySDK was installed using an ``.exe`` or ``.msi``
installer, simply use the uninstall feature of "Add/Remove Programs" in the
Control Panel.

Alternatively, you can uninstall using the pip command::

	pip uninstall cvpysdk


---------------
Code of Conduct
---------------

Everyone interacting in the CVPySDK project's codebases, issue trackers,
chat rooms, and mailing lists is expected to follow the
`PyPA Code of Conduct`_.

.. _PyPA Code of Conduct: https://www.pypa.io/en/latest/code-of-conduct/
