-- MySQL dump 10.13  Distrib 5.5.41, for debian-linux-gnu (x86_64)
--
-- Host: srsqlln01.uhbs.ch    Database: planoaa
-- ------------------------------------------------------
-- Server version	5.1.63-0+squeeze1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `action`
--

DROP TABLE IF EXISTS `action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `action` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `mask` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `def` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`aid`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `color`
--

DROP TABLE IF EXISTS `color`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `color` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `bg` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `fg` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log` (
  `lid` int(11) NOT NULL AUTO_INCREMENT,
  `ip` char(15) DEFAULT NULL,
  `tabname` varchar(50) DEFAULT NULL,
  `filename` varchar(50) DEFAULT NULL,
  `recid` int(11) DEFAULT NULL,
  `recidx` varchar(20) DEFAULT NULL,
  `recstr` text,
  `tst` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `comment` text,
  `uid` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`lid`)
) ENGINE=MyISAM AUTO_INCREMENT=196607 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `module`
--

DROP TABLE IF EXISTS `module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `module` (
  `mid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `beschrieb` varchar(150) DEFAULT NULL,
  `action` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`mid`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notes` (
  `nid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `ym` char(6) DEFAULT NULL,
  `color` char(10) DEFAULT NULL,
  `comment` text,
  PRIMARY KEY (`nid`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permission` (
  `prid` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `mid` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  PRIMARY KEY (`prid`)
) ENGINE=MyISAM AUTO_INCREMENT=361 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `personal`
--

DROP TABLE IF EXISTS `personal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `personal` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `pidp` int(11) NOT NULL DEFAULT '0',
  `personalid` varchar(20) DEFAULT NULL,
  `aktiv` varchar(1) DEFAULT NULL,
  `kuerzel` varchar(20) DEFAULT NULL,
  `ptid` int(11) NOT NULL DEFAULT '5',
  `anrede` varchar(20) DEFAULT NULL,
  `titel` varchar(20) DEFAULT NULL,
  `name` varchar(40) NOT NULL,
  `vorname` varchar(30) NOT NULL,
  `adresse` varchar(100) DEFAULT NULL,
  `plz` varchar(10) DEFAULT NULL,
  `wohnort` varchar(30) DEFAULT NULL,
  `tel_p` varchar(15) DEFAULT NULL,
  `tel_g` varchar(15) DEFAULT NULL,
  `natel` varchar(15) DEFAULT NULL,
  `fax` varchar(15) DEFAULT NULL,
  `gebdatum` date DEFAULT NULL,
  `bemerkung1` text,
  `bemerkung2` text,
  `f1` varchar(20) DEFAULT NULL,
  `f2` varchar(20) DEFAULT NULL,
  `f3` varchar(20) DEFAULT NULL,
  `f4` varchar(20) DEFAULT NULL,
  `f5` varchar(20) DEFAULT NULL,
  `f6` varchar(20) DEFAULT NULL,
  `f7` varchar(20) DEFAULT NULL,
  `f8` varchar(20) DEFAULT NULL,
  `f9` varchar(20) DEFAULT NULL,
  `f10` varchar(20) DEFAULT NULL,
  `f11` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `combi` int(10) DEFAULT NULL,
  `notarzt` varchar(1) DEFAULT NULL,
  `sgnor` varchar(1) DEFAULT NULL,
  `verfuegbar` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=MyISAM AUTO_INCREMENT=585 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `perstyp`
--

DROP TABLE IF EXISTS `perstyp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perstyp` (
  `ptid` int(11) NOT NULL AUTO_INCREMENT,
  `kurz` varchar(4) CHARACTER SET utf8 DEFAULT NULL,
  `lang` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `sort` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`ptid`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rot_einteilung`
--

DROP TABLE IF EXISTS `rot_einteilung`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rot_einteilung` (
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `deleted` int(11) DEFAULT '0',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) DEFAULT NULL,
  `von` date DEFAULT NULL,
  `bis` date DEFAULT NULL,
  `rot_id` int(11) DEFAULT NULL,
  `wunsch` int(11) DEFAULT NULL,
  `prio` int(11) DEFAULT NULL,
  `bgrad` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rot_id` (`rot_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rot_erfahrung`
--

DROP TABLE IF EXISTS `rot_erfahrung`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rot_erfahrung` (
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `deleted` int(11) DEFAULT '0',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `von_mj` int(11) DEFAULT NULL,
  `bis_mj` int(11) DEFAULT NULL,
  `monate` int(11) DEFAULT NULL,
  `ort` varchar(100) DEFAULT NULL,
  `was` varchar(100) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rot_group`
--

DROP TABLE IF EXISTS `rot_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rot_group` (
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `deleted` int(11) DEFAULT '0',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `sort` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rot_location`
--

DROP TABLE IF EXISTS `rot_location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rot_location` (
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `deleted` int(11) DEFAULT '0',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `sort` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rot_note2tags`
--

DROP TABLE IF EXISTS `rot_note2tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rot_note2tags` (
  `rotnote_id` int(11) DEFAULT NULL,
  `nodetag_id` int(11) DEFAULT NULL,
  KEY `rotnote_id` (`rotnote_id`),
  KEY `nodetag_id` (`nodetag_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rot_notes`
--

DROP TABLE IF EXISTS `rot_notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rot_notes` (
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `deleted` int(11) DEFAULT '0',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment` text,
  `pid` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `bis` date DEFAULT NULL,
  `pnid` int(11) DEFAULT NULL,
  `done` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rot_notetag`
--

DROP TABLE IF EXISTS `rot_notetag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rot_notetag` (
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `deleted` int(11) DEFAULT '0',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rot_pers`
--

DROP TABLE IF EXISTS `rot_pers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rot_pers` (
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `deleted` int(11) DEFAULT '0',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `foto` longblob,
  `foto_cropped` longblob,
  `foto_thumbnail` longblob,
  `pid` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rot_rot`
--

DROP TABLE IF EXISTS `rot_rot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rot_rot` (
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `deleted` int(11) DEFAULT '0',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `bemerkung` varchar(250) DEFAULT NULL,
  `sort` int(11) DEFAULT NULL,
  `dauer_von` int(11) DEFAULT NULL,
  `dauer_bis` int(11) DEFAULT NULL,
  `dauer_step` int(11) DEFAULT NULL,
  `erstjahr` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `location_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id` (`group_id`),
  KEY `location_id` (`location_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rot_wunsch`
--

DROP TABLE IF EXISTS `rot_wunsch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rot_wunsch` (
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `deleted` int(11) DEFAULT '0',
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) DEFAULT NULL,
  `janein` int(11) DEFAULT NULL,
  `rot_id` int(11) DEFAULT NULL,
  `prio` int(11) DEFAULT NULL,
  `latest` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rot_id` (`rot_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rotation`
--

DROP TABLE IF EXISTS `rotation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rotation` (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `rbid` int(10) unsigned NOT NULL DEFAULT '0',
  `pid` int(11) NOT NULL,
  `jm` int(11) DEFAULT NULL,
  `rtyp` varchar(10) DEFAULT NULL,
  `bgrad` float DEFAULT NULL COMMENT 'Beschäftigungsgrad 0-1',
  `bgradj` tinyint(1) NOT NULL DEFAULT '1',
  `kuerzel` varchar(10) DEFAULT NULL,
  `bemerkung1` text,
  `bemerkung2` text,
  `rort` int(11) DEFAULT NULL,
  `rpos` int(11) NOT NULL DEFAULT '0',
  `show` varchar(1) DEFAULT NULL,
  `meldung` int(1) DEFAULT NULL COMMENT 'meldung, anz. monate vor/nach start',
  `meldetyp` int(10) DEFAULT '0',
  `f1` varchar(10) DEFAULT NULL,
  `f2` varchar(10) DEFAULT NULL,
  `cid` int(11) DEFAULT '1',
  `ukbb` tinyint(1) unsigned DEFAULT '0',
  PRIMARY KEY (`rid`)
) ENGINE=MyISAM AUTO_INCREMENT=23395 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rotation2person`
--

DROP TABLE IF EXISTS `rotation2person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rotation2person` (
  `r2pid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) NOT NULL,
  `rtid` int(11) NOT NULL,
  `ym` char(6) NOT NULL,
  `pos` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`r2pid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rotationsort`
--

DROP TABLE IF EXISTS `rotationsort`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rotationsort` (
  `roid` int(11) NOT NULL AUTO_INCREMENT,
  `kuerzel` varchar(20) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `anzpos` int(11) DEFAULT NULL,
  `sort` int(11) DEFAULT NULL,
  PRIMARY KEY (`roid`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rotationstyp`
--

DROP TABLE IF EXISTS `rotationstyp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rotationstyp` (
  `rtid` int(11) NOT NULL AUTO_INCREMENT,
  `roid` int(11) DEFAULT NULL,
  `name` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `pos` int(11) NOT NULL DEFAULT '1',
  `sort` int(11) DEFAULT NULL,
  PRIMARY KEY (`rtid`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rotblock`
--

DROP TABLE IF EXISTS `rotblock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rotblock` (
  `rbid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(10) unsigned DEFAULT NULL,
  `rvon` char(6) DEFAULT NULL,
  `rbis` char(6) DEFAULT NULL,
  `neueintritt` tinyint(1) NOT NULL DEFAULT '0',
  `comment` text,
  PRIMARY KEY (`rbid`)
) ENGINE=MyISAM AUTO_INCREMENT=750 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `setting`
--

DROP TABLE IF EXISTS `setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `setting` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `value` text CHARACTER SET utf8,
  `uid` int(11) DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=MyISAM AUTO_INCREMENT=73 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `kuerzel` varchar(10) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `vorname` varchar(50) DEFAULT NULL,
  `login` varchar(20) DEFAULT NULL,
  `pw` varchar(20) DEFAULT NULL,
  `profil` varchar(20) DEFAULT NULL,
  `aktiv` tinyint(1) NOT NULL DEFAULT '1',
  `tst` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-04-29  7:46:24
