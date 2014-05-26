SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `OpenVet12` ;
CREATE SCHEMA IF NOT EXISTS `OpenVet12` DEFAULT CHARACTER SET utf8 ;
USE `OpenVet12` ;

-- -----------------------------------------------------
-- Table `OpenVet12`.`Especes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Especes` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Especes` (
  `idEspeces` INT NOT NULL AUTO_INCREMENT ,
  `Espece` VARCHAR(60) NULL ,
  PRIMARY KEY (`idEspeces`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Race`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Race` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Race` (
  `idRace` INT NOT NULL AUTO_INCREMENT ,
  `Race` VARCHAR(50) NULL ,
  `Especes_idEspeces` INT NOT NULL ,
  `Actif` TINYINT(1) NULL ,
  INDEX `fk_Races_Especes1_idx` (`Especes_idEspeces` ASC) ,
  PRIMARY KEY (`idRace`) ,
  CONSTRAINT `fk_Races_Especes1`
    FOREIGN KEY (`Especes_idEspeces` )
    REFERENCES `OpenVet12`.`Especes` (`idEspeces` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Animal`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Animal` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Animal` (
  `idAnimal` INT NOT NULL AUTO_INCREMENT ,
  `Animal_idPere` INT NULL ,
  `Animal_idMere` INT NULL ,
  `Nom` VARCHAR(45) NULL DEFAULT NULL ,
  `Especes_idEspeces` INT NOT NULL ,
  `Race_idRace` INT NULL ,
  `Race2_idRace` INT NULL ,
  `Robe` VARCHAR(45) NULL DEFAULT NULL ,
  `Sexe` CHAR(1) NULL ,
  `Naissance` DATE NULL ,
  `Sterilise` TINYINT(1) NULL DEFAULT 0 ,
  `DesactiverRelances` TINYINT(1) NULL ,
  `Identification` VARCHAR(14) NULL DEFAULT NULL COMMENT 'puce ou tatou\n' ,
  `Commentaires` VARCHAR(200) NULL DEFAULT NULL ,
  `Actif` TINYINT(1) NULL ,
  PRIMARY KEY (`idAnimal`) ,
  UNIQUE INDEX `idAnimal_UNIQUE` (`idAnimal` ASC) ,
  UNIQUE INDEX `identification_UNIQUE` (`Identification` ASC) ,
  INDEX `fk_Animal_Especes1_idx` (`Especes_idEspeces` ASC) ,
  INDEX `fk_Animal_Race1_idx` (`Race_idRace` ASC) ,
  INDEX `fk_Animal_Race2_idx` (`Race2_idRace` ASC) ,
  INDEX `fk_Animal_1_idx` (`Animal_idPere` ASC) ,
  INDEX `fk_Animal_Mere_idx` (`Animal_idMere` ASC) ,
  CONSTRAINT `fk_Animal_Especes1`
    FOREIGN KEY (`Especes_idEspeces` )
    REFERENCES `OpenVet12`.`Especes` (`idEspeces` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Animal_Race1`
    FOREIGN KEY (`Race_idRace` )
    REFERENCES `OpenVet12`.`Race` (`idRace` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Animal_Race2`
    FOREIGN KEY (`Race2_idRace` )
    REFERENCES `OpenVet12`.`Race` (`idRace` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Animal_Pere`
    FOREIGN KEY (`Animal_idPere` )
    REFERENCES `OpenVet12`.`Animal` (`idAnimal` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Animal_Mere`
    FOREIGN KEY (`Animal_idMere` )
    REFERENCES `OpenVet12`.`Animal` (`idAnimal` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Aliment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Aliment` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Aliment` (
  `idAliment` INT NOT NULL AUTO_INCREMENT ,
  `Animal_idAnimal1` INT NOT NULL ,
  `Date` DATE NULL DEFAULT NULL ,
  `Denomination` VARCHAR(45) NULL DEFAULT NULL ,
  `Cip` VARCHAR(8) NULL COMMENT 'CIp as a foreign key?' ,
  `Actif` TINYINT(1) NULL ,
  INDEX `fk_Aliment_Animal1_idx` (`Animal_idAnimal1` ASC) ,
  PRIMARY KEY (`idAliment`) ,
  CONSTRAINT `fk_Aliment_Animal1`
    FOREIGN KEY (`Animal_idAnimal1` )
    REFERENCES `OpenVet12`.`Animal` (`idAnimal` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Civilite`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Civilite` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Civilite` (
  `idCivilite` INT NOT NULL AUTO_INCREMENT ,
  `Civilite` VARCHAR(30) NOT NULL ,
  `CiviliteAbrev` VARCHAR(10) NOT NULL ,
  `Actif` TINYINT(1) NULL ,
  PRIMARY KEY (`idCivilite`) ,
  UNIQUE INDEX `Civilite_UNIQUE` (`Civilite` ASC) ,
  UNIQUE INDEX `CivilitesAbrev_UNIQUE` (`CiviliteAbrev` ASC) )
ENGINE = InnoDB
COMMENT = 'ex client1 pere de client2';


-- -----------------------------------------------------
-- Table `OpenVet12`.`Pays`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Pays` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Pays` (
  `idPays` INT NOT NULL AUTO_INCREMENT ,
  `Pays` VARCHAR(60) NULL ,
  PRIMARY KEY (`idPays`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Commune`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Commune` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Commune` (
  `idCommune` INT NOT NULL AUTO_INCREMENT ,
  `Commune` VARCHAR(45) NOT NULL ,
  `CIP` VARCHAR(45) NOT NULL ,
  `Pays_idPays` INT NOT NULL DEFAULT True ,
  `Actif` TINYINT(1) NULL ,
  PRIMARY KEY (`idCommune`) ,
  INDEX `fk_Commune_Pays_idx` (`Pays_idPays` ASC) ,
  CONSTRAINT `fk_Commune_Pays`
    FOREIGN KEY (`Pays_idPays` )
    REFERENCES `OpenVet12`.`Pays` (`idPays` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Personne`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Personne` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Personne` (
  `idPersonne` INT NOT NULL AUTO_INCREMENT ,
  `Civilite_idCivilite` INT NOT NULL ,
  `isClient` TINYINT(1) NULL DEFAULT False ,
  `IsVeterinaire` TINYINT(1) NULL DEFAULT False ,
  `isSalarie` TINYINT(1) NULL DEFAULT False ,
  `isFournisseur` TINYINT(1) NULL DEFAULT False ,
  `IsConsultant` TINYINT(1) NULL DEFAULT False ,
  `IsReferant` TINYINT(1) NULL DEFAULT False ,
  `IsReferent` TINYINT(1) NULL DEFAULT False ,
  `IsAssocie` TINYINT(1) NULL ,
  `IsCollaborateurLiberal` TINYINT(1) NULL ,
  `IsServiceGarde` TINYINT(1) NULL ,
  `Actif` TINYINT(1) NULL DEFAULT True ,
  `Commentaires` VARCHAR(200) CHARACTER SET 'latin1' NULL DEFAULT NULL ,
  `Nom` VARCHAR(60) CHARACTER SET 'latin1' NOT NULL ,
  `NomMarital` VARCHAR(45) NULL ,
  `Prenom` VARCHAR(45) CHARACTER SET 'latin1' NOT NULL ,
  `Adresse_No` VARCHAR(45) NULL ,
  `Adresse_Rue` VARCHAR(45) NULL ,
  `Commune_idCommune` INT NOT NULL ,
  `SousTutelle` TINYINT(1) NULL DEFAULT False ,
  `MauvaisPayeur` TINYINT(1) NULL DEFAULT False ,
  `Contentieux` TINYINT(1) NULL DEFAULT False ,
  `AncienClient` TINYINT(1) NULL DEFAULT False ,
  `ClientDePassage` TINYINT(1) NULL DEFAULT False ,
  `NbRetardRV` INT NULL DEFAULT 0 ,
  `NbOublieRV` INT NULL DEFAULT 0 ,
  `NbOublieOpe` INT NULL DEFAULT 0 ,
  `DateEntree` DATE NULL ,
  `PartSociales` DECIMAL(4,2) NULL ,
  `NoCARPV` VARCHAR(15) NULL ,
  `NoURSSAF` VARCHAR(15) NULL ,
  `NoOrdre` VARCHAR(8) NULL COMMENT 'Vet' ,
  `Specialite` VARCHAR(45) NULL COMMENT 'Vet' ,
  `Temporaire` TINYINT(1) NULL DEFAULT False COMMENT 'Sal\n' ,
  `Cadre` TINYINT(1) NULL DEFAULT False COMMENT 'Sal\n' ,
  `ConventionCollective` VARCHAR(8) NULL COMMENT 'Sal\n' ,
  `SalaireHoraire` DECIMAL(4,2) NULL COMMENT 'Sal\n' ,
  `Coefficient` DECIMAL(4,2) NULL COMMENT 'Sal\n' ,
  `Echellon` VARCHAR(12) NULL COMMENT 'Sal' ,
  `Emploi` VARCHAR(45) NULL COMMENT 'Sal' ,
  `LieuNaissance` VARCHAR(45) NULL ,
  `DateNaissance` DATE NULL ,
  `FinContrat` DATE NULL COMMENT 'Sal' ,
  `NoSecuriteSociale` VARCHAR(15) NULL COMMENT 'Sal' ,
  `TelephoneDomicile` VARCHAR(20) NULL ,
  `TelephoneBureau` VARCHAR(20) NULL ,
  `TelephonePortable1` VARCHAR(20) NULL ,
  `TelephonePortable2` VARCHAR(20) NULL ,
  `Mail` VARCHAR(60) NULL ,
  PRIMARY KEY (`idPersonne`) ,
  INDEX `fk_Client_Civilite_idx` (`Civilite_idCivilite` ASC) ,
  INDEX `fk_Client_Commune1_idx` (`Commune_idCommune` ASC) ,
  CONSTRAINT `fk_Client_Civilite`
    FOREIGN KEY (`Civilite_idCivilite` )
    REFERENCES `OpenVet12`.`Civilite` (`idCivilite` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Client_Commune1`
    FOREIGN KEY (`Commune_idCommune` )
    REFERENCES `OpenVet12`.`Commune` (`idCommune` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Consultation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Consultation` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Consultation` (
  `idConsultation` INT NOT NULL AUTO_INCREMENT ,
  `Animal_idAnimal` INT NOT NULL ,
  `DateConsultation` DATETIME NULL DEFAULT NULL ,
  `Personne_idVeterinaire` INT NOT NULL ,
  `Personne_idReferant` INT NULL DEFAULT NULL ,
  `Personne_idReferent` INT NULL ,
  `Examen` TEXT NULL DEFAULT NULL ,
  `Traitement` TEXT NULL DEFAULT NULL ,
  `Actif` TINYINT(1) NULL ,
  `Commentaires` VARCHAR(200) NULL ,
  INDEX `fk_Consultation_Animal1_idx` (`Animal_idAnimal` ASC) ,
  PRIMARY KEY (`idConsultation`) ,
  INDEX `fk_Consultation_Personne1_idx` (`Personne_idVeterinaire` ASC) ,
  INDEX `fk_Consultation_Personne_idReferant_idx` (`Personne_idReferant` ASC) ,
  CONSTRAINT `fk_Consultation_Animal1`
    FOREIGN KEY (`Animal_idAnimal` )
    REFERENCES `OpenVet12`.`Animal` (`idAnimal` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Consultation_Personne_idVeterinaire`
    FOREIGN KEY (`Personne_idVeterinaire` )
    REFERENCES `OpenVet12`.`Personne` (`idPersonne` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Consultation_Personne_idReferant`
    FOREIGN KEY (`Personne_idReferant` )
    REFERENCES `OpenVet12`.`Personne` (`idPersonne` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `OpenVet12`.`TypeAnalyse`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`TypeAnalyse` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`TypeAnalyse` (
  `idTypeAnalyse` INT NOT NULL AUTO_INCREMENT ,
  `Libele` VARCHAR(45) NULL ,
  `Remarque` VARCHAR(200) NULL ,
  `IsImage` TINYINT(1) NOT NULL ,
  PRIMARY KEY (`idTypeAnalyse`) ,
  UNIQUE INDEX `Libele_UNIQUE` (`Libele` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Analyse`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Analyse` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Analyse` (
  `idAnalyse` INT(11) NOT NULL AUTO_INCREMENT ,
  `Consultation_idConsultation` INT NOT NULL ,
  `TypeAnalyse_idTypeAnalyse` INT NOT NULL ,
  `DateHeure` DATETIME NULL ,
  `DescriptionAnalyse` VARCHAR(80) NULL DEFAULT NULL COMMENT 'ex: echocardio, radio bassin, electrophorèse proteines\n' ,
  `Prelevement` VARCHAR(80) NULL ,
  `SyntheseAnalyse` TINYTEXT NULL ,
  `Conclusions` TINYTEXT NULL ,
  INDEX `fk_Analyse_Consultation1_idx` (`Consultation_idConsultation` ASC) ,
  INDEX `fk_Analyse_AnalysesTypes1_idx` (`TypeAnalyse_idTypeAnalyse` ASC) ,
  PRIMARY KEY (`idAnalyse`) ,
  CONSTRAINT `fk_Analyse_Consultation`
    FOREIGN KEY (`Consultation_idConsultation` )
    REFERENCES `OpenVet12`.`Consultation` (`idConsultation` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Analyse_TypeAnalyse`
    FOREIGN KEY (`TypeAnalyse_idTypeAnalyse` )
    REFERENCES `OpenVet12`.`TypeAnalyse` (`idTypeAnalyse` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Facture`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Facture` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Facture` (
  `idFacture` INT(11) NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT(11) NOT NULL ,
  `NomClientAFacturer` VARCHAR(60) NULL ,
  `Commune_idCommune` INT NULL ,
  `AdresseFacturation` VARCHAR(100) NULL ,
  `DateFacture` DATE NULL ,
  `DateEnvoiCourrier` DATE NULL COMMENT 'si envoye +tard' ,
  `DateLimiteRelance` DATE NULL COMMENT 'si >aujourd hui=>relancer\n' ,
  `RelanceEnvoyee` TINYINT(1) NULL ,
  `NumFacture` VARCHAR(20) NULL ,
  `IsDevis` TINYINT(1) NULL DEFAULT FALSE ,
  `MontantHT` DECIMAL(6,2) NULL DEFAULT 0 ,
  `MontantTTC` DECIMAL(6,2) NULL DEFAULT 0 ,
  `MontantTVA` DECIMAL(4,2) NULL DEFAULT 0 ,
  `MontantRemises` DECIMAL(6,2) NULL DEFAULT 0 ,
  `IsRecouvrement` TINYINT(1) NULL DEFAULT FALSE ,
  `TotalRegle` DECIMAL(6,2) NULL DEFAULT 0 COMMENT 'Est-ce nécessaire?\n' ,
  `Commentaires` VARCHAR(200) NULL ,
  `Actif` TINYINT(1) NULL DEFAULT TRUE ,
  `FactureFigee` TINYINT(1) NULL DEFAULT FALSE ,
  UNIQUE INDEX `idFactures_UNIQUE` (`idFacture` ASC) ,
  INDEX `fk_Factures_Client1_idx` (`Client_idClient` ASC) ,
  PRIMARY KEY (`idFacture`) ,
  INDEX `fk_Facture_Commune1_idx` (`Commune_idCommune` ASC) ,
  CONSTRAINT `fk_Factures_Client1`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet12`.`Personne` (`idPersonne` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Facture_Commune1`
    FOREIGN KEY (`Commune_idCommune` )
    REFERENCES `OpenVet12`.`Commune` (`idCommune` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1
COMMENT = 'somme ttc utiliser fonction ou champ virtuel?';


-- -----------------------------------------------------
-- Table `OpenVet12`.`CategoriePrestation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`CategoriePrestation` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`CategoriePrestation` (
  `idCategoriePrestation` INT NOT NULL AUTO_INCREMENT ,
  `Designation` VARCHAR(80) NOT NULL ,
  `Abreviation` VARCHAR(5) NOT NULL ,
  PRIMARY KEY (`idCategoriePrestation`) ,
  UNIQUE INDEX `Designation_UNIQUE` (`Designation` ASC) ,
  UNIQUE INDEX `Abreviation_UNIQUE` (`Abreviation` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`LignesFacture`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`LignesFacture` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`LignesFacture` (
  `idLignesFacture` INT NOT NULL AUTO_INCREMENT ,
  `Facture_idFacture` INT NOT NULL ,
  `CategoriePrestation_idCategoriePrestation` INT NULL ,
  `Date` DATE NULL DEFAULT NULL ,
  `Denomination` VARCHAR(60) NULL DEFAULT '' ,
  `PrixUnitHT` DECIMAL(6,2) NULL DEFAULT 0 ,
  `TVA` DECIMAL(4,2) NULL DEFAULT 0 ,
  `PrixUnitTTC` DECIMAL(6,2) NULL DEFAULT 0 ,
  `Quantite` DECIMAL(6,2) NULL DEFAULT 0 ,
  `TauxRemise` DECIMAL(5,2) NULL DEFAULT 0 ,
  `RemisesTTC` DECIMAL(6,2) NULL DEFAULT 0 ,
  `PrixTotal` DECIMAL(6,2) NULL DEFAULT 0 ,
  `IsGratuit` TINYINT(1) NULL DEFAULT FALSE ,
  INDEX `fk_LignesFacture_Factures1_idx` (`Facture_idFacture` ASC) ,
  INDEX `fk_LignesFacture_1_idx` (`CategoriePrestation_idCategoriePrestation` ASC) ,
  PRIMARY KEY (`idLignesFacture`) ,
  CONSTRAINT `fk_LignesFacture_Factures1`
    FOREIGN KEY (`Facture_idFacture` )
    REFERENCES `OpenVet12`.`Facture` (`idFacture` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_LignesFacture_Categories`
    FOREIGN KEY (`CategoriePrestation_idCategoriePrestation` )
    REFERENCES `OpenVet12`.`CategoriePrestation` (`idCategoriePrestation` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Ordonnance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Ordonnance` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Ordonnance` (
  `idOrdonnance` INT NOT NULL AUTO_INCREMENT ,
  `Consultation_idConsultation` INT NOT NULL ,
  PRIMARY KEY (`idOrdonnance`) ,
  INDEX `fk_Ordonnances_Consultation_idx` (`Consultation_idConsultation` ASC) ,
  CONSTRAINT `fk_Ordonnances_Consultation`
    FOREIGN KEY (`Consultation_idConsultation` )
    REFERENCES `OpenVet12`.`Consultation` (`idConsultation` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`LignesOrdonnance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`LignesOrdonnance` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`LignesOrdonnance` (
  `idLigneOrdonnance` INT NOT NULL AUTO_INCREMENT ,
  `Ordonnance_idOrdonnance` INT NOT NULL ,
  `Medicament` VARCHAR(80) NULL DEFAULT NULL ,
  `Posologie` VARCHAR(255) NULL DEFAULT NULL ,
  `UnitesDelivre` DECIMAL(6,2) NULL DEFAULT NULL ,
  `UnitesPrescrites` DECIMAL(6,2) NULL ,
  `ImpressionLIgne` TINYINT(1) NULL DEFAULT True ,
  `actif` TINYINT(1) NULL ,
  `commentaires` VARCHAR(45) NULL ,
  PRIMARY KEY (`idLigneOrdonnance`) ,
  INDEX `fk_LignesOrdonnances_Ordonnances_idx` (`Ordonnance_idOrdonnance` ASC) ,
  CONSTRAINT `fk_LignesOrdonnances_Ordonnances`
    FOREIGN KEY (`Ordonnance_idOrdonnance` )
    REFERENCES `OpenVet12`.`Ordonnance` (`idOrdonnance` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Pathologie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Pathologie` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Pathologie` (
  `idPathologie` INT NOT NULL AUTO_INCREMENT ,
  `NomReference` VARCHAR(60) NULL ,
  `Chronique` TINYINT(1) NULL ,
  `DescriptifPublic` TEXT NULL ,
  PRIMARY KEY (`idPathologie`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`PlanTherapeutique`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`PlanTherapeutique` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`PlanTherapeutique` (
  `idPlanTherapeutique` INT NOT NULL AUTO_INCREMENT ,
  `Consultation_idConsultation` INT NOT NULL ,
  `Pathologie_idPathologie` INT NOT NULL ,
  `Stade` VARCHAR(60) NULL DEFAULT NULL ,
  `Traitements` TEXT NULL DEFAULT NULL ,
  `Remarques` TEXT NULL DEFAULT NULL ,
  `ProchainRDV` DATE NULL DEFAULT NULL COMMENT 'Au plus tard' ,
  INDEX `fk_PlanTherapeutique_Consultation1_idx` (`Consultation_idConsultation` ASC) ,
  PRIMARY KEY (`idPlanTherapeutique`) ,
  INDEX `fk_PlanTherapeutique_Pathologie_idx` (`Pathologie_idPathologie` ASC) ,
  CONSTRAINT `fk_PlanTherapeutique_Consultation1`
    FOREIGN KEY (`Consultation_idConsultation` )
    REFERENCES `OpenVet12`.`Consultation` (`idConsultation` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PlanTherapeutique_Pathologie`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet12`.`Pathologie` (`idPathologie` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet12`.`PoidsMesure`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`PoidsMesure` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`PoidsMesure` (
  `idPoidsMesure` INT NOT NULL AUTO_INCREMENT ,
  `Animal_idAnimal` INT(11) NOT NULL ,
  `Date` DATE NOT NULL ,
  `Poids` DECIMAL(3,1) NULL DEFAULT NULL ,
  `TailleGarrot` DECIMAL(4,1) NULL ,
  `TourThorax` DECIMAL(3,1) NULL ,
  `Photo` VARCHAR(80) NULL ,
  INDEX `fk_Poids_Animal1_idx` (`Animal_idAnimal` ASC) ,
  PRIMARY KEY (`idPoidsMesure`) ,
  CONSTRAINT `fk_Poids_Animal1`
    FOREIGN KEY (`Animal_idAnimal` )
    REFERENCES `OpenVet12`.`Animal` (`idAnimal` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet12`.`TypeReglement`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`TypeReglement` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`TypeReglement` (
  `idTypeReglement` INT NOT NULL AUTO_INCREMENT ,
  `Type` VARCHAR(45) NULL ,
  `AbrevType` VARCHAR(3) NOT NULL ,
  `Actif` TINYINT(1) NULL ,
  PRIMARY KEY (`idTypeReglement`) ,
  UNIQUE INDEX `AbrevType_UNIQUE` (`AbrevType` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Reglement`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Reglement` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Reglement` (
  `idReglement` INT(11) NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT(11) NOT NULL ,
  `NomEncaissement` VARCHAR(80) NULL ,
  `DateReglement` DATE NOT NULL ,
  `DateEncaissement` DATE NULL COMMENT 'si reglt differe' ,
  `Montant` DECIMAL(6,2) NOT NULL ,
  `TypeReglement_idTypeReglement` INT NOT NULL ,
  `EnBanque` TINYINT(1) NULL DEFAULT False ,
  `Actif` TINYINT(1) NULL ,
  `Commentaires` VARCHAR(200) NULL ,
  UNIQUE INDEX `idReglements_UNIQUE` (`idReglement` ASC) ,
  INDEX `fk_Reglements_Client1_idx` (`Client_idClient` ASC) ,
  INDEX `fk_Reglement_1_idx` (`TypeReglement_idTypeReglement` ASC) ,
  PRIMARY KEY (`idReglement`) ,
  CONSTRAINT `fk_Reglements_Client1`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet12`.`Personne` (`idPersonne` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Reglement_TypeReglement`
    FOREIGN KEY (`TypeReglement_idTypeReglement` )
    REFERENCES `OpenVet12`.`TypeReglement` (`idTypeReglement` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1
COMMENT = '<>si cheque decalé';


-- -----------------------------------------------------
-- Table `OpenVet12`.`ModelRelance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ModelRelance` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ModelRelance` (
  `idModelRelance` INT NOT NULL AUTO_INCREMENT ,
  `Text` TINYTEXT NULL ,
  `Actif` TINYINT(1) NULL ,
  PRIMARY KEY (`idModelRelance`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`RelanceVaccin`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`RelanceVaccin` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`RelanceVaccin` (
  `idRelance` INT NOT NULL AUTO_INCREMENT ,
  `Animal_idAnimal` INT NOT NULL ,
  `ModelRelance_idModelRelance` INT NOT NULL ,
  `Date` DATE NOT NULL ,
  `Type` VARCHAR(10) NOT NULL COMMENT 'TODO a definir\n' ,
  `Media` VARCHAR(10) NOT NULL COMMENT 'TODO a définir\n' ,
  `Actif` TINYINT(1) NULL ,
  `Commentaires` VARCHAR(200) NULL ,
  INDEX `fk_Relances_Animal1_idx` (`Animal_idAnimal` ASC) ,
  INDEX `fk_Relances_1_idx` (`ModelRelance_idModelRelance` ASC) ,
  PRIMARY KEY (`idRelance`) ,
  CONSTRAINT `fk_Relances_Animal1`
    FOREIGN KEY (`Animal_idAnimal` )
    REFERENCES `OpenVet12`.`Animal` (`idAnimal` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Relances_ModelRelance`
    FOREIGN KEY (`ModelRelance_idModelRelance` )
    REFERENCES `OpenVet12`.`ModelRelance` (`idModelRelance` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet12`.`ListeVaccins`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ListeVaccins` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ListeVaccins` (
  `idListeVaccins` INT NOT NULL AUTO_INCREMENT ,
  `Nom` VARCHAR(45) NOT NULL ,
  `Especes_idEspeces` INT NOT NULL ,
  PRIMARY KEY (`idListeVaccins`) ,
  INDEX `fk_ListVaccins_1_idx` (`Especes_idEspeces` ASC) ,
  CONSTRAINT `Especes`
    FOREIGN KEY (`Especes_idEspeces` )
    REFERENCES `OpenVet12`.`Especes` (`idEspeces` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`TypeSociete`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`TypeSociete` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`TypeSociete` (
  `idTypeSociete` INT NOT NULL AUTO_INCREMENT ,
  `Nom` VARCHAR(45) NULL ,
  `IsVeterinaire` TINYINT(1) NULL DEFAULT True ,
  `IsNous` TINYINT(1) NOT NULL DEFAULT False ,
  PRIMARY KEY (`idTypeSociete`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Societe`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Societe` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Societe` (
  `idSociete` INT NOT NULL ,
  `TypeSociete_idTypeSociete` INT NOT NULL COMMENT 'TODO clinique, fournisseur' ,
  `Nom` VARCHAR(45) NULL ,
  `Raisonsociale` VARCHAR(45) NULL ,
  `Adresse` VARCHAR(120) NULL ,
  `Commune_idCommune` INT NOT NULL ,
  `Siret` VARCHAR(45) NULL ,
  `NTVA` VARCHAR(45) NULL ,
  `CodeNAF` VARCHAR(45) NULL DEFAULT NULL ,
  `Actif` TINYINT(1) NULL ,
  `Remarques` VARCHAR(200) NULL ,
  PRIMARY KEY (`idSociete`) ,
  INDEX `fk_Clinique_Commune_idx` (`Commune_idCommune` ASC) ,
  INDEX `fk_Societes_1_idx` (`TypeSociete_idTypeSociete` ASC) ,
  CONSTRAINT `fk_Clinique_Commune`
    FOREIGN KEY (`Commune_idCommune` )
    REFERENCES `OpenVet12`.`Commune` (`idCommune` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Societes_TypeSociete`
    FOREIGN KEY (`TypeSociete_idTypeSociete` )
    REFERENCES `OpenVet12`.`TypeSociete` (`idTypeSociete` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Vaccin`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Vaccin` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Vaccin` (
  `idVaccin` INT NOT NULL AUTO_INCREMENT ,
  `Animal_idAnimal` INT(11) NOT NULL ,
  `Date` DATE NOT NULL ,
  `ListVaccins_idListVaccins` INT NOT NULL ,
  `DateRelance` DATE NULL DEFAULT NULL ,
  `Societe_idSociete` INT NULL ,
  `NoLot` VARCHAR(15) NULL ,
  `Actif` TINYINT(1) NULL ,
  `Remarques` VARCHAR(45) NULL ,
  INDEX `fk_Vaccins_Animal1_idx` (`Animal_idAnimal` ASC) ,
  PRIMARY KEY (`idVaccin`) ,
  INDEX `fk_Vaccins_1_idx` (`ListVaccins_idListVaccins` ASC) ,
  INDEX `fk_Vaccins_Societe_idx` (`Societe_idSociete` ASC) ,
  CONSTRAINT `fk_Vaccins_Animal1`
    FOREIGN KEY (`Animal_idAnimal` )
    REFERENCES `OpenVet12`.`Animal` (`idAnimal` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Vaccins_ListVaccins`
    FOREIGN KEY (`ListVaccins_idListVaccins` )
    REFERENCES `OpenVet12`.`ListeVaccins` (`idListeVaccins` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Vaccins_Societe`
    FOREIGN KEY (`Societe_idSociete` )
    REFERENCES `OpenVet12`.`Societe` (`idSociete` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Banque`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Banque` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Banque` (
  `idBanque` INT NOT NULL AUTO_INCREMENT ,
  `date` DATE NOT NULL ,
  `montant` DECIMAL(8,2) NOT NULL ,
  `categorie` INT NOT NULL ,
  `libele` VARCHAR(80) NOT NULL ,
  `solde` DECIMAL(8,2) NOT NULL ,
  `differe` INT NULL ,
  PRIMARY KEY (`idBanque`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Recettes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Recettes` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Recettes` (
  `idRecettes` INT NOT NULL AUTO_INCREMENT ,
  `date` DATE NOT NULL ,
  `montant` DECIMAL(8,2) NOT NULL ,
  `type` VARCHAR(20) NOT NULL ,
  `except` VARCHAR(45) NULL ,
  PRIMARY KEY (`idRecettes`) ,
  UNIQUE INDEX `date_UNIQUE` (`date` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Depenses`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Depenses` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Depenses` (
  `idDepenses` INT NOT NULL AUTO_INCREMENT ,
  `date` DATE NULL ,
  `montantTTC` DECIMAL(8,2) NULL ,
  `tva` DECIMAL(8,2) NULL ,
  `escompte` DECIMAL(8,2) NULL ,
  `categorie` INT NULL ,
  `objet` VARCHAR(80) NULL ,
  `facture` INT NULL ,
  `typay` VARCHAR(4) NULL ,
  PRIMARY KEY (`idDepenses`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`VoiesAdministration`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`VoiesAdministration` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`VoiesAdministration` (
  `idVoiesAdministration` INT NOT NULL ,
  `VoieAdministration` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`idVoiesAdministration`) ,
  UNIQUE INDEX `VoieAdministration_UNIQUE` (`VoieAdministration` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`UniteConditionnement`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`UniteConditionnement` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`UniteConditionnement` (
  `idUniteConditionnement` INT NOT NULL AUTO_INCREMENT ,
  `UniteConditionnement` VARCHAR(30) NULL ,
  PRIMARY KEY (`idUniteConditionnement`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Medicament`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Medicament` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Medicament` (
  `idMedicament` INT NOT NULL AUTO_INCREMENT ,
  `VoiesAdministration_idVoiesAdministration` INT NOT NULL ,
  `UniteConditionnement_idUniteConditionnement` INT NULL ,
  `Designation` VARCHAR(45) NULL ,
  `Presentation` VARCHAR(45) NULL ,
  `Conditionnement` INT NULL ,
  `Cip` VARCHAR(8) NULL ,
  `Pharmacie` TINYINT(1) NULL DEFAULT 1 COMMENT 'Pharmacie\n1=veto\n0=humaine' ,
  `Intergre` TINYINT(1) NULL DEFAULT false ,
  PRIMARY KEY (`idMedicament`) ,
  INDEX `fk_Medicament_VoiesAdministration1_idx` (`VoiesAdministration_idVoiesAdministration` ASC) ,
  INDEX `fk_Medicament_UniteConditionnement_idx` (`UniteConditionnement_idUniteConditionnement` ASC) ,
  CONSTRAINT `fk_Medicament_VoiesAdministration`
    FOREIGN KEY (`VoiesAdministration_idVoiesAdministration` )
    REFERENCES `OpenVet12`.`VoiesAdministration` (`idVoiesAdministration` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Medicament_UniteConditionnement`
    FOREIGN KEY (`UniteConditionnement_idUniteConditionnement` )
    REFERENCES `OpenVet12`.`UniteConditionnement` (`idUniteConditionnement` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`MoleculeGenre`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`MoleculeGenre` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`MoleculeGenre` (
  `idMoleculeGenre` INT NOT NULL ,
  `Genre` VARCHAR(45) NULL ,
  PRIMARY KEY (`idMoleculeGenre`) ,
  UNIQUE INDEX `Groupe_UNIQUE` (`Genre` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`MoleculeFamille`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`MoleculeFamille` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`MoleculeFamille` (
  `idMoleculeFamille` INT NOT NULL AUTO_INCREMENT ,
  `Famille` VARCHAR(45) NULL ,
  `MoleculeGenre_idMoleculeGenre` INT NOT NULL ,
  PRIMARY KEY (`idMoleculeFamille`) ,
  INDEX `fk_MoleculeFamille_MoleculeGenres1_idx` (`MoleculeGenre_idMoleculeGenre` ASC) ,
  CONSTRAINT `fk_MoleculeFamille_MoleculeGenres1`
    FOREIGN KEY (`MoleculeGenre_idMoleculeGenre` )
    REFERENCES `OpenVet12`.`MoleculeGenre` (`idMoleculeGenre` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Molecule`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Molecule` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Molecule` (
  `idMolecule` INT NOT NULL AUTO_INCREMENT ,
  `MoleculeFamille_idMoleculeFamille` INT NOT NULL ,
  `Molecule` VARCHAR(45) NULL ,
  PRIMARY KEY (`idMolecule`) ,
  INDEX `fk_Molecules_MoleculeFamille1_idx` (`MoleculeFamille_idMoleculeFamille` ASC) ,
  CONSTRAINT `fk_Molecules_MoleculeFamille1`
    FOREIGN KEY (`MoleculeFamille_idMoleculeFamille` )
    REFERENCES `OpenVet12`.`MoleculeFamille` (`idMoleculeFamille` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`MoleculePosologie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`MoleculePosologie` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`MoleculePosologie` (
  `idMoleculePosologie` INT NOT NULL AUTO_INCREMENT ,
  `Molecule_idMolecule` INT NOT NULL ,
  `Especes_idEspeces` INT NOT NULL ,
  `VoiesAdministration_idVoiesAdministration` INT NOT NULL ,
  `AutreAdministration` VARCHAR(80) NULL ,
  `PosologieMin_mgkg` DECIMAL(6,2) NULL ,
  `PosologieMax_mgkg` DECIMAL(6,2) NULL ,
  `FrequenceJour` DECIMAL(4,2) NULL ,
  `Specialite` VARCHAR(80) NULL ,
  `Remarque` VARCHAR(200) NULL ,
  PRIMARY KEY (`idMoleculePosologie`) ,
  INDEX `fk_PosologiesMolecules_Molecules1_idx` (`Molecule_idMolecule` ASC) ,
  INDEX `fk_PosologiesMolecules_VoiesAdministration1_idx` (`VoiesAdministration_idVoiesAdministration` ASC) ,
  INDEX `fk_MoleculesPosologies_Espece_idx` (`Especes_idEspeces` ASC) ,
  CONSTRAINT `fk_PosologiesMolecules_Molecules1`
    FOREIGN KEY (`Molecule_idMolecule` )
    REFERENCES `OpenVet12`.`Molecule` (`idMolecule` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PosologiesMolecules_VoiesAdministration1`
    FOREIGN KEY (`VoiesAdministration_idVoiesAdministration` )
    REFERENCES `OpenVet12`.`VoiesAdministration` (`idVoiesAdministration` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MoleculesPosologies_Espece`
    FOREIGN KEY (`Especes_idEspeces` )
    REFERENCES `OpenVet12`.`Especes` (`idEspeces` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`MedicamentConcentration`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`MedicamentConcentration` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`MedicamentConcentration` (
  `idMedicamentConcentration` INT NOT NULL AUTO_INCREMENT ,
  `Concentration_mg` DECIMAL(6,2) NULL ,
  `Molecule_idMolecule` INT NOT NULL ,
  `Medicament_idMedicament` INT NOT NULL ,
  PRIMARY KEY (`idMedicamentConcentration`) ,
  INDEX `fk_MedicamentConcentrations_Molecules1_idx` (`Molecule_idMolecule` ASC) ,
  INDEX `fk_MedicamentConcentrations_Medicament1_idx` (`Medicament_idMedicament` ASC) ,
  CONSTRAINT `fk_MedicamentConcentrations_Molecules1`
    FOREIGN KEY (`Molecule_idMolecule` )
    REFERENCES `OpenVet12`.`Molecule` (`idMolecule` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MedicamentConcentrations_Medicament1`
    FOREIGN KEY (`Medicament_idMedicament` )
    REFERENCES `OpenVet12`.`Medicament` (`idMedicament` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'Erreur GetMedicament(2)';


-- -----------------------------------------------------
-- Table `OpenVet12`.`Examen`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Examen` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Examen` (
  `idExamen` INT NOT NULL AUTO_INCREMENT ,
  `Examen` VARCHAR(60) NOT NULL ,
  PRIMARY KEY (`idExamen`) ,
  UNIQUE INDEX `Examen_UNIQUE` (`Examen` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Critere`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Critere` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Critere` (
  `idCritere` INT NOT NULL AUTO_INCREMENT ,
  `Pathologie_idPathologie` INT NOT NULL ,
  `Examen_idExamen` INT NOT NULL ,
  `Critere` VARCHAR(60) NOT NULL ,
  `Unite` VARCHAR(20) NULL ,
  `NbGrades` INT NULL ,
  `Remarque` TEXT NULL COMMENT 'Regles de scoring' ,
  PRIMARY KEY (`idCritere`) ,
  UNIQUE INDEX `Critere_UNIQUE` (`Critere` ASC) ,
  INDEX `fk_Criteres_Pathologie_idx` (`Pathologie_idPathologie` ASC) ,
  INDEX `fk_Criteres_Examens_idx` (`Examen_idExamen` ASC) ,
  CONSTRAINT `fk_Criteres_Pathologie`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet12`.`Pathologie` (`idPathologie` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Criteres_Examens`
    FOREIGN KEY (`Examen_idExamen` )
    REFERENCES `OpenVet12`.`Examen` (`idExamen` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`PathologieDocument`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`PathologieDocument` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`PathologieDocument` (
  `idPathologieDocument` INT NOT NULL AUTO_INCREMENT ,
  `Document` VARCHAR(80) NOT NULL ,
  PRIMARY KEY (`idPathologieDocument`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`DocumentsRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`DocumentsRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`DocumentsRef` (
  `idDocumentsRef` INT NOT NULL AUTO_INCREMENT ,
  `PathologieDocument_idPathologieDocument` INT NOT NULL ,
  `Pathologie_idPathologie` INT NOT NULL ,
  PRIMARY KEY (`idDocumentsRef`) ,
  INDEX `fk_DocumentsRef_Documents1_idx` (`PathologieDocument_idPathologieDocument` ASC) ,
  INDEX `fk_DocumentsRef_Pathologie1_idx` (`Pathologie_idPathologie` ASC) ,
  CONSTRAINT `fk_DocumentsRef_PathologieDocuments`
    FOREIGN KEY (`PathologieDocument_idPathologieDocument` )
    REFERENCES `OpenVet12`.`PathologieDocument` (`idPathologieDocument` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DocumentsRef_Pathologie`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet12`.`Pathologie` (`idPathologie` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`TypeConsultation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`TypeConsultation` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`TypeConsultation` (
  `idTypeConsultation` INT NOT NULL AUTO_INCREMENT ,
  `TypeConsultation` VARCHAR(45) NULL ,
  PRIMARY KEY (`idTypeConsultation`) ,
  UNIQUE INDEX `TypeConsultation_UNIQUE` (`TypeConsultation` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Parametres`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Parametres` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Parametres` (
  `idParametres` INT NOT NULL AUTO_INCREMENT ,
  `AnalysesTypes_idAnalysesTypes` INT NOT NULL ,
  `Especes_idEspeces` INT NOT NULL ,
  `Parametre` VARCHAR(60) NOT NULL ,
  `IsQuantitatif` TINYINT(1) NOT NULL ,
  `Unite` VARCHAR(20) NULL ,
  `NormeMin` DECIMAL(8,2) NULL ,
  `NormeMax` DECIMAL(8,2) NULL ,
  `Remarque` VARCHAR(200) NULL ,
  PRIMARY KEY (`idParametres`) ,
  INDEX `fk_ParametresQuant_AnalysesTypes1_idx` (`AnalysesTypes_idAnalysesTypes` ASC) ,
  INDEX `fk_ParametresQuant_Especes1_idx` (`Especes_idEspeces` ASC) ,
  CONSTRAINT `fk_ParametresQuant_AnalysesTypes1`
    FOREIGN KEY (`AnalysesTypes_idAnalysesTypes` )
    REFERENCES `OpenVet12`.`TypeAnalyse` (`idTypeAnalyse` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ParametresQuant_Especes1`
    FOREIGN KEY (`Especes_idEspeces` )
    REFERENCES `OpenVet12`.`Especes` (`idEspeces` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`ResultatAnalyse`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ResultatAnalyse` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ResultatAnalyse` (
  `idResultatAnalyse` INT NOT NULL AUTO_INCREMENT ,
  `Analyse_idAnalyse` INT NOT NULL ,
  `Parametres_idParametres` INT NULL ,
  `Valeur` DECIMAL(8,2) NULL ,
  `Image` VARCHAR(80) NULL COMMENT 'fichier image jpg,png,dicom' ,
  `TitreImage` VARCHAR(120) NULL ,
  `Description` TINYTEXT NULL ,
  `FichierExterne` VARCHAR(80) NULL COMMENT 'Scan de CR papier' ,
  `Remarque` VARCHAR(200) NULL ,
  PRIMARY KEY (`idResultatAnalyse`) ,
  INDEX `fk_ResutatQant_ParametresQuant1_idx` (`Parametres_idParametres` ASC) ,
  CONSTRAINT `fk_ResultatLiquide_Parametres`
    FOREIGN KEY (`Parametres_idParametres` )
    REFERENCES `OpenVet12`.`Parametres` (`idParametres` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`PathologieRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`PathologieRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`PathologieRef` (
  `idPathologieRef` INT NOT NULL AUTO_INCREMENT ,
  `Consultation_idConsultation` INT NOT NULL ,
  `Pathologie_idPathologie` INT NOT NULL ,
  PRIMARY KEY (`idPathologieRef`) ,
  INDEX `fk_PathologieRef_Consultation_idx` (`Consultation_idConsultation` ASC) ,
  INDEX `fk_PathologieRef_Pathologie1_idx` (`Pathologie_idPathologie` ASC) ,
  CONSTRAINT `fk_PathologieRef_Consultation`
    FOREIGN KEY (`Consultation_idConsultation` )
    REFERENCES `OpenVet12`.`Consultation` (`idConsultation` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PathologieRef_Pathologie`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet12`.`Pathologie` (`idPathologie` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`ConsultationCritere`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ConsultationCritere` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ConsultationCritere` (
  `idConsultationCritere` INT NOT NULL AUTO_INCREMENT ,
  `Critere_idCritere` INT NOT NULL ,
  `Consultation_idConsultation` INT NOT NULL ,
  `CritereQuantitatif` DECIMAL(8,2) NULL ,
  `CritereQualitatif` VARCHAR(20) NULL ,
  `Grade` VARCHAR(20) NULL ,
  PRIMARY KEY (`idConsultationCritere`) ,
  INDEX `fk_ConsultationCriteres_Criteres_idx` (`Critere_idCritere` ASC) ,
  INDEX `fk_ConsultationCritere_Consultation_idx` (`Consultation_idConsultation` ASC) ,
  CONSTRAINT `fk_ConsultationCriteres_Criteres`
    FOREIGN KEY (`Critere_idCritere` )
    REFERENCES `OpenVet12`.`Critere` (`idCritere` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ConsultationCritere_Consultation`
    FOREIGN KEY (`Consultation_idConsultation` )
    REFERENCES `OpenVet12`.`Consultation` (`idConsultation` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`PathologieEspece`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`PathologieEspece` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`PathologieEspece` (
  `idPathologieEspece` INT NOT NULL AUTO_INCREMENT ,
  `Pathologie_idPathologie` INT NOT NULL ,
  `Especes_idEspeces` INT NOT NULL ,
  PRIMARY KEY (`idPathologieEspece`) ,
  INDEX `fk_PathologieEspeces_Pathologie_idx` (`Pathologie_idPathologie` ASC) ,
  INDEX `fk_PathologieEspeces_Especes_idx` (`Especes_idEspeces` ASC) ,
  CONSTRAINT `fk_PathologieEspeces_Pathologie`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet12`.`Pathologie` (`idPathologie` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PathologieEspeces_Especes`
    FOREIGN KEY (`Especes_idEspeces` )
    REFERENCES `OpenVet12`.`Especes` (`idEspeces` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'TODEBUG\n';


-- -----------------------------------------------------
-- Table `OpenVet12`.`ChirurgieLibele`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ChirurgieLibele` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ChirurgieLibele` (
  `idChirurgieLibele` INT NOT NULL AUTO_INCREMENT ,
  `Libele` VARCHAR(60) NULL ,
  `Sexe` VARCHAR(1) NULL DEFAULT NULL ,
  PRIMARY KEY (`idChirurgieLibele`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Chirurgie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Chirurgie` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Chirurgie` (
  `idChirurgie` INT NOT NULL AUTO_INCREMENT ,
  `Consultation_idConsultation` INT NOT NULL ,
  `Description` VARCHAR(200) NULL ,
  `Anesthesie` VARCHAR(200) NULL ,
  `Commentaire` TEXT NULL ,
  `TraitementPerop` VARCHAR(45) NULL ,
  `CompteRendu` VARCHAR(45) NULL COMMENT 'Lien Fichier\n' ,
  PRIMARY KEY (`idChirurgie`) ,
  INDEX `fk_Chirurgie_1_idx` (`Consultation_idConsultation` ASC) ,
  CONSTRAINT `fk_Chirurgie_Consultation`
    FOREIGN KEY (`Consultation_idConsultation` )
    REFERENCES `OpenVet12`.`Consultation` (`idConsultation` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`ChirurgieRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ChirurgieRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ChirurgieRef` (
  `idChirurgieRef` INT NOT NULL AUTO_INCREMENT ,
  `Chirurgie_idChirurgie` INT NOT NULL ,
  `ChirurgieLibele_idChirurgieLibele` INT NOT NULL ,
  PRIMARY KEY (`idChirurgieRef`) ,
  INDEX `fk_ChirurgieRef_Chirurgie_idx` (`Chirurgie_idChirurgie` ASC) ,
  INDEX `fk_ChirurgieRef_ChirurgieLibele_idx` (`ChirurgieLibele_idChirurgieLibele` ASC) ,
  CONSTRAINT `fk_Chirurgieref_Chirurgie`
    FOREIGN KEY (`Chirurgie_idChirurgie` )
    REFERENCES `OpenVet12`.`Chirurgie` (`idChirurgie` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Chirurgieref_ChirurgieLibele`
    FOREIGN KEY (`ChirurgieLibele_idChirurgieLibele` )
    REFERENCES `OpenVet12`.`ChirurgieLibele` (`idChirurgieLibele` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`ModelCompteRenduChirurgie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ModelCompteRenduChirurgie` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ModelCompteRenduChirurgie` (
  `idModelCompteRenduChirurgie` INT NOT NULL AUTO_INCREMENT ,
  `ChirurgieLibele_idChirurgieLibele` INT NOT NULL ,
  `ModelCompteRendu` VARCHAR(80) NULL COMMENT 'Lien Fichier\n' ,
  PRIMARY KEY (`idModelCompteRenduChirurgie`) ,
  INDEX `fk_ModelCompte-renduChirurgie_ChirurgieLibele1_idx` (`ChirurgieLibele_idChirurgieLibele` ASC) ,
  CONSTRAINT `fk_ModelCompte-renduChirurgie_ChirurgieLibele1`
    FOREIGN KEY (`ChirurgieLibele_idChirurgieLibele` )
    REFERENCES `OpenVet12`.`ChirurgieLibele` (`idChirurgieLibele` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`PathologieSynonyme`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`PathologieSynonyme` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`PathologieSynonyme` (
  `idPathologieSynonyme` INT NOT NULL AUTO_INCREMENT ,
  `Pathologie_idPathologie` INT NOT NULL ,
  `Synonyme` VARCHAR(60) NULL ,
  PRIMARY KEY (`idPathologieSynonyme`) ,
  INDEX `fk_PathologieSynonymes_Pathologie1_idx` (`Pathologie_idPathologie` ASC) ,
  CONSTRAINT `fk_PathologieSynonymes_Pathologie1`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet12`.`Pathologie` (`idPathologie` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`PathologieDomaine`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`PathologieDomaine` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`PathologieDomaine` (
  `idPathologieDomaine` INT NOT NULL AUTO_INCREMENT ,
  `Domaine` VARCHAR(60) NOT NULL ,
  PRIMARY KEY (`idPathologieDomaine`) ,
  UNIQUE INDEX `Domaine_UNIQUE` (`Domaine` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`TypeConsultationRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`TypeConsultationRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`TypeConsultationRef` (
  `idTypeRef` INT NOT NULL AUTO_INCREMENT ,
  `Consultation_idConsultation` INT NOT NULL ,
  `TypeConsultation_idTypeConsultation` INT NOT NULL ,
  PRIMARY KEY (`idTypeRef`) ,
  INDEX `fk_TypeRef_Consultation_idx` (`Consultation_idConsultation` ASC) ,
  INDEX `fk_TypeRef_TypeRef_idx` (`TypeConsultation_idTypeConsultation` ASC) ,
  CONSTRAINT `fk_TypeRef_Consultation`
    FOREIGN KEY (`Consultation_idConsultation` )
    REFERENCES `OpenVet12`.`Consultation` (`idConsultation` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_TypeRef_TypeRef`
    FOREIGN KEY (`TypeConsultation_idTypeConsultation` )
    REFERENCES `OpenVet12`.`TypeConsultation` (`idTypeConsultation` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`CentraleClasse`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`CentraleClasse` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`CentraleClasse` (
  `CodeClasse` VARCHAR(8) NOT NULL ,
  `Classe` VARCHAR(60) NULL ,
  `Cibles` VARCHAR(60) NULL ,
  `Indication` VARCHAR(60) NULL ,
  PRIMARY KEY (`CodeClasse`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`CentraleTarif`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`CentraleTarif` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`CentraleTarif` (
  `idCentraleTarif` INT NOT NULL AUTO_INCREMENT ,
  `CentraleClasse_CodeClasse` VARCHAR(8) NULL ,
  `Cip` VARCHAR(8) NULL ,
  `Designation` VARCHAR(50) NULL ,
  `Labo` VARCHAR(45) NULL ,
  `TVA` DECIMAL(4,2) NULL ,
  `PrixHT` DECIMAL(6,2) NULL ,
  `CodeCentrale` VARCHAR(8) NULL ,
  PRIMARY KEY (`idCentraleTarif`) ,
  UNIQUE INDEX `CodeCentrale_UNIQUE` (`CodeCentrale` ASC) ,
  INDEX `fk_CentraleTarifs_CentraleClasses_idx` (`CentraleClasse_CodeClasse` ASC) ,
  CONSTRAINT `fk_CentraleTarifs_CentraleClasses`
    FOREIGN KEY (`CentraleClasse_CodeClasse` )
    REFERENCES `OpenVet12`.`CentraleClasse` (`CodeClasse` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`ContreIndication`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ContreIndication` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ContreIndication` (
  `idContreIndication` INT NOT NULL AUTO_INCREMENT ,
  `ContreIndication` VARCHAR(80) NULL ,
  PRIMARY KEY (`idContreIndication`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`ContreIndicationRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ContreIndicationRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ContreIndicationRef` (
  `idContreIndicationRef` INT NOT NULL AUTO_INCREMENT ,
  `ContreIndication_idContreIndication` INT NULL ,
  `Molecule_idMolecule` INT NULL ,
  PRIMARY KEY (`idContreIndicationRef`) ,
  INDEX `fk_ContreIndicationRef_Molecules_idx` (`Molecule_idMolecule` ASC) ,
  INDEX `fk_ContreIndicationRef_ContreIndications_idx` (`ContreIndication_idContreIndication` ASC) ,
  CONSTRAINT `fk_ContreIndicationRef_Molecules`
    FOREIGN KEY (`Molecule_idMolecule` )
    REFERENCES `OpenVet12`.`Molecule` (`idMolecule` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ContreIndicationRef_ContreIndications`
    FOREIGN KEY (`ContreIndication_idContreIndication` )
    REFERENCES `OpenVet12`.`ContreIndication` (`idContreIndication` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`PathologieMoleculeRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`PathologieMoleculeRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`PathologieMoleculeRef` (
  `idPathologieMoleculeRef` INT NOT NULL AUTO_INCREMENT ,
  `Pathologie_idPathologie` INT NULL ,
  `MoleculePosologie_idMoleculePosologie` INT NULL ,
  PRIMARY KEY (`idPathologieMoleculeRef`) ,
  INDEX `fk_PathologieMoldeculeRef_Pathologie_idx` (`Pathologie_idPathologie` ASC) ,
  INDEX `fk_PathologieMoldeculeRef_MoleculesPosologie_idx` (`MoleculePosologie_idMoleculePosologie` ASC) ,
  CONSTRAINT `fk_PathologieMoleculeRef_Pathologie`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet12`.`Pathologie` (`idPathologie` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PathologieMoleculeRef_MoleculesPosologie`
    FOREIGN KEY (`MoleculePosologie_idMoleculePosologie` )
    REFERENCES `OpenVet12`.`MoleculePosologie` (`idMoleculePosologie` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`ClientAnimalRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ClientAnimalRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ClientAnimalRef` (
  `idClientAnimalRef` INT NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT NOT NULL ,
  `Animal_idAnimal` INT NOT NULL ,
  `DebutPropriete` DATE NOT NULL ,
  `FinPropriete` DATE NULL ,
  `PourcentagePropriete` DECIMAL(4,2) NULL ,
  PRIMARY KEY (`idClientAnimalRef`) ,
  INDEX `fk_ClientAnimalRef_Client_idx` (`Client_idClient` ASC) ,
  INDEX `fk_ClientAnimalRef_Animal_idx` (`Animal_idAnimal` ASC) ,
  CONSTRAINT `fk_ClientAnimalRef_Client`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet12`.`Personne` (`idPersonne` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ClientAnimalRef_Animal`
    FOREIGN KEY (`Animal_idAnimal` )
    REFERENCES `OpenVet12`.`Animal` (`idAnimal` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`ComptebancaireClient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ComptebancaireClient` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ComptebancaireClient` (
  `idCompte bancaire` INT NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT NOT NULL ,
  `NCompteRIB` VARCHAR(45) NULL ,
  `NoCompteIBAN` VARCHAR(45) NULL ,
  `BanqueNom` VARCHAR(20) NULL ,
  `Adresse` VARCHAR(120) NULL ,
  `Commune_idCommune` INT NULL ,
  `Actif` TINYINT(1) NULL ,
  `Commentaires` VARCHAR(200) NULL ,
  PRIMARY KEY (`idCompte bancaire`) ,
  INDEX `fk_ComptebancaireClient_Client_idx` (`Client_idClient` ASC) ,
  INDEX `fk_ComptebancaireClient_Commune_idx` (`Commune_idCommune` ASC) ,
  CONSTRAINT `fk_ComptebancaireClient_Client`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet12`.`Personne` (`idPersonne` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ComptebancaireClient_Commune`
    FOREIGN KEY (`Commune_idCommune` )
    REFERENCES `OpenVet12`.`Commune` (`idCommune` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Repertoire`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Repertoire` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Repertoire` (
  `idRepertoire` INT NOT NULL AUTO_INCREMENT ,
  `RefTable` VARCHAR(45) NOT NULL COMMENT 'Client, Collaborateur, Societe,ComptebancaireClient\nMettre un INT pour meileurs cle' ,
  `id` INT NULL ,
  `Telephone` VARCHAR(12) NULL ,
  `Email` VARCHAR(30) NULL ,
  `Remarque` VARCHAR(200) NULL ,
  `IsPrincipal` TINYINT(1) NULL ,
  `IsRelance` VARCHAR(45) NULL COMMENT 'Valide pour relances\n' ,
  PRIMARY KEY (`idRepertoire`) )
ENGINE = InnoDB
COMMENT = 'Trigger sur table parente pour supprimer enregistrements';


-- -----------------------------------------------------
-- Table `OpenVet12`.`RemiseClient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`RemiseClient` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`RemiseClient` (
  `idRemiseClient` INT NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT NOT NULL ,
  `Designation` VARCHAR(120) NULL ,
  `Montant%` INT NULL ,
  `Actif` TINYINT(1) NULL ,
  `Commentaires` VARCHAR(200) NULL ,
  PRIMARY KEY (`idRemiseClient`) ,
  INDEX `fk_Remises_Client_idx` (`Client_idClient` ASC) ,
  CONSTRAINT `fk_Remises_Client`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet12`.`Personne` (`idPersonne` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`RelanceFacture`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`RelanceFacture` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`RelanceFacture` (
  `idRelanceFacture` INT NOT NULL AUTO_INCREMENT ,
  `Facture_idFacture` INT(11) NOT NULL ,
  `Date` DATE NULL ,
  `NiveauRelance` VARCHAR(45) NULL ,
  `MontantPrincipal` DECIMAL(6,2) NULL ,
  `MontantFrais` DECIMAL(6,2) NULL ,
  `Actif` TINYINT(1) NULL ,
  `Remarques` VARCHAR(200) NULL ,
  PRIMARY KEY (`idRelanceFacture`) ,
  INDEX `fk_RelanceFacture_Facture1_idx` (`Facture_idFacture` ASC) ,
  CONSTRAINT `fk_RelanceFacture_Facture1`
    FOREIGN KEY (`Facture_idFacture` )
    REFERENCES `OpenVet12`.`Facture` (`idFacture` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`TVA`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`TVA` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`TVA` (
  `idTVA` INT NOT NULL AUTO_INCREMENT ,
  `Taux` DECIMAL(6,2) NOT NULL ,
  `Actif` TINYINT(1) NULL ,
  PRIMARY KEY (`idTVA`) ,
  UNIQUE INDEX `Taux_UNIQUE` (`Taux` ASC) )
ENGINE = InnoDB
COMMENT = '\n';


-- -----------------------------------------------------
-- Table `OpenVet12`.`PrixActe`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`PrixActe` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`PrixActe` (
  `idPrixActe` INT NOT NULL AUTO_INCREMENT ,
  `Designation` VARCHAR(80) NOT NULL ,
  `NbAMO` DECIMAL(6,2) NULL ,
  `Montant TTC` DECIMAL(6,2) NULL ,
  `MontantHT` DECIMAL(6,2) NULL ,
  `TVA_idTVA` INT NULL ,
  UNIQUE INDEX `Designation_UNIQUE` (`Designation` ASC) ,
  PRIMARY KEY (`idPrixActe`) ,
  INDEX `fk_PrixActe_TVA_idx` (`TVA_idTVA` ASC) ,
  CONSTRAINT `fk_PrixActe_TVA`
    FOREIGN KEY (`TVA_idTVA` )
    REFERENCES `OpenVet12`.`TVA` (`idTVA` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`FacturationConfig`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`FacturationConfig` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`FacturationConfig` (
  `idFacturationConfig` INT NOT NULL AUTO_INCREMENT ,
  `AMO` DECIMAL(6,2) NULL ,
  `Arrondi` DECIMAL(6,2) NULL DEFAULT 0.05 ,
  `Monnaie` VARCHAR(20) NULL DEFAULT 'Euro' ,
  `AbrevMonnaie` VARCHAR(5) NULL DEFAULT '€' ,
  PRIMARY KEY (`idFacturationConfig`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Incineration`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Incineration` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Incineration` (
  `idIncineration` INT NOT NULL AUTO_INCREMENT ,
  `Animal_idAnimal` INT NOT NULL ,
  `NumeroConvention` VARCHAR(20) NULL ,
  `DateEnlevement` DATE NULL ,
  `DateRetour` VARCHAR(45) NULL ,
  `DateRecuperationClient` VARCHAR(45) NULL ,
  `Individuelle` TINYINT(1) NULL ,
  `Societe_idSociete` INT NULL COMMENT '\n' ,
  PRIMARY KEY (`idIncineration`) ,
  UNIQUE INDEX `NumeroConvention_UNIQUE` (`NumeroConvention` ASC) ,
  UNIQUE INDEX `Animal_idAnimal_UNIQUE` (`Animal_idAnimal` ASC) ,
  INDEX `fk_Incineration_Animal_idx` (`Animal_idAnimal` ASC) ,
  INDEX `fk_Incineration_Fournisseur_idx` (`Societe_idSociete` ASC) ,
  CONSTRAINT `fk_Incineration_Animal`
    FOREIGN KEY (`Animal_idAnimal` )
    REFERENCES `OpenVet12`.`Animal` (`idAnimal` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Incineration_Fournisseur`
    FOREIGN KEY (`Societe_idSociete` )
    REFERENCES `OpenVet12`.`Societe` (`idSociete` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`LienPersonne`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`LienPersonne` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`LienPersonne` (
  `idLienFamille` INT NOT NULL AUTO_INCREMENT ,
  `Client_idClient1` INT NOT NULL ,
  `client_idClient2` INT NOT NULL ,
  `TypeRelation` VARCHAR(45) NULL COMMENT 'TODO table externe?\nInclure Tutelle\n' ,
  `IsTutelle` TINYINT(1) NULL DEFAULT FALSE ,
  `Actif` TINYINT(1) NULL ,
  `Commentaires` VARCHAR(200) NULL ,
  PRIMARY KEY (`idLienFamille`) ,
  INDEX `fk_LienFamille_Client_idx` (`Client_idClient1` ASC) ,
  INDEX `fk_LienFamille_Parent_idx` (`client_idClient2` ASC) ,
  CONSTRAINT `fk_LienFamille_Client1`
    FOREIGN KEY (`Client_idClient1` )
    REFERENCES `OpenVet12`.`Personne` (`idPersonne` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_LienFamille_Client2`
    FOREIGN KEY (`client_idClient2` )
    REFERENCES `OpenVet12`.`Personne` (`idPersonne` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`RendezVous`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`RendezVous` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`RendezVous` (
  `idRendezVous` INT NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT NOT NULL ,
  `Date` DATETIME NULL ,
  `NomAnimal` VARCHAR(80) NULL ,
  `Animal_idAnimal` INT NULL ,
  `Motif` VARCHAR(80) NULL ,
  `PasVenu` TINYINT(1) NULL ,
  `MinutesDeRetard` TINYINT NULL ,
  `Veterinaires_idVeterinaires` INT NULL DEFAULT NULL ,
  `SalleAttente` TINYINT(1) NULL DEFAULT FALSE ,
  `PrisEnCharge` TINYINT(1) NULL DEFAULT FALSE ,
  `Hospitalisation` TINYINT(1) NULL DEFAULT FALSE ,
  `Commentaires` VARCHAR(200) NULL ,
  `Actif` TINYINT(1) NULL ,
  PRIMARY KEY (`idRendezVous`) ,
  INDEX `fk_RendezVous_Client_idx` (`Client_idClient` ASC) ,
  INDEX `fk_RendezVous_Animal1_idx` (`Animal_idAnimal` ASC) ,
  CONSTRAINT `fk_RendezVous_Client`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet12`.`Personne` (`idPersonne` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_RendezVous_Animal1`
    FOREIGN KEY (`Animal_idAnimal` )
    REFERENCES `OpenVet12`.`Animal` (`idAnimal` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Materiel`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Materiel` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Materiel` (
  `idMateriel` INT NOT NULL AUTO_INCREMENT ,
  `Societe_idSociete` INT NULL ,
  `Collaborateur_idCollaborateur` INT NULL COMMENT 'SAV\n' ,
  `TypeAnalyse_TypeAnalyse` INT NULL ,
  `NomAppareil` VARCHAR(60) NULL ,
  `DateAchat` VARCHAR(45) NULL ,
  `PrixHT` DECIMAL(8,2) NULL ,
  `DateOpeMaintenance` DATETIME NULL COMMENT 'Prochaine opération de maintenance\n' ,
  `LibeleOpeMaintenance` VARCHAR(80) NULL ,
  `Remarques` VARCHAR(200) NULL ,
  `Actif` TINYINT(1) NULL ,
  PRIMARY KEY (`idMateriel`) ,
  INDEX `fk_Materiel_1_idx` (`Societe_idSociete` ASC) ,
  INDEX `fk_Materiel_1_idx1` (`TypeAnalyse_TypeAnalyse` ASC) ,
  CONSTRAINT `fk_Materiel_Societe`
    FOREIGN KEY (`Societe_idSociete` )
    REFERENCES `OpenVet12`.`Societe` (`idSociete` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Materiel_TypeAnalyse`
    FOREIGN KEY (`TypeAnalyse_TypeAnalyse` )
    REFERENCES `OpenVet12`.`TypeAnalyse` (`idTypeAnalyse` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Historique`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Historique` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Historique` (
  `idHistorique` INT NOT NULL AUTO_INCREMENT ,
  `Temps` TIMESTAMP NOT NULL COMMENT 'Instant de la Modification\n' ,
  `Table` VARCHAR(60) NOT NULL COMMENT 'Table Modifiée\n' ,
  `Utilisateur` VARCHAR(60) NOT NULL ,
  PRIMARY KEY (`idHistorique`) ,
  UNIQUE INDEX `Utilisateur_UNIQUE` (`Utilisateur` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`ParametreBase`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ParametreBase` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ParametreBase` (
  `idParametreBase` INT NOT NULL AUTO_INCREMENT ,
  `CodeParametre` VARCHAR(20) NOT NULL ,
  `LibeleParametre` VARCHAR(60) NOT NULL ,
  `Valeur` VARCHAR(45) NULL COMMENT 'Colonne no-sql? ou virtuelle avec dbMaria\n' ,
  `TypeValeur` VARCHAR(10) NULL ,
  PRIMARY KEY (`idParametreBase`) ,
  UNIQUE INDEX `TypeValeur_UNIQUE` (`TypeValeur` ASC) ,
  UNIQUE INDEX `CodeParametre_UNIQUE` (`CodeParametre` ASC) ,
  UNIQUE INDEX `LibeleParametre_UNIQUE` (`LibeleParametre` ASC) )
ENGINE = InnoDB
COMMENT = 'Mettre parametres de facturation? Chemins de répertoire';


-- -----------------------------------------------------
-- Table `OpenVet12`.`Service`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Service` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Service` (
  `idService` INT NOT NULL ,
  `Nom` VARCHAR(60) NULL ,
  PRIMARY KEY (`idService`) )
ENGINE = InnoDB
COMMENT = 'ex service client\n';


-- -----------------------------------------------------
-- Table `OpenVet12`.`Societe_has_Service`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Societe_has_Service` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Societe_has_Service` (
  `Service_idService` INT NOT NULL ,
  `Societe_idSociete` INT NOT NULL ,
  `NoTelephone1` VARCHAR(20) NULL ,
  `NoTelephone2` VARCHAR(20) NULL ,
  `Mail` VARCHAR(60) NULL ,
  `Personne_idPersonne` INT NULL COMMENT 'optionnel' ,
  PRIMARY KEY (`Service_idService`, `Societe_idSociete`) ,
  INDEX `fk_Service_has_Societe_Societe1_idx` (`Societe_idSociete` ASC) ,
  INDEX `fk_Service_has_Societe_Service1_idx` (`Service_idService` ASC) ,
  INDEX `fk_Societe_has_Service_Personne1_idx` (`Personne_idPersonne` ASC) ,
  CONSTRAINT `fk_Service_has_Societe_Service1`
    FOREIGN KEY (`Service_idService` )
    REFERENCES `OpenVet12`.`Service` (`idService` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Service_has_Societe_Societe1`
    FOREIGN KEY (`Societe_idSociete` )
    REFERENCES `OpenVet12`.`Societe` (`idSociete` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Societe_has_Service_Personne1`
    FOREIGN KEY (`Personne_idPersonne` )
    REFERENCES `OpenVet12`.`Personne` (`idPersonne` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`HistoriqueDesAppels`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`HistoriqueDesAppels` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`HistoriqueDesAppels` (
  `idHistoriqueDesAppels` INT NOT NULL ,
  `Date` DATETIME NULL ,
  `Personne_idPersonne` INT NOT NULL ,
  `Commentaires` VARCHAR(200) NULL ,
  `Actif` TINYINT(1) NULL ,
  PRIMARY KEY (`idHistoriqueDesAppels`) ,
  INDEX `fk_HistoriqueDesAppels_Personne1_idx` (`Personne_idPersonne` ASC) ,
  CONSTRAINT `fk_HistoriqueDesAppels_Personne1`
    FOREIGN KEY (`Personne_idPersonne` )
    REFERENCES `OpenVet12`.`Personne` (`idPersonne` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`Facture_has_Reglement`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Facture_has_Reglement` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Facture_has_Reglement` (
  `Facture_idFacture` INT(11) NOT NULL ,
  `Reglement_idReglement` INT(11) NOT NULL ,
  PRIMARY KEY (`Facture_idFacture`, `Reglement_idReglement`) ,
  INDEX `fk_Facture_has_Reglement_Reglement1_idx` (`Reglement_idReglement` ASC) ,
  INDEX `fk_Facture_has_Reglement_Facture1_idx` (`Facture_idFacture` ASC) ,
  CONSTRAINT `fk_Facture_has_Reglement_Facture1`
    FOREIGN KEY (`Facture_idFacture` )
    REFERENCES `OpenVet12`.`Facture` (`idFacture` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Facture_has_Reglement_Reglement1`
    FOREIGN KEY (`Reglement_idReglement` )
    REFERENCES `OpenVet12`.`Reglement` (`idReglement` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1
COMMENT = '1 ou +sieurs fact <-> 1 ou +si reglts';


-- -----------------------------------------------------
-- Table `OpenVet12`.`Consultation_has_Facture`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Consultation_has_Facture` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Consultation_has_Facture` (
  `Consultation_idConsultation` INT NOT NULL ,
  `Facture_idFacture` INT(11) NOT NULL ,
  `Actif` TINYINT(1) NULL ,
  PRIMARY KEY (`Consultation_idConsultation`, `Facture_idFacture`) ,
  INDEX `fk_Facture_has_Reglement1_Facture1_idx` (`Facture_idFacture` ASC) ,
  INDEX `fk_Consultation_has_Facture_Consultation1_idx` (`Consultation_idConsultation` ASC) ,
  CONSTRAINT `fk_Facture_has_Reglement1_Facture1`
    FOREIGN KEY (`Facture_idFacture` )
    REFERENCES `OpenVet12`.`Facture` (`idFacture` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Consultation_has_Facture_Consultation1`
    FOREIGN KEY (`Consultation_idConsultation` )
    REFERENCES `OpenVet12`.`Consultation` (`idConsultation` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1
COMMENT = '1 facture pour 1 ou + consult';


-- -----------------------------------------------------
-- Table `OpenVet12`.`Documents`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`Documents` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`Documents` (
  `idDocuments` INT NOT NULL AUTO_INCREMENT ,
  `FichierExterne` VARCHAR(80) NULL ,
  PRIMARY KEY (`idDocuments`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`DomaineRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`DomaineRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`DomaineRef` (
  `idDomaineRef` INT NOT NULL AUTO_INCREMENT ,
  `Pathologie_idPathologie` INT NOT NULL ,
  `PathologieDomaine_idPathologieDomaine` INT NOT NULL ,
  `IsPrincipal` TINYINT(1) NULL ,
  PRIMARY KEY (`idDomaineRef`) ,
  INDEX `fk_DomaineRef_Pathologie_idx` (`Pathologie_idPathologie` ASC) ,
  INDEX `fk_DomaineRef_Domaine_idx` (`PathologieDomaine_idPathologieDomaine` ASC) ,
  CONSTRAINT `fk_DomaineRef_Pathologie`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet12`.`Pathologie` (`idPathologie` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DomaineRef_Domaine`
    FOREIGN KEY (`PathologieDomaine_idPathologieDomaine` )
    REFERENCES `OpenVet12`.`PathologieDomaine` (`idPathologieDomaine` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`CritereSeuil`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`CritereSeuil` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`CritereSeuil` (
  `idCritereSeuil` INT NOT NULL AUTO_INCREMENT ,
  `Critere_idCritere` INT NULL ,
  `LimiteInf` DECIMAL(8,2) NULL ,
  `LimiteSup` DECIMAL(8,2) NULL ,
  `Grade` VARCHAR(45) NULL ,
  `Score` INT NULL ,
  PRIMARY KEY (`idCritereSeuil`) ,
  INDEX `fk_CritereSeuils_Critere_idx` (`Critere_idCritere` ASC) ,
  CONSTRAINT `fk_CritereSeuils_Critere`
    FOREIGN KEY (`Critere_idCritere` )
    REFERENCES `OpenVet12`.`Critere` (`idCritere` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`ModelExamen`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ModelExamen` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ModelExamen` (
  `idModelExamen` INT NOT NULL AUTO_INCREMENT ,
  `Examen_idExamen` INT NOT NULL ,
  `Pathologie_idPathologie` INT NOT NULL ,
  `NomModel` VARCHAR(45) NOT NULL ,
  `Remarque` VARCHAR(200) NULL ,
  PRIMARY KEY (`idModelExamen`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet12`.`ModelCritere`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet12`.`ModelCritere` ;

CREATE  TABLE IF NOT EXISTS `OpenVet12`.`ModelCritere` (
  `idModelCritere` INT NOT NULL AUTO_INCREMENT ,
  `ModelExamen_idModelExamen` INT NOT NULL ,
  `Critere_idCritere` INT NOT NULL ,
  PRIMARY KEY (`idModelCritere`) ,
  INDEX `fk_ModelCritere_ModelExamen_idx` (`ModelExamen_idModelExamen` ASC) ,
  INDEX `fk_ModelCritere_Critere_idx` (`Critere_idCritere` ASC) ,
  CONSTRAINT `fk_ModelCritere_ModelExamen`
    FOREIGN KEY (`ModelExamen_idModelExamen` )
    REFERENCES `OpenVet12`.`ModelExamen` (`idModelExamen` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ModelCritere_Critere`
    FOREIGN KEY (`Critere_idCritere` )
    REFERENCES `OpenVet12`.`Critere` (`idCritere` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `OpenVet12` ;

-- -----------------------------------------------------
-- Placeholder table for view `OpenVet12`.`viewPersonne`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OpenVet12`.`viewPersonne` (`idPersonne` INT, `Civilite_idCivilite` INT, `isClient` INT, `IsVeterinaire` INT, `isSalarie` INT, `isFournisseur` INT, `IsConsultant` INT, `IsReferant` INT, `IsReferent` INT, `IsAssocie` INT, `IsCollaborateurLiberal` INT, `IsServiceGarde` INT, `Actif` INT, `Commentaires` INT, `Nom` INT, `NomMarital` INT, `Prenom` INT, `Adresse_No` INT, `Adresse_Rue` INT, `Commune_idCommune` INT, `SousTutelle` INT, `MauvaisPayeur` INT, `Contentieux` INT, `AncienClient` INT, `ClientDePassage` INT, `NbRetardRV` INT, `NbOublieRV` INT, `NbOublieOpe` INT, `DateEntree` INT, `PartSociales` INT, `NoCARPV` INT, `NoURSSAF` INT, `NoOrdre` INT, `Specialite` INT, `Temporaire` INT, `Cadre` INT, `ConventionCollective` INT, `SalaireHoraire` INT, `Coefficient` INT, `Echellon` INT, `Emploi` INT, `LieuNaissance` INT, `DateNaissance` INT, `FinContrat` INT, `NoSecuriteSociale` INT, `TelephoneDomicile` INT, `TelephoneBureau` INT, `TelephonePortable1` INT, `TelephonePortable2` INT, `Mail` INT);

-- -----------------------------------------------------
-- Placeholder table for view `OpenVet12`.`viewCommune`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OpenVet12`.`viewCommune` (`idCommune` INT, `Commune` INT, `CIP` INT, `Pays` INT);

-- -----------------------------------------------------
-- Placeholder table for view `OpenVet12`.`viewClient`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `OpenVet12`.`viewClient` (`id` INT);

-- -----------------------------------------------------
-- procedure GetOrdonnance
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetOrdonnance`;

DELIMITER $$
USE `OpenVet12`$$





CREATE DEFINER=`root`@`localhost` PROCEDURE `GetOrdonnance`(IN IndexConsultation INT)
BEGIN
SELECT ImpressionLigne,Medicament,Posologie,UnitesDelivre
FROM LignesOrdonnances,Ordonnances
WHERE Ordonnances_idOrdonnances=idOrdonnances AND Consultation_idConsultation=IndexConsultation;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetPlanTherapeutique
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetPlanTherapeutique`;

DELIMITER $$
USE `OpenVet12`$$





CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPlanTherapeutique`(IN IndexConsultation INT)
BEGIN
SELECT idPlanTherapeutique,
(SELECT NomReference FROM Pathologie WHERE idPathologie=Pathologie_idPathologie) AS Pathologie,
(SELECT GROUP_CONCAT(CONCAT(Critere,";",CritereValeur,";",Seuil)) FROM Criteres,ConsultationCriteres WHERE PlanTherapeutique_idPlanTherapeutique=idPlanTherapeutique AND idCriteres=Criteres_idCriteres) AS Criteres,
Stade,Traitements,Remarques,ProchainRDV
FROM PlanTherapeutique
WHERE Consultation_idConsultation=Indexconsultation;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetChirurgie
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetChirurgie`;

DELIMITER $$
USE `OpenVet12`$$





CREATE DEFINER=`root`@`localhost` PROCEDURE `GetChirurgie`(IN IndexConsultation INT)
BEGIN
SELECT Description,
(SELECT GROUP_CONCAT(Libele) FROM ChirurgieLibele,ChirurgieRef WHERE idChirurgieLibele=ChirurgieLibele_idChirurgieLibele AND Chirurgie_idChirurgie=idChirurgie) AS Libele,
CompteRendu
FROM Chirurgie
WHERE Consultation_idConsultation=IndexConsultation;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetImagerie
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetImagerie`;

DELIMITER $$
USE `OpenVet12`$$










CREATE DEFINER=`root`@`localhost` PROCEDURE `GetImagerie`(IN IndexAnalyse INT)
BEGIN
SELECT 
(SELECT Description FROM Analyse WHERE idAnalyse=Analyse_idAnalyse) AS Description,
Commentaire,Conclusion,
(SELECT GROUP_CONCAT(Image) FROM Images WHERE Imagerie_idImagerie=idImagerie) AS Images,
(SELECT idResultatFichier FROM ResultatFichier WHERE Analyse_idAnalyse=IndexAnalyse) AS Document,
(SELECT IsCompteRendu FROM ResultatFichier WHERE Analyse_idAnalyse=IndexAnalyse) AS IsCompteRendu
FROM Imagerie
WHERE Analyse_idAnalyse=IndexAnalyse;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure SelectPathologie
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`SelectPathologie`;

DELIMITER $$
USE `OpenVet12`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `SelectPathologie`(IN INNomRef VARCHAR(60),IN INDomaine INT)
BEGIN
IF INDomaine=0 Then
SELECT idPathologie,NomReference FROM ScanPathologie 
WHERE NomReference LIKE CONCAT(INNomRef,"%") OR Synonymes LIKE CONCAT("%",INNomRef,"%");
ELSE
SELECT idPathologie,NomReference FROM ScanPathologie 
WHERE NomReference LIKE CONCAT(INNomRef,"%") OR Synonymes LIKE CONCAT("%",INNomRef,"%") AND idDomaine=INDomaine;
END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetPathologie
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetPathologie`;

DELIMITER $$
USE `OpenVet12`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPathologie`(IN IndexPathologie INT)
BEGIN
SELECT NomReference,Chronique,DescriptifPublic,GROUP_CONCAT(Synonyme) 
FROM Pathologie 
JOIN PathologieSynonyme ON PathologieSynonyme.Pathologie_idPathologie=idPathologie
WHERE idPathologie=IndexPathologie;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetCriteres
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetCriteres`;

DELIMITER $$
USE `OpenVet12`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `GetCriteres`(IN IndexPathologie INT, IN IndexExamen INT)
BEGIN
SELECT idCritere,Critere
FROM Critere WHERE Pathologie_idPathologie=IndexPathologie AND Examen_idExamen=IndexExamen;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetMoleculesForPathologie
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetMoleculesForPathologie`;

DELIMITER $$
USE `OpenVet12`$$








CREATE DEFINER=`root`@`localhost` PROCEDURE `GetMoleculesForPathologie`(IN IndexPathologie INT, IN IndexEspece INT)
BEGIN
SELECT
(SELECT idMolecules FROM Molecules WHERE idMolecules=MoleculesPosologies.Molecules_idMolecules) AS idMolecules,
(SELECT Molecule FROM Molecules WHERE idMolecules=MoleculesPosologies.Molecules_idMolecules) AS Molecule,
(SELECT VoieAdministration FROM VoiesAdministration WHERE idVoiesAdministration=VoiesAdministration_idVoiesAdministration) AS VoieAdmin,
PosologieMin_mgkg,PosologieMax_mgkg,FrequenceJour,AutreAdministration,Specialite,Remarque
FROM MoleculesPosologies,PathologieMoleculeRef
WHERE Pathologie_idPathologie=IndexPathologie AND Espece_idEspece=IndexEspece AND idMoleculesPosologies=MoleculesPosologies_idMoleculesPosologies;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetMolecule
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetMolecule`;

DELIMITER $$
USE `OpenVet12`$$










CREATE DEFINER=`root`@`localhost` PROCEDURE `GetMolecule`(IN IndexMolecule INT)
BEGIN
SELECT
(SELECT Molecule FROM Molecules WHERE idMolecules=MoleculesPosologies.Molecules_idMolecules) AS Molecule,
(SELECT VoieAdministration FROM VoiesAdministration WHERE idVoiesAdministration=VoiesAdministration_idVoiesAdministration) AS VoieAdmin,
PosologieMin_mgkg,PosologieMax_mgkg,FrequenceJour,AutreAdministration,Specialite,
(SELECT GROUP_CONCAT(NomReference) FROM Pathologie,PathologieMoleculeRef WHERE idPathologie=Pathologie_idPathologie AND MoleculesPosologies_idMoleculesPosologies=idMoleculesPosologies) AS Indications,
(SELECT GROUP_CONCAT(ContreIndication) FROM ContreIndications,ContreIndicationRef WHERE Molecules_idMolecules=MoleculesPosologies.Molecules_idMolecules AND idContreIndications=ContreIndications_idContreIndications) AS ContreIndications,
Remarque
FROM MoleculesPosologies,PathologieMoleculeRef
WHERE Molecules_idMolecules=IndexMolecule;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetMedicament
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetMedicament`;

DELIMITER $$
USE `OpenVet12`$$










CREATE DEFINER=`root`@`localhost` PROCEDURE `GetMedicament`(IN IndexMolecule INT)
BEGIN
SELECT
idMedicament,Designation, Presentation,Concentration_mg,
(SELECT UniteConditionnement FROM UniteConditionnement WHERE idUniteConditionnement=UniteConditionnement_idUniteConditionnement) AS unite,
Conditionnement,Pharmacie
FROM Medicament,MedicamentConcentrations
WHERE Molecules_idMolecules=IndexMolecule AND idMedicament=Medicament_idMedicament;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetTarif
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetTarif`;

DELIMITER $$
USE `OpenVet12`$$










CREATE DEFINER=`root`@`localhost` PROCEDURE `GetTarif`(IN IndexMedicament INT)
BEGIN
SELECT
PrixHT,TVA,CodeCentrale
FROM CentraleTarifs,Medicament
WHERE CentraleTarifs.Cip=Medicament.Cip AND idMedicament=IndexMedicament;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetResultatLiquide
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetResultatLiquide`;

DELIMITER $$
USE `OpenVet12`$$








CREATE DEFINER=`root`@`localhost` PROCEDURE `GetResultatLiquide`(IN IndexAnalyse INT)
BEGIN
SELECT
(SELECT Parametre FROM Parametres WHERE idParametres=Parametres_idParametres) AS Parametre,
Valeur,
(SELECT unite FROM Parametres WHERE idParametres=Parametres_idParametres) AS Unite,
(SELECT NormeMin FROM Parametres WHERE idParametres=Parametres_idParametres) AS NormeMin,
(SELECT NormeMax FROM Parametres WHERE idParametres=Parametres_idParametres) AS NormeMax,
FichierExterne,Remarque
FROM ResultatAnalyse
WHERE Analyse_idAnalyse=IndexAnalyse;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetResultatImage
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetResultatImage`;

DELIMITER $$
USE `OpenVet12`$$










CREATE DEFINER=`root`@`localhost` PROCEDURE `GetResultatImage`(IN IndexAnalyse INT)
BEGIN
SELECT Image,TitreImage,Description,FichierExterne,Remarque
FROM ResultatAnalyse
WHERE Analyse_idAnalyse=IndexAnalyse;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetAnalyseAnimal
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetAnalyseAnimal`;

DELIMITER $$
USE `OpenVet12`$$










CREATE DEFINER=`root`@`localhost` PROCEDURE `GetAnalyseAnimal`(IN IndexAnimal INT)
BEGIN
SELECT idAnalyse,DescriptionAnalyse,DateHeure,
(SELECT Libele FROM TypeAnalyse WHERE idTypeAnalyse=TypeAnalyse_idTypeAnalyse) AS TypeAnalyse,
(SELECT count(FichierExterne) FROM ResultatAnalyse WHERE Analyse_idAnalyse=idAnalyse AND FichierExterne IS NOT NULL) AS Document
FROM Analyse,Consultation
WHERE Consultation_idConsultation=idConsultation AND Animal_idAnimal=IndexAnimal;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetConsultations
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetConsultations`;

DELIMITER $$
USE `OpenVet12`$$


CREATE DEFINER=`root`@`localhost` PROCEDURE `GetConsultations`(IN IndexAnimal INT)
BEGIN
SELECT idConsultation,DateConsultation,
(SELECT GROUP_CONCAT(TypeConsultation) FROM TypeConsultation,TypeConsultationRef WHERE idTypeConsultation=TypeConsultation_idTypeConsultation AND TypeConsultationRef.Consultation_idConsultation=idConsultation) AS TypeConsultation,
(SELECT CONCAT(Nom," ",Prenom) FROM Personne WHERE idPersonne=Personne_idVeterinaire) AS Veterinaire,
(SELECT CONCAT(Nom," ",Prenom) FROM Personne WHERE idPersonne=Personne_idReferant) AS Referant,
(SELECT GROUP_CONCAT(NomReference) FROM Pathologie,PathologieRef WHERE idPathologie=Pathologie_idPathologie AND Consultation_idConsultation=idConsultation) AS Pathologie,
Examen,Traitement,
(SELECT COUNT(idAnalyse) FROM Analyse, TypeAnalyse WHERE Analyse.Consultation_idConsultation=idConsultation AND idTypeAnalyse=TypeAnalyse_idTypeAnalyse AND !TypeAnalyse.IsImage) AS Biologie,
(SELECT COUNT(idAnalyse) FROM Analyse, TypeAnalyse WHERE Analyse.Consultation_idConsultation=idConsultation AND idTypeAnalyse=TypeAnalyse_idTypeAnalyse AND TypeAnalyse.IsImage) AS Imagerie,
(SELECT COUNT(idChirurgie) FROM Chirurgie WHERE Chirurgie.Consultation_idConsultation=idConsultation) AS Chirurgie,
(SELECT COUNT(idOrdonnance) FROM Ordonnance WHERE Ordonnance.Consultation_idConsultation=idConsultation) AS Ordonnance,
(SELECT COUNT(idPlanTherapeutique) FROM PlanTherapeutique WHERE PlanTherapeutique.Consultation_idConsultation=idConsultation) AS PlanTherapeutique,
Commentaires
FROM Consultation WHERE Animal_idAnimal=IndexAnimal;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetConsultation
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetConsultation`;

DELIMITER $$
USE `OpenVet12`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `GetConsultation`(IN IndexConsultation INT)
BEGIN
SELECT idConsultation,DateConsultation,
(SELECT GROUP_CONCAT(TypeConsultation) FROM TypeConsultation,TypeConsultationRef WHERE idTypeConsultation=TypeConsultation_idTypeConsultation AND TypeConsultationRef.Consultation_idConsultation=idConsultation) AS TypeConsultation,
(SELECT CONCAT(Nom," ",Prenom) FROM Personne WHERE idPersonne=Personne_idVeterinaire) AS Veterinaire,
(SELECT CONCAT(Nom," ",Prenom) FROM Personne WHERE idPersonne=Personne_idReferant) AS Referant,
(SELECT GROUP_CONCAT(NomReference) FROM Pathologie,PathologieRef WHERE idPathologie=Pathologie_idPathologie AND Consultation_idConsultation=idConsultation) AS Pathologie,
Examen,Traitement,
(SELECT COUNT(idAnalyse) FROM Analyse, TypeAnalyse WHERE Analyse.Consultation_idConsultation=idConsultation AND idTypeAnalyse=TypeAnalyse_idTypeAnalyse AND !TypeAnalyse.IsImage) AS Biologie,
(SELECT COUNT(idAnalyse) FROM Analyse, TypeAnalyse WHERE Analyse.Consultation_idConsultation=idConsultation AND idTypeAnalyse=TypeAnalyse_idTypeAnalyse AND TypeAnalyse.IsImage) AS Imagerie,
(SELECT COUNT(idChirurgie) FROM Chirurgie WHERE Chirurgie.Consultation_idConsultation=idConsultation) AS Chirurgie,
(SELECT COUNT(idOrdonnance) FROM Ordonnance WHERE Ordonnance.Consultation_idConsultation=idConsultation) AS Ordonnance,
(SELECT COUNT(idPlanTherapeutique) FROM PlanTherapeutique WHERE PlanTherapeutique.Consultation_idConsultation=idConsultation) AS PlanTherapeutique,
Commentaires
FROM Consultation WHERE idConsultation=IndexConsultation;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetBiologies
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetBiologies`;

DELIMITER $$
USE `OpenVet12`$$





CREATE DEFINER=`root`@`localhost` PROCEDURE `GetBiologies`(IN IndexConsultation INT)
BEGIN
SELECT idAnalyse,DescriptionAnalyse
FROM Analyse,TypeAnalyse
WHERE Consultation_idConsultation=Indexconsultation AND idTypeAnalyse=TypeAnalyse_idTypeAnalyse AND !TypeAnalyse.IsImage;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetImages
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetImages`;

DELIMITER $$
USE `OpenVet12`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `GetImages`(IN IndexConsultation INT)
BEGIN
SELECT idAnalyse,DescriptionAnalyse
FROM Analyse,TypeAnalyse
WHERE Consultation_idConsultation=Indexconsultation AND idTypeAnalyse=TypeAnalyse_idTypeAnalyse AND TypeAnalyse.IsImage;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure SelectPathologies
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`SelectPathologies`;

DELIMITER $$
USE `OpenVet12`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `SelectPathologies`(IN INEspece INT, IN INDomaine INT)
BEGIN
IF INDomaine=0 Then
SELECT idPathologie,NomReference
FROM Pathologie 
JOIN DomaineRef ON DomaineRef.Pathologie_idPathologie=idPathologie
JOIN PathologieDomaine ON PathologieDomaine_idPathologieDomaine=idPathologieDomaine
JOIN PathologieEspece ON PathologieEspece.Pathologie_idPathologie=idPathologie 
WHERE Especes_idEspeces=INEspece GROUP BY idPathologie
UNION 
SELECT idPathologie,Synonyme
FROM Pathologie 
JOIN DomaineRef ON DomaineRef.Pathologie_idPathologie=idPathologie
JOIN PathologieDomaine ON PathologieDomaine_idPathologieDomaine=idPathologieDomaine
JOIN PathologieEspece ON PathologieEspece.Pathologie_idPathologie=idPathologie 
JOIN PathologieSynonyme ON PathologieSynonyme.Pathologie_idPathologie=idPathologie
WHERE Especes_idEspeces=INEspece 
ORDER BY NomReference;
ELSE
SELECT idPathologie,NomReference
FROM Pathologie 
JOIN DomaineRef ON DomaineRef.Pathologie_idPathologie=idPathologie
JOIN PathologieDomaine ON PathologieDomaine_idPathologieDomaine=idPathologieDomaine
JOIN PathologieEspece ON PathologieEspece.Pathologie_idPathologie=idPathologie 
WHERE Especes_idEspeces=INEspece AND idPathologieDomaine=INDomaine GROUP BY idPathologie
UNION 
SELECT idPathologie,Synonyme
FROM Pathologie 
JOIN DomaineRef ON DomaineRef.Pathologie_idPathologie=idPathologie
JOIN PathologieDomaine ON PathologieDomaine_idPathologieDomaine=idPathologieDomaine
JOIN PathologieEspece ON PathologieEspece.Pathologie_idPathologie=idPathologie 
JOIN PathologieSynonyme ON PathologieSynonyme.Pathologie_idPathologie=idPathologie
WHERE Especes_idEspeces=INEspece AND idPathologieDomaine=INDomaine 
ORDER BY NomReference;
END IF;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetDomaine
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetDomaine`;

DELIMITER $$
USE `OpenVet12`$$


CREATE DEFINER=`root`@`localhost` PROCEDURE `GetDomaine`(IN INpathologie VARCHAR(60))
BEGIN
SELECT idPathologieDomaine,Domaine 
FROM Pathologie 
JOIN DomaineRef ON Pathologie_idPathologie=idPathologie
JOIN PathologieDomaine ON PathologieDomaine_idPathologieDomaine=idPathologieDomaine
WHERE NomReference=INpathologie;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetDomaines
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetDomaines`;

DELIMITER $$
USE `OpenVet12`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `GetDomaines`()
BEGIN
SELECT idPathologieDomaine,Domaine
FROM PathologieDomaine;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetExamens
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetExamens`;

DELIMITER $$
USE `OpenVet12`$$





CREATE DEFINER=`root`@`localhost` PROCEDURE `GetExamens`(IN IndexPathologie INT)
BEGIN
SELECT idExamen,Examen
FROM Critere 
JOIN Examen ON idExamen=Examen_idExamen
WHERE Pathologie_idPathologie=IndexPathologie
GROUP BY idExamen ORDER BY Examen;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetPathologieDocuments
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetPathologieDocuments`;

DELIMITER $$
USE `OpenVet12`$$





CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPathologieDocuments` (IN IndexPathologie INT)
BEGIN
SELECT Document
FROM DocumentsRef 
JOIN PathologieDocument ON idPathologieDocument=PathologieDocument_idPathologieDocument
WHERE Pathologie_idPathologie=IndexPathologie;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetCritereGrade
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetCritereGrade`;

DELIMITER $$
USE `OpenVet12`$$





CREATE DEFINER=`root`@`localhost` PROCEDURE `GetCritereGrade`(IN IndexCritere INT, IN Valeur DECIMAL)
BEGIN
SELECT Grade,NbGrades,LimiteInf,LimiteSup FROM Critere 
JOIN CritereSeuil ON Critere_idCritere=idCritere 
WHERE idCritere=IndexCritere 
AND IF(LimiteInf IS NULL,TRUE,Valeur>LimiteInf) AND IF(LimiteSup IS NULL,TRUE, Valeur<=LimiteSup);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetPathologie_old
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetPathologie_old`;

DELIMITER $$
USE `OpenVet12`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPathologie_old`(IN IndexPathologie INT)
BEGIN
SELECT NomReference,Chronique,GROUP_CONCAT(Domaine) AS Domaine,
(SELECT GROUP_CONCAT(PathologieDocument_idPathologieDocument) FROM DocumentsRef WHERE Pathologie_idPathologie=idPathologie) AS Documents,
DescriptifPublic,
(SELECT COUNT(idCritere) FROM Critere WHERE Pathologie_idPathologie=idPathologie) AS Critere
FROM Pathologie 
JOIN DomaineRef ON DomaineRef.Pathologie_idPathologie=idPathologie
JOIN PathologieDomaine ON PathologieDomaine_idPathologieDomaine=idPathologieDomaine
WHERE idPathologie=IndexPathologie;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetCritere
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetCritere`;

DELIMITER $$
USE `OpenVet12`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `GetCritere`(IN IndexCritere INT)
BEGIN
SELECT IF(Remarque iS NULL, Critere,CONCAT(Critere," (",Remarque,")")) AS Critere,Unite,
(SELECT CONCAT(IF(LimiteInf IS NULL,"...",CAST(LimiteInf AS CHAR(10)))," - ",IF(LimiteSup IS NULL,"...",CAST(LimiteSup AS CHAR(10)))) FROM CritereSeuil WHERE Critere_idCritere=idCritere AND Grade=0) AS Norme
FROM Critere  
WHERE idCritere=IndexCritere;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetPathologiesConsult
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetPathologiesConsult`;

DELIMITER $$
USE `OpenVet12`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPathologiesConsult`(IN IndexConsultation INT)
BEGIN
SELECT idPathologie,NomReference
FROM Pathologie,PathologieRef
WHERE Consultation_idConsultation=IndexConsultation AND idPathologie=Pathologie_idPathologie;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetExamensConsult
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetExamensConsult`;

DELIMITER $$
USE `OpenVet12`$$





CREATE DEFINER=`root`@`localhost` PROCEDURE `GetExamensConsult`(IN IndexConsultation INT, IN IndexPathologie INT)
BEGIN
SELECT idExamen, Examen
FROM ConsultationCritere 
JOIN Critere ON Critere_idCritere=idCritere
JOIN Examen ON Examen_idExamen=idExamen
WHERE Consultation_idConsultation=IndexConsultation AND Pathologie_idPathologie=IndexPathologie 
GROUP BY idExamen;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetCriteresConsult
-- -----------------------------------------------------

USE `OpenVet12`;
DROP procedure IF EXISTS `OpenVet12`.`GetCriteresConsult`;

DELIMITER $$
USE `OpenVet12`$$





CREATE DEFINER=`root`@`localhost` PROCEDURE `GetCriteresConsult`(IN IndexConsultation INT, IN IndexPathologie INT)
BEGIN
SELECT idConsultationCritere,idCritere,Examen,Critere,
IF(CritereQuantitatif IS NULL, CritereQualitatif, CAST(CritereQuantitatif AS CHAR(20))) AS Valeur,
IF(Unite IS NULL,"",Unite) AS Unite,
(SELECT CONCAT(IF(LimiteInf IS NULL,"...",CAST(LimiteInf AS CHAR(10)))," - ",IF(LimiteSup IS NULL,"...",CAST(LimiteSup AS CHAR(10)))) FROM CritereSeuil WHERE Critere_idCritere=idCritere AND Grade=0) AS Norme,
Grade 
FROM ConsultationCritere 
JOIN Critere ON Critere_idCritere=idCritere
JOIN Examen ON Examen_idExamen=idExamen
WHERE Consultation_idConsultation=IndexConsultation AND Pathologie_idPathologie=IndexPathologie
ORDER BY Examen;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- View `OpenVet12`.`viewPersonne`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `OpenVet12`.`viewPersonne` ;
DROP TABLE IF EXISTS `OpenVet12`.`viewPersonne`;
USE `OpenVet12`;
CREATE  OR REPLACE VIEW `OpenVet12`.`viewPersonne` AS SELECT * FROM Personne P LEFT JOIN viewCommune C ON Commune_idCommune=idCommune;
;

-- -----------------------------------------------------
-- View `OpenVet12`.`viewCommune`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `OpenVet12`.`viewCommune` ;
DROP TABLE IF EXISTS `OpenVet12`.`viewCommune`;
USE `OpenVet12`;
CREATE  OR REPLACE VIEW `OpenVet12`.`viewCommune` AS SELECT idCommune,Commune,CIP, Pays  FROM Commune LEFT JOIN Pays 
ON Pays_idPays = idPays
WHERE Commune.Actif=True;
;

-- -----------------------------------------------------
-- View `OpenVet12`.`viewClient`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `OpenVet12`.`viewClient` ;
DROP TABLE IF EXISTS `OpenVet12`.`viewClient`;
USE `OpenVet12`;
CREATE  OR REPLACE VIEW `OpenVet12`.`viewClient` AS SELECT * FROM viewPersonne WHERE isClient=True;
;
USE `OpenVet12`;

DELIMITER $$

USE `OpenVet12`$$
DROP TRIGGER IF EXISTS `OpenVet12`.`Facture_BINS` $$
USE `OpenVet12`$$




CREATE TRIGGER `Facture_BINS` BEFORE INSERT ON Facture FOR EACH ROW
-- Edit trigger body code below this line. Do not edit lines above this one
BEGIN
	SET New.MontantTVA= 0;
	SET New.MontantTTC=0;
	SET New.MontantHT=0;
	SET New.TotalRegle=0;
	IF (New.DateFacture IS NULL) THEN  
		SET New.DateFacture=Now(); 
	END IF;
	#SET New.Commentaires='debug Facture bins';
END

$$


USE `OpenVet12`$$
DROP TRIGGER IF EXISTS `OpenVet12`.`Facture_BUPD` $$
USE `OpenVet12`$$




CREATE TRIGGER `Facture_BUPD` BEFORE UPDATE ON Facture FOR EACH ROW
-- Edit trigger body code below this line. Do not edit lines above this one
BEGIN
	SET New.MontantTVA= New.MontantTTC-New.MontantHT;
	SET New.Commentaires='debug Facture BUDP';
END $$


USE `OpenVet12`$$
DROP TRIGGER IF EXISTS `OpenVet12`.`Facture_BDEL` $$
USE `OpenVet12`$$




CREATE TRIGGER `Facture_BDEL` BEFORE DELETE ON Facture FOR EACH ROW
-- Edit trigger body code below this line. Do not edit lines above this one
BEGIN
END
$$


DELIMITER ;

DELIMITER $$

USE `OpenVet12`$$
DROP TRIGGER IF EXISTS `OpenVet12`.`LignesFacture_AINS` $$
USE `OpenVet12`$$






CREATE TRIGGER `LignesFacture_AINS` AFTER INSERT ON LignesFacture FOR EACH ROW
-- Edit trigger body code below this line. Do not edit lines above this one
BEGIN

	UPDATE Facture SET MontantHT = (SELECT sum(PrixUnitHT*Quantite*(1-TauxRemise/100)) FROM LignesFacture where Facture_idFacture=NEW.Facture_idFacture) WHERE idFacture=NEW.Facture_idFacture;
	UPDATE Facture SET MontantTTC = (SELECT sum(PrixTotal) FROM LignesFacture where Facture_idFacture=NEW.Facture_idFacture) WHERE idFacture=NEW.Facture_idFacture;
	UPDATE Facture SET MontantRemises = (SELECT sum(RemisesTTC) FROM LignesFacture where Facture_idFacture=NEW.Facture_idFacture) WHERE idFacture=NEW.Facture_idFacture;
END $$


USE `OpenVet12`$$
DROP TRIGGER IF EXISTS `OpenVet12`.`LignesFacture_BINS` $$
USE `OpenVet12`$$




CREATE TRIGGER `LignesFacture_BINS` BEFORE INSERT ON LignesFacture FOR EACH ROW
-- Edit trigger body code below this line. Do not edit lines above this one
BEGIN
	#SET New.Denomination='debug --- BEFOREINS 2';

	IF (New.Date IS NULL) THEN  
		SET New.Date=Now(); 
	END IF;


	IF New.PrixUnitTTC>0 THEN
			SET New.PrixUnitHT = New.PrixUnitTTC /(1+New.TVA/100);
	ELSEIF New.PrixUnitHT >0 THEN
		SET New.PrixUnitTTC = New.PrixUnitHT *(1+New.TVA/100);
	END IF;


	IF (New.TauxRemise > 100) THEN  
		SET New.TauxRemise = 100; 
		SET New.RemisesTTC=New.PrixUnitTTC*New.Quantite;
	ELSEIF (New.TauxRemise <0) THEN  
		SET New.TauxRemise = 0;
		SET New.RemisesTTC=0;
	END IF;

	IF (New.TauxRemise > 0 AND New.TauxRemise <100) THEN
		SET New.RemisesTTC=New.TauxRemise/100*(New.PrixUnitTTC*New.Quantite);
	END IF;

	IF ( NOT(New.TauxRemise) AND (New.RemisesTTC>0) ) THEN

		IF New.RemisesTTC >= (New.PrixUnitTTC*New.Quantite) THEN
			SET New.RemisesTTC = (New.PrixUnitTTC*New.Quantite);
			SET New.TauxRemise=100;
		ELSE
			SET New.TauxRemise=New.RemisesTTC*100/(New.PrixUnitTTC*New.Quantite);
		END IF;
	END IF;
	SET New.PrixTotal = (New.PrixUnitTTC*New.Quantite)- New.RemisesTTC;

END
$$


USE `OpenVet12`$$
DROP TRIGGER IF EXISTS `OpenVet12`.`LignesFacture_ADEL` $$
USE `OpenVet12`$$






CREATE TRIGGER `LignesFacture_ADEL` AFTER DELETE ON LignesFacture FOR EACH ROW
-- Edit trigger body code below this line. Do not edit lines above this one
BEGIN

	UPDATE Facture SET MontantHT = (SELECT sum(PrixUnitHT*Quantite*(1-TauxRemise/100)) FROM LignesFacture where Facture_idFacture=OLD.Facture_idFacture) WHERE idFacture=OLD.Facture_idFacture;
	UPDATE Facture SET MontantTTC = (SELECT sum(PrixTotal) FROM LignesFacture where Facture_idFacture=OLD.Facture_idFacture) WHERE idFacture=OLD.Facture_idFacture;
	UPDATE Facture SET MontantRemises = (SELECT sum(RemisesTTC) FROM LignesFacture where Facture_idFacture=OLD.Facture_idFacture) WHERE idFacture=OLD.Facture_idFacture;

END $$


USE `OpenVet12`$$
DROP TRIGGER IF EXISTS `OpenVet12`.`LignesFacture_AUPD` $$
USE `OpenVet12`$$




CREATE TRIGGER `LignesFacture_AUPD` AFTER UPDATE ON LignesFacture FOR EACH ROW
-- Edit trigger body code below this line. Do not edit lines above this one
BEGIN

	UPDATE Facture SET MontantHT = (SELECT sum(PrixUnitHT*Quantite*(1-TauxRemise/100)) FROM LignesFacture where Facture_idFacture=NEW.Facture_idFacture) WHERE idFacture=NEW.Facture_idFacture;
	UPDATE Facture SET MontantTTC = (SELECT sum(PrixTotal) FROM LignesFacture where Facture_idFacture=NEW.Facture_idFacture) WHERE idFacture=NEW.Facture_idFacture;
	UPDATE Facture SET MontantRemises = (SELECT sum(RemisesTTC) FROM LignesFacture where Facture_idFacture=NEW.Facture_idFacture) WHERE idFacture=NEW.Facture_idFacture;

END
$$


USE `OpenVet12`$$
DROP TRIGGER IF EXISTS `OpenVet12`.`LignesFacture_BUPD` $$
USE `OpenVet12`$$




CREATE TRIGGER `LignesFacture_BUPD` BEFORE UPDATE ON LignesFacture FOR EACH ROW
-- Edit trigger body code below this line. Do not edit lines above this one
BEGIN
	#SET New.Denomination='debug --- BEFOREINS 2';

	IF (New.Date IS NULL) THEN  
		SET New.Date=Now(); 
	END IF;


	IF New.PrixUnitTTC>0 THEN
			SET New.PrixUnitHT = New.PrixUnitTTC /(1+New.TVA/100);
	ELSEIF New.PrixUnitHT >0 THEN
		SET New.PrixUnitTTC = New.PrixUnitHT *(1+New.TVA/100);
	END IF;


	IF (New.TauxRemise > 100) THEN  
		SET New.TauxRemise = 100; 
		SET New.RemisesTTC=New.PrixUnitTTC*New.Quantite;
	ELSEIF (New.TauxRemise <0) THEN  
		SET New.TauxRemise = 0;
		SET New.RemisesTTC=0;
	END IF;

	IF (New.TauxRemise > 0 AND New.TauxRemise <100) THEN
		SET New.RemisesTTC=New.TauxRemise/100*(New.PrixUnitTTC*New.Quantite);
	END IF;

	IF ( NOT(New.TauxRemise) AND (New.RemisesTTC>0) ) THEN

		IF New.RemisesTTC >= (New.PrixUnitTTC*New.Quantite) THEN
			SET New.RemisesTTC = (New.PrixUnitTTC*New.Quantite);
			SET New.TauxRemise=100;
		ELSE
			SET New.TauxRemise=New.RemisesTTC*100/(New.PrixUnitTTC*New.Quantite);
		END IF;
	END IF;
	SET New.PrixTotal = (New.PrixUnitTTC*New.Quantite)- New.RemisesTTC;

END $$


DELIMITER ;

DELIMITER $$

USE `OpenVet12`$$
DROP TRIGGER IF EXISTS `OpenVet12`.`IsDoublon` $$
USE `OpenVet12`$$










CREATE TRIGGER IsDoublon BEFORE INSERT ON Medicament
FOR EACH ROW
BEGIN
DECLARE msg varchar(255);
	IF EXISTS (SELECT idMedicament FROM Medicament WHERE Designation=NEW.Designation AND Presentation=NEW.Presentation AND Conditionnement=NEW.Conditionnement) THEN
		set msg='Doublon pour % % % non ajouté dans la base.'%( NEW.Designation, NEW.Presentation, NEW.Conditionnement);
		#signal sqlstate '45000' set message_text = msg;
	END IF;
END
$$


DELIMITER ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Especes`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Especes` (`idEspeces`, `Espece`) VALUES (1, 'Chat');
INSERT INTO `OpenVet12`.`Especes` (`idEspeces`, `Espece`) VALUES (2, 'Chien');
INSERT INTO `OpenVet12`.`Especes` (`idEspeces`, `Espece`) VALUES (3, 'Lapin');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Race`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Race` (`idRace`, `Race`, `Especes_idEspeces`, `Actif`) VALUES (1, 'Européen', 1, NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Animal`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Animal` (`idAnimal`, `Animal_idPere`, `Animal_idMere`, `Nom`, `Especes_idEspeces`, `Race_idRace`, `Race2_idRace`, `Robe`, `Sexe`, `Naissance`, `Sterilise`, `DesactiverRelances`, `Identification`, `Commentaires`, `Actif`) VALUES (1, NULL, NULL, 'Toto', 1, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Civilite`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Civilite` (`idCivilite`, `Civilite`, `CiviliteAbrev`, `Actif`) VALUES (1, 'Monsieur', 'M', NULL);
INSERT INTO `OpenVet12`.`Civilite` (`idCivilite`, `Civilite`, `CiviliteAbrev`, `Actif`) VALUES (2, 'Monsieur et Madame', 'M et Mme', NULL);
INSERT INTO `OpenVet12`.`Civilite` (`idCivilite`, `Civilite`, `CiviliteAbrev`, `Actif`) VALUES (3, 'Mademoiselle', 'Melle', NULL);
INSERT INTO `OpenVet12`.`Civilite` (`idCivilite`, `Civilite`, `CiviliteAbrev`, `Actif`) VALUES (4, 'Docteur', 'Dr', NULL);
INSERT INTO `OpenVet12`.`Civilite` (`idCivilite`, `Civilite`, `CiviliteAbrev`, `Actif`) VALUES (5, 'Maitre', 'Me', NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Pays`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Pays` (`idPays`, `Pays`) VALUES (1, 'France');
INSERT INTO `OpenVet12`.`Pays` (`idPays`, `Pays`) VALUES (2, 'Belgique');
INSERT INTO `OpenVet12`.`Pays` (`idPays`, `Pays`) VALUES (3, 'Suisse');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Commune`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Commune` (`idCommune`, `Commune`, `CIP`, `Pays_idPays`, `Actif`) VALUES (1, 'Sochaux', '25600', 1, True);
INSERT INTO `OpenVet12`.`Commune` (`idCommune`, `Commune`, `CIP`, `Pays_idPays`, `Actif`) VALUES (2, 'Dinard', '35800', 1, True);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Personne`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Personne` (`idPersonne`, `Civilite_idCivilite`, `isClient`, `IsVeterinaire`, `isSalarie`, `isFournisseur`, `IsConsultant`, `IsReferant`, `IsReferent`, `IsAssocie`, `IsCollaborateurLiberal`, `IsServiceGarde`, `Actif`, `Commentaires`, `Nom`, `NomMarital`, `Prenom`, `Adresse_No`, `Adresse_Rue`, `Commune_idCommune`, `SousTutelle`, `MauvaisPayeur`, `Contentieux`, `AncienClient`, `ClientDePassage`, `NbRetardRV`, `NbOublieRV`, `NbOublieOpe`, `DateEntree`, `PartSociales`, `NoCARPV`, `NoURSSAF`, `NoOrdre`, `Specialite`, `Temporaire`, `Cadre`, `ConventionCollective`, `SalaireHoraire`, `Coefficient`, `Echellon`, `Emploi`, `LieuNaissance`, `DateNaissance`, `FinContrat`, `NoSecuriteSociale`, `TelephoneDomicile`, `TelephoneBureau`, `TelephonePortable1`, `TelephonePortable2`, `Mail`) VALUES (1, 1, True, True, False, False, True, False, NULL, NULL, NULL, NULL, True, NULL, 'POINT (client+veto)', NULL, 'Yvon', NULL, NULL, 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `OpenVet12`.`Personne` (`idPersonne`, `Civilite_idCivilite`, `isClient`, `IsVeterinaire`, `isSalarie`, `isFournisseur`, `IsConsultant`, `IsReferant`, `IsReferent`, `IsAssocie`, `IsCollaborateurLiberal`, `IsServiceGarde`, `Actif`, `Commentaires`, `Nom`, `NomMarital`, `Prenom`, `Adresse_No`, `Adresse_Rue`, `Commune_idCommune`, `SousTutelle`, `MauvaisPayeur`, `Contentieux`, `AncienClient`, `ClientDePassage`, `NbRetardRV`, `NbOublieRV`, `NbOublieOpe`, `DateEntree`, `PartSociales`, `NoCARPV`, `NoURSSAF`, `NoOrdre`, `Specialite`, `Temporaire`, `Cadre`, `ConventionCollective`, `SalaireHoraire`, `Coefficient`, `Echellon`, `Emploi`, `LieuNaissance`, `DateNaissance`, `FinContrat`, `NoSecuriteSociale`, `TelephoneDomicile`, `TelephoneBureau`, `TelephonePortable1`, `TelephonePortable2`, `Mail`) VALUES (2, 1, False, True, False, False, True, True, NULL, NULL, NULL, NULL, True, NULL, 'BAGAINI (veto)', NULL, 'François', NULL, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `OpenVet12`.`Personne` (`idPersonne`, `Civilite_idCivilite`, `isClient`, `IsVeterinaire`, `isSalarie`, `isFournisseur`, `IsConsultant`, `IsReferant`, `IsReferent`, `IsAssocie`, `IsCollaborateurLiberal`, `IsServiceGarde`, `Actif`, `Commentaires`, `Nom`, `NomMarital`, `Prenom`, `Adresse_No`, `Adresse_Rue`, `Commune_idCommune`, `SousTutelle`, `MauvaisPayeur`, `Contentieux`, `AncienClient`, `ClientDePassage`, `NbRetardRV`, `NbOublieRV`, `NbOublieOpe`, `DateEntree`, `PartSociales`, `NoCARPV`, `NoURSSAF`, `NoOrdre`, `Specialite`, `Temporaire`, `Cadre`, `ConventionCollective`, `SalaireHoraire`, `Coefficient`, `Echellon`, `Emploi`, `LieuNaissance`, `DateNaissance`, `FinContrat`, `NoSecuriteSociale`, `TelephoneDomicile`, `TelephoneBureau`, `TelephonePortable1`, `TelephonePortable2`, `Mail`) VALUES (3, 1, False, True, False, False, False, True, NULL, NULL, NULL, NULL, True, NULL, 'Lambda', NULL, 'Jules', '10', 'rue des ballons', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Consultation`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Consultation` (`idConsultation`, `Animal_idAnimal`, `DateConsultation`, `Personne_idVeterinaire`, `Personne_idReferant`, `Personne_idReferent`, `Examen`, `Traitement`, `Actif`, `Commentaires`) VALUES (1, 1, '2012-02-25', 1, 2, NULL, 'Galop Cardiaque', 'Hypercard', NULL, 'Quelque chose sans signification.');
INSERT INTO `OpenVet12`.`Consultation` (`idConsultation`, `Animal_idAnimal`, `DateConsultation`, `Personne_idVeterinaire`, `Personne_idReferant`, `Personne_idReferent`, `Examen`, `Traitement`, `Actif`, `Commentaires`) VALUES (2, 1, '2013-03-08', 2, NULL, NULL, 'Vomissements,Amaigrissement. Palaption masse abdominale.', 'inj Dexafort.', NULL, NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`TypeAnalyse`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`TypeAnalyse` (`idTypeAnalyse`, `Libele`, `Remarque`, `IsImage`) VALUES (1, 'Radio', NULL, TRUE);
INSERT INTO `OpenVet12`.`TypeAnalyse` (`idTypeAnalyse`, `Libele`, `Remarque`, `IsImage`) VALUES (2, 'Numération Formule', NULL, FALSE);
INSERT INTO `OpenVet12`.`TypeAnalyse` (`idTypeAnalyse`, `Libele`, `Remarque`, `IsImage`) VALUES (3, 'Biochimie', NULL, FALSE);
INSERT INTO `OpenVet12`.`TypeAnalyse` (`idTypeAnalyse`, `Libele`, `Remarque`, `IsImage`) VALUES (4, 'Cytologie', NULL, TRUE);
INSERT INTO `OpenVet12`.`TypeAnalyse` (`idTypeAnalyse`, `Libele`, `Remarque`, `IsImage`) VALUES (5, 'Sérologie', NULL, FALSE);
INSERT INTO `OpenVet12`.`TypeAnalyse` (`idTypeAnalyse`, `Libele`, `Remarque`, `IsImage`) VALUES (6, 'Echographie', NULL, TRUE);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Analyse`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Analyse` (`idAnalyse`, `Consultation_idConsultation`, `TypeAnalyse_idTypeAnalyse`, `DateHeure`, `DescriptionAnalyse`, `Prelevement`, `SyntheseAnalyse`, `Conclusions`) VALUES (1, 1, 1, NULL, 'Radio Thoracique', NULL, NULL, NULL);
INSERT INTO `OpenVet12`.`Analyse` (`idAnalyse`, `Consultation_idConsultation`, `TypeAnalyse_idTypeAnalyse`, `DateHeure`, `DescriptionAnalyse`, `Prelevement`, `SyntheseAnalyse`, `Conclusions`) VALUES (2, 2, 2, NULL, 'Numération-Formule', NULL, NULL, NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Facture`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Facture` (`idFacture`, `Client_idClient`, `NomClientAFacturer`, `Commune_idCommune`, `AdresseFacturation`, `DateFacture`, `DateEnvoiCourrier`, `DateLimiteRelance`, `RelanceEnvoyee`, `NumFacture`, `IsDevis`, `MontantHT`, `MontantTTC`, `MontantTVA`, `MontantRemises`, `IsRecouvrement`, `TotalRegle`, `Commentaires`, `Actif`, `FactureFigee`) VALUES (1, 1, '', NULL, NULL, NULL, NULL, NULL, NULL, 'No1', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Ordonnance`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Ordonnance` (`idOrdonnance`, `Consultation_idConsultation`) VALUES (1, 1);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`LignesOrdonnance`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`LignesOrdonnance` (`idLigneOrdonnance`, `Ordonnance_idOrdonnance`, `Medicament`, `Posologie`, `UnitesDelivre`, `UnitesPrescrites`, `ImpressionLIgne`, `actif`, `commentaires`) VALUES (1, 1, NULL, '1 cp 3 fois par jour pendant 3 mois.', 1, 6, True, NULL, NULL);
INSERT INTO `OpenVet12`.`LignesOrdonnance` (`idLigneOrdonnance`, `Ordonnance_idOrdonnance`, `Medicament`, `Posologie`, `UnitesDelivre`, `UnitesPrescrites`, `ImpressionLIgne`, `actif`, `commentaires`) VALUES (2, 1, NULL, 'Metacam chat 15 ml\\\\n Une dose pour 5Kg avec la nourriture une fois par jour pendant 3 semaines.', 1, 1, True, NULL, NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Pathologie`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Pathologie` (`idPathologie`, `NomReference`, `Chronique`, `DescriptifPublic`) VALUES (1, 'Cardio Myopathie Hypertrophique', True, 'Epaississement de la paroi du ventricule gauche, avec diminution de la capacité de remplissage du coeur.');
INSERT INTO `OpenVet12`.`Pathologie` (`idPathologie`, `NomReference`, `Chronique`, `DescriptifPublic`) VALUES (2, 'Lymphome Intestinal', True, 'Tumeur d\'origine sanguine localisée au niveau des intestins.');
INSERT INTO `OpenVet12`.`Pathologie` (`idPathologie`, `NomReference`, `Chronique`, `DescriptifPublic`) VALUES (3, 'Epanchement Thoracique', True, 'Accumulation de liquide entre les plèvres');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`PlanTherapeutique`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`PlanTherapeutique` (`idPlanTherapeutique`, `Consultation_idConsultation`, `Pathologie_idPathologie`, `Stade`, `Traitements`, `Remarques`, `ProchainRDV`) VALUES (1, 1, 1, '2', 'Diltiazem', NULL, 'Echographie dans 3 mois');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`TypeReglement`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`TypeReglement` (`idTypeReglement`, `Type`, `AbrevType`, `Actif`) VALUES (1, 'ESP', 'Espèces', NULL);
INSERT INTO `OpenVet12`.`TypeReglement` (`idTypeReglement`, `Type`, `AbrevType`, `Actif`) VALUES (2, 'CB', 'Carte Bancaire', NULL);
INSERT INTO `OpenVet12`.`TypeReglement` (`idTypeReglement`, `Type`, `AbrevType`, `Actif`) VALUES (3, 'CHQ', 'Chèque', NULL);
INSERT INTO `OpenVet12`.`TypeReglement` (`idTypeReglement`, `Type`, `AbrevType`, `Actif`) VALUES (4, 'VIR', 'Virement', NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`TypeSociete`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`TypeSociete` (`idTypeSociete`, `Nom`, `IsVeterinaire`, `IsNous`) VALUES (1, 'Clinique Vétérinaire', True, True);
INSERT INTO `OpenVet12`.`TypeSociete` (`idTypeSociete`, `Nom`, `IsVeterinaire`, `IsNous`) VALUES (2, 'Cabinet Vétérinaire', True, False);
INSERT INTO `OpenVet12`.`TypeSociete` (`idTypeSociete`, `Nom`, `IsVeterinaire`, `IsNous`) VALUES (3, 'CHU Vétérinaire', True, False);
INSERT INTO `OpenVet12`.`TypeSociete` (`idTypeSociete`, `Nom`, `IsVeterinaire`, `IsNous`) VALUES (4, 'Fournisseur', False, False);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`VoiesAdministration`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`VoiesAdministration` (`idVoiesAdministration`, `VoieAdministration`) VALUES (1, 'PO');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`UniteConditionnement`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`UniteConditionnement` (`idUniteConditionnement`, `UniteConditionnement`) VALUES (1, 'CPS');
INSERT INTO `OpenVet12`.`UniteConditionnement` (`idUniteConditionnement`, `UniteConditionnement`) VALUES (2, 'ML');
INSERT INTO `OpenVet12`.`UniteConditionnement` (`idUniteConditionnement`, `UniteConditionnement`) VALUES (3, 'GEL');
INSERT INTO `OpenVet12`.`UniteConditionnement` (`idUniteConditionnement`, `UniteConditionnement`) VALUES (4, 'PIP');
INSERT INTO `OpenVet12`.`UniteConditionnement` (`idUniteConditionnement`, `UniteConditionnement`) VALUES (5, 'g');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Medicament`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Medicament` (`idMedicament`, `VoiesAdministration_idVoiesAdministration`, `UniteConditionnement_idUniteConditionnement`, `Designation`, `Presentation`, `Conditionnement`, `Cip`, `Pharmacie`, `Intergre`) VALUES (1, 1, 1, 'Hypercard', '10 mg', 30, '8906585', 1, 1);
INSERT INTO `OpenVet12`.`Medicament` (`idMedicament`, `VoiesAdministration_idVoiesAdministration`, `UniteConditionnement_idUniteConditionnement`, `Designation`, `Presentation`, `Conditionnement`, `Cip`, `Pharmacie`, `Intergre`) VALUES (2, 1, 1, 'Clavaseptin', '250 mg', 100, '6788874', 1, 1);
INSERT INTO `OpenVet12`.`Medicament` (`idMedicament`, `VoiesAdministration_idVoiesAdministration`, `UniteConditionnement_idUniteConditionnement`, `Designation`, `Presentation`, `Conditionnement`, `Cip`, `Pharmacie`, `Intergre`) VALUES (3, 1, 1, 'Clavaseptin', '50 mg', 100, '6788876', 1, 1);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`MoleculeGenre`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`MoleculeGenre` (`idMoleculeGenre`, `Genre`) VALUES (1, 'Antibiotique');
INSERT INTO `OpenVet12`.`MoleculeGenre` (`idMoleculeGenre`, `Genre`) VALUES (2, 'Cardio_Vasculaire');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`MoleculeFamille`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`MoleculeFamille` (`idMoleculeFamille`, `Famille`, `MoleculeGenre_idMoleculeGenre`) VALUES (1, 'Inhibiteur Calcique', 2);
INSERT INTO `OpenVet12`.`MoleculeFamille` (`idMoleculeFamille`, `Famille`, `MoleculeGenre_idMoleculeGenre`) VALUES (2, 'Betalactamines', 1);
INSERT INTO `OpenVet12`.`MoleculeFamille` (`idMoleculeFamille`, `Famille`, `MoleculeGenre_idMoleculeGenre`) VALUES (3, 'Inhibiteur de Betalactamases', 1);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Molecule`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Molecule` (`idMolecule`, `MoleculeFamille_idMoleculeFamille`, `Molecule`) VALUES (1, 1, 'diltiazem');
INSERT INTO `OpenVet12`.`Molecule` (`idMolecule`, `MoleculeFamille_idMoleculeFamille`, `Molecule`) VALUES (2, 2, 'amoxicilline');
INSERT INTO `OpenVet12`.`Molecule` (`idMolecule`, `MoleculeFamille_idMoleculeFamille`, `Molecule`) VALUES (3, 3, 'acide clavulanique');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`MoleculePosologie`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`MoleculePosologie` (`idMoleculePosologie`, `Molecule_idMolecule`, `Especes_idEspeces`, `VoiesAdministration_idVoiesAdministration`, `AutreAdministration`, `PosologieMin_mgkg`, `PosologieMax_mgkg`, `FrequenceJour`, `Specialite`, `Remarque`) VALUES (1, 1, 1, 1, NULL, 1.5, 3, 3, 'Cardiologie', NULL);
INSERT INTO `OpenVet12`.`MoleculePosologie` (`idMoleculePosologie`, `Molecule_idMolecule`, `Especes_idEspeces`, `VoiesAdministration_idVoiesAdministration`, `AutreAdministration`, `PosologieMin_mgkg`, `PosologieMax_mgkg`, `FrequenceJour`, `Specialite`, `Remarque`) VALUES (2, 2, 1, 1, NULL, 10, 10, 2, 'Infectiologie', NULL);
INSERT INTO `OpenVet12`.`MoleculePosologie` (`idMoleculePosologie`, `Molecule_idMolecule`, `Especes_idEspeces`, `VoiesAdministration_idVoiesAdministration`, `AutreAdministration`, `PosologieMin_mgkg`, `PosologieMax_mgkg`, `FrequenceJour`, `Specialite`, `Remarque`) VALUES (3, 2, 2, 1, NULL, 10, 10, 2, 'Infectiologie', NULL);
INSERT INTO `OpenVet12`.`MoleculePosologie` (`idMoleculePosologie`, `Molecule_idMolecule`, `Especes_idEspeces`, `VoiesAdministration_idVoiesAdministration`, `AutreAdministration`, `PosologieMin_mgkg`, `PosologieMax_mgkg`, `FrequenceJour`, `Specialite`, `Remarque`) VALUES (4, 3, 1, 1, NULL, 2.5, 2.5, 2, 'Infectiologie', NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`MedicamentConcentration`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`MedicamentConcentration` (`idMedicamentConcentration`, `Concentration_mg`, `Molecule_idMolecule`, `Medicament_idMedicament`) VALUES (1, 9.2, 1, 1);
INSERT INTO `OpenVet12`.`MedicamentConcentration` (`idMedicamentConcentration`, `Concentration_mg`, `Molecule_idMolecule`, `Medicament_idMedicament`) VALUES (2, 200, 2, 2);
INSERT INTO `OpenVet12`.`MedicamentConcentration` (`idMedicamentConcentration`, `Concentration_mg`, `Molecule_idMolecule`, `Medicament_idMedicament`) VALUES (3, 50, 3, 2);
INSERT INTO `OpenVet12`.`MedicamentConcentration` (`idMedicamentConcentration`, `Concentration_mg`, `Molecule_idMolecule`, `Medicament_idMedicament`) VALUES (4, 40, 2, 3);
INSERT INTO `OpenVet12`.`MedicamentConcentration` (`idMedicamentConcentration`, `Concentration_mg`, `Molecule_idMolecule`, `Medicament_idMedicament`) VALUES (5, 10, 3, 3);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Examen`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Examen` (`idExamen`, `Examen`) VALUES (1, 'Echocardiographie');
INSERT INTO `OpenVet12`.`Examen` (`idExamen`, `Examen`) VALUES (2, 'Echocardiographie doppler');
INSERT INTO `OpenVet12`.`Examen` (`idExamen`, `Examen`) VALUES (3, 'Radio');
INSERT INTO `OpenVet12`.`Examen` (`idExamen`, `Examen`) VALUES (4, 'Biochimie');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Critere`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Critere` (`idCritere`, `Pathologie_idPathologie`, `Examen_idExamen`, `Critere`, `Unite`, `NbGrades`, `Remarque`) VALUES (1, 1, 1, 'Epaisseur SIVd', 'mm', 3, 'en diastole');
INSERT INTO `OpenVet12`.`Critere` (`idCritere`, `Pathologie_idPathologie`, `Examen_idExamen`, `Critere`, `Unite`, `NbGrades`, `Remarque`) VALUES (2, 1, 1, 'Epaisseur PPG', 'mm', NULL, NULL);
INSERT INTO `OpenVet12`.`Critere` (`idCritere`, `Pathologie_idPathologie`, `Examen_idExamen`, `Critere`, `Unite`, `NbGrades`, `Remarque`) VALUES (3, 1, 1, 'Sténose sous Aortique', NULL, NULL, NULL);
INSERT INTO `OpenVet12`.`Critere` (`idCritere`, `Pathologie_idPathologie`, `Examen_idExamen`, `Critere`, `Unite`, `NbGrades`, `Remarque`) VALUES (4, 1, 2, 'Rapport E/A', NULL, NULL, NULL);
INSERT INTO `OpenVet12`.`Critere` (`idCritere`, `Pathologie_idPathologie`, `Examen_idExamen`, `Critere`, `Unite`, `NbGrades`, `Remarque`) VALUES (5, 1, 2, 'Durée Ar Veine Pulmonaire', 's', NULL, NULL);
INSERT INTO `OpenVet12`.`Critere` (`idCritere`, `Pathologie_idPathologie`, `Examen_idExamen`, `Critere`, `Unite`, `NbGrades`, `Remarque`) VALUES (6, 1, 2, 'Onde S/D Veine Pulmonaire', NULL, NULL, 'Non validé');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`PathologieDocument`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`PathologieDocument` (`idPathologieDocument`, `Document`) VALUES (1, 'CMH.pdf');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`DocumentsRef`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`DocumentsRef` (`idDocumentsRef`, `PathologieDocument_idPathologieDocument`, `Pathologie_idPathologie`) VALUES (1, 1, 1);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`TypeConsultation`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`TypeConsultation` (`idTypeConsultation`, `TypeConsultation`) VALUES (1, 'Vaccinale');
INSERT INTO `OpenVet12`.`TypeConsultation` (`idTypeConsultation`, `TypeConsultation`) VALUES (2, 'Motivée');
INSERT INTO `OpenVet12`.`TypeConsultation` (`idTypeConsultation`, `TypeConsultation`) VALUES (3, 'Contrôle');
INSERT INTO `OpenVet12`.`TypeConsultation` (`idTypeConsultation`, `TypeConsultation`) VALUES (4, 'Spécialisée');
INSERT INTO `OpenVet12`.`TypeConsultation` (`idTypeConsultation`, `TypeConsultation`) VALUES (5, 'Référée');
INSERT INTO `OpenVet12`.`TypeConsultation` (`idTypeConsultation`, `TypeConsultation`) VALUES (6, 'Urgence');
INSERT INTO `OpenVet12`.`TypeConsultation` (`idTypeConsultation`, `TypeConsultation`) VALUES (7, 'Chirurgie');
INSERT INTO `OpenVet12`.`TypeConsultation` (`idTypeConsultation`, `TypeConsultation`) VALUES (8, 'Comptoire');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Parametres`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Parametres` (`idParametres`, `AnalysesTypes_idAnalysesTypes`, `Especes_idEspeces`, `Parametre`, `IsQuantitatif`, `Unite`, `NormeMin`, `NormeMax`, `Remarque`) VALUES (1, 3, 1, 'Urée', 1, 'g/l', 0.4, 0.7, NULL);
INSERT INTO `OpenVet12`.`Parametres` (`idParametres`, `AnalysesTypes_idAnalysesTypes`, `Especes_idEspeces`, `Parametre`, `IsQuantitatif`, `Unite`, `NormeMin`, `NormeMax`, `Remarque`) VALUES (2, 3, 2, 'Urée', 1, 'g/l', 0.4, 0.8, NULL);
INSERT INTO `OpenVet12`.`Parametres` (`idParametres`, `AnalysesTypes_idAnalysesTypes`, `Especes_idEspeces`, `Parametre`, `IsQuantitatif`, `Unite`, `NormeMin`, `NormeMax`, `Remarque`) VALUES (3, 3, 1, 'Créatinine', 1, 'mg/l', 10, 20, NULL);
INSERT INTO `OpenVet12`.`Parametres` (`idParametres`, `AnalysesTypes_idAnalysesTypes`, `Especes_idEspeces`, `Parametre`, `IsQuantitatif`, `Unite`, `NormeMin`, `NormeMax`, `Remarque`) VALUES (4, 3, 1, 'FIV', 0, NULL, NULL, NULL, NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`ResultatAnalyse`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`ResultatAnalyse` (`idResultatAnalyse`, `Analyse_idAnalyse`, `Parametres_idParametres`, `Valeur`, `Image`, `TitreImage`, `Description`, `FichierExterne`, `Remarque`) VALUES (1, 1, 1, 1.2, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `OpenVet12`.`ResultatAnalyse` (`idResultatAnalyse`, `Analyse_idAnalyse`, `Parametres_idParametres`, `Valeur`, `Image`, `TitreImage`, `Description`, `FichierExterne`, `Remarque`) VALUES (2, 1, 3, 44, NULL, NULL, NULL, NULL, NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`PathologieRef`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`PathologieRef` (`idPathologieRef`, `Consultation_idConsultation`, `Pathologie_idPathologie`) VALUES (1, 1, 1);
INSERT INTO `OpenVet12`.`PathologieRef` (`idPathologieRef`, `Consultation_idConsultation`, `Pathologie_idPathologie`) VALUES (2, 2, 2);
INSERT INTO `OpenVet12`.`PathologieRef` (`idPathologieRef`, `Consultation_idConsultation`, `Pathologie_idPathologie`) VALUES (3, 1, 3);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`ConsultationCritere`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`ConsultationCritere` (`idConsultationCritere`, `Critere_idCritere`, `Consultation_idConsultation`, `CritereQuantitatif`, `CritereQualitatif`, `Grade`) VALUES (1, 1, 1, 8, NULL, '2/3');
INSERT INTO `OpenVet12`.`ConsultationCritere` (`idConsultationCritere`, `Critere_idCritere`, `Consultation_idConsultation`, `CritereQuantitatif`, `CritereQualitatif`, `Grade`) VALUES (2, 2, 1, 6.5, NULL, '1/3');
INSERT INTO `OpenVet12`.`ConsultationCritere` (`idConsultationCritere`, `Critere_idCritere`, `Consultation_idConsultation`, `CritereQuantitatif`, `CritereQualitatif`, `Grade`) VALUES (3, 3, 1, NULL, 'absence', '0');
INSERT INTO `OpenVet12`.`ConsultationCritere` (`idConsultationCritere`, `Critere_idCritere`, `Consultation_idConsultation`, `CritereQuantitatif`, `CritereQualitatif`, `Grade`) VALUES (4, 4, 1, 0.8, NULL, '1/3');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`PathologieEspece`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`PathologieEspece` (`idPathologieEspece`, `Pathologie_idPathologie`, `Especes_idEspeces`) VALUES (1, 1, 1);
INSERT INTO `OpenVet12`.`PathologieEspece` (`idPathologieEspece`, `Pathologie_idPathologie`, `Especes_idEspeces`) VALUES (2, 2, 1);
INSERT INTO `OpenVet12`.`PathologieEspece` (`idPathologieEspece`, `Pathologie_idPathologie`, `Especes_idEspeces`) VALUES (3, 3, 1);
INSERT INTO `OpenVet12`.`PathologieEspece` (`idPathologieEspece`, `Pathologie_idPathologie`, `Especes_idEspeces`) VALUES (4, 3, 2);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`ChirurgieLibele`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`ChirurgieLibele` (`idChirurgieLibele`, `Libele`, `Sexe`) VALUES (1, 'Entérectomie', NULL);
INSERT INTO `OpenVet12`.`ChirurgieLibele` (`idChirurgieLibele`, `Libele`, `Sexe`) VALUES (2, 'Castration', 'M');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`Chirurgie`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`Chirurgie` (`idChirurgie`, `Consultation_idConsultation`, `Description`, `Anesthesie`, `Commentaire`, `TraitementPerop`, `CompteRendu`) VALUES (1, 2, 'Enterectomie jéjunale sur Lymphome', 'Morphine+Dexdomitor+Isuflurane', 'Exeerese du NL mesentérique sans adhérences', 'Perf RL+Marbocyl', NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`ChirurgieRef`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`ChirurgieRef` (`idChirurgieRef`, `Chirurgie_idChirurgie`, `ChirurgieLibele_idChirurgieLibele`) VALUES (1, 1, 1);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`PathologieSynonyme`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`PathologieSynonyme` (`idPathologieSynonyme`, `Pathologie_idPathologie`, `Synonyme`) VALUES (1, 1, 'CMH');
INSERT INTO `OpenVet12`.`PathologieSynonyme` (`idPathologieSynonyme`, `Pathologie_idPathologie`, `Synonyme`) VALUES (2, 1, 'Cardiomyopathie féline');
INSERT INTO `OpenVet12`.`PathologieSynonyme` (`idPathologieSynonyme`, `Pathologie_idPathologie`, `Synonyme`) VALUES (3, 3, 'Pleurésie exudative');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`PathologieDomaine`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`PathologieDomaine` (`idPathologieDomaine`, `Domaine`) VALUES (1, 'Cancerologie');
INSERT INTO `OpenVet12`.`PathologieDomaine` (`idPathologieDomaine`, `Domaine`) VALUES (2, 'Cardiologie');
INSERT INTO `OpenVet12`.`PathologieDomaine` (`idPathologieDomaine`, `Domaine`) VALUES (3, 'Gastro-entérologie');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`TypeConsultationRef`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`TypeConsultationRef` (`idTypeRef`, `Consultation_idConsultation`, `TypeConsultation_idTypeConsultation`) VALUES (1, 1, 5);
INSERT INTO `OpenVet12`.`TypeConsultationRef` (`idTypeRef`, `Consultation_idConsultation`, `TypeConsultation_idTypeConsultation`) VALUES (2, 2, 4);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`ContreIndication`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`ContreIndication` (`idContreIndication`, `ContreIndication`) VALUES (1, 'BAV-II et III');
INSERT INTO `OpenVet12`.`ContreIndication` (`idContreIndication`, `ContreIndication`) VALUES (2, 'Hypotension');
INSERT INTO `OpenVet12`.`ContreIndication` (`idContreIndication`, `ContreIndication`) VALUES (3, 'Bradycardie');
INSERT INTO `OpenVet12`.`ContreIndication` (`idContreIndication`, `ContreIndication`) VALUES (4, 'Insuffisance Renale');
INSERT INTO `OpenVet12`.`ContreIndication` (`idContreIndication`, `ContreIndication`) VALUES (5, 'Beta-Bloquants');

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`ContreIndicationRef`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`ContreIndicationRef` (`idContreIndicationRef`, `ContreIndication_idContreIndication`, `Molecule_idMolecule`) VALUES (1, 1, 1);
INSERT INTO `OpenVet12`.`ContreIndicationRef` (`idContreIndicationRef`, `ContreIndication_idContreIndication`, `Molecule_idMolecule`) VALUES (2, 2, 1);
INSERT INTO `OpenVet12`.`ContreIndicationRef` (`idContreIndicationRef`, `ContreIndication_idContreIndication`, `Molecule_idMolecule`) VALUES (3, 3, 1);
INSERT INTO `OpenVet12`.`ContreIndicationRef` (`idContreIndicationRef`, `ContreIndication_idContreIndication`, `Molecule_idMolecule`) VALUES (4, 4, 1);
INSERT INTO `OpenVet12`.`ContreIndicationRef` (`idContreIndicationRef`, `ContreIndication_idContreIndication`, `Molecule_idMolecule`) VALUES (5, 5, 1);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`PathologieMoleculeRef`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`PathologieMoleculeRef` (`idPathologieMoleculeRef`, `Pathologie_idPathologie`, `MoleculePosologie_idMoleculePosologie`) VALUES (1, 1, 1);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`ClientAnimalRef`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`ClientAnimalRef` (`idClientAnimalRef`, `Client_idClient`, `Animal_idAnimal`, `DebutPropriete`, `FinPropriete`, `PourcentagePropriete`) VALUES (1, 1, 1, '2013-08-11', NULL, NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`DomaineRef`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`DomaineRef` (`idDomaineRef`, `Pathologie_idPathologie`, `PathologieDomaine_idPathologieDomaine`, `IsPrincipal`) VALUES (1, 1, 2, 1);
INSERT INTO `OpenVet12`.`DomaineRef` (`idDomaineRef`, `Pathologie_idPathologie`, `PathologieDomaine_idPathologieDomaine`, `IsPrincipal`) VALUES (2, 2, 1, NULL);
INSERT INTO `OpenVet12`.`DomaineRef` (`idDomaineRef`, `Pathologie_idPathologie`, `PathologieDomaine_idPathologieDomaine`, `IsPrincipal`) VALUES (3, 2, 3, 1);
INSERT INTO `OpenVet12`.`DomaineRef` (`idDomaineRef`, `Pathologie_idPathologie`, `PathologieDomaine_idPathologieDomaine`, `IsPrincipal`) VALUES (4, 3, 2, NULL);

COMMIT;

-- -----------------------------------------------------
-- Data for table `OpenVet12`.`CritereSeuil`
-- -----------------------------------------------------
START TRANSACTION;
USE `OpenVet12`;
INSERT INTO `OpenVet12`.`CritereSeuil` (`idCritereSeuil`, `Critere_idCritere`, `LimiteInf`, `LimiteSup`, `Grade`, `Score`) VALUES (1, 1, NULL, 6, '0', NULL);
INSERT INTO `OpenVet12`.`CritereSeuil` (`idCritereSeuil`, `Critere_idCritere`, `LimiteInf`, `LimiteSup`, `Grade`, `Score`) VALUES (2, 1, 6, 7.5, '1', NULL);
INSERT INTO `OpenVet12`.`CritereSeuil` (`idCritereSeuil`, `Critere_idCritere`, `LimiteInf`, `LimiteSup`, `Grade`, `Score`) VALUES (5, 4, 0.9, 1.2, '0', NULL);
INSERT INTO `OpenVet12`.`CritereSeuil` (`idCritereSeuil`, `Critere_idCritere`, `LimiteInf`, `LimiteSup`, `Grade`, `Score`) VALUES (3, 1, 7.5, 9, '2', NULL);
INSERT INTO `OpenVet12`.`CritereSeuil` (`idCritereSeuil`, `Critere_idCritere`, `LimiteInf`, `LimiteSup`, `Grade`, `Score`) VALUES (4, 1, 9, NULL, '3', NULL);

COMMIT;
