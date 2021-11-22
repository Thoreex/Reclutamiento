BEGIN TRANSACTION;

DROP TABLE IF EXISTS tbl_user;

CREATE TABLE tbl_user (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username VARCHAR(32) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(32) NOT NULL,
    last_name VARCHAR(32) NOT NULL
);

INSERT INTO tbl_user (username, password, first_name, last_name)
VALUES ('admin', 'pbkdf2:sha256:260000$YAw3lhu3TjFjxfsz$59bac94ff7b09a12133a6dec8f23defe8a03d30e87c394cb89a74056ef31381a', 'Administrator', 'User');

END TRANSACTION;