CREATE TABLE tbl_education_type (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(64) NOT NULL
);

INSERT INTO tbl_education_type (name)
VALUES ('Associate''s degree'),
       ('Bachelor''s degree'),
       ('Master''s degree'),
       ('Doctor''s degree');

CREATE TABLE tbl_education (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    applicant_id INT NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    institution_name VARCHAR(128) NOT NULL,
    education_type_id INT NOT NULL,
    education_name VARCHAR(128) NOT NULL,
    CONSTRAINT fk_tbl_education_tbl_user_applicant_id FOREIGN KEY(applicant_id) REFERENCES tbl_user(id),
    CONSTRAINT fk_tbl_education_tbl_education_type_education_type_id FOREIGN KEY(education_type_id) REFERENCES tbl_education_type(id)
);