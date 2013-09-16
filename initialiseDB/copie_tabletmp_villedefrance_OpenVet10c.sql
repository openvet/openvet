
DELETE from Client;



DELETE FROM Commune;

DELETE FROM Pays;

INSERT INTO Pays(idPays,Nom) VALUES(33,'France');


INSERT INTO Commune (Commune,CIP,Pays_idPays)
SELECT commune , codepost,33 FROM villes_france;

DROP TABLE villes_france;
