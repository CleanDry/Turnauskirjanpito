# Turnauskirjanpito
HY Tietokantasovelluksen harjoitustyö

Sovelluksen velmistuttua sillä voi:
- Luoda uuden käyttäjän ja kirjautua olemassaolevan käyttäjän tiedoilla sovellukseen
- Lisätä ja poistaa yksiköitä
- Lisätä ja poistaa armeijoita
- Liittää ja irroittaa yksiköitä armeijoihin
- Lisätä, poistaa ja muokata otteluita
- Nähdä yhteenvedon otteluista

Starting a PSQL-server:
``start-pg.sh``
Shut down server with ctrl-c

Connecting to PQSL-server with interactive terminal:
``pqsl``

Installing required dependencies to virtual environment:
``(venv) $ pip install -r requirements.txt``

Creating SQL-tables required in App in virtual environment:
``(venv) $ psql < schema.sql``