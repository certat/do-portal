CREATE TABLE fody.autonomous_system_annotation (
    autonomous_system_annotation_id integer NOT NULL,
    asn bigint NOT NULL,
    annotation json NOT NULL
);
ALTER TABLE fody.autonomous_system_annotation OWNER TO do_portal;
CREATE SEQUENCE fody.autonomous_system_annotation_autonomous_system_annotation_i_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.autonomous_system_annotation_autonomous_system_annotation_i_seq OWNER TO do_portal;
ALTER SEQUENCE fody.autonomous_system_annotation_autonomous_system_annotation_i_seq OWNED BY public.autonomous_system_annotation.autonomous_system_annotation_id;
CREATE TABLE fody.contact (
    contact_id integer NOT NULL,
    firstname character varying(500) DEFAULT ''::character varying NOT NULL,
    lastname character varying(500) DEFAULT ''::character varying NOT NULL,
    tel character varying(500) DEFAULT ''::character varying NOT NULL,
    openpgp_fpr character varying(128) DEFAULT ''::character varying NOT NULL,
    email character varying(100) NOT NULL,
    comment text DEFAULT ''::text NOT NULL,
    organisation_id integer NOT NULL
);
ALTER TABLE fody.contact OWNER TO do_portal;
CREATE TABLE fody.contact_automatic (
    contact_automatic_id integer NOT NULL,
    firstname character varying(500) DEFAULT ''::character varying NOT NULL,
    lastname character varying(500) DEFAULT ''::character varying NOT NULL,
    tel character varying(500) DEFAULT ''::character varying NOT NULL,
    openpgp_fpr character varying(128) DEFAULT ''::character varying NOT NULL,
    email character varying(100) NOT NULL,
    comment text DEFAULT ''::text NOT NULL,
    import_source character varying(500) NOT NULL,
    import_time timestamp without time zone NOT NULL,
    organisation_automatic_id integer NOT NULL,
    CONSTRAINT automatic_templ_import_source_check CHECK (((import_source)::text <> ''::text))
);
ALTER TABLE fody.contact_automatic OWNER TO do_portal;
CREATE SEQUENCE fody.contact_automatic_contact_automatic_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.contact_automatic_contact_automatic_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.contact_automatic_contact_automatic_id_seq OWNED BY public.contact_automatic.contact_automatic_id;
CREATE SEQUENCE fody.contact_contact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.contact_contact_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.contact_contact_id_seq OWNED BY public.contact.contact_id;
CREATE TABLE fody.email_status (
    email character varying(100) NOT NULL,
    enabled boolean NOT NULL,
    added timestamp with time zone DEFAULT now() NOT NULL
);
ALTER TABLE fody.email_status OWNER TO do_portal;
CREATE TABLE fody.fqdn (
    fqdn_id integer NOT NULL,
    fqdn text NOT NULL,
    comment text DEFAULT ''::text NOT NULL
);
ALTER TABLE fody.fqdn OWNER TO do_portal;
CREATE TABLE fody.fqdn_annotation (
    fqdn_annotation_id integer NOT NULL,
    fqdn_id integer NOT NULL,
    annotation json NOT NULL
);
ALTER TABLE fody.fqdn_annotation OWNER TO do_portal;
CREATE SEQUENCE fody.fqdn_annotation_fqdn_annotation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.fqdn_annotation_fqdn_annotation_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.fqdn_annotation_fqdn_annotation_id_seq OWNED BY public.fqdn_annotation.fqdn_annotation_id;
CREATE TABLE fody.fqdn_automatic (
    fqdn_automatic_id integer NOT NULL,
    fqdn text NOT NULL,
    comment text DEFAULT ''::text NOT NULL,
    import_source character varying(500) NOT NULL,
    import_time timestamp without time zone NOT NULL,
    CONSTRAINT automatic_templ_import_source_check CHECK (((import_source)::text <> ''::text))
);
ALTER TABLE fody.fqdn_automatic OWNER TO do_portal;
CREATE SEQUENCE fody.fqdn_automatic_fqdn_automatic_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.fqdn_automatic_fqdn_automatic_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.fqdn_automatic_fqdn_automatic_id_seq OWNED BY public.fqdn_automatic.fqdn_automatic_id;
CREATE SEQUENCE fody.fqdn_fqdn_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.fqdn_fqdn_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.fqdn_fqdn_id_seq OWNED BY public.fqdn.fqdn_id;
CREATE TABLE fody.national_cert (
    national_cert_id integer NOT NULL,
    country_code character(2) NOT NULL,
    comment text DEFAULT ''::text NOT NULL,
    organisation_id integer NOT NULL
);
ALTER TABLE fody.national_cert OWNER TO do_portal;
CREATE TABLE fody.national_cert_automatic (
    national_cert_automatic_id integer NOT NULL,
    country_code character(2) NOT NULL,
    comment text DEFAULT ''::text NOT NULL,
    organisation_automatic_id integer NOT NULL,
    import_source character varying(500) NOT NULL,
    import_time timestamp without time zone NOT NULL,
    CONSTRAINT automatic_templ_import_source_check CHECK (((import_source)::text <> ''::text))
);
ALTER TABLE fody.national_cert_automatic OWNER TO do_portal;
CREATE SEQUENCE fody.national_cert_automatic_national_cert_automatic_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.national_cert_automatic_national_cert_automatic_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.national_cert_automatic_national_cert_automatic_id_seq OWNED BY public.national_cert_automatic.national_cert_automatic_id;
CREATE SEQUENCE fody.national_cert_national_cert_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.national_cert_national_cert_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.national_cert_national_cert_id_seq OWNED BY public.national_cert.national_cert_id;
CREATE TABLE fody.network (
    network_id integer NOT NULL,
    address cidr NOT NULL,
    comment text DEFAULT ''::text NOT NULL
);
ALTER TABLE fody.network OWNER TO do_portal;
CREATE TABLE fody.network_annotation (
    network_annotation_id integer NOT NULL,
    network_id integer NOT NULL,
    annotation json NOT NULL
);
ALTER TABLE fody.network_annotation OWNER TO do_portal;
CREATE SEQUENCE fody.network_annotation_network_annotation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.network_annotation_network_annotation_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.network_annotation_network_annotation_id_seq OWNED BY public.network_annotation.network_annotation_id;
CREATE TABLE fody.network_automatic (
    network_automatic_id integer NOT NULL,
    address cidr NOT NULL,
    comment text DEFAULT ''::text NOT NULL,
    import_source character varying(500) NOT NULL,
    import_time timestamp without time zone NOT NULL,
    CONSTRAINT automatic_templ_import_source_check CHECK (((import_source)::text <> ''::text))
);
ALTER TABLE fody.network_automatic OWNER TO do_portal;
CREATE SEQUENCE fody.network_automatic_network_automatic_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.network_automatic_network_automatic_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.network_automatic_network_automatic_id_seq OWNED BY public.network_automatic.network_automatic_id;
CREATE SEQUENCE fody.network_network_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.network_network_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.network_network_id_seq OWNED BY public.network.network_id;
CREATE TABLE fody.organisation (
    organisation_id integer NOT NULL,
    name character varying(500) NOT NULL,
    sector_id integer,
    comment text DEFAULT ''::text NOT NULL,
    ripe_org_hdl character varying(100) DEFAULT ''::character varying NOT NULL,
    ti_handle character varying(500) DEFAULT ''::character varying NOT NULL,
    first_handle character varying(500) DEFAULT ''::character varying NOT NULL
);
ALTER TABLE fody.organisation OWNER TO do_portal;
CREATE TABLE fody.organisation_annotation (
    organisation_annotation_id integer NOT NULL,
    organisation_id integer NOT NULL,
    annotation json NOT NULL
);
ALTER TABLE fody.organisation_annotation OWNER TO do_portal;
CREATE SEQUENCE fody.organisation_annotation_organisation_annotation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.organisation_annotation_organisation_annotation_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.organisation_annotation_organisation_annotation_id_seq OWNED BY public.organisation_annotation.organisation_annotation_id;
CREATE TABLE fody.organisation_automatic (
    organisation_automatic_id integer NOT NULL,
    name character varying(500) NOT NULL,
    sector_id integer,
    comment text DEFAULT ''::text NOT NULL,
    ripe_org_hdl character varying(100) DEFAULT ''::character varying NOT NULL,
    ti_handle character varying(500) DEFAULT ''::character varying NOT NULL,
    first_handle character varying(500) DEFAULT ''::character varying NOT NULL,
    import_source character varying(500) NOT NULL,
    import_time timestamp without time zone NOT NULL,
    CONSTRAINT automatic_templ_import_source_check CHECK (((import_source)::text <> ''::text))
);
ALTER TABLE fody.organisation_automatic OWNER TO do_portal;
CREATE SEQUENCE fody.organisation_automatic_organisation_automatic_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.organisation_automatic_organisation_automatic_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.organisation_automatic_organisation_automatic_id_seq OWNED BY public.organisation_automatic.organisation_automatic_id;
CREATE SEQUENCE fody.organisation_organisation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.organisation_organisation_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.organisation_organisation_id_seq OWNED BY public.organisation.organisation_id;
CREATE TABLE fody.organisation_to_asn (
    organisation_id integer NOT NULL,
    asn bigint NOT NULL
);
ALTER TABLE fody.organisation_to_asn OWNER TO do_portal;
CREATE TABLE fody.organisation_to_asn_automatic (
    organisation_automatic_id integer NOT NULL,
    asn bigint NOT NULL,
    import_source character varying(500) NOT NULL,
    import_time timestamp without time zone NOT NULL,
    CONSTRAINT automatic_templ_import_source_check CHECK (((import_source)::text <> ''::text))
);
ALTER TABLE fody.organisation_to_asn_automatic OWNER TO do_portal;
CREATE TABLE fody.organisation_to_fqdn (
    organisation_id integer NOT NULL,
    fqdn_id integer NOT NULL
);
ALTER TABLE fody.organisation_to_fqdn OWNER TO do_portal;
CREATE TABLE fody.organisation_to_fqdn_automatic (
    organisation_automatic_id integer NOT NULL,
    fqdn_automatic_id integer NOT NULL,
    import_source character varying(500) NOT NULL,
    import_time timestamp without time zone NOT NULL,
    CONSTRAINT automatic_templ_import_source_check CHECK (((import_source)::text <> ''::text))
);
ALTER TABLE fody.organisation_to_fqdn_automatic OWNER TO do_portal;
CREATE TABLE fody.organisation_to_network (
    organisation_id integer NOT NULL,
    network_id integer NOT NULL
);
ALTER TABLE fody.organisation_to_network OWNER TO do_portal;
CREATE TABLE fody.organisation_to_network_automatic (
    organisation_automatic_id integer NOT NULL,
    network_automatic_id integer NOT NULL,
    import_source character varying(500) NOT NULL,
    import_time timestamp without time zone NOT NULL,
    CONSTRAINT automatic_templ_import_source_check CHECK (((import_source)::text <> ''::text))
);
ALTER TABLE fody.organisation_to_network_automatic OWNER TO do_portal;
CREATE TABLE fody.sector (
    sector_id integer NOT NULL,
    name character varying(100) NOT NULL
);
ALTER TABLE fody.sector OWNER TO do_portal;
CREATE SEQUENCE fody.sector_sector_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE fody.sector_sector_id_seq OWNER TO do_portal;
ALTER SEQUENCE fody.sector_sector_id_seq OWNED BY public.sector.sector_id;
ALTER TABLE ONLY fody.autonomous_system_annotation ALTER COLUMN autonomous_system_annotation_id SET DEFAULT nextval('public.autonomous_system_annotation_autonomous_system_annotation_i_seq'::regclass);
ALTER TABLE ONLY fody.contact ALTER COLUMN contact_id SET DEFAULT nextval('public.contact_contact_id_seq'::regclass);
ALTER TABLE ONLY fody.contact_automatic ALTER COLUMN contact_automatic_id SET DEFAULT nextval('public.contact_automatic_contact_automatic_id_seq'::regclass);
ALTER TABLE ONLY fody.fqdn ALTER COLUMN fqdn_id SET DEFAULT nextval('public.fqdn_fqdn_id_seq'::regclass);
ALTER TABLE ONLY fody.fqdn_annotation ALTER COLUMN fqdn_annotation_id SET DEFAULT nextval('public.fqdn_annotation_fqdn_annotation_id_seq'::regclass);
ALTER TABLE ONLY fody.fqdn_automatic ALTER COLUMN fqdn_automatic_id SET DEFAULT nextval('public.fqdn_automatic_fqdn_automatic_id_seq'::regclass);
ALTER TABLE ONLY fody.national_cert ALTER COLUMN national_cert_id SET DEFAULT nextval('public.national_cert_national_cert_id_seq'::regclass);
ALTER TABLE ONLY fody.national_cert_automatic ALTER COLUMN national_cert_automatic_id SET DEFAULT nextval('public.national_cert_automatic_national_cert_automatic_id_seq'::regclass);
ALTER TABLE ONLY fody.network ALTER COLUMN network_id SET DEFAULT nextval('public.network_network_id_seq'::regclass);
ALTER TABLE ONLY fody.network_annotation ALTER COLUMN network_annotation_id SET DEFAULT nextval('public.network_annotation_network_annotation_id_seq'::regclass);
ALTER TABLE ONLY fody.network_automatic ALTER COLUMN network_automatic_id SET DEFAULT nextval('public.network_automatic_network_automatic_id_seq'::regclass);
ALTER TABLE ONLY fody.organisation ALTER COLUMN organisation_id SET DEFAULT nextval('public.organisation_organisation_id_seq'::regclass);
ALTER TABLE ONLY fody.organisation_annotation ALTER COLUMN organisation_annotation_id SET DEFAULT nextval('public.organisation_annotation_organisation_annotation_id_seq'::regclass);
ALTER TABLE ONLY fody.organisation_automatic ALTER COLUMN organisation_automatic_id SET DEFAULT nextval('public.organisation_automatic_organisation_automatic_id_seq'::regclass);
ALTER TABLE ONLY fody.sector ALTER COLUMN sector_id SET DEFAULT nextval('public.sector_sector_id_seq'::regclass);
COPY fody.contact_automatic (contact_automatic_id, firstname, lastname, tel, openpgp_fpr, email, comment, import_source, import_time, organisation_automatic_id) FROM stdin;
1162					abuse@colt.net		ripe	2019-01-18 15:57:04.748489	1303
1163					abuse.de@telefonica.com		ripe	2019-01-18 15:57:04.748489	1313
\.
COPY fody.network_automatic (network_automatic_id, address, comment, import_source, import_time) FROM stdin;
4800	2a04:40::/29		ripe	2019-01-18 15:57:04.748489
9401	176.96.105.0/24		ripe	2019-01-18 15:57:04.748489
\.
COPY fody.organisation_automatic (organisation_automatic_id, name, sector_id, comment, ripe_org_hdl, ti_handle, first_handle, import_source, import_time) FROM stdin;
1162	AT&T Global Network Services Nederland B.V.	\N		ORG-AGNS1-RIPE			ripe	2019-01-18 15:57:04.748489
2333	BlackHOST Abuse Team	\N		ABUS-BH			ripe	2019-01-18 15:57:04.748489
2334	Abuse contact role object ACRO18078-RIPE	\N		ACRO18078-RIPE			ripe	2019-01-18 15:57:04.748489
\.
COPY fody.organisation_to_asn_automatic (organisation_automatic_id, asn, import_source, import_time) FROM stdin;
1168	8437	ripe	2019-01-18 15:57:04.748489
1330	5404	ripe	2019-01-18 15:57:04.748489
1845	6883	ripe	2019-01-18 15:57:04.748489
2008	203501	ripe	2019-01-18 15:57:04.748489
\.
COPY fody.organisation_to_network_automatic (organisation_automatic_id, network_automatic_id, import_source, import_time) FROM stdin;
1591	5095	ripe	2019-01-18 15:57:04.748489
2108	5107	ripe	2019-01-18 15:57:04.748489
1820	5152	ripe	2019-01-18 15:57:04.748489
\.
ALTER TABLE ONLY fody.autonomous_system_annotation
    ADD CONSTRAINT autonomous_system_annotation_pkey PRIMARY KEY (autonomous_system_annotation_id);
ALTER TABLE ONLY fody.contact_automatic
    ADD CONSTRAINT contact_automatic_pkey PRIMARY KEY (contact_automatic_id);
ALTER TABLE ONLY fody.contact
    ADD CONSTRAINT contact_pkey PRIMARY KEY (contact_id);
ALTER TABLE ONLY fody.email_status
    ADD CONSTRAINT email_status_pkey PRIMARY KEY (email);
ALTER TABLE ONLY fody.fqdn_annotation
    ADD CONSTRAINT fqdn_annotation_pkey PRIMARY KEY (fqdn_annotation_id);
ALTER TABLE ONLY fody.fqdn_automatic
    ADD CONSTRAINT fqdn_automatic_fqdn_import_source_key UNIQUE (fqdn, import_source);
ALTER TABLE ONLY fody.fqdn_automatic
    ADD CONSTRAINT fqdn_automatic_pkey PRIMARY KEY (fqdn_automatic_id);
ALTER TABLE ONLY fody.fqdn
    ADD CONSTRAINT fqdn_pkey PRIMARY KEY (fqdn_id);
ALTER TABLE ONLY fody.national_cert_automatic
    ADD CONSTRAINT national_cert_automatic_pkey PRIMARY KEY (national_cert_automatic_id);
ALTER TABLE ONLY fody.national_cert
    ADD CONSTRAINT national_cert_pkey PRIMARY KEY (national_cert_id);
ALTER TABLE ONLY fody.network_annotation
    ADD CONSTRAINT network_annotation_pkey PRIMARY KEY (network_annotation_id);
ALTER TABLE ONLY fody.network_automatic
    ADD CONSTRAINT network_automatic_address_import_source_key UNIQUE (address, import_source);
ALTER TABLE ONLY fody.network_automatic
    ADD CONSTRAINT network_automatic_pkey PRIMARY KEY (network_automatic_id);
ALTER TABLE ONLY fody.network
    ADD CONSTRAINT network_pkey PRIMARY KEY (network_id);
ALTER TABLE ONLY fody.organisation_annotation
    ADD CONSTRAINT organisation_annotation_pkey PRIMARY KEY (organisation_annotation_id);
ALTER TABLE ONLY fody.organisation_automatic
    ADD CONSTRAINT organisation_automatic_pkey PRIMARY KEY (organisation_automatic_id);
ALTER TABLE ONLY fody.organisation
    ADD CONSTRAINT organisation_pkey PRIMARY KEY (organisation_id);
ALTER TABLE ONLY fody.organisation_to_asn_automatic
    ADD CONSTRAINT organisation_to_asn_automatic_pkey PRIMARY KEY (organisation_automatic_id, asn);
ALTER TABLE ONLY fody.organisation_to_asn
    ADD CONSTRAINT organisation_to_asn_pkey PRIMARY KEY (organisation_id, asn);
ALTER TABLE ONLY fody.organisation_to_fqdn_automatic
    ADD CONSTRAINT organisation_to_fqdn_automatic_pkey PRIMARY KEY (organisation_automatic_id, fqdn_automatic_id);
ALTER TABLE ONLY fody.organisation_to_fqdn
    ADD CONSTRAINT organisation_to_fqdn_pkey PRIMARY KEY (organisation_id, fqdn_id);
ALTER TABLE ONLY fody.organisation_to_network_automatic
    ADD CONSTRAINT organisation_to_network_automatic_pkey PRIMARY KEY (organisation_automatic_id, network_automatic_id);
ALTER TABLE ONLY fody.organisation_to_network
    ADD CONSTRAINT organisation_to_network_pkey PRIMARY KEY (organisation_id, network_id);
ALTER TABLE ONLY fody.sector
    ADD CONSTRAINT sector_pkey PRIMARY KEY (sector_id);
CREATE INDEX autonomous_system_annotation_asn_idx ON fody.autonomous_system_annotation USING btree (asn);
CREATE INDEX contact_automatic_organisation_idx ON fody.contact_automatic USING btree (organisation_automatic_id);
CREATE INDEX contact_organisation_idx ON fody.contact USING btree (organisation_id);
CREATE INDEX fqdn_annotation_fqdn_idx ON fody.fqdn_annotation USING btree (fqdn_id);
CREATE INDEX fqdn_fqdn_idx ON fody.fqdn USING btree (fqdn);
CREATE INDEX national_cert_automatic_country_code_idx ON fody.national_cert_automatic USING btree (country_code);
CREATE INDEX national_cert_country_code_idx ON fody.national_cert USING btree (country_code);
CREATE INDEX network_annotation_network_idx ON fody.network_annotation USING btree (network_id);
CREATE INDEX network_automatic_cidr_lower_idx ON fody.network_automatic USING btree (((host((network((address)::inet))::inet))::inet));
CREATE INDEX network_automatic_cidr_upper_idx ON fody.network_automatic USING btree (((host(broadcast((address)::inet)))::inet));
CREATE INDEX network_cidr_lower_idx ON fody.network USING btree (((host((network((address)::inet))::inet))::inet));
CREATE INDEX network_cidr_upper_idx ON fody.network USING btree (((host(broadcast((address)::inet)))::inet));
CREATE INDEX organisation_annotation_organisation_idx ON fody.organisation_annotation USING btree (organisation_id);
CREATE INDEX organisation_to_asn_asn_idx ON fody.organisation_to_asn USING btree (asn);
CREATE INDEX organisation_to_asn_automatic_asn_idx ON fody.organisation_to_asn_automatic USING btree (asn);
ALTER TABLE ONLY fody.contact_automatic
    ADD CONSTRAINT contact_automatic_organisation_automatic_id_fkey FOREIGN KEY (organisation_automatic_id) REFERENCES fody.organisation_automatic(organisation_automatic_id);
ALTER TABLE ONLY fody.contact
    ADD CONSTRAINT contact_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES fody.organisation(organisation_id);
ALTER TABLE ONLY fody.fqdn_annotation
    ADD CONSTRAINT fqdn_annotation_fqdn_id_fkey FOREIGN KEY (fqdn_id) REFERENCES fody.fqdn(fqdn_id);
ALTER TABLE ONLY fody.national_cert_automatic
    ADD CONSTRAINT national_cert_automatic_organisation_automatic_id_fkey FOREIGN KEY (organisation_automatic_id) REFERENCES fody.organisation_automatic(organisation_automatic_id);
ALTER TABLE ONLY fody.national_cert
    ADD CONSTRAINT national_cert_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES fody.organisation(organisation_id);
ALTER TABLE ONLY fody.network_annotation
    ADD CONSTRAINT network_annotation_network_id_fkey FOREIGN KEY (network_id) REFERENCES fody.network(network_id);
ALTER TABLE ONLY fody.organisation_annotation
    ADD CONSTRAINT organisation_annotation_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES fody.organisation(organisation_id);
ALTER TABLE ONLY fody.organisation_automatic
    ADD CONSTRAINT organisation_automatic_sector_id_fkey FOREIGN KEY (sector_id) REFERENCES fody.sector(sector_id);
ALTER TABLE ONLY fody.organisation
    ADD CONSTRAINT organisation_sector_id_fkey FOREIGN KEY (sector_id) REFERENCES fody.sector(sector_id);
ALTER TABLE ONLY fody.organisation_to_asn_automatic
    ADD CONSTRAINT organisation_to_asn_automatic_organisation_automatic_id_fkey FOREIGN KEY (organisation_automatic_id) REFERENCES fody.organisation_automatic(organisation_automatic_id);
ALTER TABLE ONLY fody.organisation_to_asn
    ADD CONSTRAINT organisation_to_asn_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES fody.organisation(organisation_id);
ALTER TABLE ONLY fody.organisation_to_fqdn_automatic
    ADD CONSTRAINT organisation_to_fqdn_automatic_fqdn_automatic_id_fkey FOREIGN KEY (fqdn_automatic_id) REFERENCES fody.fqdn_automatic(fqdn_automatic_id);
ALTER TABLE ONLY fody.organisation_to_fqdn_automatic
    ADD CONSTRAINT organisation_to_fqdn_automatic_organisation_automatic_id_fkey FOREIGN KEY (organisation_automatic_id) REFERENCES fody.organisation_automatic(organisation_automatic_id);
ALTER TABLE ONLY fody.organisation_to_fqdn
    ADD CONSTRAINT organisation_to_fqdn_fqdn_id_fkey FOREIGN KEY (fqdn_id) REFERENCES fody.fqdn(fqdn_id);
ALTER TABLE ONLY fody.organisation_to_fqdn
    ADD CONSTRAINT organisation_to_fqdn_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES fody.organisation(organisation_id);
ALTER TABLE ONLY fody.organisation_to_network_automatic
    ADD CONSTRAINT organisation_to_network_automati_organisation_automatic_id_fkey FOREIGN KEY (organisation_automatic_id) REFERENCES fody.organisation_automatic(organisation_automatic_id);
ALTER TABLE ONLY fody.organisation_to_network_automatic
    ADD CONSTRAINT organisation_to_network_automatic_network_automatic_id_fkey FOREIGN KEY (network_automatic_id) REFERENCES fody.network_automatic(network_automatic_id);
ALTER TABLE ONLY fody.organisation_to_network
    ADD CONSTRAINT organisation_to_network_network_id_fkey FOREIGN KEY (network_id) REFERENCES fody.network(network_id);
ALTER TABLE ONLY fody.organisation_to_network
    ADD CONSTRAINT organisation_to_network_organisation_id_fkey FOREIGN KEY (organisation_id) REFERENCES fody.organisation(organisation_id);
