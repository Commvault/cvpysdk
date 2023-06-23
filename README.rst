CVPySDK
=======

CVPySDK is a Python Package for Commvault Software.

CVPySDK uses REST APIs to perform CommCell operations.


Requirements
------------

- Python 3 and above
- `requests <https://pypi.python.org/pypi/requests/>`_ Python package
- `future <https://pypi.python.org/pypi/future>`_ Python package
- `xmltodict <https://pypi.python.org/pypi/xmltodict>`_ Python package
- Commvault Software v11 SP7 or later release with WebConsole installed


Installing CVPySDK
------------------

CVPySDK can be installed directly from PyPI using pip:

    >>> pip install cvpysdk


CVPySDK is available on GitHub `here <https://github.com/Commvault/cvpysdk>`_

It can also be installed from source.

After downloading, from within the ``cvpysdk`` directory, execute:

    >>> python setup.py install


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

Get an instance:
	>>> instance = agent.instances.get(instance_name)

Browsing content at instance level:
	>>> paths, dictionary = instance.browse(path='c:\\', show_deleted=True)

Browsing content of a instance in a specific time range:
	>>> paths, dictionary = instance.browse(path='f:\\', from_time='2010-04-19 02:30:00', to_time='2014-12-20 12:00:00')

Searching a file in instance backup content:
	>>> paths, dictionary = instance.find(file_name="*.csv")

Get a backupset:
	>>> backupset = instance.backupsets.get(backupset_name)

Run backup for a backupset:
	>>> job = backupset.backup()

Browsing content at backupset level:
	>>> paths, dictionary = backupset.browse(path='c:\\', show_deleted=True)

Browsing content of a backupset in a specific time range:
	>>> paths, dictionary = backupset.browse(path='f:\\', from_time='2010-04-19 02:30:00', to_time='2014-12-20 12:00:00')

Searching a file in backupset backup content:
	>>> paths, dictionary = backupset.find(file_name="*.csv")

Get a subclient:
	>>> subclient = backupset.subclients.get(subclient_name)

Run backup for a subclient:
	>>> job = subclient.backup(backup_level, incremental_backup, incremental_level)

Browsing content at subclient level:
	>>> paths, dictionary = subclient.browse(path='c:\\', show_deleted=True)

Browsing content of a subclient in a specific time range:
	>>> paths, dictionary = subclient.browse(path='f:\\', from_time='2010-04-19 02:30:00', to_time='2014-12-20 12:00:00')

Searching a file in subclient backup content:
	>>> paths, dictionary = subclient.find(file_name="*.txt")

Run restore in place job for a subclient:
	>>> job = subclient.restore_in_place(paths, overwrite, restore_data_and_acl)

Run restore out of place job for a subclient:
	>>> job = subclient.restore_out_of_place(client, destination_path, paths, overwrite, restore_data_and_acl)

Job Operations:
	>>> job.pause()		    # Suspends the Job
	>>> job.resume()	    # Resumes the Job
	>>> job.kill()		    # Kills the Job
	>>> job.status		    # Current Status the Job  --  Completed / Pending / Failed / .... / etc.
	>>> job.is_finished	    # Job finished or not     --  True / False
	>>> job.delay_reason	    # Job delay reason (if any)
	>>> job.pending_reason	    # Job pending reason (if any)


Uninstalling
------------

On Windows, if CVPySDK was installed using an ``.exe`` or ``.msi``
installer, simply use the uninstall feature of "**Add/Remove Programs**" in the
Control Panel.

Alternatively, you can uninstall using the **pip** command:

    >>> pip uninstall cvpysdk


Subclient Support
-----------------

Subclient operations are currently supported for the following Agents:

#. File System

#. Virtual Server

#. Cloud Apps

#. SQL Server

#. NAS / NDMP

#. SAP HANA

#. ORACLE

#. Sybase

#. SAP ORACLE

#. Exchange Database

#. Exchange Mailbox

#. Informix

#. Notes Database

#. MySQL

#. PostgreS

#. Big Data Apps


Documentation
-------------

To get started, please see the `full documentation for this library <https://commvault.github.io/cvpysdk/>`_


Contribution Guidelines
-----------------------

#. We welcome all the enhancements from everyone although we request the developer to follow some guidelines while interacting with the ``CVPySDK`` codebase.

#. Before adding any enhancements/bug-fixes, we request you to open an Issue first.

#. The SDK team will go over the Issue and notify if it is required or already been worked on.

#. If the Issue is approved, the contributor can then make the changes to their fork and open a pull request.

Pull Requests
*************
- CVPySDK has 2 active branches, namely:
    - **master**
    - **dev**

- The contributor should *Fork* the **dev** branch, and make their changes on top of it, and open a *Pull Request*
- The **master** branch will then be updated with the **dev** branch, once everything is verified

 **Note:** The SDK team will not accept any *Pull Requests* on the **master** branch

Coding Considerations
*********************

- All python code should be **PEP8** compliant.
- All changes should be consistent with the design of the SDK.
- The code should be formatted using **autopep8** with line-length set to **99** instead of default **79**.
- All changes and any new methods/classes should be properly documented.
- The doc strings should be of the same format as existing docs.

Code of Conduct
***************

Everyone interacting in the **CVPySDK** project's codebases, issue trackers,
chat rooms, and mailing lists is expected to follow the
`PyPA Code of Conduct`_.

.. _PyPA Code of Conduct: https://www.pypa.io/en/latest/code-of-conduct/


License
-------
**CVPySDK** and its contents are licensed under `Commvault License <https://raw.githubusercontent.com/Commvault/cvpysdk/master/LICENSE.txt>`_


About Commvault
---------------
.. image:: https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Commvault_logo.svg/320px-Commvault_logo.svg.png
    :align: center

|

`Commvault <https://www.commvault.com/>`_
(NASDAQ: CVLT) is a publicly traded data protection and information management software company headquartered in Tinton Falls, New Jersey.

It was formed in 1988 as a development group in Bell Labs, and later became a business unit of AT&T Network Systems. It was incorporated in 1996.

Commvault software assists organizations with data backup and recovery, cloud and infrastructure management, and retention and compliance.
