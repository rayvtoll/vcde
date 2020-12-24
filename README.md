# Virtual Container Desktop Environment
In-browser desktop environment based on containers. Environment scales automaticly so that no unneeded resources are waisted.
By using X forwarding between containers users can use applications that are not locally installed (a form of published applications if you will). VCDE uses the Guacamole protocol so you can enter your desktop container using rdp in a browser. 

## Install Guide

### Prerequisites
Make sure docker and docker-compose are correctly installed.

### Installing
Run the following to create the Docker networks:
```
for i in {frontend,backend} ; do docker network create vcd_$i ; done
docker pull rayvtoll/containerdesktop
```

git clone https://github.com/rayvtoll/vcde and run:
```
touch db.sqlite3
docker-compose up --build --force-recreate &
docker exec -it login sh
python manage.py migrate
python manage.py createsuperuser
```

Follow instructions, open a browser and go to localhost. Enter your credentials 

### Using LDAP
If you change docker-compose.yml to use LDAP, make sure you set USELDAP to True and set all environment variables below:

```
USELDAP=True
LDAPURI=ldap://<ldapuri> # ldap://contosoOpenLdap
LDAPBIND=<cn,dc> # cn=ldap-ro,dc=contoso,dc=com
LDAPPASSWRD=<password> # P@ss1W0Rd!
LDAPUSERS=<users> # ou=users,dc=contoso,dc=com
LDAPGROUPS=<groups> # ou=groups,dc=contoso,dc=com
```

## Notes
I created the login container for dynamically creating containerdesktops at login. After login a Guacamole session is initiated with Guacamole python client. 

The first time you try to start an application, it has to be downloaded first (may take a minute).

Home directory will be saved outside of the container at /opt/vcde/{username}
The directory can be set by changing the directorylocation somewhere in the upperlines of backend.py

More information will follow soon.
