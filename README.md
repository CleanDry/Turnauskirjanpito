# Turnauskirjanpito
HY Tietokantasovelluksen harjoitustyö

Sovelluksen velmistuttua sillä voi:
- Luoda uuden käyttäjän ja kirjautua olemassaolevan käyttäjän tiedoilla sovellukseen
- Lisätä ja poistaa yksiköitä
- Lisätä ja poistaa armeijoita
- Liittää ja irroittaa yksiköitä armeijoihin
- Lisätä, poistaa ja muokata otteluita
- Nähdä yhteenvedon otteluista

Sovellus on testattavissa osoitteessa:
https://tsoha-membrancer.herokuapp.com/

Tällä hetkellä sovelluksessa voi:
- Luoda uuden käyttäjän ja kirjautua olemassaolevan käyttäjän tiedoilla sovellukseen
- Nähdä yhteenvedon otteluista
- Lisätä otteluita
- Lisätä armeijoita

Tällä hetkellä sovelluksen backend tukee jo:
- Luoda uuden käyttäjän ja kirjautua olemassaolevan käyttäjän tiedoilla sovellukseen
- Lisätä ja poistaa yksiköitä
- Lisätä ja poistaa armeijoita
- Liittää ja irroittaa yksiköitä armeijoihin
- Lisätä, poistaa ja muokata otteluita
- Nähdä yhteenvedon otteluista

Todo
- Sovelluksen ja backendin yhdistäminen loppuun
- Syötteiden validointi
- Tietoturvan varmistaminen

Development notes (users need not worry):

Starting a PSQL-server:
``start-pg.sh``
Shut down server with ctrl-c

Connecting to PQSL-server with interactive terminal:
``pqsl``

Activating virtual environment
``source venv/bin/activate``

Installing required dependencies to virtual environment:
``(venv) $ pip install -r requirements.txt``

Creating SQL-tables required in App in virtual environment:
``(venv) $ psql < schema.sql``
