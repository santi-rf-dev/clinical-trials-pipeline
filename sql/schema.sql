DROP SCHEMA IF EXISTS {{schema}} CASCADE;

CREATE SCHEMA {{schema}};

SET search_path TO {{schema}};


CREATE TABLE studies (
    nct_id VARCHAR(11) PRIMARY KEY,
    brief_title TEXT NOT NULL,
    official_title TEXT,
    organization_name TEXT,
    organization_class VARCHAR(50),
    overall_status VARCHAR(50),
    study_type VARCHAR(50),
    phase VARCHAR(50),
    enrollment_count INTEGER,
    enrollment_type VARCHAR(50),
    start_date DATE,
    primary_completion_date DATE,
    completion_date DATE,

    CONSTRAINT chk_studies_enrollment_count
        CHECK (
            enrollment_count IS NULL
            OR enrollment_count >= 0
        )
);


CREATE TABLE conditions (
    condition_id BIGSERIAL PRIMARY KEY,
    condition_name TEXT NOT NULL UNIQUE
);


CREATE TABLE study_conditions (
    nct_id VARCHAR(11) NOT NULL,
    condition_id BIGINT NOT NULL,

    PRIMARY KEY (nct_id, condition_id),

    CONSTRAINT fk_study_conditions_study
        FOREIGN KEY (nct_id)
        REFERENCES studies (nct_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_study_conditions_condition
        FOREIGN KEY (condition_id)
        REFERENCES conditions (condition_id)
        ON DELETE CASCADE
);


CREATE TABLE interventions (
    intervention_id BIGSERIAL PRIMARY KEY,
    intervention_name TEXT NOT NULL,
    intervention_type VARCHAR(50) NOT NULL,

    CONSTRAINT uq_interventions_name_type
        UNIQUE (intervention_name, intervention_type)
);


CREATE TABLE study_interventions (
    nct_id VARCHAR(11) NOT NULL,
    intervention_id BIGINT NOT NULL,

    PRIMARY KEY (nct_id, intervention_id),

    CONSTRAINT fk_study_interventions_study
        FOREIGN KEY (nct_id)
        REFERENCES studies (nct_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_study_interventions_intervention
        FOREIGN KEY (intervention_id)
        REFERENCES interventions (intervention_id)
        ON DELETE CASCADE
);


CREATE TABLE locations (
    location_id BIGSERIAL PRIMARY KEY,
    nct_id VARCHAR(11) NOT NULL,
    facility TEXT,
    city VARCHAR(255),
    state VARCHAR(255),
    country VARCHAR(255),
    zip_code VARCHAR(50),
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),

    CONSTRAINT fk_locations_study
        FOREIGN KEY (nct_id)
        REFERENCES studies (nct_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_locations_latitude
        CHECK (
            latitude IS NULL
            OR latitude BETWEEN -90 AND 90
        ),

    CONSTRAINT chk_locations_longitude
        CHECK (
            longitude IS NULL
            OR longitude BETWEEN -180 AND 180
        )
);


CREATE INDEX idx_studies_overall_status
    ON studies (overall_status);

CREATE INDEX idx_studies_study_type
    ON studies (study_type);

CREATE INDEX idx_studies_phase
    ON studies (phase);

CREATE INDEX idx_locations_country
    ON locations (country);

CREATE INDEX idx_interventions_type
    ON interventions (intervention_type);