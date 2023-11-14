-- Apaga as tabelas caso existam.
-- CUIDADO! Isso destroy todos os bancos de dados.

DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS owner;

-- Cria a tabela 'owner'

CREATE TABLE owner (
    owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    owner_name TEXT,
    owner_email TEXT,
    owner_password TEXT,
    owner_birth DATE,
    owner_status TEXT COMMENTS "Valores: on, off",
	owner_field1 TEXT,
    owner_field2 TEXT
);

-- Popular a tabela owner com dados 'fake'.

INSERT INTO owner (owner_id, owner_date, owner_name, owner_email, owner_password, owner_birth, owner_status)
VALUES
	('1', '2023-09-28 10:11:12', 'Felipe Gama Pereira', 'felipete009@outlook.com', '123321', '1999-12-16', 'on'),
	('2','2023-01-15 08:30:00', 'John Doe', 'john.doe@example.com', 'password123', '1990-05-15', 'on'),
    ('3','2023-02-20 12:45:00', 'Jane Smith', 'jane.smith@example.com', 'securepass', '1985-09-22', 'off'),
    ('4','2023-03-10 18:20:00', 'Alice Johnson', 'alice.johnson@example.com', 'pass1234', '1992-12-10', 'on'),
    ('5','2023-04-05 14:10:00', 'Bob Williams', 'bob.williams@example.com', 'bobpass', '1988-03-28', 'on'),
    ('6','2023-05-08 09:00:00', 'Emily Davis', 'emily.davis@example.com', 'emily123', '1995-08-05', 'off'),
    ('7','2023-06-12 16:30:00', 'Michael Brown', 'michael.brown@example.com', 'brownpass', '1982-11-17', 'on'),
    ('8','2023-07-18 10:15:00', 'Sophia Miller', 'sophia.miller@example.com', 'sophiapass', '1998-02-03', 'off'),
    ('9','2023-08-14 22:45:00', 'David Wilson', 'david.wilson@example.com', 'davidpass', '1987-07-14', 'on'),
    ('10','2023-09-30 11:20:00', 'Olivia Taylor', 'olivia.taylor@example.com', 'oliviapass', '1993-09-30', 'on'),
    ('11','2023-10-25 13:05:00', 'Daniel Anderson', 'daniel.anderson@example.com', 'danpass', '1980-12-22', 'off'),
    ('12','2023-11-08 17:40:00', 'Grace White', 'grace.white@example.com', 'gracepass', '1991-04-18', 'on'),
    ('13','2023-12-05 08:00:00', 'Henry Jones', 'henry.jones@example.com', 'henrypass', '1984-06-25', 'off'),
	('14','2024-10-20 12:20:00', 'Benjamin Brown', 'benjamin.brown@example.com', 'benjaminpass', '1984-09-30', 'off'),
    ('15','2024-11-15 15:50:00', 'Isabella Johnson', 'isabella.johnson@example.com', 'isabellapass', '1997-12-12', 'on');
	
CREATE TABLE item (
	item_id INTEGER PRIMARY KEY AUTOINCREMENT,
	item_date DATETIME DEFAULT CURRENT_TIMESTAMP,
	item_name TEXT,
	item_description TEXT,
	item_location TEXT,
	item_owner INTEGER,
	item_status TEXT DEFAULT 'on',
	item_field1 TEXT,
	item_field2 TEXT,
	FOREIGN KEY (item_owner) REFERENCES owner (owner_id)
);

INSERT INTO item (item_id, item_date, item_name, item_description, item_location, item_owner, item_status)
VALUES
('1', '2023-12-05 10:15:03', 'carteira', 'usado pra guardar dinheiro', 'loc 1', '1', 'on'),
('2', '2023-06-12 07:10:03', 'chaves', 'abre fechaduras', 'loc 2', '2', 'on'),
('3', '2023-9-07 05:20:35', 'dinheiro', 'compra coisas', 'loc 3', '3', 'on'),
('4', '2023-9-07 05:20:35', 'name 4', 'description 4', 'loc 4', '4', 'on')


