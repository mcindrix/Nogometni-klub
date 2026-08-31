-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: nogometni_klub
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `nogometni_klub`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `nogometni_klub` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `nogometni_klub`;

--
-- Table structure for table `clanarine`
--

DROP TABLE IF EXISTS `clanarine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clanarine` (
  `ClanarinaID` int NOT NULL AUTO_INCREMENT,
  `IgracID` int NOT NULL,
  `Iznos` float NOT NULL,
  `DatumUplate` date NOT NULL,
  `Razdoblje` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ClanarinaID`),
  KEY `IgracID` (`IgracID`),
  CONSTRAINT `clanarine_ibfk_1` FOREIGN KEY (`IgracID`) REFERENCES `igraci` (`IgracID`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clanarine`
--

LOCK TABLES `clanarine` WRITE;
/*!40000 ALTER TABLE `clanarine` DISABLE KEYS */;
INSERT INTO `clanarine` VALUES (1,1,50,'2026-08-30','2026-Q1'),(2,2,50,'2026-08-30','2026-Q2'),(3,3,45,'2026-08-30','2026-Q2');
/*!40000 ALTER TABLE `clanarine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ekipe`
--

DROP TABLE IF EXISTS `ekipe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ekipe` (
  `EkipaID` int NOT NULL AUTO_INCREMENT,
  `Naziv` varchar(100) NOT NULL,
  `Liga` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`EkipaID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ekipe`
--

LOCK TABLES `ekipe` WRITE;
/*!40000 ALTER TABLE `ekipe` DISABLE KEYS */;
INSERT INTO `ekipe` VALUES (1,'Prva momcad','1. HNL'),(2,'Juniori','Juniorska liga');
/*!40000 ALTER TABLE `ekipe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `igraci`
--

DROP TABLE IF EXISTS `igraci`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `igraci` (
  `IgracID` int NOT NULL AUTO_INCREMENT,
  `Ime` varchar(100) NOT NULL,
  `Prezime` varchar(100) NOT NULL,
  `DatumRodjenja` date DEFAULT NULL,
  `PozicijaID` int NOT NULL,
  `EkipaID` int DEFAULT NULL,
  PRIMARY KEY (`IgracID`),
  KEY `EkipaID` (`EkipaID`),
  KEY `PozicijaID` (`PozicijaID`),
  CONSTRAINT `igraci_ibfk_1` FOREIGN KEY (`EkipaID`) REFERENCES `ekipe` (`EkipaID`) ON DELETE RESTRICT,
  CONSTRAINT `igraci_ibfk_2` FOREIGN KEY (`PozicijaID`) REFERENCES `pozicije` (`PozicijaID`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `igraci`
--

LOCK TABLES `igraci` WRITE;
/*!40000 ALTER TABLE `igraci` DISABLE KEYS */;
INSERT INTO `igraci` VALUES (1,'Luka','Modric','1985-09-09',3,1),(2,'Marko','Peric','1998-02-20',4,1),(3,'Josip','Novak','2000-11-04',4,1),(4,'Ante','Maric','1996-06-15',2,1),(5,'Ivan','Juric','1994-03-30',2,1),(6,'Filip','Kovacevic','1997-07-19',2,1),(7,'Dario','Vidovic','1993-12-02',1,1),(8,'Tomislav','Barisic','1999-04-08',3,1),(9,'Nikola','Radic','1995-10-27',3,1),(10,'Karlo','Matic','2001-08-14',4,1),(11,'Mateo','Saric','2002-05-06',4,2),(12,'Borna','Blazevic','2003-01-17',2,2),(13,'Roko','Tomic','2003-09-25',1,2);
/*!40000 ALTER TABLE `igraci` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `korisnici`
--

DROP TABLE IF EXISTS `korisnici`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `korisnici` (
  `KorisnickoIme` varchar(50) NOT NULL,
  `LozinkaHash` varchar(255) NOT NULL,
  `Uloga` varchar(20) NOT NULL,
  `TrenerID` int DEFAULT NULL,
  `IgracID` int DEFAULT NULL,
  PRIMARY KEY (`KorisnickoIme`),
  KEY `IgracID` (`IgracID`),
  KEY `TrenerID` (`TrenerID`),
  CONSTRAINT `korisnici_ibfk_1` FOREIGN KEY (`IgracID`) REFERENCES `igraci` (`IgracID`) ON DELETE SET NULL,
  CONSTRAINT `korisnici_ibfk_2` FOREIGN KEY (`TrenerID`) REFERENCES `treneri` (`TrenerID`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `korisnici`
--

LOCK TABLES `korisnici` WRITE;
/*!40000 ALTER TABLE `korisnici` DISABLE KEYS */;
INSERT INTO `korisnici` VALUES ('admin','$2b$12$OARmhJw8eTCTDHDF2Eswz.1TAkHLNtbXTz/kxdg5.mdTFrjcULAk6','Admin',NULL,NULL),('igrac1','$2b$12$Qs5/OpTBo0G9h5Q2hVoalu6gue2GoE3t7amsx2YipodKubsL7MUJa','Igrac',NULL,1),('igrac2','$2b$12$lgQ/oC8yzjKibSz.MS7KyOwsqDnaVJQ8X74ShiYrmh8YDWLVtwrJO','Igrac',NULL,2),('igrac3','$2b$12$7GlQwH51GNQNN3flFl4bB.yvJH/cu9MQRUPnHeUYHlS0h6z.qquzy','Igrac',NULL,3),('igrac4','$2b$12$gb5dC5S3QCwnCfEy11IRMuXItMpWSrd11MVE3TVM3zfTfRKDG7Ekq','Igrac',NULL,4),('igrac5','$2b$12$v.oFsUDzVWUqLMUS/C/YGO5VPOGrTS4vcVXfA4Zc91QxpJVKO6AKC','Igrac',NULL,5),('trener','$2b$12$Nett4NAaGFZ.NjkayZ6nHuLgns7EqwneQk6NnQe8QhQ5DybIrLqRq','Trener',1,NULL);
/*!40000 ALTER TABLE `korisnici` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pozicije`
--

DROP TABLE IF EXISTS `pozicije`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pozicije` (
  `PozicijaID` int NOT NULL AUTO_INCREMENT,
  `Naziv` varchar(100) NOT NULL,
  `Opis` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`PozicijaID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pozicije`
--

LOCK TABLES `pozicije` WRITE;
/*!40000 ALTER TABLE `pozicije` DISABLE KEYS */;
INSERT INTO `pozicije` VALUES (1,'Vratar','Brani gol'),(2,'Branic','Igra u obrani'),(3,'Vezni','Povezuje obranu i napad'),(4,'Napadac','Zaduzen za postizanje golova');
/*!40000 ALTER TABLE `pozicije` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stadioni`
--

DROP TABLE IF EXISTS `stadioni`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stadioni` (
  `StadionID` int NOT NULL AUTO_INCREMENT,
  `Naziv` varchar(100) NOT NULL,
  `Grad` varchar(100) NOT NULL,
  `Kapacitet` int DEFAULT NULL,
  PRIMARY KEY (`StadionID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stadioni`
--

LOCK TABLES `stadioni` WRITE;
/*!40000 ALTER TABLE `stadioni` DISABLE KEYS */;
INSERT INTO `stadioni` VALUES (1,'Gradski stadion','Zagreb',15000),(2,'Stadion Kranjceviceva','Zagreb',8000),(3,'Stadion Rujevica','Rijeka',8600);
/*!40000 ALTER TABLE `stadioni` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `treneri`
--

DROP TABLE IF EXISTS `treneri`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `treneri` (
  `TrenerID` int NOT NULL AUTO_INCREMENT,
  `Ime` varchar(100) NOT NULL,
  `Prezime` varchar(100) NOT NULL,
  `Licenca` varchar(100) DEFAULT NULL,
  `DatumRodjenja` date DEFAULT NULL,
  PRIMARY KEY (`TrenerID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treneri`
--

LOCK TABLES `treneri` WRITE;
/*!40000 ALTER TABLE `treneri` DISABLE KEYS */;
INSERT INTO `treneri` VALUES (1,'Ivan','Horvat','UEFA Pro','1975-05-12'),(2,'Ana','Kovac','UEFA A','1980-09-03'),(3,'Petar','Babic','UEFA B','1988-01-22');
/*!40000 ALTER TABLE `treneri` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `treninzi`
--

DROP TABLE IF EXISTS `treninzi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `treninzi` (
  `TreningID` int NOT NULL AUTO_INCREMENT,
  `EkipaID` int NOT NULL,
  `TrenerID` int NOT NULL,
  `StadionID` int DEFAULT NULL,
  `DatumVrijeme` datetime NOT NULL,
  `Trajanje` int DEFAULT NULL,
  PRIMARY KEY (`TreningID`),
  KEY `EkipaID` (`EkipaID`),
  KEY `StadionID` (`StadionID`),
  KEY `TrenerID` (`TrenerID`),
  CONSTRAINT `treninzi_ibfk_1` FOREIGN KEY (`EkipaID`) REFERENCES `ekipe` (`EkipaID`) ON DELETE RESTRICT,
  CONSTRAINT `treninzi_ibfk_2` FOREIGN KEY (`StadionID`) REFERENCES `stadioni` (`StadionID`) ON DELETE RESTRICT,
  CONSTRAINT `treninzi_ibfk_3` FOREIGN KEY (`TrenerID`) REFERENCES `treneri` (`TrenerID`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treninzi`
--

LOCK TABLES `treninzi` WRITE;
/*!40000 ALTER TABLE `treninzi` DISABLE KEYS */;
INSERT INTO `treninzi` VALUES (1,1,1,1,'2026-08-29 14:45:40',90),(2,1,3,1,'2026-08-27 14:45:40',90),(3,2,2,2,'2026-08-28 14:45:40',90);
/*!40000 ALTER TABLE `treninzi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utakmice`
--

DROP TABLE IF EXISTS `utakmice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utakmice` (
  `UtakmicaID` int NOT NULL AUTO_INCREMENT,
  `EkipaID` int NOT NULL,
  `Protivnik` varchar(150) NOT NULL,
  `StadionID` int NOT NULL,
  `DatumVrijeme` datetime NOT NULL,
  `RezultatNas` int DEFAULT NULL,
  `RezultatProtivnik` int DEFAULT NULL,
  PRIMARY KEY (`UtakmicaID`),
  KEY `EkipaID` (`EkipaID`),
  KEY `StadionID` (`StadionID`),
  CONSTRAINT `utakmice_ibfk_1` FOREIGN KEY (`EkipaID`) REFERENCES `ekipe` (`EkipaID`) ON DELETE RESTRICT,
  CONSTRAINT `utakmice_ibfk_2` FOREIGN KEY (`StadionID`) REFERENCES `stadioni` (`StadionID`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utakmice`
--

LOCK TABLES `utakmice` WRITE;
/*!40000 ALTER TABLE `utakmice` DISABLE KEYS */;
INSERT INTO `utakmice` VALUES (1,1,'NK Susjedgrad',1,'2026-08-23 14:45:40',2,1),(2,1,'HNK Primorje',2,'2026-09-02 14:45:40',NULL,NULL),(3,2,'NK Mladost',3,'2026-08-27 14:45:40',3,0);
/*!40000 ALTER TABLE `utakmice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'nogometni_klub'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-31 19:42:32
