#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE orbit_gate;
    CREATE DATABASE orbit_writer;
    CREATE DATABASE orbit_planet;
    CREATE DATABASE orbit_turbotick;
    CREATE DATABASE orbit_wallet;
    CREATE DATABASE orbit_dock;
    CREATE DATABASE orbit_capitalhub;
    CREATE DATABASE orbit_atlas;
    CREATE DATABASE orbit_fitterme;
    CREATE DATABASE orbit_secure;
    CREATE DATABASE orbit_mail;
    CREATE DATABASE orbit_calendar;
    CREATE DATABASE orbit_controlcenter;
    CREATE DATABASE orbit_search;
    CREATE DATABASE orbit_connect;
    CREATE DATABASE orbit_meet;
EOSQL
