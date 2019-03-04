CIMBL/CITAR/Advisories/etc. Distribution Tool
=============================================

1) Mailing Lists Management:
    a) ability to manage multiple lists recipients (and their PGP keys)
    b) ability to define sending rules per list (encryption or not, products applicable for the list - e.g. CIMBL, etc.)
    c) full traceback capability - who changed what in the mailing lists

2) Automation:
    a) package creation - including the required files, mail body, etc. for various mailing lists, and various products
    b) encrypting mails according to the various mailing lists
    c) encrypting with hidden recipients (option)
    d) sending mails

3) Logging:
    a) full logging of all system activities
    b) full logging of all e-mails sent (who sent, to whom, what was sent, keys used to encrypt, etc.)

4) User Management:
    a) individual identifiable users of the system
    b) various access rights (e.g. right to sent emails, right to manage the lists, right to view logs)

5) Integration:
    a) integration with the key server,
    b) integration with CTI (if useful for CIMBL)
    c) integration with DeepSight

6) External Access (optional/future):
    a) ability for external customers to sign-up for specific products
    b) ability to filter specific products (e.g. only specific DeepSight advisories)


Notes:
------
Flask-JsonSchema is not actively maintained.To use format validators you need to patch it.