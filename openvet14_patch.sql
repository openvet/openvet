USE `OpenVet13`;
CREATE  OR REPLACE VIEW `OpenVet13`.`viewAnimal` AS SELECT A.*, E.*, R1.idRace AS idRace1, R1.Race AS Race1 , R2.idRace AS idRace2, R2.Race  AS Race2 FROM Animal A
LEFT JOIN Especes E ON Especes_idEspeces = idEspeces
 LEFT JOIN Race R1 ON Race_idRace = R1.idRace 
LEFT JOIN Race R2 ON Race2_idRace = R2.idRace
