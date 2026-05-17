-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.8.2-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.13.0.7147
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for resta_
CREATE DATABASE IF NOT EXISTS `resta_` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `resta_`;

-- Dumping structure for table resta_.account_emailaddress
CREATE TABLE IF NOT EXISTS `account_emailaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_emailaddress_user_id_email_987c8728_uniq` (`user_id`,`email`),
  KEY `account_emailaddress_email_03be32b2` (`email`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.account_emailaddress: ~0 rows (approximately)

-- Dumping structure for table resta_.account_emailconfirmation
CREATE TABLE IF NOT EXISTS `account_emailconfirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.account_emailconfirmation: ~0 rows (approximately)

-- Dumping structure for table resta_.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.auth_group: ~0 rows (approximately)

-- Dumping structure for table resta_.auth_group_permissions
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

-- Dumping data for table resta_.auth_group_permissions: ~0 rows (approximately)

-- Dumping structure for table resta_.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.auth_permission: ~100 rows (approximately)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 2, 'add_permission'),
	(6, 'Can change permission', 2, 'change_permission'),
	(7, 'Can delete permission', 2, 'delete_permission'),
	(8, 'Can view permission', 2, 'view_permission'),
	(9, 'Can add group', 3, 'add_group'),
	(10, 'Can change group', 3, 'change_group'),
	(11, 'Can delete group', 3, 'delete_group'),
	(12, 'Can view group', 3, 'view_group'),
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
	(25, 'Can add customer', 7, 'add_customer'),
	(26, 'Can change customer', 7, 'change_customer'),
	(27, 'Can delete customer', 7, 'delete_customer'),
	(28, 'Can view customer', 7, 'view_customer'),
	(29, 'Can add item', 8, 'add_item'),
	(30, 'Can change item', 8, 'change_item'),
	(31, 'Can delete item', 8, 'delete_item'),
	(32, 'Can view item', 8, 'view_item'),
	(33, 'Can add menu', 9, 'add_menu'),
	(34, 'Can change menu', 9, 'change_menu'),
	(35, 'Can delete menu', 9, 'delete_menu'),
	(36, 'Can view menu', 9, 'view_menu'),
	(37, 'Can add order item', 10, 'add_orderitem'),
	(38, 'Can change order item', 10, 'change_orderitem'),
	(39, 'Can delete order item', 10, 'delete_orderitem'),
	(40, 'Can view order item', 10, 'view_orderitem'),
	(41, 'Can add staff', 11, 'add_staff'),
	(42, 'Can change staff', 11, 'change_staff'),
	(43, 'Can delete staff', 11, 'delete_staff'),
	(44, 'Can view staff', 11, 'view_staff'),
	(45, 'Can add order', 12, 'add_order'),
	(46, 'Can change order', 12, 'change_order'),
	(47, 'Can delete order', 12, 'delete_order'),
	(48, 'Can view order', 12, 'view_order'),
	(49, 'Can add Token', 13, 'add_token'),
	(50, 'Can change Token', 13, 'change_token'),
	(51, 'Can delete Token', 13, 'delete_token'),
	(52, 'Can view Token', 13, 'view_token'),
	(53, 'Can add Token', 14, 'add_tokenproxy'),
	(54, 'Can change Token', 14, 'change_tokenproxy'),
	(55, 'Can delete Token', 14, 'delete_tokenproxy'),
	(56, 'Can view Token', 14, 'view_tokenproxy'),
	(57, 'Can add site', 15, 'add_site'),
	(58, 'Can change site', 15, 'change_site'),
	(59, 'Can delete site', 15, 'delete_site'),
	(60, 'Can view site', 15, 'view_site'),
	(61, 'Can add email address', 16, 'add_emailaddress'),
	(62, 'Can change email address', 16, 'change_emailaddress'),
	(63, 'Can delete email address', 16, 'delete_emailaddress'),
	(64, 'Can view email address', 16, 'view_emailaddress'),
	(65, 'Can add email confirmation', 17, 'add_emailconfirmation'),
	(66, 'Can change email confirmation', 17, 'change_emailconfirmation'),
	(67, 'Can delete email confirmation', 17, 'delete_emailconfirmation'),
	(68, 'Can view email confirmation', 17, 'view_emailconfirmation'),
	(69, 'Can add social account', 18, 'add_socialaccount'),
	(70, 'Can change social account', 18, 'change_socialaccount'),
	(71, 'Can delete social account', 18, 'delete_socialaccount'),
	(72, 'Can view social account', 18, 'view_socialaccount'),
	(73, 'Can add social application', 19, 'add_socialapp'),
	(74, 'Can change social application', 19, 'change_socialapp'),
	(75, 'Can delete social application', 19, 'delete_socialapp'),
	(76, 'Can view social application', 19, 'view_socialapp'),
	(77, 'Can add social application token', 20, 'add_socialtoken'),
	(78, 'Can change social application token', 20, 'change_socialtoken'),
	(79, 'Can delete social application token', 20, 'delete_socialtoken'),
	(80, 'Can view social application token', 20, 'view_socialtoken'),
	(81, 'Can add SMS Message', 21, 'add_smsmessage'),
	(82, 'Can change SMS Message', 21, 'change_smsmessage'),
	(83, 'Can delete SMS Message', 21, 'delete_smsmessage'),
	(84, 'Can view SMS Message', 21, 'view_smsmessage'),
	(85, 'Can add chat room', 22, 'add_chatroom'),
	(86, 'Can change chat room', 22, 'change_chatroom'),
	(87, 'Can delete chat room', 22, 'delete_chatroom'),
	(88, 'Can view chat room', 22, 'view_chatroom'),
	(89, 'Can add message', 23, 'add_message'),
	(90, 'Can change message', 23, 'change_message'),
	(91, 'Can delete message', 23, 'delete_message'),
	(92, 'Can view message', 23, 'view_message'),
	(93, 'Can add payment', 24, 'add_payment'),
	(94, 'Can change payment', 24, 'change_payment'),
	(95, 'Can delete payment', 24, 'delete_payment'),
	(96, 'Can view payment', 24, 'view_payment'),
	(97, 'Can add inventory items', 25, 'add_inventoryitems'),
	(98, 'Can change inventory items', 25, 'change_inventoryitems'),
	(99, 'Can delete inventory items', 25, 'delete_inventoryitems'),
	(100, 'Can view inventory items', 25, 'view_inventoryitems');

-- Dumping structure for table resta_.auth_user
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.auth_user: ~2 rows (approximately)
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
	(1, 'pbkdf2_sha256$1000000$BOucuGdMrrcXShfsjH9GI8$UFGVGW+cjc/8r+xpaQoGb8s0o0/WJ07pYlH/cZgalwY=', '2025-11-04 09:02:31.364874', 0, 'demo', 'Omari ', 'Jumapilli', 'demo@gmail.com', 0, 1, '2025-11-04 09:02:12.471545'),
	(2, '!RudMwGjnbGgiBBhihl0K70aPBsZneXi70pkaj2nx', NULL, 0, 'infonet20th', 'omari', 'jumapili', 'infonet20th@gmail.com', 0, 1, '2026-05-17 06:56:04.377436');

-- Dumping structure for table resta_.auth_user_groups
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

-- Dumping data for table resta_.auth_user_groups: ~0 rows (approximately)

-- Dumping structure for table resta_.auth_user_user_permissions
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

-- Dumping data for table resta_.auth_user_user_permissions: ~0 rows (approximately)

-- Dumping structure for table resta_.authtoken_token
CREATE TABLE IF NOT EXISTS `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.authtoken_token: ~0 rows (approximately)

-- Dumping structure for table resta_.chatbot_chatroom
CREATE TABLE IF NOT EXISTS `chatbot_chatroom` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.chatbot_chatroom: ~0 rows (approximately)

-- Dumping structure for table resta_.chatbot_message
CREATE TABLE IF NOT EXISTS `chatbot_message` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `is_bot` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `room_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chatbot_message_room_id_a1055f49_fk_chatbot_chatroom_id` (`room_id`),
  CONSTRAINT `chatbot_message_room_id_a1055f49_fk_chatbot_chatroom_id` FOREIGN KEY (`room_id`) REFERENCES `chatbot_chatroom` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.chatbot_message: ~0 rows (approximately)

-- Dumping structure for table resta_.customer
CREATE TABLE IF NOT EXISTS `customer` (
  `customerID` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(100) NOT NULL,
  `phoneNumber` varchar(10) NOT NULL,
  `physicalAddress` varchar(255) NOT NULL,
  `region` varchar(255) NOT NULL,
  PRIMARY KEY (`customerID`),
  UNIQUE KEY `Customer_phoneNumber_85ba9903_uniq` (`phoneNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.customer: ~0 rows (approximately)

-- Dumping structure for table resta_.django_admin_log
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.django_admin_log: ~0 rows (approximately)

-- Dumping structure for table resta_.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.django_content_type: ~25 rows (approximately)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(2, 'auth', 'permission'),
	(3, 'auth', 'group'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(6, 'sessions', 'session'),
	(7, 'Customer', 'customer'),
	(8, 'Items', 'item'),
	(9, 'Menus', 'menu'),
	(10, 'OrderItem', 'orderitem'),
	(11, 'Staff', 'staff'),
	(12, 'Order', 'order'),
	(13, 'authtoken', 'token'),
	(14, 'authtoken', 'tokenproxy'),
	(15, 'sites', 'site'),
	(16, 'account', 'emailaddress'),
	(17, 'account', 'emailconfirmation'),
	(18, 'socialaccount', 'socialaccount'),
	(19, 'socialaccount', 'socialapp'),
	(20, 'socialaccount', 'socialtoken'),
	(21, 'sms', 'smsmessage'),
	(22, 'chatbot', 'chatroom'),
	(23, 'chatbot', 'message'),
	(24, 'Payment', 'payment'),
	(25, 'InventoryItems', 'inventoryitems');

-- Dumping structure for table resta_.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.django_migrations: ~68 rows (approximately)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'Staff', '0001_initial', '2025-11-04 09:00:33.731158'),
	(2, 'Customer', '0001_initial', '2025-11-04 09:00:33.789377'),
	(3, 'Customer', '0002_alter_customer_table', '2025-11-04 09:00:33.805339'),
	(4, 'Customer', '0003_auto_20250908_0953', '2025-11-04 09:00:33.853158'),
	(5, 'Customer', '0004_remove_customer_employee_customer_region', '2025-11-04 09:00:34.472559'),
	(6, 'Customer', '0005_rename_firstname_customer_fullname_and_more', '2025-11-04 09:00:34.508289'),
	(7, 'Customer', '0006_alter_customer_table', '2025-11-04 09:00:34.521499'),
	(8, 'Customer', '0007_alter_customer_phonenumber_alter_customer_table', '2025-11-04 09:00:34.561181'),
	(9, 'Customer', '0008_alter_customer_phonenumber', '2025-11-04 09:00:34.582240'),
	(10, 'Items', '0001_initial', '2025-11-04 09:00:34.598278'),
	(11, 'Items', '0002_item_dateadded', '2025-11-04 09:00:34.643632'),
	(12, 'Items', '0003_item_unitofmeasure', '2025-11-04 09:00:34.679483'),
	(13, 'InventoryItems', '0001_initial', '2025-11-04 09:00:34.693296'),
	(14, 'InventoryItems', '0002_inventoryitems_itemid', '2025-11-04 09:00:34.723113'),
	(15, 'Menus', '0001_initial', '2025-11-04 09:00:34.736704'),
	(16, 'Menus', '0002_alter_menu_table', '2025-11-04 09:00:34.749442'),
	(17, 'Menus', '0003_menu_itemid_menu_price_alter_menu_table', '2025-11-04 09:00:34.825649'),
	(18, 'Menus', '0004_remove_menu_is_active', '2025-11-04 09:00:34.850876'),
	(19, 'Menus', '0005_menu_category', '2025-11-04 09:00:34.882207'),
	(20, 'Staff', '0002_rename_employeeid_staff_mobile_and_more', '2025-11-04 09:00:35.098438'),
	(21, 'Staff', '0003_alter_staff_address_alter_staff_email_and_more', '2025-11-04 09:00:35.208665'),
	(22, 'Staff', '0004_remove_staff_mobile_alter_staff_phone', '2025-11-04 09:00:35.538170'),
	(23, 'Order', '0001_initial', '2025-11-04 09:00:35.630958'),
	(24, 'OrderItem', '0001_initial', '2025-11-04 09:00:35.698251'),
	(25, 'Payment', '0001_initial', '2025-11-04 09:00:35.768382'),
	(26, 'contenttypes', '0001_initial', '2025-11-04 09:00:35.801687'),
	(27, 'auth', '0001_initial', '2025-11-04 09:00:36.110508'),
	(28, 'account', '0001_initial', '2025-11-04 09:00:36.193516'),
	(29, 'account', '0002_email_max_length', '2025-11-04 09:00:36.224158'),
	(30, 'account', '0003_alter_emailaddress_create_unique_verified_email', '2025-11-04 09:00:36.258623'),
	(31, 'account', '0004_alter_emailaddress_drop_unique_email', '2025-11-04 09:00:36.549540'),
	(32, 'account', '0005_emailaddress_idx_upper_email', '2025-11-04 09:00:36.557535'),
	(33, 'account', '0006_emailaddress_lower', '2025-11-04 09:00:36.578395'),
	(34, 'account', '0007_emailaddress_idx_email', '2025-11-04 09:00:36.610573'),
	(35, 'account', '0008_emailaddress_unique_primary_email_fixup', '2025-11-04 09:00:36.630114'),
	(36, 'account', '0009_emailaddress_unique_primary_email', '2025-11-04 09:00:36.638201'),
	(37, 'admin', '0001_initial', '2025-11-04 09:00:36.714661'),
	(38, 'admin', '0002_logentry_remove_auto_add', '2025-11-04 09:00:36.724023'),
	(39, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-04 09:00:36.732713'),
	(40, 'contenttypes', '0002_remove_content_type_name', '2025-11-04 09:00:36.798908'),
	(41, 'auth', '0002_alter_permission_name_max_length', '2025-11-04 09:00:36.835470'),
	(42, 'auth', '0003_alter_user_email_max_length', '2025-11-04 09:00:36.860812'),
	(43, 'auth', '0004_alter_user_username_opts', '2025-11-04 09:00:36.872394'),
	(44, 'auth', '0005_alter_user_last_login_null', '2025-11-04 09:00:36.905372'),
	(45, 'auth', '0006_require_contenttypes_0002', '2025-11-04 09:00:36.909587'),
	(46, 'auth', '0007_alter_validators_add_error_messages', '2025-11-04 09:00:36.921160'),
	(47, 'auth', '0008_alter_user_username_max_length', '2025-11-04 09:00:36.948512'),
	(48, 'auth', '0009_alter_user_last_name_max_length', '2025-11-04 09:00:36.971608'),
	(49, 'auth', '0010_alter_group_name_max_length', '2025-11-04 09:00:37.000731'),
	(50, 'auth', '0011_update_proxy_permissions', '2025-11-04 09:00:37.014704'),
	(51, 'auth', '0012_alter_user_first_name_max_length', '2025-11-04 09:00:37.043325'),
	(52, 'authtoken', '0001_initial', '2025-11-04 09:00:37.086874'),
	(53, 'authtoken', '0002_auto_20160226_1747', '2025-11-04 09:00:37.118463'),
	(54, 'authtoken', '0003_tokenproxy', '2025-11-04 09:00:37.123456'),
	(55, 'authtoken', '0004_alter_tokenproxy_options', '2025-11-04 09:00:37.128723'),
	(56, 'chatbot', '0001_initial', '2025-11-04 09:00:37.180127'),
	(57, 'mambosmsbulk', '0001_initial', '2025-11-04 09:00:37.238328'),
	(58, 'mambosmsbulk', '0002_remove_smscampaign_created_by_delete_smslog_and_more', '2025-11-04 09:00:37.550637'),
	(59, 'sessions', '0001_initial', '2025-11-04 09:00:37.584396'),
	(60, 'sites', '0001_initial', '2025-11-04 09:00:37.596089'),
	(61, 'sites', '0002_alter_domain_unique', '2025-11-04 09:00:37.616698'),
	(62, 'sms', '0001_initial', '2025-11-04 09:00:37.669912'),
	(63, 'socialaccount', '0001_initial', '2025-11-04 09:00:37.938899'),
	(64, 'socialaccount', '0002_token_max_lengths', '2025-11-04 09:00:38.008313'),
	(65, 'socialaccount', '0003_extra_data_default_dict', '2025-11-04 09:00:38.025636'),
	(66, 'socialaccount', '0004_app_provider_id_settings', '2025-11-04 09:00:38.119269'),
	(67, 'socialaccount', '0005_socialtoken_nullable_app', '2025-11-04 09:00:38.478371'),
	(68, 'socialaccount', '0006_alter_socialaccount_extra_data', '2025-11-04 09:00:38.520952');

-- Dumping structure for table resta_.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.django_session: ~0 rows (approximately)

-- Dumping structure for table resta_.django_site
CREATE TABLE IF NOT EXISTS `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.django_site: ~1 rows (approximately)
INSERT INTO `django_site` (`id`, `domain`, `name`) VALUES
	(1, 'example.com', 'example.com');

-- Dumping structure for table resta_.inventoryitems
CREATE TABLE IF NOT EXISTS `inventoryitems` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `item_name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `quantity` int(10) unsigned NOT NULL CHECK (`quantity` >= 0),
  `itemID` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `InventoryItems_itemID_498a3e97_fk_items_itemID` (`itemID`),
  CONSTRAINT `InventoryItems_itemID_498a3e97_fk_items_itemID` FOREIGN KEY (`itemID`) REFERENCES `items` (`itemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.inventoryitems: ~0 rows (approximately)

-- Dumping structure for table resta_.items
CREATE TABLE IF NOT EXISTS `items` (
  `itemID` int(11) NOT NULL AUTO_INCREMENT,
  `itemName` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `category` varchar(50) NOT NULL,
  `dateAdded` date NOT NULL,
  `unitOfMeasure` varchar(50) NOT NULL,
  PRIMARY KEY (`itemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.items: ~0 rows (approximately)

-- Dumping structure for table resta_.menuitem
CREATE TABLE IF NOT EXISTS `menuitem` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `itemid` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `category` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `menu_itemid_cb154cd9_fk_items_itemID` (`itemid`),
  CONSTRAINT `menu_itemid_cb154cd9_fk_items_itemID` FOREIGN KEY (`itemid`) REFERENCES `items` (`itemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.menuitem: ~0 rows (approximately)

-- Dumping structure for table resta_.order_
CREATE TABLE IF NOT EXISTS `order_` (
  `orderNumber` int(11) NOT NULL AUTO_INCREMENT,
  `orderDate` datetime(6) NOT NULL,
  `customerID` int(11) NOT NULL,
  `employee_id` varchar(20) DEFAULT NULL,
  `itemID` int(11) NOT NULL,
  PRIMARY KEY (`orderNumber`),
  KEY `order__customerID_80ede0c5_fk_Customer_customerID` (`customerID`),
  KEY `order__employee_id_199e8337_fk_Staff_phone` (`employee_id`),
  KEY `order__itemID_0d8d3b93_fk_items_itemID` (`itemID`),
  CONSTRAINT `order__customerID_80ede0c5_fk_Customer_customerID` FOREIGN KEY (`customerID`) REFERENCES `customer` (`customerID`),
  CONSTRAINT `order__employee_id_199e8337_fk_Staff_phone` FOREIGN KEY (`employee_id`) REFERENCES `staff` (`phone`),
  CONSTRAINT `order__itemID_0d8d3b93_fk_items_itemID` FOREIGN KEY (`itemID`) REFERENCES `items` (`itemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.order_: ~0 rows (approximately)

-- Dumping structure for table resta_.orderitem
CREATE TABLE IF NOT EXISTS `orderitem` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `quantity` int(10) unsigned NOT NULL CHECK (`quantity` >= 0),
  `item_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orderitem_item_id_cd3c0387_fk_items_itemID` (`item_id`),
  KEY `orderitem_order_id_e716e9f7_fk_order__orderNumber` (`order_id`),
  CONSTRAINT `orderitem_item_id_cd3c0387_fk_items_itemID` FOREIGN KEY (`item_id`) REFERENCES `items` (`itemID`),
  CONSTRAINT `orderitem_order_id_e716e9f7_fk_order__orderNumber` FOREIGN KEY (`order_id`) REFERENCES `order_` (`orderNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.orderitem: ~0 rows (approximately)

-- Dumping structure for table resta_.payment
CREATE TABLE IF NOT EXISTS `payment` (
  `paymentID` int(11) NOT NULL AUTO_INCREMENT,
  `paymentName` varchar(100) NOT NULL,
  `paymentDate` datetime(6) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`paymentID`),
  KEY `Payment_customer_id_d552952f_fk_Customer_customerID` (`customer_id`),
  KEY `Payment_order_id_03532fe1_fk_order__orderNumber` (`order_id`),
  CONSTRAINT `Payment_customer_id_d552952f_fk_Customer_customerID` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customerID`),
  CONSTRAINT `Payment_order_id_03532fe1_fk_order__orderNumber` FOREIGN KEY (`order_id`) REFERENCES `order_` (`orderNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.payment: ~0 rows (approximately)

-- Dumping structure for table resta_.sms_smsmessage
CREATE TABLE IF NOT EXISTS `sms_smsmessage` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `from_phone` varchar(20) NOT NULL,
  `to_phone` varchar(20) NOT NULL,
  `message_body` longtext NOT NULL,
  `message_sid` varchar(50) NOT NULL,
  `received_at` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `message_sid` (`message_sid`),
  KEY `sms_smsmessage_user_id_0436e25a_fk_auth_user_id` (`user_id`),
  CONSTRAINT `sms_smsmessage_user_id_0436e25a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.sms_smsmessage: ~0 rows (approximately)

-- Dumping structure for table resta_.socialaccount_socialaccount
CREATE TABLE IF NOT EXISTS `socialaccount_socialaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(200) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`extra_data`)),
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.socialaccount_socialaccount: ~1 rows (approximately)
INSERT INTO `socialaccount_socialaccount` (`id`, `provider`, `uid`, `last_login`, `date_joined`, `extra_data`, `user_id`) VALUES
	(1, 'google', '111276668317878029805', '2026-05-17 06:56:04.415880', '2026-05-17 06:56:04.415880', '{"id": "111276668317878029805", "email": "infonet20th@gmail.com", "verified_email": true, "name": "omari jumapili", "given_name": "omari", "family_name": "jumapili", "picture": "https://lh3.googleusercontent.com/a/ACg8ocJSHXqFJvV9DHROt__iMeIGcRgPHUnw_30CIKZybB6ZJht3UAE=s96-c"}', 2);

-- Dumping structure for table resta_.socialaccount_socialapp
CREATE TABLE IF NOT EXISTS `socialaccount_socialapp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  `provider_id` varchar(200) NOT NULL,
  `settings` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`settings`)),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.socialaccount_socialapp: ~0 rows (approximately)

-- Dumping structure for table resta_.socialaccount_socialapp_sites
CREATE TABLE IF NOT EXISTS `socialaccount_socialapp_sites` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `socialapp_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.socialaccount_socialapp_sites: ~0 rows (approximately)

-- Dumping structure for table resta_.socialaccount_socialtoken
CREATE TABLE IF NOT EXISTS `socialaccount_socialtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int(11) NOT NULL,
  `app_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.socialaccount_socialtoken: ~0 rows (approximately)

-- Dumping structure for table resta_.staff
CREATE TABLE IF NOT EXISTS `staff` (
  `firstName` varchar(100) NOT NULL,
  `lastName` varchar(100) NOT NULL,
  `address` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `position` varchar(100) NOT NULL,
  `region` varchar(100) NOT NULL,
  `salary` decimal(10,2) NOT NULL,
  PRIMARY KEY (`phone`),
  UNIQUE KEY `Staff_email_8a5f37f0_uniq` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table resta_.staff: ~0 rows (approximately)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
