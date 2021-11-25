CREATE TABLE tbl_job (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    responsible_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    title VARCHAR(100) NOT NULL,
    body TEXT NOT NULL,
    CONSTRAINT fk_tbl_job_tbl_user_responsible_id FOREIGN KEY(responsible_id) REFERENCES tbl_user(id)
);