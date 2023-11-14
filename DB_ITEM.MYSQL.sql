-- apaga o  banco de dados caso ele já exista.
DROP DATABASE IF EXISTS db_items;

-- cria o banco de dados com atenção à tabela de caracteres.
CREATE DATABASE db_items CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

-- selecionar o banco de dados.
USE db_items;

-- Cria a tabela users conforme o modelo.
CREATE TABLE user (
	user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    user_name VARCHAR(127) NOT NULL,
	user_email VARCHAR(255) NOT NULL,
    user_password VARCHAR(63) NOT NULL,
    user_birth DATE,
    user_status ENUM('on', 'off') DEFAULT 'on'

);

-- Insere dados em 'user'.
INSERT INTO user (user_name, user_email, user_password, user_birth) VALUE
('Joca da Silva', 'joca@silva.com', '123', '1980-12-14'),
('Marineuza Siriliano', 'mari@neuza.com', '123', '2000-12-15'),
('Felipe Gama Pereira', 'felipete009@outlook.com', '1234', '1999-12-16');

-- Lista a inserção em 'user'.
SELECT * FROM user WHERE user_status = 'on' ORDER BY 'user_name';

-- Apaga o Joca.
UPDATE user SET user_status = 'off' WHERE user_id = 1;