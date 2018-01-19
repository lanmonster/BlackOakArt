--
-- PostgreSQL database dump
--

-- Dumped from database version 10.1
-- Dumped by pg_dump version 10.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: have; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA have;


ALTER SCHEMA have OWNER TO postgres;

--
-- Name: leftover; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA leftover;


ALTER SCHEMA leftover OWNER TO postgres;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = have, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: assemble; Type: TABLE; Schema: have; Owner: jonathanmartin
--

CREATE TABLE assemble (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: debat; Type: TABLE; Schema: have; Owner: jonathanmartin
--

CREATE TABLE debat (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: handle; Type: TABLE; Schema: have; Owner: jonathanmartin
--

CREATE TABLE handle (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: polish; Type: TABLE; Schema: have; Owner: jonathanmartin
--

CREATE TABLE polish (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: prep; Type: TABLE; Schema: have; Owner: jonathanmartin
--

CREATE TABLE prep (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: stamp; Type: TABLE; Schema: have; Owner: jonathanmartin
--

CREATE TABLE stamp (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: throw; Type: TABLE; Schema: have; Owner: jonathanmartin
--

CREATE TABLE throw (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: trim; Type: TABLE; Schema: have; Owner: jonathanmartin
--

CREATE TABLE "trim" (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



SET search_path = leftover, pg_catalog;

--
-- Name: assemble; Type: TABLE; Schema: leftover; Owner: jonathanmartin
--

CREATE TABLE assemble (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: debat; Type: TABLE; Schema: leftover; Owner: jonathanmartin
--

CREATE TABLE debat (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: handle; Type: TABLE; Schema: leftover; Owner: jonathanmartin
--

CREATE TABLE handle (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: polish; Type: TABLE; Schema: leftover; Owner: jonathanmartin
--

CREATE TABLE polish (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: prep; Type: TABLE; Schema: leftover; Owner: jonathanmartin
--

CREATE TABLE prep (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: stamp; Type: TABLE; Schema: leftover; Owner: jonathanmartin
--

CREATE TABLE stamp (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: throw; Type: TABLE; Schema: leftover; Owner: jonathanmartin
--

CREATE TABLE throw (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



--
-- Name: trim; Type: TABLE; Schema: leftover; Owner: jonathanmartin
--

CREATE TABLE "trim" (
    item character varying(255),
    clay_type character varying(255),
    amount integer,
    id integer
);



SET search_path = public, pg_catalog;

--
-- Name: debat; Type: TABLE; Schema: public; Owner: jonathanmartin
--

CREATE TABLE debat (
    id integer,
    amount integer
);



--
-- Name: purchaseorders; Type: TABLE; Schema: public; Owner: jonathanmartin
--

CREATE TABLE purchaseorders (
    item character varying NOT NULL,
    glaze_color character varying NOT NULL,
    description character varying NOT NULL,
    delivery_date date NOT NULL,
    company character varying NOT NULL,
    buffer double precision NOT NULL,
    amount integer NOT NULL,
    miscellaneous character varying,
    adjusted_amount integer NOT NULL,
    clay_type character varying NOT NULL,
    id integer NOT NULL,
    prepped integer DEFAULT 0,
    thrown integer DEFAULT 0,
    debatted integer DEFAULT 0,
    trimmed integer DEFAULT 0,
    assembled integer DEFAULT 0,
    polished integer DEFAULT 0,
    stamps integer DEFAULT 0,
    handles integer DEFAULT 0
);



--
-- Name: purchaseorders_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathanmartin
--

CREATE SEQUENCE purchaseorders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: purchaseorders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathanmartin
--

ALTER SEQUENCE purchaseorders_id_seq OWNED BY purchaseorders.id;


--
-- Name: purchaseorders id; Type: DEFAULT; Schema: public; Owner: jonathanmartin
--

ALTER TABLE ONLY purchaseorders ALTER COLUMN id SET DEFAULT nextval('purchaseorders_id_seq'::regclass);


