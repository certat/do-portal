--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.17
-- Dumped by pg_dump version 11.7 (Debian 11.7-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: epplication
--

INSERT INTO public.tag (id, name, color) VALUES (1, 'config', '#ffffff');
INSERT INTO public.tag (id, name, color) VALUES (4, 'run', '#bbffbb');


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: epplication
--

SELECT pg_catalog.setval('public.tag_id_seq', 4, true);


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.17
-- Dumped by pg_dump version 11.7 (Debian 11.7-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: branch; Type: TABLE DATA; Schema: public; Owner: epplication
--

INSERT INTO public.branch (id, name) VALUES (1, 'master');


--
-- Name: branch_id_seq; Type: SEQUENCE SET; Schema: public; Owner: epplication
--

SELECT pg_catalog.setval('public.branch_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.17
-- Dumped by pg_dump version 11.7 (Debian 11.7-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: test; Type: TABLE DATA; Schema: public; Owner: epplication
--

INSERT INTO public.test (id, name, branch_id) VALUES (4, 'login', 1);
INSERT INTO public.test (id, name, branch_id) VALUES (6, 'logout', 1);
INSERT INTO public.test (id, name, branch_id) VALUES (8, 'create organization', 1);
INSERT INTO public.test (id, name, branch_id) VALUES (9, 'create contact', 1);
INSERT INTO public.test (id, name, branch_id) VALUES (7, 'test portal', 1);
INSERT INTO public.test (id, name, branch_id) VALUES (10, 'create membership', 1);
INSERT INTO public.test (id, name, branch_id) VALUES (11, 'create RIPE handle', 1);
INSERT INTO public.test (id, name, branch_id) VALUES (5, 'do-config', 1);


--
-- Name: test_id_seq; Type: SEQUENCE SET; Schema: public; Owner: epplication
--

SELECT pg_catalog.setval('public.test_id_seq', 11, true);


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.17
-- Dumped by pg_dump version 11.7 (Debian 11.7-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: test_tag; Type: TABLE DATA; Schema: public; Owner: epplication
--

INSERT INTO public.test_tag (id, test_id, tag_id) VALUES (20, 7, 4);
INSERT INTO public.test_tag (id, test_id, tag_id) VALUES (22, 5, 1);


--
-- Name: test_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: epplication
--

SELECT pg_catalog.setval('public.test_tag_id_seq', 22, true);


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.17
-- Dumped by pg_dump version 11.7 (Debian 11.7-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: step; Type: TABLE DATA; Schema: public; Owner: epplication
--

INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (110, 'password', 3, true, false, '1', 5, 'VarVal', '{"value":"Bla12345%","variable":"password","global":0}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (224, 'set db_username', 9, true, false, '1', 5, 'VarVal', '{"value":"do_portal","variable":"db_username","global":0}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (223, 'set db_database', 8, true, false, '1', 5, 'VarVal', '{"variable":"db_database","global":0,"value":"do_portal"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (222, 'set db_port', 7, true, false, '1', 5, 'VarVal', '{"global":0,"variable":"db_port","value":"5432"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (236, 'set db_host', 6, true, false, '1', 5, 'VarVal', '{"global":0,"value":"portal-db","variable":"db_host"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (203, 'sleep', 3, true, false, '1', 10, 'Script', '{"command":"sleep 3","var_stdout":"script_response"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (243, 'create random ripe_org identifier', 3, true, false, '1', 11, 'VarRand', '{"variable":"ripe_org","rand":"d{3}[A-Z]{3}[a-z]{3}"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (220, 'filter contact names', 4, true, false, '1', 10, 'SeleniumInput', '{"selector":".ui-grid-filter-input-0","locator":"css","identifier":"selenium","input":"[% contact_name %]"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (226, 'connect to backend DB', 1, true, false, '1', 11, 'DBConnect', '{"password":"[% db_password %]","host":"[% db_host %]","database":"[% db_database %]","username":"[% db_username %]","port":"[% db_port %]"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (107, 'set host', 1, true, false, '1', 5, 'VarVal', '{"global":0,"variable":"host","value":"http://portal-frontend:8081"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (109, 'set username', 2, true, false, '1', 5, 'VarVal', '{"value":"master@master.master","variable":"username","global":0}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (122, 'goto login page', 2, true, false, '1', 4, 'SeleniumRequest', '{"url":"[%host%]/#!/login","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (200, 'request Contacts page', 2, true, false, '1', 10, 'SeleniumClick', '{"selector":"Contacts","locator":"link_text","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (123, 'get page content', 3, true, false, '1', 4, 'SeleniumContent', '{"variable":"selenium_content","content_type":"body_text","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (124, 'check "Login" text exists', 4, true, false, '1', 4, 'VarCheckRegExp', '{"modifiers":"xms","value":"[%selenium_content%]","regexp":"Login"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (201, 'sleep', 1, true, false, '1', 10, 'Script', '{"var_stdout":"script_response","command":"sleep 3"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (121, 'connect to portal', 1, true, false, '1', 4, 'SeleniumConnect', '{"port":"4444","host":"epplication-selenium","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (125, 'check "Lost Password" text exists', 5, true, false, '1', 4, 'VarCheckRegExp', '{"modifiers":"xms","value":"[%selenium_content%]","regexp":"Lost\\sPassword\\?"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (211, 'select role', 11, true, false, '1', 10, 'SeleniumJS', '{"javascript":"js_select_helper(0,''Administrator Organisation'',''#membership-details-1'');","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (204, 'debug', 5, true, false, '1', 10, 'SeleniumContent', '{"content_type":"body_text","identifier":"selenium","variable":"selenium_content"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (127, 'enter username', 6, true, false, '1', 4, 'SeleniumInput', '{"input":"[%username%]","selector":"email","locator":"name","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (218, 'js_select_helper', 2, true, false, '1', 7, 'Multiline', '{"global":0,"value":"window.js_select_helper = function(index, label, parent_selector) {\r\n  var selector = typeof parent_selector !== ''undefined'' ? parent_selector+'' '' : '''';\r\n  selector = selector + ''select'';\r\n  var select = document.querySelectorAll(selector)[index];\r\n  var options = select.querySelectorAll(''option'');\r\n  var value;\r\n  for (let o of options) {\r\n    if (o.label === label) { value = o.value; }\r\n  }\r\n  select.value = value;\r\n  var evt = document.createEvent(\"HTMLEvents\");\r\n  evt.initEvent(\"change\", false, true);\r\n  select.dispatchEvent(evt);\r\n};","variable":"js_select_helper"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (202, 'click existing contact', 7, true, false, '1', 10, 'SeleniumClick', '{"selector":"[% contact_name %]","locator":"link_text","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (208, 'sleep', 8, true, false, '1', 10, 'Script', '{"var_stdout":"script_response","command":"sleep 3"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (209, 'click add-membership button', 9, true, false, '1', 10, 'SeleniumClick', '{"locator":"id","identifier":"selenium","selector":"add-membership"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (210, 'sleep', 10, true, false, '1', 10, 'Script', '{"var_stdout":"script_response","command":"sleep 3"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (128, 'enter password', 7, true, false, '1', 4, 'SeleniumInput', '{"identifier":"selenium","locator":"name","selector":"password","input":"[%password%]"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (213, 'save membership', 13, true, false, '1', 10, 'SeleniumClick', '{"selector":"#membership-details-1 .save-membership","identifier":"selenium","locator":"css"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (205, 'debug', 14, true, false, '1', 10, 'PrintVars', '{"filter":""}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (216, 'check created user exists', 6, true, false, '1', 10, 'VarCheckRegExp', '{"modifiers":"xms","regexp":"[% contact_name %]","value":"[% selenium_content %]"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (212, 'select org', 12, true, false, '1', 10, 'SeleniumJS', '{"identifier":"selenium","javascript":"js_select_helper(1,''[%parent_org%]'',''#membership-details-1'');"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (207, 'create membership', 9, true, false, '1', 7, 'SubTest', '{"subtest_id":"10"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (133, 'selenium disconnect', 4, true, false, '1', 6, 'SeleniumDisconnect', '{"identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (237, 'create RIPE handle', 2, true, false, '1', 11, 'DB', '{"sql":"SELECT ripe_org_hdl FROM fody.organisation;","var_result":"db_response"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (234, 'check "Lost Password" text exists', 3, true, false, '1', 6, 'VarCheckRegExp', '{"modifiers":"xms","value":"[%selenium_content%]","regexp":"Lost\\sPassword\\?"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (230, 'create RIPE handle', 17, true, false, '1', 7, 'SubTest', '{"subtest_id":"11"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (129, 'click login button', 8, true, false, '1', 4, 'SeleniumClick', '{"selector":"//button[@type=''submit'' and contains(., \"Login\")]","identifier":"selenium","locator":"xpath"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (131, 'check "My Account" text exists', 11, true, false, '1', 4, 'VarCheckRegExp', '{"modifiers":"xms","value":"[%selenium_content%]","regexp":"My\\sAccount"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (130, 'get page content', 10, true, false, '1', 4, 'SeleniumContent', '{"variable":"selenium_content","content_type":"body_text","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (132, 'sleep', 9, true, false, '1', 4, 'Script', '{"command":"sleep 3","var_stdout":"script_response"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (108, 'set rest headers', 4, true, false, '1', 5, 'VarVal', '{"global":0,"value":"{ \"Content-Type\":\"application/json; charset=utf-8\", \"Accept\": \"application/json\"}","variable":"rest_headers_default"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (135, 'login', 1, true, false, '1', 7, 'SubTest', '{"subtest_id":"4"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (188, 'create random org name', 15, true, false, '1', 7, 'VarRand', '{"rand":"[a-z]{5}","variable":"org_name"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (189, 'create random org name', 13, true, false, '1', 7, 'VarRand', '{"rand":"[a-z]{5}","variable":"org_name"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (197, 'inject js_select_helper function', 3, true, false, '1', 7, 'SeleniumJS', '{"javascript":"[%js_select_helper%]","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (245, 'query organisation_automatic_id', 7, true, false, '1', 11, 'VarQueryPath', '{"var_result":"organisation_automatic_id","query_path":"//organisation_automatic_id","input":"[% db_response %]"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (167, 'create contact', 8, true, false, '1', 7, 'SubTest', '{"subtest_id":"9"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (143, 'create org', 6, true, false, '1', 7, 'SubTest', '{"subtest_id":"8"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (231, 'click login button', 1, true, false, '1', 6, 'SeleniumClick', '{"identifier":"selenium","locator":"xpath","selector":"//a[contains(., \"Logout (\")]"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (155, 'request Contacts page', 1, true, false, '1', 9, 'SeleniumClick', '{"selector":"Contacts","locator":"link_text","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (233, 'get page content', 2, true, false, '1', 6, 'SeleniumContent', '{"identifier":"selenium","variable":"selenium_content","content_type":"body_text"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (156, 'click "New Contact" link', 2, true, false, '1', 9, 'SeleniumClick', '{"identifier":"selenium","locator":"link_text","selector":"New Contact"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (225, 'set db_password', 10, true, false, '1', 5, 'VarVal', '{"global":0,"variable":"db_password","value":"do_portal"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (185, 'set parent_org', 10, true, false, '1', 7, 'VarVal', '{"variable":"parent_org","value":"[%org_name%]_abbreviation","global":0}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (182, 'create org', 12, true, false, '1', 7, 'SubTest', '{"subtest_name":"create organization","subtest_id":"8"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (187, 'create random org name', 11, true, false, '1', 7, 'VarRand', '{"rand":"[a-z]{5}","variable":"org_name"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (159, 'sleep', 3, true, false, '1', 9, 'Script', '{"var_stdout":"script_response","command":"sleep 3"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (164, 'click "Save" link', 8, true, false, '1', 9, 'SeleniumClick', '{"selector":"create-user","identifier":"selenium","locator":"id"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (160, 'get page content', 10, true, false, '1', 9, 'SeleniumContent', '{"variable":"selenium_content","content_type":"body_text","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (163, 'check "Delete" text exists', 11, true, false, '1', 9, 'VarCheckRegExp', '{"modifiers":"xms","value":"[%selenium_content%]","regexp":"Delete"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (157, 'enter email', 4, true, false, '1', 9, 'SeleniumInput', '{"locator":"xpath","identifier":"selenium","input":"[%contact_name%]@asdf.com","selector":"//input[@placeholder=\"Email\"]"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (162, 'select role', 6, true, false, '1', 9, 'SeleniumJS', '{"identifier":"selenium","javascript":"js_select_helper(0, ''Privat'');"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (158, 'enter name', 5, true, false, '1', 9, 'SeleniumInput', '{"identifier":"selenium","locator":"xpath","selector":"//input[@placeholder=\"Name\"]","input":"[%contact_name%]"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (183, 'create org', 14, true, false, '1', 7, 'SubTest', '{"subtest_name":"create organization","subtest_id":"8"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (184, 'create org', 16, true, false, '1', 7, 'SubTest', '{"subtest_name":"create organization","subtest_id":"8"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (154, 'create random org name', 4, true, false, '1', 7, 'VarRand', '{"rand":"[a-z]{5}","variable":"org_name"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (166, 'create random contact name', 7, true, false, '1', 7, 'VarRand', '{"variable":"contact_name","rand":"[a-z]{5}"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (177, 'set parent_org', 5, true, false, '1', 7, 'VarVal', '{"variable":"parent_org","global":0,"value":"[%root_org%]"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (175, 'select org', 7, true, false, '1', 9, 'SeleniumJS', '{"javascript":"js_select_helper(1, ''[%org_name%]_abbreviation'');","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (165, 'sleep', 9, true, false, '1', 9, 'Script', '{"command":"sleep 3","var_stdout":"script_response"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (176, 'set root_org', 5, true, false, '1', 5, 'VarVal', '{"variable":"root_org","value":"Austrian Energy CERT","global":1}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (139, 'click "New Organization" link', 3, true, false, '1', 8, 'SeleniumClick', '{"selector":"New Organization","locator":"link_text","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (244, 'check org id', 8, true, false, '1', 11, 'VarCheckRegExp', '{"regexp":"\\d+","value":"[%organisation_automatic_id%]","modifiers":"xms"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (241, 'create ripe_org contact', 9, true, false, '1', 11, 'DB', '{"sql":"insert into fody.contact_automatic (firstname, lastname, email, import_source, import_time, organisation_automatic_id) values (''firstname_[%ripe_org%]'', ''lastname_[%ripe_org%]'', ''email@ripe_org_[%ripe_org%].at'', ''ripe'', NOW(), [%organisation_automatic_id%]);","var_result":"db_response"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (137, 'logout', 18, true, false, '1', 7, 'SubTest', '{"subtest_id":"6"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (145, 'enter org abbreviation', 6, true, false, '1', 8, 'SeleniumInput', '{"selector":"//input[@placeholder=\"Abbreviation\"]","input":"[%org_name%]_abbreviation","identifier":"selenium","locator":"xpath"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (144, 'enter org name', 7, true, false, '1', 8, 'SeleniumInput', '{"input":"[%org_name%]_name","selector":"//input[@placeholder=\"Name\"]","locator":"xpath","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (141, 'sleep', 9, true, false, '1', 8, 'Script', '{"var_stdout":"script_response","command":"sleep 3"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (151, 'get page content', 10, true, false, '1', 8, 'SeleniumContent', '{"variable":"selenium_content","content_type":"body_text","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (152, 'check "No memberships available." text exists', 12, true, false, '1', 8, 'VarCheckRegExp', '{"value":"[%selenium_content%]","modifiers":"xms","regexp":"No\\smemberships\\savailable\\."}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (153, 'check "org_name" text exists', 11, true, false, '1', 8, 'VarCheckRegExp', '{"regexp":"Name:\\s[%org_name%]_name","value":"[%selenium_content%]","modifiers":"xms"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (148, 'click "Create" link', 8, true, false, '1', 8, 'SeleniumClick', '{"selector":"//button[contains(., \"Create\")]","identifier":"selenium","locator":"xpath"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (147, 'sleep', 4, true, false, '1', 8, 'Script', '{"var_stdout":"script_response","command":"sleep 3"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (140, 'select parent org', 5, true, false, '1', 8, 'SeleniumJS', '{"identifier":"selenium","javascript":"js_select_helper(0,''[%parent_org%]'');"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (246, 'sleep', 1, true, false, '1', 8, 'Script', '{"var_stdout":"script_response","command":"sleep 3"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (227, 'disconnect from backend DB', 10, true, false, '1', 11, 'DBDisconnect', '{}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (264, 'submit new ripe hdl', 23, true, false, '1', 11, 'SeleniumClick', '{"locator":"id","selector":"submit-add-ripe_hdl","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (262, 'add ripe_org_hdl to org', 11, true, true, '1', 11, 'Comment', '{"comment":"."}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (248, 'set ripe_org_hdl', 4, true, false, '1', 11, 'VarVal', '{"global":1,"variable":"ripe_org_hdl","value":"ripe_org_[%ripe_org%]"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (240, 'select organisation_automatic_id', 6, true, false, '1', 11, 'DB', '{"var_result":"db_response","sql":"SELECT organisation_automatic_id FROM fody.organisation_automatic WHERE ripe_org_hdl = ''[%ripe_org_hdl%]'';"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (239, 'create org', 5, true, false, '1', 11, 'DB', '{"sql":"insert into fody.organisation_automatic (name, ripe_org_hdl, import_source, import_time) values (''name_[%ripe_org%]'', ''[%ripe_org_hdl%]'', ''ripe'', NOW());","var_result":"db_response"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (249, 'request Organizations page', 2, true, false, '1', 8, 'SeleniumClick', '{"locator":"link_text","identifier":"selenium","selector":"Organizations"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (265, 'sleep', 24, true, false, '1', 11, 'Script', '{"var_stdout":"script_response","command":"sleep 1"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (266, 'get selenium content', 25, true, false, '1', 11, 'SeleniumContent', '{"variable":"selenium_content","content_type":"body_text","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (253, 'p', 27, true, false, '1', 11, 'PrintVars', '{"filter":""}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (250, 'request Organizations page', 12, true, false, '1', 11, 'SeleniumClick', '{"locator":"link_text","identifier":"selenium","selector":"Organizations"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (267, 'check ripe_org has been added', 26, true, false, '1', 11, 'VarCheckRegExp', '{"modifiers":"xms","value":"[%selenium_content%]","regexp":"[%ripe_org_hdl%]"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (258, 'get selenium content', 20, true, false, '1', 11, 'SeleniumContent', '{"variable":"selenium_content","content_type":"body_text","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (260, 'sleep', 19, true, false, '1', 11, 'Script', '{"var_stdout":"script_response","command":"sleep 3"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (252, 'check "org_name" text exists', 17, true, false, '1', 11, 'VarCheckRegExp', '{"regexp":"Name:\\s[%org_name%]_name","value":"[%selenium_content%]","modifiers":"xms"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (251, 'click "org_name" link', 14, true, false, '1', 11, 'SeleniumClick', '{"identifier":"selenium","locator":"link_text","selector":"[%org_name%]_name"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (254, 'sleep', 13, true, false, '1', 11, 'Script', '{"var_stdout":"script_response","command":"sleep 3"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (255, 'click "edit" link', 18, true, false, '1', 11, 'SeleniumClick', '{"locator":"link_text","selector":"edit","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (257, 'get selenium content', 16, true, false, '1', 11, 'SeleniumContent', '{"variable":"selenium_content","content_type":"body_text","identifier":"selenium"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (256, 'sleep', 15, true, false, '1', 11, 'Script', '{"var_stdout":"script_response","command":"sleep 3"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (259, 'check ripe_org input field exists', 21, true, false, '1', 11, 'VarCheckRegExp', '{"regexp":"Add\\ RIPE\\ organization\\ handle","value":"[%selenium_content%]","modifiers":"xms"}');
INSERT INTO public.step (id, name, "position", active, highlight, condition, test_id, type, parameters) VALUES (263, 'enter ripe_org_hdl', 22, true, false, '1', 11, 'SeleniumInput', '{"input":"[%ripe_org_hdl%]","selector":"add-ripe-handle","locator":"id","identifier":"selenium"}');


--
-- Name: step_id_seq; Type: SEQUENCE SET; Schema: public; Owner: epplication
--

SELECT pg_catalog.setval('public.step_id_seq', 267, true);


--
-- PostgreSQL database dump complete
--

