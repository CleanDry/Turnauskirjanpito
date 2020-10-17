# Turnauskirjanpito
HY Tietokantasovelluksen harjoitustyö

Sovellus pöytäsotapelien suunnittelua ja taltioimista varten.
Sovelluksella voi:
- Luoda uuden käyttäjän ja kirjautua olemassaolevan käyttäjän tiedoilla sovellukseen
- Lisätä ja poistaa yksiköitä
- Lisätä ja poistaa armeijoita
- Lisätä ja muokata otteluita
- Liittää ja irroittaa yksiköitä armeijoihin
- Liittää ja irroittaa armeijoita otteluihin
- Nähdä yhteenvedon otteluista, armeijoista ja yksiköistä

Sovellus on testattavissa osoitteessa:
https://tsoha-membrancer.herokuapp.com/



Development notes (users need not worry):

Starting a PSQL-server:
``start-pg.sh``
Shut down server with ctrl-c

Connecting to PQSL-server with interactive terminal:
``pqsl``

Activating virtual environment:
``source venv/bin/activate``

Running app locally in venv:
``flask run``

Installing required dependencies to virtual environment:
``(venv) $ pip install -r requirements.txt``

Creating SQL-tables required in App in virtual environment:
``(venv) $ psql < schema.sql``
