Changelog
=========

.. _1.7.1:

``Release 1.7.1``
-----------------

`Features`
++++++++++
* Add possible typosquats list (Using `domain fuzzer <https://github.com/ics/domainfuzzer>`_)
* Add daily task to fuzz all constituency FQDNS

`Fixes`
+++++++
* Explicitly forbid changing the following organization fields from CP:
  ``is_sla``, ``mail_template``, ``group_id``, ``old_ID``,
  ``group``, ``group_id``
* Increase account activation expiry time to 72 hours

`Other`
+++++++
* Allow downloading deliverables by name
* Add Font Awesome icon framework for future use
* Disable SAVAPI AV scanner
* Disable message sending from distribution lists


.. _1.6.5:

``Release 1.6.5``
-----------------

`Features`
++++++++++
* Add download links for dynamic analysis
* Add BGP Ranking expert
* Add EC Reference Configuration expert
* Mark client for extended services (SLA)
* Admin can download deliverables

`Fixes`
+++++++
* Add SHA256 and SHA512 query keys to VirusTotal expert
* Extract zip archives and submit contents for analysis
  Zip archives encrypted with password 'infected' are also supported
* Fix validator
* Flatten deliverable endpoint responses

`Other`
+++++++
* Update VxStream Sandbox to 4.4.0
* Use KernelMode for all VMs
* Include more details in :ref:`organizations` endpoint examples


.. _1.5.4:

``Release 1.5.4``
-----------------

`Features`
++++++++++
* Add Two-factor authentication
* Report first-factor authentication as ``pre-authenticated`` when a
  second-factor is required
* Store all session data server-side

`Fixes`
+++++++
* Fixed URL scanner reports
* Encrypt distribution list message attachments
* Fix session timeout issues
* Don't use SQL query pools
* Code formatting cleanup

`Other`
+++++++
* Added kernel mode to all VMs.
* Updated AV scanner; Current engines: Avira, ClamAV, ESET, F-Prot, F-Secure


.. _1.4.0:

``Release 1.4.0``
-----------------

`Features`
++++++++++
* Add URL scanner (using VxStream sandbox)
* Add ``notes`` to vulnerabilities
* Add :attr:`~app.models.Permission.SLAACCOUNT` permission. Constituents with
  an SLA will have this bit turned on.
* Add ``My Account`` section

`Other`
+++++++
* Improve distribution lists tests
* Improve the :ref:`auth` documentation
* Add sample usage of ``API-Authorization`` header in :ref:`organizations`

.. _1.3.0:

``Release 1.3.0``
-----------------

`Features`
++++++++++

* Add web vulnerabilities module (a.k.a. Hall of Fame)
* Return URL of newly created resource when adding resources

`Other`
+++++++
* API docs are now separated by module
* Add versioning scheme details


.. _1.2.3:

``Release 1.2.3``
-----------------

`Features`
++++++++++

* Split CP documentation from DO.
* Create build and deployment system for CP documentation
* Update CP docs
* Use :http:statuscode:`422` HTTP status code for CP validation errors

`Fixes`
+++++++
* Limit CP samples query to current_user
* Remove deprecated endpoints from DO API

`Other`
+++++++
* Add more unit tests for CP endpoints
* Remove unused endpoints from DO and CP


.. _1.2.2:

``Release 1.2.2``
-----------------

`Features`
++++++++++

* Use :http:statuscode:`422` HTTP status code for API validation errors
* Replace authorization header with the generic API-Authorization
* Add endpoit to return HTML, BIN and PCAP reports for CP users

`Fixes`
+++++++
* Allow users to submit the same file multiple times
* Add confirmation dialog when deleting an organization;
  closes `#622 <https://trac.cert.europa.eu/ticket/622>`_

`Other`
+++++++
* Allow User model serialization
* Add more unit test for authentication endpoints


.. _1.2.1:

``Release 1.2.1``
-----------------

`Features`
++++++++++

* Add :attr:`~app.models.Permission.ADDCPACCOUNT` permission

`Fixes`
+++++++
* Add register/unregister CP accounts for constituent users
* Fix CP organization update
* Set rate limit for auth endpoints to 10req/s


.. _1.2.0:

``Release 1.2.0``
-----------------

`Features`
++++++++++
* Add ``file analysis`` endpoints for CP
* Require authentication for all CP endpoints
* Add relationship between User and Sample
* Add CP unregister option
* Add FMB (functional mailbox) marker for contact emails
* Add validation rules for contact and abuse emails
* Automatically try to cleanup unused emails

`Fixes`
+++++++
* Increase rate limit for admin endpoints to 50 req/s
* Set rate limit for CP to 30 req/s

`Other`
+++++++
* Add documentation for CP endpoints
  Customer portal endpoints are documented from customer perspective.
* Add savapi_client module documentation
* Update requirements
* Add VxStream tests
* Update unit tests


.. _1.1.1:

``Release 1.1.1``
-----------------

`Fixes`
+++++++
* `1c103ef <https://git.cert.europa.eu/?p=do-portal.git;a=commit;h=1c103ef>`_ Update tests
* 09e06a0 Update default test user password
* 45ba5ae Update test user creation
* 7277744 Fix permissions typo
* cc9479e Fix automatic role selection for users


.. _1.1.0:

``Release 1.1.0``
-----------------

`Features`
++++++++++
* Initial integration with VxStream Sandbox:

  * DO portal is using the ``VxStream Sandbox REST API`` to submit files
    for analysis and retrieve results;
  * Sandbox endpoints serve as upstream for CP (customer portal);
  * Available environments: Windows 7 x86, Windows 7 x64, Windows 8.1 x64,
    Windows 10 x64, Windows 7 x86 (Stealth), Windows 7 x64 (Stealth);
  * display analysis status and retrieve analysis summaries;
  * integrate the HTML report in the dynamic analysis tab;

* Add ability to create customer portal credentials for constituents;
* Allow authentication of users outside LDAP (constituents);
* Allow CP users to upload samples and submit for analysis;
* Implement ACL and granular permissions.
  For details see :class:`app.models.Permission`;
* Add mailing function with template capability;
* Refactor templates for malware analysis section;
* Add basic static analysis tools: metadata extraction, file identification;
* Add hexdump of file (first 1024 bytes for now);
* Calculate MD5, SHA-1, SHA-256, SHA-512 and CTPH hashes (a.k.a. fuzzy-hashes)
  of uploaded samples;
* Create API endpoints for sample submission and reports retrieval;
* Use a 64 character random string as API key;
* Save the audit log on disk (this is the fallback in case Splunk is down);
* Samples are uploaded to another disk mounted with the following options:
  noexec, nosuid, nodev
* Add ``DO-`` prefix to custom HTTP headers;

`Fixes`
+++++++
* Show errors messages and notifications from AbuseHelper;
* Show abuse emails when no contact emails where found;
* Remove colorpicker from distribution lists form;
* Change list encryption success message;
* Allow adding IP ranges, ASNs, Abuse E-mails and Contact E-mails when creating
  a new organization.

`Other`
+++++++
* Change the versioning scheme to major.minor.fix;
* Add automatic code linting;
* Update all 3rd party libraries to the latest stable version;
* Customize documentation template;
* Update documentation;


.. _1.0.1:

``Release 1.0.1``
-----------------

* Re-order main menu to fit DOs requirements;
* Display contact email on organization page if abuse e-mails are unavailable;
* Don't show augment sha-1 in investigation results;
* Show old IDs in organization list and edit page;
* Various API bug fixes.


.. _1.0.0:

``Release 1.0.0``
-----------------

Initial release
