#!/bin/sh

psql -U postgres -d moscow -c "CREATE EXTENSION postgis";

osm2pgsql -U postgres -d moscow -l moscow.osm.pbf


[Unit]
  Description=MapsHackathonBackend

[Service]
  ExecStart=/usr/bin/python3 /var/hack/MapsHackathonBackend/app.py
  Type=idle
  KillMode=process

  SyslogIdentifier=hack-back
  SyslogFacility=daemon

  Restart=on-failure

[Install]
  WantedBy=multiuser.target