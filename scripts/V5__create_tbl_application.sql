CREATE TABLE tbl_application (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    applicant_id INT NOT NULL,
    job_id INT NOT NULL,
    application_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (applicant_id, job_id),
    CONSTRAINT fk_tbl_application_tbl_user_applicant_id FOREIGN KEY(applicant_id) REFERENCES tbl_user(id),
    CONSTRAINT fk_tbl_application_tbl_job_job_id FOREIGN KEY(job_id) REFERENCES tbl_job(id)
);