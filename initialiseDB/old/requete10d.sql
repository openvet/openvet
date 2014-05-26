USE OpenVet10d;
SET profiling = 1;
-- Vider cache
RESET QUERY CACHE;
SELECT Client.Nom,Client.Prenom,Adresse.No,NomRue.NomRue, Commune.Commune FROM Client
INNER JOIN AdresseHistorique ON AdresseHistorique.Client_idClient=Client.idClient
INNER JOIN Adresse ON idAdresse=AdresseHistorique.idAdresseHistorique
INNER JOIN NomRue ON idNomRue=Adresse.NomRue_idNomRue
INNER JOIN Commune ON idCommune=Adresse.Commune_idCommune
WHERE Nom LIKE 'A%' AND Adresse.IsValide=True;

SHOW PROFILES;
SET profiling = 0;