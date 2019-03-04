Changelog
=========

.. _0.6.5:

``Release 0.6.5``
-----------------

`Features`
++++++++++
* Add download links for dynamic analysis
* Add SHA256 query option
* Add BGP Ranking expert
* Add EC Reference Configuration expert
* Add deliverables endpoints
* Add possible typosquats list (Using `domain fuzzer <https://github.com/ics/domainfuzzer>`_)

`Fixes`
+++++++
* Extract zip archives and submit contents for analysis
  Zip archives encrypted with password 'infected' are also supported
* Increase account activation expiry time to 72 hours
* Fix wrong URL mapping (/cp vs. /api)

`Other`
+++++++
* Update VxStream Sandbox to latest release
* Use KernelMode for all VMs
* Allow downloading deliverables by name


.. _0.5.0:

``Release 0.5.0``
-----------------

`Features`
++++++++++
* Add two-factor authentication. The second factor is a token computed by a
  Time-based One-time Password Algorithm from a shared secret key.
* Add URL scanner (dynamic analysis of URLs using VxStream Sandbox)

`Other`
+++++++
* AV update. Current engines: Avira, ClamAV, ESET, F-Prot, F-Secure


.. _0.4.0:

``Release 0.4.0``
-----------------

`Features`
++++++++++
* Add vulnerabilities module. This module will display vulnerabilities
  reported by 3rd parties and confirmed by CERT-EU. For details see
  :ref:`cp_rest_api`.

`Fixes`
+++++++
* Fix register/unregister new email (CP+)

`Other`
+++++++
* Add cookies authentication example


.. _0.3.2:

``Release 0.3.2``
-----------------

`Features`
++++++++++
* Add searching by SHA-1 hash in investigation
* Add search by e-mail in investigation

`Other`
+++++++
* Require IE Edge or higher
* Show browserhappy.com notification if client is outdated


.. _0.3.1:

``Release 0.3.1``
-----------------

`Fixes`
+++++++
* Bring back the bulk searching option
* Fix account unregister errors
* Fix authentication delay

`Other`
+++++++
* Created automatic build system. This will shorten the time between releases.
* Add :ref:`investigation_experts` doc page


.. _0.3.0:

``Release 0.3.0``
-----------------

`Features`
++++++++++
* Add register/unregister CP accounts for constituent users
* Add ``file analysis`` endpoints for CP
* Require authentication for all CP endpoints
* All samples are now associated to the user submitting them
* Add CP unregister option
* Add FMB (functional mailbox) marker for contact emails
* Add validation rules for contact and abuse emails
* Automatically try to cleanup unused emails

`Fixes`
+++++++
* Use :http:statuscode:`422` HTTP status code for API validation errors
* Replace authorization header with the generic API-Authorization
* Add endpoit to return VxStream HTML, BIN and PCAP reports for CP users
* Allow users to submit the same file multiple times
* Fix wrong reports permissions allowing users to retrieve all reports

`Other`
+++++++
* Set rate limit for /api endpoints to 30 req/s
* Set rate limit for /auth endpoints to 10 req/s
* Add documentation for CP endpoints
  Customer portal endpoints are documented from customer perspective
* Update requirements
* Add VxStream tests
* Update unit tests


.. _0.2.0:

``Release 0.2.0``
-----------------

First release available to customers (EC, EP, GSC, EUROPOL).

`Features`
++++++++++
* Initial integration with VxStream Sandbox:

  * CP portal is using the ``VxStream Sandbox REST API`` to submit files
    for analysis and retrieve results;
  * Sandbox endpoints serve as upstream for CP (customer portal);
  * Available environments: Windows 7 x86, Windows 7 x64, Windows 8.1 x64,
    Windows 10 x64, Windows 7 x86 (Stealth), Windows 7 x64 (Stealth);
  * display analysis status and retrieve analysis summaries;
  * integrate the HTML report in the dynamic analysis tab;

* Add ability to create customer portal credentials for constituents;
* Allow authentication of users outside LDAP (constituents);
* Allow CP users to upload samples and submit for analysis;
* Add basic static analysis tools: metadata extraction, file identification;
* Add hexdump of file (first 1024 bytes for now);
* Calculate MD5, SHA-1, SHA-256, SHA-512 and CTPH hashes (a.k.a. fuzzy-hashes)
  of uploaded samples;
* Create API endpoints for sample submission and reports retrieval;

`Fixes`
+++++++
* Show errors messages and notifications from AbuseHelper
* Allow adding IP ranges, ASNs, Abuse E-mails and Contact E-mails when creating
  a new organization.

`Other`
+++++++
* Add automatic code linting
* Customize documentation template
* Update documentation


.. _0.1.0:

``Release 0.1.0``
-----------------

* Add initial REST API endpoints
* Add web investigation


.. _0.0.1:

``Release 0.0.1``
-----------------

Initial deployment
