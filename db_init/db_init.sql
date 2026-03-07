--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4 (Debian 15.4-2.pgdg120+1)
-- Dumped by pg_dump version 15.4 (Debian 15.4-2.pgdg120+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin; Type: TABLE; Schema: public; Owner: shop
--

CREATE TABLE public.admin (
    id integer NOT NULL,
    fullnamead character varying(100),
    gmail character varying(100),
    usernamead character varying(100),
    password character varying(100)
);


ALTER TABLE public.admin OWNER TO shop;

--
-- Name: admin_id_seq; Type: SEQUENCE; Schema: public; Owner: shop
--

CREATE SEQUENCE public.admin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.admin_id_seq OWNER TO shop;

--
-- Name: admin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shop
--

ALTER SEQUENCE public.admin_id_seq OWNED BY public.admin.id;


--
-- Name: cart_item; Type: TABLE; Schema: public; Owner: shop
--

CREATE TABLE public.cart_item (
    id integer NOT NULL,
    user_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity integer,
    total_price numeric(15,0) NOT NULL
);


ALTER TABLE public.cart_item OWNER TO shop;

--
-- Name: cart_item_id_seq; Type: SEQUENCE; Schema: public; Owner: shop
--

CREATE SEQUENCE public.cart_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cart_item_id_seq OWNER TO shop;

--
-- Name: cart_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shop
--

ALTER SEQUENCE public.cart_item_id_seq OWNED BY public.cart_item.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: shop
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    user_id integer NOT NULL,
    total_amount numeric(15,0) NOT NULL,
    payment_method character varying(50),
    status character varying(50),
    bank_name character varying(100),
    bank_account character varying(50),
    bank_account_name character varying(100),
    transfer_note character varying(255),
    paid_at timestamp without time zone,
    created_at timestamp without time zone
);


ALTER TABLE public.orders OWNER TO shop;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: shop
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO shop;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shop
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: otp_register; Type: TABLE; Schema: public; Owner: shop
--

CREATE TABLE public.otp_register (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    otp_code character varying(10) NOT NULL,
    created_at timestamp without time zone,
    expire_at timestamp without time zone NOT NULL,
    is_verified boolean
);


ALTER TABLE public.otp_register OWNER TO shop;

--
-- Name: otp_register_id_seq; Type: SEQUENCE; Schema: public; Owner: shop
--

CREATE SEQUENCE public.otp_register_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.otp_register_id_seq OWNER TO shop;

--
-- Name: otp_register_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shop
--

ALTER SEQUENCE public.otp_register_id_seq OWNED BY public.otp_register.id;


--
-- Name: product; Type: TABLE; Schema: public; Owner: shop
--

CREATE TABLE public.product (
    id integer NOT NULL,
    name character varying(100),
    price numeric(15,0),
    image_url character varying(200),
    description text,
    category character varying(50),
    brand character varying(100),
    chipset character varying(100),
    ram character varying(50),
    storage character varying(50),
    battery integer,
    screen_size double precision,
    weight double precision,
    performance_score double precision,
    release_year integer
);


ALTER TABLE public.product OWNER TO shop;

--
-- Name: product_id_seq; Type: SEQUENCE; Schema: public; Owner: shop
--

CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_id_seq OWNER TO shop;

--
-- Name: product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shop
--

ALTER SEQUENCE public.product_id_seq OWNED BY public.product.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: shop
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    fullname character varying(100),
    gmail character varying(100),
    username character varying(50),
    password character varying(255)
);


ALTER TABLE public."user" OWNER TO shop;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: shop
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO shop;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shop
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: admin id; Type: DEFAULT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.admin ALTER COLUMN id SET DEFAULT nextval('public.admin_id_seq'::regclass);


--
-- Name: cart_item id; Type: DEFAULT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.cart_item ALTER COLUMN id SET DEFAULT nextval('public.cart_item_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: otp_register id; Type: DEFAULT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.otp_register ALTER COLUMN id SET DEFAULT nextval('public.otp_register_id_seq'::regclass);


--
-- Name: product id; Type: DEFAULT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.product ALTER COLUMN id SET DEFAULT nextval('public.product_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: admin; Type: TABLE DATA; Schema: public; Owner: shop
--

COPY public.admin (id, fullnamead, gmail, usernamead, password) FROM stdin;
\.


--
-- Data for Name: cart_item; Type: TABLE DATA; Schema: public; Owner: shop
--

COPY public.cart_item (id, user_id, product_id, quantity, total_price) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: shop
--

COPY public.orders (id, user_id, total_amount, payment_method, status, bank_name, bank_account, bank_account_name, transfer_note, paid_at, created_at) FROM stdin;
\.


--
-- Data for Name: otp_register; Type: TABLE DATA; Schema: public; Owner: shop
--

COPY public.otp_register (id, email, otp_code, created_at, expire_at, is_verified) FROM stdin;
\.


--
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: shop
--

COPY public.product (id, name, price, image_url, description, category, brand, chipset, ram, storage, battery, screen_size, weight, performance_score, release_year) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: shop
--

COPY public."user" (id, fullname, gmail, username, password) FROM stdin;
\.


--
-- Name: admin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shop
--

SELECT pg_catalog.setval('public.admin_id_seq', 1, false);


--
-- Name: cart_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shop
--

SELECT pg_catalog.setval('public.cart_item_id_seq', 1, false);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shop
--

SELECT pg_catalog.setval('public.orders_id_seq', 1, false);


--
-- Name: otp_register_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shop
--

SELECT pg_catalog.setval('public.otp_register_id_seq', 1, false);


--
-- Name: product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shop
--

SELECT pg_catalog.setval('public.product_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shop
--

SELECT pg_catalog.setval('public.user_id_seq', 1, false);


--
-- Name: admin admin_pkey; Type: CONSTRAINT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (id);


--
-- Name: admin admin_usernamead_key; Type: CONSTRAINT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_usernamead_key UNIQUE (usernamead);


--
-- Name: cart_item cart_item_pkey; Type: CONSTRAINT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.cart_item
    ADD CONSTRAINT cart_item_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: otp_register otp_register_email_key; Type: CONSTRAINT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.otp_register
    ADD CONSTRAINT otp_register_email_key UNIQUE (email);


--
-- Name: otp_register otp_register_pkey; Type: CONSTRAINT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.otp_register
    ADD CONSTRAINT otp_register_pkey PRIMARY KEY (id);


--
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);


--
-- Name: user user_gmail_key; Type: CONSTRAINT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_gmail_key UNIQUE (gmail);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: cart_item cart_item_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.cart_item
    ADD CONSTRAINT cart_item_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id);


--
-- Name: cart_item cart_item_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.cart_item
    ADD CONSTRAINT cart_item_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shop
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

