CREATE TABLE Users (UserId SERIAL PRIMARY KEY, Username varchar(32) UNIQUE NOT NULL, Password varchar NOT NULL, visible integer DEFAULT 1);
CREATE TABLE Match (MatchId SERIAL PRIMARY KEY, Matchname varchar(64) NOT NULL, Matchsize integer, User_id integer NOT NULL, visible integer DEFAULT 1, FOREIGN KEY (User_id) REFERENCES Users(UserId));
CREATE TABLE Army (ArmyId SERIAL PRIMARY KEY, Armyname varchar(64) NOT NULL, Armysize integer, visible integer DEFAULT 1);
CREATE TABLE Unit (UnitId SERIAL PRIMARY KEY, Unitname varchar(64) NOT NULL, Points integer, visible integer DEFAULT 1);

CREATE TABLE MatchArmy (Match_id integer, Army_id integer, Army_side integer NOT NULL,
                        FOREIGN KEY (Match_id) REFERENCES Match(MatchId),
                        FOREIGN KEY (Army_id) REFERENCES Army(ArmyId));
CREATE TABLE ArmyUnit (Army_id integer, Unit_id integer,
                        FOREIGN KEY (Army_id) REFERENCES Army(ArmyId),
                        FOREIGN KEY (Unit_id) REFERENCES Unit(UnitId));