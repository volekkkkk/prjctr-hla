# CREATE DATABASE hla;

USE hla; 


CREATE TABLE USERS (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    birth_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE InnoDB

DELIMITER //

CREATE PROCEDURE hla.InsertBulkUsers(IN total INT)
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE username VARCHAR(255);
    DECLARE email VARCHAR(255);
    DECLARE pswrd VARCHAR(255);
    DECLARE birth_date DATE;
    DECLARE created_at TIMESTAMP;

    START TRANSACTION;

    WHILE i <= total DO
        SET username = CONCAT("user", i);
        SET email = CONCAT(username, "@example.com");
        SET pswrd = CONCAT(i, "pswrd");
        SET birth_date = DATE_ADD('1980-01-01', INTERVAL FLOOR(RAND() * 40) YEAR);
        SET created_at = DATE_ADD(NOW(), INTERVAL -FLOOR(RAND() * 365) DAY);

        INSERT INTO USERS (username, email, password, birth_date, created_at) VALUES (username, email, pswrd, birth_date, created_at);

        SET i = i + 1;
    END WHILE;

    COMMIT;
END //

DELIMITER ;

CALL InsertBulkUsers(40000000);

