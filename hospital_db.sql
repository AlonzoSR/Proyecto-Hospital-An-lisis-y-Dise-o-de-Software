-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         12.3.2-MariaDB - MariaDB Server
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.17.0.7270
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Volcando estructura para tabla hospital_db.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.auth_group: ~0 rows (aproximadamente)

-- Volcando estructura para tabla hospital_db.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.auth_group_permissions: ~0 rows (aproximadamente)

-- Volcando estructura para tabla hospital_db.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.auth_permission: ~52 rows (aproximadamente)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 3, 'add_permission'),
	(6, 'Can change permission', 3, 'change_permission'),
	(7, 'Can delete permission', 3, 'delete_permission'),
	(8, 'Can view permission', 3, 'view_permission'),
	(9, 'Can add group', 2, 'add_group'),
	(10, 'Can change group', 2, 'change_group'),
	(11, 'Can delete group', 2, 'delete_group'),
	(12, 'Can view group', 2, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session'),
	(25, 'Can add medico', 7, 'add_medico'),
	(26, 'Can change medico', 7, 'change_medico'),
	(27, 'Can delete medico', 7, 'delete_medico'),
	(28, 'Can view medico', 7, 'view_medico'),
	(29, 'Can add paciente', 8, 'add_paciente'),
	(30, 'Can change paciente', 8, 'change_paciente'),
	(31, 'Can delete paciente', 8, 'delete_paciente'),
	(32, 'Can view paciente', 8, 'view_paciente'),
	(33, 'Can add personal', 9, 'add_personal'),
	(34, 'Can change personal', 9, 'change_personal'),
	(35, 'Can delete personal', 9, 'delete_personal'),
	(36, 'Can view personal', 9, 'view_personal'),
	(37, 'Can add signo vital', 10, 'add_signovital'),
	(38, 'Can change signo vital', 10, 'change_signovital'),
	(39, 'Can delete signo vital', 10, 'delete_signovital'),
	(40, 'Can view signo vital', 10, 'view_signovital'),
	(41, 'Can add consulta', 11, 'add_consulta'),
	(42, 'Can change consulta', 11, 'change_consulta'),
	(43, 'Can delete consulta', 11, 'delete_consulta'),
	(44, 'Can view consulta', 11, 'view_consulta'),
	(45, 'Can add ticket soporte', 12, 'add_ticketsoporte'),
	(46, 'Can change ticket soporte', 12, 'change_ticketsoporte'),
	(47, 'Can delete ticket soporte', 12, 'delete_ticketsoporte'),
	(48, 'Can view ticket soporte', 12, 'view_ticketsoporte'),
	(49, 'Can add cita', 13, 'add_cita'),
	(50, 'Can change cita', 13, 'change_cita'),
	(51, 'Can delete cita', 13, 'delete_cita'),
	(52, 'Can view cita', 13, 'view_cita');

-- Volcando estructura para tabla hospital_db.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.auth_user: ~1 rows (aproximadamente)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, 'pbkdf2_sha256$1500000$9SqOdwQry4KJWpMlwa5YWs$yJnhS+CgBzO1BdKTRpVNa0m5CxtlgI72y6xAmu+SwiA=', '2026-08-09 00:57:22.445114', 1, 'Admin', '', '', 'alonzo.mexico@gmail.com', 1, 1, '2026-08-09 00:54:26.549031');

-- Volcando estructura para tabla hospital_db.auth_user_groups
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.auth_user_groups: ~0 rows (aproximadamente)

-- Volcando estructura para tabla hospital_db.auth_user_user_permissions
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.auth_user_user_permissions: ~0 rows (aproximadamente)

-- Volcando estructura para tabla hospital_db.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.django_admin_log: ~2 rows (aproximadamente)
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
	(1, '2026-08-09 01:54:58.080695', '1', 'Dr. Gabriel Garcia Perez - Cardiologo', 1, '[{"added": {}}]', 7, 1),
	(2, '2026-08-09 01:55:13.461428', '1', 'Dr. Gabriel Garcia Perez - Cardiologo', 2, '[]', 7, 1);

-- Volcando estructura para tabla hospital_db.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.django_content_type: ~13 rows (aproximadamente)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(2, 'auth', 'group'),
	(3, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(6, 'sessions', 'session'),
	(7, 'gestion', 'medico'),
	(8, 'gestion', 'paciente'),
	(9, 'gestion', 'personal'),
	(10, 'gestion', 'signovital'),
	(11, 'gestion', 'consulta'),
	(12, 'gestion', 'ticketsoporte'),
	(13, 'gestion', 'cita');

-- Volcando estructura para tabla hospital_db.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.django_migrations: ~30 rows (aproximadamente)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2026-08-09 00:51:31.182361'),
	(2, 'auth', '0001_initial', '2026-08-09 00:51:32.596953'),
	(3, 'admin', '0001_initial', '2026-08-09 00:51:32.890615'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2026-08-09 00:51:32.905108'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-08-09 00:51:32.920934'),
	(6, 'contenttypes', '0002_remove_content_type_name', '2026-08-09 00:51:33.131774'),
	(7, 'auth', '0002_alter_permission_name_max_length', '2026-08-09 00:51:33.260297'),
	(8, 'auth', '0003_alter_user_email_max_length', '2026-08-09 00:51:33.353000'),
	(9, 'auth', '0004_alter_user_username_opts', '2026-08-09 00:51:33.375027'),
	(10, 'auth', '0005_alter_user_last_login_null', '2026-08-09 00:51:33.501722'),
	(11, 'auth', '0006_require_contenttypes_0002', '2026-08-09 00:51:33.508057'),
	(12, 'auth', '0007_alter_validators_add_error_messages', '2026-08-09 00:51:33.524315'),
	(13, 'auth', '0008_alter_user_username_max_length', '2026-08-09 00:51:33.614384'),
	(14, 'auth', '0009_alter_user_last_name_max_length', '2026-08-09 00:51:33.695245'),
	(15, 'auth', '0010_alter_group_name_max_length', '2026-08-09 00:51:33.775336'),
	(16, 'auth', '0011_update_proxy_permissions', '2026-08-09 00:51:33.788933'),
	(17, 'auth', '0012_alter_user_first_name_max_length', '2026-08-09 00:51:33.874154'),
	(18, 'sessions', '0001_initial', '2026-08-09 00:51:34.001151'),
	(19, 'gestion', '0001_initial', '2026-08-09 01:08:16.179041'),
	(20, 'gestion', '0002_personal_remove_paciente_alergias_and_more', '2026-08-09 02:49:41.540067'),
	(21, 'gestion', '0003_signovital', '2026-08-09 02:58:27.086491'),
	(22, 'gestion', '0004_consulta', '2026-08-09 03:08:22.576711'),
	(23, 'gestion', '0005_ticketsoporte', '2026-08-10 01:09:53.015225'),
	(24, 'gestion', '0006_personal_horario', '2026-08-10 01:25:20.605015'),
	(25, 'gestion', '0007_paciente_curp_paciente_fecha_registro_and_more', '2026-08-10 02:20:06.953052'),
	(26, 'gestion', '0008_remove_paciente_fecha_registro_and_more', '2026-08-10 21:31:53.011220'),
	(27, 'gestion', '0009_alter_paciente_apellido_materno', '2026-08-10 21:31:53.135683'),
	(28, 'gestion', '0010_paciente_edad_paciente_genero', '2026-08-11 13:29:29.103676'),
	(29, 'gestion', '0011_alter_cita_estado_alter_medico_cedula', '2026-08-11 19:47:56.394911'),
	(30, 'gestion', '0012_ticketsoporte_resuelto_por', '2026-08-11 19:53:03.440473');

-- Volcando estructura para tabla hospital_db.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.django_session: ~1 rows (aproximadamente)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('1678shza20ewae23x3nw2szq2am4p9vp', '.eJyrVipKTU4tSM7Mz4vPTFGyMtVRKs4vyC8qSQVzzXWUUvPSUotyU4syE8EiljpKuakpmcn5YJ5JLQDvWxZR:1wtwwB:bvQuwDXmq4xendoLYY1XhH69zi-vj016ElpVEV97oKc', '2026-08-26 00:35:19.920942');

-- Volcando estructura para tabla hospital_db.gestion_cita
CREATE TABLE IF NOT EXISTS `gestion_cita` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `hora` time(6) NOT NULL,
  `motivo` varchar(200) NOT NULL,
  `estado` varchar(40) NOT NULL,
  `medico_id` bigint(20) NOT NULL,
  `paciente_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gestion_cita_medico_id_c60ed614_fk_gestion_medico_id` (`medico_id`),
  KEY `gestion_cita_paciente_id_249893fa_fk_gestion_paciente_id` (`paciente_id`),
  CONSTRAINT `gestion_cita_medico_id_c60ed614_fk_gestion_medico_id` FOREIGN KEY (`medico_id`) REFERENCES `gestion_medico` (`id`),
  CONSTRAINT `gestion_cita_paciente_id_249893fa_fk_gestion_paciente_id` FOREIGN KEY (`paciente_id`) REFERENCES `gestion_paciente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.gestion_cita: ~2 rows (aproximadamente)
INSERT INTO `gestion_cita` (`id`, `fecha`, `hora`, `motivo`, `estado`, `medico_id`, `paciente_id`) VALUES
	(31, '2026-08-10', '08:30:00.000000', 'Dolor de cabeza', 'En Espera', 2, 28),
	(43, '2026-08-11', '23:30:00.000000', 'Dolor de espalda', 'Espera Extra (Emergencia)', 4, 28);

-- Volcando estructura para tabla hospital_db.gestion_consulta
CREATE TABLE IF NOT EXISTS `gestion_consulta` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `medico_nombre` varchar(100) NOT NULL,
  `diagnostico` longtext NOT NULL,
  `receta` longtext NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `paciente_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gestion_consulta_paciente_id_7235ff82_fk_gestion_paciente_id` (`paciente_id`),
  CONSTRAINT `gestion_consulta_paciente_id_7235ff82_fk_gestion_paciente_id` FOREIGN KEY (`paciente_id`) REFERENCES `gestion_paciente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.gestion_consulta: ~4 rows (aproximadamente)
INSERT INTO `gestion_consulta` (`id`, `medico_nombre`, `diagnostico`, `receta`, `fecha`, `paciente_id`) VALUES
	(4, 'Dr(a). Drew Martinez Castro', 'Malestar de esaplda', 'Masajes y pastillas de diclofenaco ', '2026-08-11 15:19:13.231071', 28),
	(5, 'Dr(a). Gabriel Garcia Perez', 'Dolor de cabeza\r\n', 'Paracetamol', '2026-08-11 16:52:27.447581', 28),
	(6, 'Dr(a). Oscar Marin Rodriguez ', 'Fractura de pie', 'Yeso 6 meses', '2026-08-11 22:55:34.240270', 42),
	(7, 'Dr(a). Oscar Marin Rodriguez ', 'Fractura de craneo', 'Descanso abosoluto y operaicon', '2026-08-12 00:17:09.501836', 45);

-- Volcando estructura para tabla hospital_db.gestion_medico
CREATE TABLE IF NOT EXISTS `gestion_medico` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `especialidad` varchar(100) NOT NULL,
  `cedula` varchar(50) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `horario` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gestion_medico_cedula_75834eba_uniq` (`cedula`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.gestion_medico: ~4 rows (aproximadamente)
INSERT INTO `gestion_medico` (`id`, `nombre`, `especialidad`, `cedula`, `telefono`, `horario`, `password`, `usuario`) VALUES
	(1, 'Gabriel Garcia Perez', 'Cardiologo', '11112', '1111111112', '00:00 - 08:00', 'gabo', 'gabo'),
	(2, 'Carlos Alberto Sanchez Alejo', 'Pediatra', '11111', '1111111111', '08:00 - 16:00', 'carlos', 'carlos'),
	(4, 'Oscar Marin Rodriguez ', 'Cirujano', '56789', '4567890764', '16:00 - 00:00', 'oscar', 'oscar'),
	(5, 'Drew Martinez Castro', 'Neurologo ', '24387', '5678908765', '08:00 - 16:00', 'dre', 'Dre');

-- Volcando estructura para tabla hospital_db.gestion_paciente
CREATE TABLE IF NOT EXISTS `gestion_paciente` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `tipo_sangre` varchar(5) NOT NULL,
  `curp` varchar(18) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `apellido_materno` varchar(100) DEFAULT NULL,
  `apellido_paterno` varchar(100) NOT NULL,
  `edad` int(10) unsigned DEFAULT NULL CHECK (`edad` >= 0),
  `genero` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `curp` (`curp`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.gestion_paciente: ~4 rows (aproximadamente)
INSERT INTO `gestion_paciente` (`id`, `nombre`, `tipo_sangre`, `curp`, `telefono`, `apellido_materno`, `apellido_paterno`, `edad`, `genero`) VALUES
	(28, 'Sebastián ', 'B-', '621DF56W81F62F5862', '2131231241', 'Romero', 'Ramirez', 20, 'Masculino'),
	(42, 'Alex', 'O+', '3463463463HTRHDEEF', '7645974696', 'Cruz', 'Salazar', 56, 'Masculino'),
	(45, 'Alex', 'B-', 'VCDT7S7VCTSFCGC78F', '7832832762', 'Cruz', 'Castro', 34, 'Masculino'),
	(46, 'Mario', 'A+', 'FGTHYUJIKJUHYGTFRD', '7878787878', 'L', 'Bross', 34, 'Masculino');

-- Volcando estructura para tabla hospital_db.gestion_personal
CREATE TABLE IF NOT EXISTS `gestion_personal` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `rol` varchar(20) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `horario` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario` (`usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.gestion_personal: ~9 rows (aproximadamente)
INSERT INTO `gestion_personal` (`id`, `nombre`, `rol`, `usuario`, `password`, `telefono`, `horario`) VALUES
	(1, 'Claudia Valeria Marin Liceaga ', 'recepcion', 'Clau', 'clau', '2987982739', '08:00 - 16:00'),
	(2, 'Alejandro Castillo Salcido ', 'enfermeria', 'Ale', 'ale', '8738762386', '08:00 - 16:00'),
	(3, 'Emiliano Paulin Cruz', 'soporte', 'Pau', 'pau', '8973948789', '08:00 - 16:00'),
	(4, 'Carolina Marisol Frías Díaz ', 'recepcion', 'caro', 'caro', '6786567784', '00:00 - 08:00'),
	(5, 'Yael Yoel Lopez Caseres ', 'recepcion', 'yayo', 'yayo', '9438759230', '16:00 - 00:00'),
	(6, 'Jose Jose ', 'soporte', 'Jose', 'Jose', '2389457902', '00:00 - 08:00'),
	(7, 'Luis Miguel', 'soporte', 'Luis', 'Luis', '3289479023', '16:00 - 00:00'),
	(8, 'David Gorgonio', 'enfermeria', 'David', 'David', '0912873092', '00:00 - 08:00'),
	(9, 'Joaquin Alejandro', 'enfermeria', 'Joa', 'Joa', '9837490872', '16:00 - 00:00');

-- Volcando estructura para tabla hospital_db.gestion_signovital
CREATE TABLE IF NOT EXISTS `gestion_signovital` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `presion` varchar(20) NOT NULL,
  `temperatura` varchar(10) NOT NULL,
  `peso` varchar(10) NOT NULL,
  `estatura` varchar(10) NOT NULL,
  `oxigenacion` varchar(10) DEFAULT NULL,
  `fecha` datetime(6) NOT NULL,
  `paciente_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gestion_signovital_paciente_id_73e6eb4a_fk_gestion_paciente_id` (`paciente_id`),
  CONSTRAINT `gestion_signovital_paciente_id_73e6eb4a_fk_gestion_paciente_id` FOREIGN KEY (`paciente_id`) REFERENCES `gestion_paciente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.gestion_signovital: ~4 rows (aproximadamente)
INSERT INTO `gestion_signovital` (`id`, `presion`, `temperatura`, `peso`, `estatura`, `oxigenacion`, `fecha`, `paciente_id`) VALUES
	(10, '120/80', '36.0', '63.0', '1.83', '100', '2026-08-12 00:14:09.377742', 28),
	(14, '120/80', '36.0', '80.0', '1.9', '98', '2026-08-11 22:46:20.085011', 42),
	(15, '120/80', '36.0', '78.0', '1.9', '80', '2026-08-12 00:15:44.972534', 45),
	(16, '120/80', '45.0', '67.0', '1.2', '98', '2026-08-12 00:26:16.779367', 46);

-- Volcando estructura para tabla hospital_db.gestion_ticketsoporte
CREATE TABLE IF NOT EXISTS `gestion_ticketsoporte` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `empleado` varchar(100) NOT NULL,
  `area` varchar(50) NOT NULL,
  `falla` longtext NOT NULL,
  `estado` varchar(20) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `resuelto_por` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla hospital_db.gestion_ticketsoporte: ~4 rows (aproximadamente)
INSERT INTO `gestion_ticketsoporte` (`id`, `empleado`, `area`, `falla`, `estado`, `fecha`, `resuelto_por`) VALUES
	(6, 'Dr(a). Gabriel Garcia Perez', 'Consultorio Médico', 'no sirve nada', 'Resuelto', '2026-08-11 19:54:59.456584', 'Emiliano Paulin Cruz'),
	(7, 'Dr(a). Gabriel Garcia Perez', 'Consultorio Médico', 'no sirve nada\r\n', 'Resuelto', '2026-08-11 19:56:31.674815', 'Jose Jose '),
	(8, 'Dr(a). Oscar Marin Rodriguez ', 'Consultorio Médico', 'Fallo la impresiora ', 'Resuelto', '2026-08-12 00:19:10.480161', 'Luis Miguel'),
	(9, 'Yael Yoel Lopez Caseres ', 'Recepción', 'no sirve nada\r\n', 'Resuelto', '2026-08-12 00:35:37.382672', 'Luis Miguel');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
