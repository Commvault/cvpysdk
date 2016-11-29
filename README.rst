# --------------------------------------------------------------------------
# Copyright ©2016 Commvault Systems, Inc.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

=======
CVPySDK
=======

CVPySDK is a Python Package for Commvault Software.
CVPySDK uses REST API to perform operations on a Commcell.


------------
Requirements
------------

	.. Python 2.7
	.. Commvault Software v11 SP6 or later release


------------------
Installing CVPySDK
------------------

CVPySDK is available as a Windows executable distribution as well as Zip format source distribution.

The easiest way to install CVPySDK is via pip::

    pip install cvpysdk


Alternatively it can be installed from source. From within the ``cvpysdk`` directory, execute::

    python setup.py install


-------------
Using CVPySDK
-------------

Login to Commcell:

    >>> from cvpysdk import commcell
    >>> commcell_object = commcell.Commcell(commcell_name, commcell_username, commcell_password, port)

Print all clients:
    >>> print commcell_object.clients

Get a client:
	>>> client_object = commcell_object.clients.get(client_name)

Get an agent:
	>>> agent_object = client_object.agents.get(agent_name)

Get a backupset:
	>>> backupset_object = agent_object.backupsets.get(backupset_name)

Get a subclient:
	>>> subclient_object = backupset_object.subclients.get(subclient_name)

Run backup for a backupset:
	>>> job = backupset_object.backup()

Run backup for a subclient:
	>>> job = subclient_object.backup(backup_level, incremental_backup, incremental_level)

Browsing content of a subclient:
	>>> job = subclient_object.browse()

Browsing content of a subclient in a specific time range:
	>>> job = subclient_object.browse_in_time()

Run restore in place job for a subclient:
	>>> job = subclient_object.restore_in_place()

Run restore out of place job for a subclient:
	>>> job = subclient_object.restore_out_of_place()

Job Operations:
	>>> job.pause()			# Suspends the Job
	>>> job.resume()		# Resumes the Job
	>>> job.kill()			# Kills the Job
	>>> job.status			# Current Status the Job  --	Completed / Pending / Failed / .... / etc.
	>>> job.finished		# Job finished or not     --	True / False


------------
Uninstalling
------------

On Windows, if CVPySDK was installed using an ``.exe`` or ``.msi``
installer, simply use the uninstall feature of "Add/Remove Programs" in the
Control Panel.

Alternatively, you can uninstall using the pip command.

	pip uninstall cvpysdk


---------------
Code of Conduct
---------------

Everyone interacting in the CVPySDK project's codebases, issue trackers,
chat rooms, and mailing lists is expected to follow the
`PyPA Code of Conduct`_.

.. _PyPA Code of Conduct: https://www.pypa.io/en/latest/code-of-conduct/
