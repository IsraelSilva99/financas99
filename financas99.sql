-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: financas99
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `badge`
--

DROP TABLE IF EXISTS `badge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `badge` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `descricao` text NOT NULL,
  `data_conquista` date NOT NULL DEFAULT '2024-01-01',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `badge_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `badge`
--

LOCK TABLES `badge` WRITE;
/*!40000 ALTER TABLE `badge` DISABLE KEYS */;
INSERT INTO `badge` VALUES (3,4,'Economizador do M├¬s','Voc├¬ terminou o m├¬s com saldo positivo!','2024-01-31'),(4,4,'Mestre das Categorias','Voc├¬ criou 5 ou mais categorias!','2024-02-15'),(5,4,'Planejador Nato','Voc├¬ configurou 3 ou mais lembretes!','2024-02-28'),(6,4,'Investidor Iniciante','Primeira receita de investimento!','2024-03-10'),(7,4,'Guru Financeiro','Saldo positivo por 3 meses consecutivos!','2024-03-31'),(8,4,'Organizador de Elite','Criou 10 ou mais categorias!','2024-04-15'),(9,4,'Vision├írio','Configurou 10 ou mais lembretes!','2024-04-30'),(10,4,'Economista','Economizou 20% do sal├írio!','2024-05-15'),(11,4,'Explorador Financeiro','Adicionou 50 transa├º├Áes!','2024-05-31'),(12,4,'Magnata','Recebeu mais de R$5000 em um m├¬s!','2024-06-15'),(13,4,'Controlador de Gastos','Gastou menos de R$1000 em um m├¬s!','2024-06-30'),(14,4,'Planejador de Longo Prazo','Configurou lembretes para 6 meses!','2024-07-15'),(15,4,'Investidor Experiente','Recebeu mais de R$2000 em investimentos!','2024-07-31'),(16,4,'Mestre do Or├ºamento','Saldo positivo por 6 meses!','2024-08-15'),(17,4,'Lenda Financeira','Adicionou 100 transa├º├Áes!','2024-08-31'),(18,5,'Economizador do M├¬s','Voc├¬ terminou o m├¬s com saldo positivo!','2025-04-17');
/*!40000 ALTER TABLE `badge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lembrete`
--

DROP TABLE IF EXISTS `lembrete`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lembrete` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `categoria` varchar(50) NOT NULL,
  `valor` decimal(10,2) NOT NULL,
  `dia` int(11) NOT NULL,
  `mes` varchar(20) NOT NULL,
  `mensagem` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `lembrete_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lembrete`
--

LOCK TABLES `lembrete` WRITE;
/*!40000 ALTER TABLE `lembrete` DISABLE KEYS */;
/*!40000 ALTER TABLE `lembrete` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `meta`
--

DROP TABLE IF EXISTS `meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `valor` float NOT NULL,
  `mes` varchar(20) NOT NULL,
  `ano` int(11) NOT NULL,
  `descricao` varchar(200) NOT NULL,
  `data_criacao` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `meta_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meta`
--

LOCK TABLES `meta` WRITE;
/*!40000 ALTER TABLE `meta` DISABLE KEYS */;
/*!40000 ALTER TABLE `meta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transacao`
--

DROP TABLE IF EXISTS `transacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transacao` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `categoria` varchar(50) NOT NULL,
  `valor` decimal(10,2) NOT NULL,
  `mes` varchar(20) NOT NULL,
  `ano` int(11) NOT NULL,
  `tipo` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `transacao_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transacao`
--

LOCK TABLES `transacao` WRITE;
/*!40000 ALTER TABLE `transacao` DISABLE KEYS */;
/*!40000 ALTER TABLE `transacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `senha` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (4,'Ana Silva','ana.silva@email.com','pbkdf2:sha256:1000000$2GKFgxtRbCtYYz0d$af06a0f739659819305f0ea2cd4a642ac7740556cd8a8be01bc179cfcea7002d'),(5,'Israel Pereira Silva','israelsilvacontato@gmail.com','pbkdf2:sha256:1000000$7QbfG0ADsulbGfhb$10fe332d791ed1e78633ab11bb0177b8b8ba23a71306a54360d59804b5973e26'),(6,'igor Felipe','klebinhabiska@gmail.com','scrypt:32768:8:1$81VEQLyFQsc2UIcD$287670048de8cf2e033f00ac66b1e941ce7267bc1155555c41d16a3e180e9a0732193af743e57321789e1fc24c3ce9023bcdb1561f836ab18b5157df3c7e47ce');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-19 14:46:37
