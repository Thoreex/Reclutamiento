CREATE TABLE tbl_user (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username VARCHAR(32) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(32) NOT NULL,
    last_name VARCHAR(32) NOT NULL,
    email varchar(320) NOT NULL,
    phone_number VARCHAR(50) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);