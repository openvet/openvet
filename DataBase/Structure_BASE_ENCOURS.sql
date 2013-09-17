SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Especes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Especes` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Especes` (
  `idEspeces` INT NOT NULL AUTO_INCREMENT ,
  `Espece` VARCHAR(60) NULL ,
  PRIMARY KEY (`idEspeces`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Race`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Race` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Race` (
  `idRace` INT NOT NULL AUTO_INCREMENT ,
  `Race` VARCHAR(50) NULL ,
  `Especes_idEspeces` INT NOT NULL ,
  INDEX `fk_Races_Especes1_idx` (`Especes_idEspeces` ASC) ,
  PRIMARY KEY (`idRace`) ,
  CONSTRAINT `fk_Races_Especes1`
    FOREIGN KEY (`Especes_idEspeces` )
    REFERENCES `OpenVet10d`.`Especes` (`idEspeces` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Animal`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Animal` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Animal` (
  `idAnimal` INT NOT NULL AUTO_INCREMENT ,
  `Animal_idPere` INT NULL ,
  `Animal_idMere` INT NULL ,
  `Nom` VARCHAR(45) NULL DEFAULT NULL ,
  `Especes_idEspeces` INT NOT NULL ,
  `Race_idRace` INT NOT NULL ,
  `Race2_idRace` INT NULL ,
  `Robe` VARCHAR(45) NULL DEFAULT NULL ,
  `Sexe` CHAR(1) NOT NULL ,
  `Naissance` DATE NOT NULL ,
  `Sterilise` TINYINT(1) NULL DEFAULT 0 ,
  `Identification` VARCHAR(14) NULL DEFAULT NULL ,
  `Remarque` VARCHAR(200) NULL DEFAULT NULL ,
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
    REFERENCES `OpenVet10d`.`Especes` (`idEspeces` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Animal_Race1`
    FOREIGN KEY (`Race_idRace` )
    REFERENCES `OpenVet10d`.`Race` (`idRace` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Animal_Race2`
    FOREIGN KEY (`Race2_idRace` )
    REFERENCES `OpenVet10d`.`Race` (`idRace` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Animal_Pere`
    FOREIGN KEY (`Animal_idPere` )
    REFERENCES `OpenVet10d`.`Animal` (`idAnimal` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Animal_Mere`
    FOREIGN KEY (`Animal_idMere` )
    REFERENCES `OpenVet10d`.`Animal` (`idAnimal` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Aliment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Aliment` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Aliment` (
  `idAliment` INT NOT NULL AUTO_INCREMENT ,
  `Animal_idAnimal1` INT NOT NULL ,
  `Date` DATE NULL DEFAULT NULL ,
  `Denomination` VARCHAR(45) NULL DEFAULT NULL ,
  `Cip` VARCHAR(8) NULL COMMENT 'CIp as a foreign key?' ,
  INDEX `fk_Aliment_Animal1_idx` (`Animal_idAnimal1` ASC) ,
  PRIMARY KEY (`idAliment`) ,
  CONSTRAINT `fk_Aliment_Animal1`
    FOREIGN KEY (`Animal_idAnimal1` )
    REFERENCES `OpenVet10d`.`Animal` (`idAnimal` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Consultation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Consultation` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Consultation` (
  `idConsultation` INT NOT NULL AUTO_INCREMENT ,
  `Animal_idAnimal` INT NOT NULL ,
  `DateConsultation` DATETIME NULL DEFAULT NULL ,
  `Veterinaires_idVeterinaires` INT NOT NULL ,
  `Examen` TEXT NULL DEFAULT NULL ,
  `Traitement` TEXT NULL DEFAULT NULL ,
  INDEX `fk_Consultation_Animal1_idx` (`Animal_idAnimal` ASC) ,
  PRIMARY KEY (`idConsultation`) ,
  CONSTRAINT `fk_Consultation_Animal1`
    FOREIGN KEY (`Animal_idAnimal` )
    REFERENCES `OpenVet10d`.`Animal` (`idAnimal` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`TypeAnalyse`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`TypeAnalyse` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`TypeAnalyse` (
  `idTypeAnalyse` INT NOT NULL AUTO_INCREMENT ,
  `Libele` VARCHAR(45) NULL ,
  `Remarque` VARCHAR(200) NULL ,
  PRIMARY KEY (`idTypeAnalyse`) ,
  UNIQUE INDEX `Libele_UNIQUE` (`Libele` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Analyse`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Analyse` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Analyse` (
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
    REFERENCES `OpenVet10d`.`Consultation` (`idConsultation` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Analyse_TypeAnalyse`
    FOREIGN KEY (`TypeAnalyse_idTypeAnalyse` )
    REFERENCES `OpenVet10d`.`TypeAnalyse` (`idTypeAnalyse` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Civilite`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Civilite` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Civilite` (
  `idCivilite` INT NOT NULL AUTO_INCREMENT ,
  `Civilite` VARCHAR(30) NOT NULL ,
  `CiviliteAbrev` VARCHAR(10) NOT NULL ,
  PRIMARY KEY (`idCivilite`) ,
  UNIQUE INDEX `Civilite_UNIQUE` (`Civilite` ASC) ,
  UNIQUE INDEX `CivilitesAbrev_UNIQUE` (`CiviliteAbrev` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Client`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Client` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Client` (
  `idClient` INT NOT NULL AUTO_INCREMENT ,
  `Civilite_idCivilite` INT NOT NULL ,
  `Nom` VARCHAR(60) CHARACTER SET 'latin1' NOT NULL ,
  `Prenom` VARCHAR(45) CHARACTER SET 'latin1' NULL ,
  `Remarque` VARCHAR(200) CHARACTER SET 'latin1' NULL DEFAULT NULL ,
  PRIMARY KEY (`idClient`) ,
  INDEX `fk_Client_Civilite_idx` (`Civilite_idCivilite` ASC) ,
  CONSTRAINT `fk_Client_Civilite`
    FOREIGN KEY (`Civilite_idCivilite` )
    REFERENCES `OpenVet10d`.`Civilite` (`idCivilite` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Facture`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Facture` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Facture` (
  `idFacture` INT(11) NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT(11) NOT NULL ,
  `Date` DATE NOT NULL ,
  `NumFacture` VARCHAR(20) NOT NULL ,
  `Reliquat` DECIMAL(6,2) NULL DEFAULT 0 ,
  `IsDevis` TINYINT(1) NULL DEFAULT FALSE ,
  `MontantHT` DECIMAL(6,2) NULL ,
  `MontantTTC` DECIMAL(6,2) NOT NULL ,
  `MontantTVA` DECIMAL(4,2) NULL ,
  `MontantRemises` DECIMAL(6,2) NULL DEFAULT 0 ,
  `IsRecouvrement` TINYINT(1) NULL DEFAULT FALSE ,
  `TotalRegle` DECIMAL(6,2) NULL COMMENT 'Est-ce nécessaire?\n' ,
  `Remarque` VARCHAR(200) NULL ,
  UNIQUE INDEX `idFactures_UNIQUE` (`idFacture` ASC) ,
  INDEX `fk_Factures_Client1_idx` (`Client_idClient` ASC) ,
  CONSTRAINT `fk_Factures_Client1`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet10d`.`Client` (`idClient` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1
COMMENT = 'Conserver données client en dur?\n';


-- -----------------------------------------------------
-- Table `OpenVet10d`.`CategoriePrestation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`CategoriePrestation` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`CategoriePrestation` (
  `idCategoriePrestation` INT NOT NULL AUTO_INCREMENT ,
  `Designation` VARCHAR(80) NOT NULL ,
  `Abreviation` VARCHAR(5) NOT NULL ,
  PRIMARY KEY (`idCategoriePrestation`) ,
  UNIQUE INDEX `Designation_UNIQUE` (`Designation` ASC) ,
  UNIQUE INDEX `Abreviation_UNIQUE` (`Abreviation` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`LignesFacture`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`LignesFacture` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`LignesFacture` (
  `Facture_idFacture` INT NOT NULL ,
  `CategoriePrestation_idCategoriePrestation` INT NOT NULL ,
  `Date` DATE NOT NULL ,
  `Denomination` VARCHAR(60) NOT NULL ,
  `PrixUnitHT` DECIMAL(6,2) NOT NULL ,
  `TVA` DECIMAL(4,2) NOT NULL ,
  `PrixUnitTTC` DECIMAL(6,2) NOT NULL ,
  `Quantite` DECIMAL(6,2) NOT NULL ,
  `TauxRemise` DECIMAL(4,2) NULL ,
  `RemisesTTC` DECIMAL(6,2) NULL ,
  `PrixTotal` DECIMAL(6,2) NOT NULL ,
  `IsGratuit` TINYINT(1) NULL DEFAULT FALSE ,
  INDEX `fk_LignesFacture_Factures1_idx` (`Facture_idFacture` ASC) ,
  INDEX `fk_LignesFacture_1_idx` (`CategoriePrestation_idCategoriePrestation` ASC) ,
  CONSTRAINT `fk_LignesFacture_Factures1`
    FOREIGN KEY (`Facture_idFacture` )
    REFERENCES `OpenVet10d`.`Facture` (`idFacture` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_LignesFacture_Categories`
    FOREIGN KEY (`CategoriePrestation_idCategoriePrestation` )
    REFERENCES `OpenVet10d`.`CategoriePrestation` (`idCategoriePrestation` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Ordonnance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Ordonnance` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Ordonnance` (
  `idOrdonnance` INT NOT NULL AUTO_INCREMENT ,
  `Consultation_idConsultation` INT NOT NULL ,
  PRIMARY KEY (`idOrdonnance`) ,
  INDEX `fk_Ordonnances_Consultation_idx` (`Consultation_idConsultation` ASC) ,
  CONSTRAINT `fk_Ordonnances_Consultation`
    FOREIGN KEY (`Consultation_idConsultation` )
    REFERENCES `OpenVet10d`.`Consultation` (`idConsultation` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`LignesOrdonnance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`LignesOrdonnance` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`LignesOrdonnance` (
  `idLigneOrdonnance` INT NOT NULL AUTO_INCREMENT ,
  `Ordonnance_idOrdonnance` INT NOT NULL ,
  `Medicament` VARCHAR(80) NULL DEFAULT NULL ,
  `Posologie` VARCHAR(255) NULL DEFAULT NULL ,
  `UnitesDelivre` DECIMAL(6,2) NULL DEFAULT NULL ,
  `UnitesPrescrites` DECIMAL(6,2) NULL ,
  `ImpressionLIgne` TINYINT(1) NULL DEFAULT True ,
  PRIMARY KEY (`idLigneOrdonnance`) ,
  INDEX `fk_LignesOrdonnances_Ordonnances_idx` (`Ordonnance_idOrdonnance` ASC) ,
  CONSTRAINT `fk_LignesOrdonnances_Ordonnances`
    FOREIGN KEY (`Ordonnance_idOrdonnance` )
    REFERENCES `OpenVet10d`.`Ordonnance` (`idOrdonnance` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`PathologieDomaine`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`PathologieDomaine` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`PathologieDomaine` (
  `idPathologieDomaine` INT NOT NULL AUTO_INCREMENT ,
  `Domaine` VARCHAR(60) NOT NULL ,
  PRIMARY KEY (`idPathologieDomaine`) ,
  UNIQUE INDEX `Domaine_UNIQUE` (`Domaine` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Pathologie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Pathologie` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Pathologie` (
  `idPathologie` INT NOT NULL AUTO_INCREMENT ,
  `PathologieDomaine_idPathologieDomaine` INT NOT NULL ,
  `NomReference` VARCHAR(60) NULL ,
  `Chronique` TINYINT(1) NULL ,
  `DescriptifPublic` TEXT NULL ,
  PRIMARY KEY (`idPathologie`) ,
  INDEX `fk_Pathologie_PathologieDomaines1_idx` (`PathologieDomaine_idPathologieDomaine` ASC) ,
  CONSTRAINT `fk_Pathologie_PathologieDomaines1`
    FOREIGN KEY (`PathologieDomaine_idPathologieDomaine` )
    REFERENCES `OpenVet10d`.`PathologieDomaine` (`idPathologieDomaine` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`PlanTherapeutique`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`PlanTherapeutique` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`PlanTherapeutique` (
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
    REFERENCES `OpenVet10d`.`Consultation` (`idConsultation` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PlanTherapeutique_Pathologie`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet10d`.`Pathologie` (`idPathologie` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`PoidsMesure`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`PoidsMesure` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`PoidsMesure` (
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
    REFERENCES `OpenVet10d`.`Animal` (`idAnimal` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`ReglementDiffere`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`ReglementDiffere` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`ReglementDiffere` (
  `idReglementDiffere` INT NOT NULL AUTO_INCREMENT ,
  `Designation` VARCHAR(45) NULL ,
  PRIMARY KEY (`idReglementDiffere`) ,
  UNIQUE INDEX `Designation_UNIQUE` (`Designation` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`TypeReglement`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`TypeReglement` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`TypeReglement` (
  `idTypeReglement` INT NOT NULL AUTO_INCREMENT ,
  `Type` VARCHAR(45) NULL ,
  `AbrevType` VARCHAR(3) NOT NULL ,
  PRIMARY KEY (`idTypeReglement`) ,
  UNIQUE INDEX `AbrevType_UNIQUE` (`AbrevType` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Reglement`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Reglement` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Reglement` (
  `idReglement` INT(11) NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT(11) NOT NULL ,
  `NomEncaissement` VARCHAR(80) NOT NULL ,
  `Date` DATE NOT NULL ,
  `Montant` DECIMAL(6,2) NOT NULL ,
  `TypeReglement_idTypeReglement` INT NOT NULL ,
  `ReglementDiffere_idReglementDiffere` INT NULL ,
  `EnBanque` TINYINT(1) NULL DEFAULT False ,
  UNIQUE INDEX `idReglements_UNIQUE` (`idReglement` ASC) ,
  INDEX `fk_Reglements_Client1_idx` (`Client_idClient` ASC) ,
  INDEX `fk_Reglements_ReglementDiffere_idx` (`ReglementDiffere_idReglementDiffere` ASC) ,
  INDEX `fk_Reglement_1_idx` (`TypeReglement_idTypeReglement` ASC) ,
  CONSTRAINT `fk_Reglements_Client1`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet10d`.`Client` (`idClient` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Reglements_ReglementDiffere`
    FOREIGN KEY (`ReglementDiffere_idReglementDiffere` )
    REFERENCES `OpenVet10d`.`ReglementDiffere` (`idReglementDiffere` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Reglement_TypeReglement`
    FOREIGN KEY (`TypeReglement_idTypeReglement` )
    REFERENCES `OpenVet10d`.`TypeReglement` (`idTypeReglement` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1
COMMENT = 'TODO : éliminer enum';


-- -----------------------------------------------------
-- Table `OpenVet10d`.`ModelRelance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`ModelRelance` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`ModelRelance` (
  `idModelRelance` INT NOT NULL AUTO_INCREMENT ,
  `Text` TINYTEXT NULL ,
  PRIMARY KEY (`idModelRelance`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Relance`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Relance` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Relance` (
  `idRelance` INT NOT NULL AUTO_INCREMENT ,
  `Animal_idAnimal` INT NOT NULL ,
  `ModelRelance_idModelRelance` INT NOT NULL ,
  `Date` DATE NOT NULL ,
  `Type` VARCHAR(10) NOT NULL COMMENT 'TODO a definir\n' ,
  `Media` VARCHAR(10) NOT NULL COMMENT 'TODO a définir\n' ,
  INDEX `fk_Relances_Animal1_idx` (`Animal_idAnimal` ASC) ,
  INDEX `fk_Relances_1_idx` (`ModelRelance_idModelRelance` ASC) ,
  PRIMARY KEY (`idRelance`) ,
  CONSTRAINT `fk_Relances_Animal1`
    FOREIGN KEY (`Animal_idAnimal` )
    REFERENCES `OpenVet10d`.`Animal` (`idAnimal` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Relances_ModelRelance`
    FOREIGN KEY (`ModelRelance_idModelRelance` )
    REFERENCES `OpenVet10d`.`ModelRelance` (`idModelRelance` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`ListVaccins`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`ListVaccins` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`ListVaccins` (
  `idListVaccins` INT NOT NULL AUTO_INCREMENT ,
  `Nom` VARCHAR(45) NOT NULL ,
  `Especes_idEspeces` INT NOT NULL ,
  PRIMARY KEY (`idListVaccins`) ,
  INDEX `fk_ListVaccins_1_idx` (`Especes_idEspeces` ASC) ,
  CONSTRAINT `Especes`
    FOREIGN KEY (`Especes_idEspeces` )
    REFERENCES `OpenVet10d`.`Especes` (`idEspeces` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Pays`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Pays` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Pays` (
  `idPays` INT NOT NULL AUTO_INCREMENT ,
  `Nom` VARCHAR(60) NULL ,
  PRIMARY KEY (`idPays`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Commune`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Commune` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Commune` (
  `idCommune` INT NOT NULL AUTO_INCREMENT ,
  `Commune` VARCHAR(45) NOT NULL ,
  `CIP` VARCHAR(45) NOT NULL ,
  `Pays_idPays` INT NOT NULL ,
  PRIMARY KEY (`idCommune`) ,
  INDEX `fk_Commune_Pays_idx` (`Pays_idPays` ASC) ,
  CONSTRAINT `fk_Commune_Pays`
    FOREIGN KEY (`Pays_idPays` )
    REFERENCES `OpenVet10d`.`Pays` (`idPays` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`TypeSociete`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`TypeSociete` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`TypeSociete` (
  `idTypeSociete` INT NOT NULL AUTO_INCREMENT ,
  `Nom` VARCHAR(45) NULL ,
  `IsVeterinaire` TINYINT(1) NULL DEFAULT True ,
  `IsNous` TINYINT(1) NOT NULL DEFAULT False ,
  PRIMARY KEY (`idTypeSociete`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Societe`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Societe` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Societe` (
  `idSociete` INT NOT NULL ,
  `TypeSociete_idTypeSociete` INT NOT NULL COMMENT 'TODO clinique, fournisseur' ,
  `Nom` VARCHAR(45) NULL ,
  `Raisonsociale` VARCHAR(45) NULL ,
  `Adresse` VARCHAR(120) NULL ,
  `Commune_idCommune` INT NOT NULL ,
  `Siret` VARCHAR(45) NULL ,
  `NTVA` VARCHAR(45) NULL ,
  `CodeNAF` VARCHAR(45) NULL DEFAULT NULL ,
  PRIMARY KEY (`idSociete`) ,
  INDEX `fk_Clinique_Commune_idx` (`Commune_idCommune` ASC) ,
  INDEX `fk_Societes_1_idx` (`TypeSociete_idTypeSociete` ASC) ,
  CONSTRAINT `fk_Clinique_Commune`
    FOREIGN KEY (`Commune_idCommune` )
    REFERENCES `OpenVet10d`.`Commune` (`idCommune` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Societes_TypeSociete`
    FOREIGN KEY (`TypeSociete_idTypeSociete` )
    REFERENCES `OpenVet10d`.`TypeSociete` (`idTypeSociete` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Vaccin`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Vaccin` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Vaccin` (
  `idVaccin` INT NOT NULL AUTO_INCREMENT ,
  `Animal_idAnimal` INT(11) NOT NULL ,
  `Date` DATE NOT NULL ,
  `ListVaccins_idListVaccins` INT NOT NULL ,
  `Relance` DATE NULL DEFAULT NULL ,
  `Societe_idSociete` INT NULL ,
  `N°Lot` VARCHAR(15) NULL ,
  INDEX `fk_Vaccins_Animal1_idx` (`Animal_idAnimal` ASC) ,
  PRIMARY KEY (`idVaccin`) ,
  INDEX `fk_Vaccins_1_idx` (`ListVaccins_idListVaccins` ASC) ,
  INDEX `fk_Vaccins_Societe_idx` (`Societe_idSociete` ASC) ,
  CONSTRAINT `fk_Vaccins_Animal1`
    FOREIGN KEY (`Animal_idAnimal` )
    REFERENCES `OpenVet10d`.`Animal` (`idAnimal` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Vaccins_ListVaccins`
    FOREIGN KEY (`ListVaccins_idListVaccins` )
    REFERENCES `OpenVet10d`.`ListVaccins` (`idListVaccins` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Vaccins_Societe`
    FOREIGN KEY (`Societe_idSociete` )
    REFERENCES `OpenVet10d`.`Societe` (`idSociete` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Banque`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Banque` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Banque` (
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
-- Table `OpenVet10d`.`Recettes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Recettes` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Recettes` (
  `idRecettes` INT NOT NULL AUTO_INCREMENT ,
  `date` DATE NOT NULL ,
  `montant` DECIMAL(8,2) NOT NULL ,
  `type` VARCHAR(20) NOT NULL ,
  `except` VARCHAR(45) NULL ,
  PRIMARY KEY (`idRecettes`) ,
  UNIQUE INDEX `date_UNIQUE` (`date` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Depenses`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Depenses` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Depenses` (
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
-- Table `OpenVet10d`.`VoiesAdministration`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`VoiesAdministration` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`VoiesAdministration` (
  `idVoiesAdministration` INT NOT NULL ,
  `VoieAdministration` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`idVoiesAdministration`) ,
  UNIQUE INDEX `VoieAdministration_UNIQUE` (`VoieAdministration` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`UniteConditionnement`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`UniteConditionnement` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`UniteConditionnement` (
  `idUniteConditionnement` INT NOT NULL AUTO_INCREMENT ,
  `UniteConditionnement` VARCHAR(30) NULL ,
  PRIMARY KEY (`idUniteConditionnement`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Medicament`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Medicament` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Medicament` (
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
    REFERENCES `OpenVet10d`.`VoiesAdministration` (`idVoiesAdministration` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Medicament_UniteConditionnement`
    FOREIGN KEY (`UniteConditionnement_idUniteConditionnement` )
    REFERENCES `OpenVet10d`.`UniteConditionnement` (`idUniteConditionnement` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`MoleculeGenre`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`MoleculeGenre` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`MoleculeGenre` (
  `idMoleculeGenre` INT NOT NULL ,
  `Genre` VARCHAR(45) NULL ,
  PRIMARY KEY (`idMoleculeGenre`) ,
  UNIQUE INDEX `Groupe_UNIQUE` (`Genre` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`MoleculeFamille`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`MoleculeFamille` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`MoleculeFamille` (
  `idMoleculeFamille` INT NOT NULL AUTO_INCREMENT ,
  `Famille` VARCHAR(45) NULL ,
  `MoleculeGenre_idMoleculeGenre` INT NOT NULL ,
  PRIMARY KEY (`idMoleculeFamille`) ,
  INDEX `fk_MoleculeFamille_MoleculeGenres1_idx` (`MoleculeGenre_idMoleculeGenre` ASC) ,
  CONSTRAINT `fk_MoleculeFamille_MoleculeGenres1`
    FOREIGN KEY (`MoleculeGenre_idMoleculeGenre` )
    REFERENCES `OpenVet10d`.`MoleculeGenre` (`idMoleculeGenre` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Molecule`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Molecule` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Molecule` (
  `idMolecule` INT NOT NULL AUTO_INCREMENT ,
  `MoleculeFamille_idMoleculeFamille` INT NOT NULL ,
  `Molecule` VARCHAR(45) NULL ,
  PRIMARY KEY (`idMolecule`) ,
  INDEX `fk_Molecules_MoleculeFamille1_idx` (`MoleculeFamille_idMoleculeFamille` ASC) ,
  CONSTRAINT `fk_Molecules_MoleculeFamille1`
    FOREIGN KEY (`MoleculeFamille_idMoleculeFamille` )
    REFERENCES `OpenVet10d`.`MoleculeFamille` (`idMoleculeFamille` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`MoleculePosologie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`MoleculePosologie` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`MoleculePosologie` (
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
    REFERENCES `OpenVet10d`.`Molecule` (`idMolecule` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PosologiesMolecules_VoiesAdministration1`
    FOREIGN KEY (`VoiesAdministration_idVoiesAdministration` )
    REFERENCES `OpenVet10d`.`VoiesAdministration` (`idVoiesAdministration` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MoleculesPosologies_Espece`
    FOREIGN KEY (`Especes_idEspeces` )
    REFERENCES `OpenVet10d`.`Especes` (`idEspeces` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`MedicamentConcentration`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`MedicamentConcentration` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`MedicamentConcentration` (
  `idMedicamentConcentration` INT NOT NULL AUTO_INCREMENT ,
  `Concentration_mg` DECIMAL(6,2) NULL ,
  `Molecule_idMolecule` INT NOT NULL ,
  `Medicament_idMedicament` INT NOT NULL ,
  PRIMARY KEY (`idMedicamentConcentration`) ,
  INDEX `fk_MedicamentConcentrations_Molecules1_idx` (`Molecule_idMolecule` ASC) ,
  INDEX `fk_MedicamentConcentrations_Medicament1_idx` (`Medicament_idMedicament` ASC) ,
  CONSTRAINT `fk_MedicamentConcentrations_Molecules1`
    FOREIGN KEY (`Molecule_idMolecule` )
    REFERENCES `OpenVet10d`.`Molecule` (`idMolecule` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MedicamentConcentrations_Medicament1`
    FOREIGN KEY (`Medicament_idMedicament` )
    REFERENCES `OpenVet10d`.`Medicament` (`idMedicament` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'Erreur GetMedicament(2)';


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Examen`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Examen` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Examen` (
  `idExamen` INT NOT NULL AUTO_INCREMENT ,
  `Examen` VARCHAR(60) NOT NULL ,
  PRIMARY KEY (`idExamen`) ,
  UNIQUE INDEX `Examen_UNIQUE` (`Examen` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Critere`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Critere` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Critere` (
  `idCritere` INT NOT NULL AUTO_INCREMENT ,
  `Pathologie_idPathologie` INT NOT NULL ,
  `Examen_idExamen` INT NOT NULL ,
  `Critere` VARCHAR(60) NOT NULL ,
  `Seuil` VARCHAR(60) NULL ,
  `Grade` VARCHAR(60) NULL ,
  `Score` INT NULL ,
  `Remarque` TEXT NULL COMMENT 'Regles de scoring' ,
  PRIMARY KEY (`idCritere`) ,
  UNIQUE INDEX `Critere_UNIQUE` (`Critere` ASC) ,
  INDEX `fk_Criteres_Pathologie_idx` (`Pathologie_idPathologie` ASC) ,
  INDEX `fk_Criteres_Examens_idx` (`Examen_idExamen` ASC) ,
  CONSTRAINT `fk_Criteres_Pathologie`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet10d`.`Pathologie` (`idPathologie` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Criteres_Examens`
    FOREIGN KEY (`Examen_idExamen` )
    REFERENCES `OpenVet10d`.`Examen` (`idExamen` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`PathologieDocument`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`PathologieDocument` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`PathologieDocument` (
  `idPathologieDocument` INT NOT NULL AUTO_INCREMENT ,
  `Document` VARCHAR(80) NOT NULL ,
  PRIMARY KEY (`idPathologieDocument`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`DocumentsRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`DocumentsRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`DocumentsRef` (
  `idDocumentsRef` INT NOT NULL AUTO_INCREMENT ,
  `PathologieDocument_idPathologieDocument` INT NOT NULL ,
  `Pathologie_idPathologie` INT NOT NULL ,
  PRIMARY KEY (`idDocumentsRef`) ,
  INDEX `fk_DocumentsRef_Documents1_idx` (`PathologieDocument_idPathologieDocument` ASC) ,
  INDEX `fk_DocumentsRef_Pathologie1_idx` (`Pathologie_idPathologie` ASC) ,
  CONSTRAINT `fk_DocumentsRef_PathologieDocuments`
    FOREIGN KEY (`PathologieDocument_idPathologieDocument` )
    REFERENCES `OpenVet10d`.`PathologieDocument` (`idPathologieDocument` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DocumentsRef_Pathologie`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet10d`.`Pathologie` (`idPathologie` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`TypeConsultation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`TypeConsultation` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`TypeConsultation` (
  `idTypeConsultation` INT NOT NULL AUTO_INCREMENT ,
  `TypeConsultation` VARCHAR(45) NULL ,
  PRIMARY KEY (`idTypeConsultation`) ,
  UNIQUE INDEX `TypeConsultation_UNIQUE` (`TypeConsultation` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Parametres`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Parametres` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Parametres` (
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
    REFERENCES `OpenVet10d`.`TypeAnalyse` (`idTypeAnalyse` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ParametresQuant_Especes1`
    FOREIGN KEY (`Especes_idEspeces` )
    REFERENCES `OpenVet10d`.`Especes` (`idEspeces` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`ResultatAnalyse`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`ResultatAnalyse` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`ResultatAnalyse` (
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
    REFERENCES `OpenVet10d`.`Parametres` (`idParametres` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`PathologieRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`PathologieRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`PathologieRef` (
  `idPathologieRef` INT NOT NULL AUTO_INCREMENT ,
  `Consultation_idConsultation` INT NOT NULL ,
  `Pathologie_idPathologie` INT NOT NULL ,
  PRIMARY KEY (`idPathologieRef`) ,
  INDEX `fk_PathologieRef_Consultation_idx` (`Consultation_idConsultation` ASC) ,
  INDEX `fk_PathologieRef_Pathologie1_idx` (`Pathologie_idPathologie` ASC) ,
  CONSTRAINT `fk_PathologieRef_Consultation`
    FOREIGN KEY (`Consultation_idConsultation` )
    REFERENCES `OpenVet10d`.`Consultation` (`idConsultation` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PathologieRef_Pathologie`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet10d`.`Pathologie` (`idPathologie` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`ConsultationCritere`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`ConsultationCritere` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`ConsultationCritere` (
  `idConsultationCritere` INT NOT NULL AUTO_INCREMENT ,
  `PlanTherapeutique_idPlanTherapeutique` INT NOT NULL ,
  `Critere_idCritere` INT NOT NULL ,
  `CritereValeur` VARCHAR(60) NULL ,
  PRIMARY KEY (`idConsultationCritere`) ,
  INDEX `fk_ConsultationCriteres_PlanTherapeutique_idx` (`PlanTherapeutique_idPlanTherapeutique` ASC) ,
  INDEX `fk_ConsultationCriteres_Criteres_idx` (`Critere_idCritere` ASC) ,
  CONSTRAINT `fk_ConsultationCriteres_PlanTherapeutique`
    FOREIGN KEY (`PlanTherapeutique_idPlanTherapeutique` )
    REFERENCES `OpenVet10d`.`PlanTherapeutique` (`idPlanTherapeutique` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ConsultationCriteres_Criteres`
    FOREIGN KEY (`Critere_idCritere` )
    REFERENCES `OpenVet10d`.`Critere` (`idCritere` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`PathologieEspece`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`PathologieEspece` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`PathologieEspece` (
  `idPathologieEspece` INT NOT NULL AUTO_INCREMENT ,
  `Pathologie_idPathologie` INT NOT NULL ,
  `Especes_idEspeces` INT NOT NULL ,
  PRIMARY KEY (`idPathologieEspece`) ,
  INDEX `fk_PathologieEspeces_Pathologie_idx` (`Pathologie_idPathologie` ASC) ,
  INDEX `fk_PathologieEspeces_Especes_idx` (`Especes_idEspeces` ASC) ,
  CONSTRAINT `fk_PathologieEspeces_Pathologie`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet10d`.`Pathologie` (`idPathologie` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PathologieEspeces_Especes`
    FOREIGN KEY (`Especes_idEspeces` )
    REFERENCES `OpenVet10d`.`Especes` (`idEspeces` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'TODEBUG\n';


-- -----------------------------------------------------
-- Table `OpenVet10d`.`ChirurgieLibele`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`ChirurgieLibele` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`ChirurgieLibele` (
  `idChirurgieLibele` INT NOT NULL AUTO_INCREMENT ,
  `Libele` VARCHAR(60) NULL ,
  PRIMARY KEY (`idChirurgieLibele`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Chirurgie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Chirurgie` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Chirurgie` (
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
    REFERENCES `OpenVet10d`.`Consultation` (`idConsultation` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`ChirurgieRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`ChirurgieRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`ChirurgieRef` (
  `idChirurgieRef` INT NOT NULL AUTO_INCREMENT ,
  `Chirurgie_idChirurgie` INT NOT NULL ,
  `ChirurgieLibele_idChirurgieLibele` INT NOT NULL ,
  PRIMARY KEY (`idChirurgieRef`) ,
  INDEX `fk_ChirurgieRef_Chirurgie_idx` (`Chirurgie_idChirurgie` ASC) ,
  INDEX `fk_ChirurgieRef_ChirurgieLibele_idx` (`ChirurgieLibele_idChirurgieLibele` ASC) ,
  CONSTRAINT `fk_Chirurgieref_Chirurgie`
    FOREIGN KEY (`Chirurgie_idChirurgie` )
    REFERENCES `OpenVet10d`.`Chirurgie` (`idChirurgie` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Chirurgieref_ChirurgieLibele`
    FOREIGN KEY (`ChirurgieLibele_idChirurgieLibele` )
    REFERENCES `OpenVet10d`.`ChirurgieLibele` (`idChirurgieLibele` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`ModelCompteRenduChirurgie`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`ModelCompteRenduChirurgie` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`ModelCompteRenduChirurgie` (
  `idModelCompteRenduChirurgie` INT NOT NULL AUTO_INCREMENT ,
  `ChirurgieLibele_idChirurgieLibele` INT NOT NULL ,
  `ModelCompteRendu` VARCHAR(80) NULL COMMENT 'Lien Fichier\n' ,
  PRIMARY KEY (`idModelCompteRenduChirurgie`) ,
  INDEX `fk_ModelCompte-renduChirurgie_ChirurgieLibele1_idx` (`ChirurgieLibele_idChirurgieLibele` ASC) ,
  CONSTRAINT `fk_ModelCompte-renduChirurgie_ChirurgieLibele1`
    FOREIGN KEY (`ChirurgieLibele_idChirurgieLibele` )
    REFERENCES `OpenVet10d`.`ChirurgieLibele` (`idChirurgieLibele` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`PathologieSynonyme`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`PathologieSynonyme` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`PathologieSynonyme` (
  `idPathologieSynonyme` INT NOT NULL AUTO_INCREMENT ,
  `Pathologie_idPathologie` INT NOT NULL ,
  `Synonyme` VARCHAR(60) NULL ,
  PRIMARY KEY (`idPathologieSynonyme`) ,
  INDEX `fk_PathologieSynonymes_Pathologie1_idx` (`Pathologie_idPathologie` ASC) ,
  CONSTRAINT `fk_PathologieSynonymes_Pathologie1`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet10d`.`Pathologie` (`idPathologie` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`TypeRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`TypeRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`TypeRef` (
  `idTypeRef` INT NOT NULL AUTO_INCREMENT ,
  `Consultation_idConsultation` INT NOT NULL ,
  `TypeConsultation_idTypeConsultation` INT NOT NULL ,
  PRIMARY KEY (`idTypeRef`) ,
  INDEX `fk_TypeRef_Consultation_idx` (`Consultation_idConsultation` ASC) ,
  INDEX `fk_TypeRef_TypeRef_idx` (`TypeConsultation_idTypeConsultation` ASC) ,
  CONSTRAINT `fk_TypeRef_Consultation`
    FOREIGN KEY (`Consultation_idConsultation` )
    REFERENCES `OpenVet10d`.`Consultation` (`idConsultation` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_TypeRef_TypeRef`
    FOREIGN KEY (`TypeConsultation_idTypeConsultation` )
    REFERENCES `OpenVet10d`.`TypeConsultation` (`idTypeConsultation` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`CentraleClasse`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`CentraleClasse` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`CentraleClasse` (
  `CodeClasse` VARCHAR(8) NOT NULL ,
  `Classe` VARCHAR(60) NULL ,
  `Cibles` VARCHAR(60) NULL ,
  `Indication` VARCHAR(60) NULL ,
  PRIMARY KEY (`CodeClasse`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`CentraleTarif`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`CentraleTarif` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`CentraleTarif` (
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
    REFERENCES `OpenVet10d`.`CentraleClasse` (`CodeClasse` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`ContreIndication`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`ContreIndication` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`ContreIndication` (
  `idContreIndication` INT NOT NULL AUTO_INCREMENT ,
  `ContreIndication` VARCHAR(80) NULL ,
  PRIMARY KEY (`idContreIndication`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`ContreIndicationRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`ContreIndicationRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`ContreIndicationRef` (
  `idContreIndicationRef` INT NOT NULL AUTO_INCREMENT ,
  `ContreIndication_idContreIndication` INT NULL ,
  `Molecule_idMolecule` INT NULL ,
  PRIMARY KEY (`idContreIndicationRef`) ,
  INDEX `fk_ContreIndicationRef_Molecules_idx` (`Molecule_idMolecule` ASC) ,
  INDEX `fk_ContreIndicationRef_ContreIndications_idx` (`ContreIndication_idContreIndication` ASC) ,
  CONSTRAINT `fk_ContreIndicationRef_Molecules`
    FOREIGN KEY (`Molecule_idMolecule` )
    REFERENCES `OpenVet10d`.`Molecule` (`idMolecule` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ContreIndicationRef_ContreIndications`
    FOREIGN KEY (`ContreIndication_idContreIndication` )
    REFERENCES `OpenVet10d`.`ContreIndication` (`idContreIndication` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`PathologieMoleculeRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`PathologieMoleculeRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`PathologieMoleculeRef` (
  `idPathologieMoleculeRef` INT NOT NULL AUTO_INCREMENT ,
  `Pathologie_idPathologie` INT NULL ,
  `MoleculePosologie_idMoleculePosologie` INT NULL ,
  PRIMARY KEY (`idPathologieMoleculeRef`) ,
  INDEX `fk_PathologieMoldeculeRef_Pathologie_idx` (`Pathologie_idPathologie` ASC) ,
  INDEX `fk_PathologieMoldeculeRef_MoleculesPosologie_idx` (`MoleculePosologie_idMoleculePosologie` ASC) ,
  CONSTRAINT `fk_PathologieMoleculeRef_Pathologie`
    FOREIGN KEY (`Pathologie_idPathologie` )
    REFERENCES `OpenVet10d`.`Pathologie` (`idPathologie` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PathologieMoleculeRef_MoleculesPosologie`
    FOREIGN KEY (`MoleculePosologie_idMoleculePosologie` )
    REFERENCES `OpenVet10d`.`MoleculePosologie` (`idMoleculePosologie` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`ClientAnimalRef`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`ClientAnimalRef` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`ClientAnimalRef` (
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
    REFERENCES `OpenVet10d`.`Client` (`idClient` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ClientAnimalRef_Animal`
    FOREIGN KEY (`Animal_idAnimal` )
    REFERENCES `OpenVet10d`.`Animal` (`idAnimal` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`ComptebancaireClient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`ComptebancaireClient` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`ComptebancaireClient` (
  `idCompte bancaire` INT NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT NOT NULL ,
  `NCompte` VARCHAR(45) NULL ,
  `BanqueNom` VARCHAR(45) NULL ,
  `Adresse` VARCHAR(120) NULL ,
  `Commune_idCommune` INT NULL ,
  PRIMARY KEY (`idCompte bancaire`) ,
  INDEX `fk_ComptebancaireClient_Client_idx` (`Client_idClient` ASC) ,
  INDEX `fk_ComptebancaireClient_Commune_idx` (`Commune_idCommune` ASC) ,
  CONSTRAINT `fk_ComptebancaireClient_Client`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet10d`.`Client` (`idClient` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_ComptebancaireClient_Commune`
    FOREIGN KEY (`Commune_idCommune` )
    REFERENCES `OpenVet10d`.`Commune` (`idCommune` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Repertoire`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Repertoire` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Repertoire` (
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
-- Table `OpenVet10d`.`TypeCollaborateur`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`TypeCollaborateur` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`TypeCollaborateur` (
  `idTypeCollaborateur` INT NOT NULL AUTO_INCREMENT ,
  `Nom` VARCHAR(45) NULL ,
  `IsVeterinaire` TINYINT(1) NULL DEFAULT TRUE ,
  `IsSalarie` TINYINT(1) NULL ,
  PRIMARY KEY (`idTypeCollaborateur`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Collaborateur`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Collaborateur` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Collaborateur` (
  `idCollaborateur` INT NOT NULL AUTO_INCREMENT ,
  `TypeCollaborateur_idTypeCollaborateur` INT NOT NULL COMMENT 'TODO definir\n' ,
  `Societe_idSociete` INT NOT NULL COMMENT 'Nom de compagnie pour fournisseurs\n' ,
  `Civilite_idCivilite` INT NOT NULL ,
  `Nom` VARCHAR(45) NULL ,
  `NomMarital` VARCHAR(45) NULL ,
  `Prenom` VARCHAR(45) NULL ,
  `AutresPrénoms` VARCHAR(120) NULL ,
  `Adresse` VARCHAR(120) NULL ,
  `Commune_idCommune` INT NULL ,
  `NSS` VARCHAR(15) NULL COMMENT 'Sal' ,
  `DateEntree` DATE NULL ,
  `FinContrat` DATE NULL COMMENT 'Sal' ,
  `DateNaissance` DATE NULL ,
  `LieuNaissance` VARCHAR(45) NULL ,
  `Emploi` VARCHAR(45) NULL COMMENT 'Sal' ,
  `Echellon` VARCHAR(12) NULL COMMENT 'Sal' ,
  `Coefficient` DECIMAL(4,2) NULL COMMENT 'Sal\n' ,
  `SalaireHoraire` DECIMAL(4,2) NULL COMMENT 'Sal\n' ,
  `ConventionCollective` VARCHAR(8) NULL COMMENT 'Sal\n' ,
  `Cadre` TINYINT(1) NULL DEFAULT False COMMENT 'Sal\n' ,
  `Temporaire` TINYINT(1) NULL DEFAULT False COMMENT 'Sal\n' ,
  `Specialite` VARCHAR(45) NULL COMMENT 'Vet' ,
  `N°Ordre` VARCHAR(8) NULL COMMENT 'Vet' ,
  `N°URSSAF` VARCHAR(15) NULL ,
  `N°CARPV` VARCHAR(15) NULL ,
  `PartSociales` DECIMAL(4,2) NULL ,
  `Remarque` VARCHAR(200) NULL ,
  PRIMARY KEY (`idCollaborateur`) ,
  UNIQUE INDEX `N°URSSAF_UNIQUE` (`N°URSSAF` ASC) ,
  UNIQUE INDEX `N°CARPV_UNIQUE` (`N°CARPV` ASC) ,
  UNIQUE INDEX `N°Ordre_UNIQUE` (`N°Ordre` ASC) ,
  INDEX `fk_Collaborateurs_Commune_idx` (`Commune_idCommune` ASC) ,
  INDEX `fk_Collaborateurs_Societe_idx` (`Societe_idSociete` ASC) ,
  INDEX `fk_Collaborateurs_TypeCollaborateur_idx` (`TypeCollaborateur_idTypeCollaborateur` ASC) ,
  INDEX `fk_Collaborateurs_Civilite_idx` (`Civilite_idCivilite` ASC) ,
  CONSTRAINT `fk_Collaborateurs_Commune`
    FOREIGN KEY (`Commune_idCommune` )
    REFERENCES `OpenVet10d`.`Commune` (`idCommune` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Collaborateurs_Societe`
    FOREIGN KEY (`Societe_idSociete` )
    REFERENCES `OpenVet10d`.`Societe` (`idSociete` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Collaborateurs_TypeCollaborateur`
    FOREIGN KEY (`TypeCollaborateur_idTypeCollaborateur` )
    REFERENCES `OpenVet10d`.`TypeCollaborateur` (`idTypeCollaborateur` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Collaborateurs_Civilite`
    FOREIGN KEY (`Civilite_idCivilite` )
    REFERENCES `OpenVet10d`.`Civilite` (`idCivilite` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`RemiseClient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`RemiseClient` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`RemiseClient` (
  `idRemiseClient` INT NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT NOT NULL ,
  `Designation` VARCHAR(120) NULL ,
  `Montant%` INT NULL ,
  PRIMARY KEY (`idRemiseClient`) ,
  INDEX `fk_Remises_Client_idx` (`Client_idClient` ASC) ,
  CONSTRAINT `fk_Remises_Client`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet10d`.`Client` (`idClient` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`RelanceFacture`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`RelanceFacture` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`RelanceFacture` (
  `idRelanceFacture` INT NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT NOT NULL ,
  `Date` DATE NULL ,
  `NiveauRelance` VARCHAR(45) NULL ,
  `MontantPrincipal` DECIMAL(6,2) NULL ,
  `MontantFrais` DECIMAL(6,2) NULL ,
  PRIMARY KEY (`idRelanceFacture`) ,
  INDEX `fk_Relances_Client_idx` (`Client_idClient` ASC) ,
  CONSTRAINT `fk_Relances_Client`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet10d`.`Client` (`idClient` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`TVA`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`TVA` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`TVA` (
  `idTVA` INT NOT NULL AUTO_INCREMENT ,
  `Taux` DECIMAL(6,2) NOT NULL ,
  PRIMARY KEY (`idTVA`) ,
  UNIQUE INDEX `Taux_UNIQUE` (`Taux` ASC) )
ENGINE = InnoDB
COMMENT = '\n';


-- -----------------------------------------------------
-- Table `OpenVet10d`.`PrixActe`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`PrixActe` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`PrixActe` (
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
    REFERENCES `OpenVet10d`.`TVA` (`idTVA` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`FacturationConfig`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`FacturationConfig` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`FacturationConfig` (
  `idFacturationConfig` INT NOT NULL AUTO_INCREMENT ,
  `AMO` DECIMAL(6,2) NULL ,
  `Arrondi` DECIMAL(6,2) NULL DEFAULT 0.05 ,
  `Monnaie` VARCHAR(20) NULL DEFAULT 'Euro' ,
  `AbrevMonnaie` VARCHAR(5) NULL DEFAULT '€' ,
  PRIMARY KEY (`idFacturationConfig`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Incineration`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Incineration` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Incineration` (
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
    REFERENCES `OpenVet10d`.`Animal` (`idAnimal` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Incineration_Fournisseur`
    FOREIGN KEY (`Societe_idSociete` )
    REFERENCES `OpenVet10d`.`Societe` (`idSociete` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`LienClient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`LienClient` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`LienClient` (
  `idLienFamille` INT NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT NOT NULL ,
  `client_idRelation` INT NOT NULL ,
  `TypeRelation` VARCHAR(45) NULL COMMENT 'TODO table externe?\nInclure Tutelle\n' ,
  `IsTutelle` TINYINT(1) NULL DEFAULT FALSE ,
  PRIMARY KEY (`idLienFamille`) ,
  INDEX `fk_LienFamille_Client_idx` (`Client_idClient` ASC) ,
  INDEX `fk_LienFamille_Parent_idx` (`client_idRelation` ASC) ,
  CONSTRAINT `fk_LienFamille_Client`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet10d`.`Client` (`idClient` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_LienFamille_Relation`
    FOREIGN KEY (`client_idRelation` )
    REFERENCES `OpenVet10d`.`Client` (`idClient` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`NomRue`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`NomRue` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`NomRue` (
  `idNomRue` INT NOT NULL AUTO_INCREMENT ,
  `NomRue` VARCHAR(60) NULL ,
  PRIMARY KEY (`idNomRue`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Adresse`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Adresse` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Adresse` (
  `idAdresse` INT NOT NULL AUTO_INCREMENT ,
  `Commune_idCommune` INT NOT NULL ,
  `NomRue_idNomRue` INT NOT NULL ,
  `No` VARCHAR(80) NULL COMMENT 'No rue,batiment' ,
  `IsValide` TINYINT(1) NULL DEFAULT TRUE ,
  `IsPrincipale` TINYINT(1) NULL ,
  `DateEnregistrement` DATE NOT NULL ,
  `DateFinValidite` DATE NULL DEFAULT NULL ,
  `Remarque` VARCHAR(200) NULL ,
  INDEX `fk_Adresse_Commune_idx` (`Commune_idCommune` ASC) ,
  PRIMARY KEY (`idAdresse`) ,
  INDEX `fk_Adresse_NomRue1_idx` (`NomRue_idNomRue` ASC) ,
  CONSTRAINT `fk_Adresse_Commune`
    FOREIGN KEY (`Commune_idCommune` )
    REFERENCES `OpenVet10d`.`Commune` (`idCommune` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Adresse_NomRue1`
    FOREIGN KEY (`NomRue_idNomRue` )
    REFERENCES `OpenVet10d`.`NomRue` (`idNomRue` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`AdresseHistorique`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`AdresseHistorique` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`AdresseHistorique` (
  `idAdresseHistorique` INT NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT NOT NULL ,
  `Adresse_idAdresse` INT NOT NULL ,
  `DateChangement` DATE NULL ,
  PRIMARY KEY (`idAdresseHistorique`) ,
  INDEX `fk_AdresseHistorique_Client_idx` (`Client_idClient` ASC) ,
  INDEX `fk_AdresseHistorique_Adresse1_idx` (`Adresse_idAdresse` ASC) ,
  CONSTRAINT `fk_AdresseHistorique_Client`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet10d`.`Client` (`idClient` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_AdresseHistorique_Adresse1`
    FOREIGN KEY (`Adresse_idAdresse` )
    REFERENCES `OpenVet10d`.`Adresse` (`idAdresse` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
COMMENT = 'TODO';


-- -----------------------------------------------------
-- Table `OpenVet10d`.`RendezVous`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`RendezVous` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`RendezVous` (
  `idRendezVous` INT NOT NULL AUTO_INCREMENT ,
  `Client_idClient` INT NOT NULL ,
  `RendezVous` DATETIME NULL ,
  `Animal` VARCHAR(80) NULL ,
  `Motif` VARCHAR(80) NULL ,
  `Veterinaires_idVeterinaires` INT NULL DEFAULT NULL ,
  `SalleAttente` TINYINT(1) NULL DEFAULT FALSE ,
  `PrisEnCharge` TINYINT(1) NULL DEFAULT FALSE ,
  `Hospitalisation` TINYINT(1) NULL DEFAULT FALSE ,
  `Remarque` VARCHAR(200) NULL ,
  PRIMARY KEY (`idRendezVous`) ,
  INDEX `fk_RendezVous_Client_idx` (`Client_idClient` ASC) ,
  INDEX `fk_RendezVous_1_idx` (`Veterinaires_idVeterinaires` ASC) ,
  CONSTRAINT `fk_RendezVous_Client`
    FOREIGN KEY (`Client_idClient` )
    REFERENCES `OpenVet10d`.`Client` (`idClient` )
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_RendezVous_Veterinaire`
    FOREIGN KEY (`Veterinaires_idVeterinaires` )
    REFERENCES `OpenVet10d`.`Collaborateur` (`idCollaborateur` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Materiel`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Materiel` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Materiel` (
  `idMateriel` INT NOT NULL AUTO_INCREMENT ,
  `Societe_idSociete` INT NULL ,
  `Collaborateur_idCollaborateur` INT NULL COMMENT 'SAV\n' ,
  `TypeAnalyse_TypeAnalyse` INT NULL ,
  `NomAppareil` VARCHAR(60) NULL ,
  `DateAchat` VARCHAR(45) NULL ,
  `PrixHT` DECIMAL(8,2) NULL ,
  `DateOpeMaintenance` DATETIME NULL COMMENT 'Prochaine opération de maintenance\n' ,
  `LibeleOpeMaintenance` VARCHAR(80) NULL ,
  `Remarque` VARCHAR(200) NULL ,
  PRIMARY KEY (`idMateriel`) ,
  INDEX `fk_Materiel_Collaborateur_idx` (`Collaborateur_idCollaborateur` ASC) ,
  INDEX `fk_Materiel_1_idx` (`Societe_idSociete` ASC) ,
  INDEX `fk_Materiel_1_idx1` (`TypeAnalyse_TypeAnalyse` ASC) ,
  CONSTRAINT `fk_Materiel_Collaborateur`
    FOREIGN KEY (`Collaborateur_idCollaborateur` )
    REFERENCES `OpenVet10d`.`Collaborateur` (`idCollaborateur` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Materiel_Societe`
    FOREIGN KEY (`Societe_idSociete` )
    REFERENCES `OpenVet10d`.`Societe` (`idSociete` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Materiel_TypeAnalyse`
    FOREIGN KEY (`TypeAnalyse_TypeAnalyse` )
    REFERENCES `OpenVet10d`.`TypeAnalyse` (`idTypeAnalyse` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`Historique`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Historique` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Historique` (
  `idHistorique` INT NOT NULL AUTO_INCREMENT ,
  `Temps` TIMESTAMP NOT NULL COMMENT 'Instant de la Modification\n' ,
  `Table` VARCHAR(60) NOT NULL COMMENT 'Table Modifiée\n' ,
  `Utilisateur` VARCHAR(60) NOT NULL ,
  PRIMARY KEY (`idHistorique`) ,
  UNIQUE INDEX `Utilisateur_UNIQUE` (`Utilisateur` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `OpenVet10d`.`ParametreBase`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`ParametreBase` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`ParametreBase` (
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
-- Table `OpenVet10d`.`Commune_has_Rue`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OpenVet10d`.`Commune_has_Rue` ;

CREATE  TABLE IF NOT EXISTS `OpenVet10d`.`Commune_has_Rue` (
  `NomRue_idNomRue` INT NOT NULL ,
  `Commune_idCommune` INT NOT NULL ,
  PRIMARY KEY (`NomRue_idNomRue`, `Commune_idCommune`) ,
  INDEX `fk_NomRue_has_Commune_Commune1_idx` (`Commune_idCommune` ASC) ,
  INDEX `fk_NomRue_has_Commune_NomRue1_idx` (`NomRue_idNomRue` ASC) ,
  CONSTRAINT `fk_NomRue_has_Commune_NomRue1`
    FOREIGN KEY (`NomRue_idNomRue` )
    REFERENCES `OpenVet10d`.`NomRue` (`idNomRue` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_NomRue_has_Commune_Commune1`
    FOREIGN KEY (`Commune_idCommune` )
    REFERENCES `OpenVet10d`.`Commune` (`idCommune` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- procedure GetConsultation
-- -----------------------------------------------------

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetConsultation`;

DELIMITER $$
USE `OpenVet10d`$$


CREATE DEFINER=`root`@`localhost` PROCEDURE `GetConsultation`(IN IndexAnimal INT)
BEGIN
SELECT idConsultation,DateConsultation,
(SELECT GROUP_CONCAT(TypeConsultation) FROM TypeConsultation,TypeRef WHERE idTypeConsultation=TypeConsultation_idTypeConsultation AND TypeRef.Consultation_idConsultation=idConsultation) AS TypeConsultation,
(SELECT CONCAT(Nom," ",Prenom) FROM Veterinaires WHERE idVeterinaires=Veterinaires_idVeterinaires) AS Veterinaire,
(SELECT GROUP_CONCAT(NomReference) FROM Pathologie,PathologieRef WHERE idPathologie=Pathologie_idPathologie AND Consultation_idConsultation=idConsultation) AS Pathologie,
Examen,Traitement,
(SELECT COUNT(idAnalyse) FROM Analyse, AnalysesTypes WHERE Analyse.Consultation_idConsultation=idConsultation AND idAnalysesTypes=AnalysesTypes_idAnalysesTypes AND Genre!='image') AS Biologie,
(SELECT COUNT(idAnalyse) FROM Analyse, AnalysesTypes WHERE Analyse.Consultation_idConsultation=idConsultation AND idAnalysesTypes=AnalysesTypes_idAnalysesTypes AND Genre='image') AS Imagerie,
(SELECT COUNT(idChirurgie) FROM Chirurgie WHERE Chirurgie.Consultation_idConsultation=idConsultation) AS Chirurgie,
(SELECT COUNT(idOrdonnances) FROM Ordonnances WHERE Ordonnances.Consultation_idConsultation=idConsultation) AS Ordonnance,
(SELECT COUNT(idPlanTherapeutique) FROM PlanTherapeutique WHERE PlanTherapeutique.Consultation_idConsultation=idConsultation) AS PlanTherapeutique
FROM Consultation WHERE Animal_idAnimal=IndexAnimal;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetOrdonnance
-- -----------------------------------------------------

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetOrdonnance`;

DELIMITER $$
USE `OpenVet10d`$$




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

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetPlanTherapeutique`;

DELIMITER $$
USE `OpenVet10d`$$




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
-- procedure GetBiologie
-- -----------------------------------------------------

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetBiologie`;

DELIMITER $$
USE `OpenVet10d`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `GetBiologie`(IN IndexConsultation INT)
BEGIN
SELECT idAnalyse,Description
FROM Analyse,AnalysesTypes
WHERE Consultation_idConsultation=Indexconsultation AND idAnalyse=AnalysesTypes_idAnalysesTypes AND Genre!='image';
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetImages
-- -----------------------------------------------------

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetImages`;

DELIMITER $$
USE `OpenVet10d`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `GetImages`(IN IndexConsultation INT)
BEGIN
SELECT idAnalyse,Description
FROM Analyse,AnalysesTypes
WHERE Consultation_idConsultation=Indexconsultation AND idAnalyse=AnalysesTypes_idAnalysesTypes AND Genre='image';
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetChirurgie
-- -----------------------------------------------------

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetChirurgie`;

DELIMITER $$
USE `OpenVet10d`$$





CREATE DEFINER=`root`@`localhost` PROCEDURE `GetChirurgie`(IN IndexConsultation INT)
BEGIN
SELECT Description,
(SELECT Libele FROM ChirurgieLibele,ChirurgieRef WHERE idChirurgieLibele=ChirurgieLibele_idChirurgieLibele AND Chirurgie_idChirurgie=idChirurgie) AS Libele,
(SELECT CompteRendu FROM CompteRenduChirurgie WHERE Chirurgie_idChirurgie=1) AS CompteRendu
FROM Chirurgie
WHERE Consultation_idConsultation=IndexConsultation;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetImagerie
-- -----------------------------------------------------

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetImagerie`;

DELIMITER $$
USE `OpenVet10d`$$




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

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`SelectPathologie`;

DELIMITER $$
USE `OpenVet10d`$$




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

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetPathologie`;

DELIMITER $$
USE `OpenVet10d`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPathologie`(IN IndexPathologie INT)
BEGIN
SELECT NomReference,Chronique,
(SELECT Domaine FROM PathologieDomaines WHERE idPathologieDomaines=PathologieDomaines_idPathologieDomaines) AS Domaine,
(SELECT GROUP_CONCAT(PathologieDocuments_idPathologieDocuments) FROM DocumentsRef WHERE Pathologie_idPathologie=idPathologie) AS Documents,
DescriptifPublic,
(SELECT COUNT(idCriteres) FROM Criteres WHERE Pathologie_idPathologie=idPathologie) AS Criteres
FROM Pathologie WHERE idPathologie=IndexPathologie;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetCriteres
-- -----------------------------------------------------

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetCriteres`;

DELIMITER $$
USE `OpenVet10d`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `GetCriteres`(IN IndexPathologie INT)
BEGIN
SELECT (SELECT Examen FROM Examens WHERE idExamens=Examens_idExamens) AS Examen,
Critere,Seuil,Grade,Score
FROM Criteres WHERE Pathologie_idPathologie=IndexPathologie;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetMoleculesForPathologie
-- -----------------------------------------------------

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetMoleculesForPathologie`;

DELIMITER $$
USE `OpenVet10d`$$


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
-- procedure ViewPathologies
-- -----------------------------------------------------

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`ViewPathologies`;

DELIMITER $$
USE `OpenVet10d`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `ViewPathologies`(IN IndexEspece INT)
BEGIN
DROP TABLE IF EXISTS ScanPathologie ;
CREATE TABLE ScanPathologie AS
SELECT idPathologie,NomReference,
(SELECT GROUP_CONCAT(Synonyme) FROM PathologieSynonymes WHERE Pathologie_idPathologie=idPathologie) AS Synonymes,
(SELECT idPathologieDomaines FROM PathologieDomaines WHERE idPathologieDomaines=PathologieDomaines_idPathologieDomaines) AS idDomaine
FROM Pathologie,PathologieEspeces
WHERE idPathologie=PathologieEspeces.Pathologie_idPathologie
AND PathologieEspeces.Especes_idEspeces=IndexEspece ORDER BY idDomaine;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetPathologiesConsult
-- -----------------------------------------------------

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetPathologiesConsult`;

DELIMITER $$
USE `OpenVet10d`$$


CREATE DEFINER=`root`@`localhost` PROCEDURE `GetPathologiesConsult`(IN IndexConsultation INT)
BEGIN
SELECT idPathologie,NomReference
FROM Pathologie,PathologieRef
WHERE Consultation_idConsultation=IndexConsultation AND idPathologie=Pathologie_idPathologie;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure GetMolecule
-- -----------------------------------------------------

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetMolecule`;

DELIMITER $$
USE `OpenVet10d`$$




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

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetMedicament`;

DELIMITER $$
USE `OpenVet10d`$$




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

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetTarif`;

DELIMITER $$
USE `OpenVet10d`$$




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

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetResultatLiquide`;

DELIMITER $$
USE `OpenVet10d`$$


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

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetResultatImage`;

DELIMITER $$
USE `OpenVet10d`$$




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

USE `OpenVet10d`;
DROP procedure IF EXISTS `OpenVet10d`.`GetAnalyseAnimal`;

DELIMITER $$
USE `OpenVet10d`$$




CREATE DEFINER=`root`@`localhost` PROCEDURE `GetAnalyseAnimal`(IN IndexAnimal INT)
BEGIN
SELECT idAnalyse,DescriptionAnalyse,DateHeure,
(SELECT Libele FROM TypeAnalyse WHERE idTypeAnalyse=TypeAnalyse_idTypeAnalyse) AS TypeAnalyse,
(SELECT count(FichierExterne) FROM ResultatAnalyse WHERE Analyse_idAnalyse=idAnalyse AND FichierExterne IS NOT NULL) AS Document
FROM Analyse,Consultation
WHERE Consultation_idConsultation=idConsultation AND Animal_idAnimal=IndexAnimal;
END$$

DELIMITER ;
USE `OpenVet10d`;

DELIMITER $$

USE `OpenVet10d`$$
DROP TRIGGER IF EXISTS `OpenVet10d`.`IsDoublon` $$
USE `OpenVet10d`$$




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
