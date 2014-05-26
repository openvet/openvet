
INSERT INTO Pays(idPays,Pays) VALUES(33,'France');


INSERT INTO Commune (Commune,CIP,Pays_idPays,Actif)
SELECT commune , codepost,33,1 FROM villes_france;

DROP TABLE villes_france;
