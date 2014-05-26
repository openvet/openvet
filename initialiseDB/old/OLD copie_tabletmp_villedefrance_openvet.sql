
-- DELETE FROM Ville;

-- err contrainte DELETE FROM Pays;

INSERT INTO Pays(idPays,Nom) VALUES(33,'France');


INSERT INTO Ville (Nom,CodePostal,Pays_idPays)
SELECT commune , codepost,33 FROM villes_france;

DROP TABLE villes_france;
