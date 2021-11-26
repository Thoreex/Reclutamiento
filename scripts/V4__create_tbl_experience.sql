CREATE TABLE tbl_experience (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    applicant_id INT NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    company_name VARCHAR(128) NOT NULL,
    job_title VARCHAR(128) NOT NULL,
    job_description TEXT NULL,
    CONSTRAINT fk_tbl_experience_tbl_user_applicant_id FOREIGN KEY(applicant_id) REFERENCES tbl_user(id)
);