CREATE TABLE risk_categories (
    id INT PRIMARY KEY,
    risk_name VARCHAR(255) NOT NULL
);

INSERT INTO risk_categories (id, risk_name)
VALUES 
(0, 'Very Low Risk'),
(1, 'Low Risk'),
(2, 'Medium Risk'),
(3, 'High Risk'),
(4, 'Very High Risk'),
(5, 'Critical Risk');


CREATE OR REPLACE FUNCTION prevent_changes_to_risk_categories()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Modification of data in risk_categories is not allowed';
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_insert_update_delete
    BEFORE INSERT OR UPDATE OR DELETE ON risk_categories
    FOR EACH ROW EXECUTE FUNCTION prevent_changes_to_risk_categories();

--------------------------------------------------------------------------

CREATE TABLE organization (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    short_name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    specialization TEXT NOT NULL,
    bank_details TEXT NOT NULL
);

INSERT INTO organization (code, full_name, short_name, address, specialization, bank_details)
VALUES 
('ORG001', 'Global Tech Solutions', 'GTS', '123 Main Street, Tech City', 'IT Services', 'GLOB1234'),
('ORG002', 'HealthCare Corp', 'HCC', '456 Health Avenue, MedTown', 'Healthcare Services', 'HEAL5678'),
('ORG003', 'EduCore Academy', 'ECA', '789 Learning Lane, EduTown', 'Education Services', 'EDU12345');


CREATE OR REPLACE PROCEDURE add_organization(
    p_code VARCHAR,
    p_full_name VARCHAR,
    p_short_name VARCHAR,
    p_address TEXT,
    p_specialization TEXT,
    p_bank_details TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO organization (code, full_name, short_name, address, specialization, bank_details)
    VALUES (p_code, p_full_name, p_short_name, p_address, p_specialization, p_bank_details);
END;
$$;


CREATE OR REPLACE PROCEDURE update_organization(
    p_id INT,
    p_code VARCHAR,
    p_full_name VARCHAR,
    p_short_name VARCHAR,
    p_address TEXT,
    p_specialization TEXT,
    p_bank_details TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE organization
    SET
        code = CASE WHEN TRIM(p_code) <> '' THEN p_code ELSE code END,
        full_name = CASE WHEN TRIM(p_full_name) <> '' THEN p_full_name ELSE full_name END,
        short_name = CASE WHEN TRIM(p_short_name) <> '' THEN p_short_name ELSE short_name END,
        address = CASE WHEN TRIM(p_address) <> '' THEN p_address ELSE address END,
        specialization = CASE WHEN TRIM(p_specialization) <> '' THEN p_specialization ELSE specialization END,
        bank_details = CASE WHEN TRIM(p_bank_details) <> '' THEN p_bank_details ELSE bank_details END
    WHERE id = p_id;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_organization(p_id INT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM organization WHERE id = p_id;
END;
$$;

--------------------------------------------------------------------------

CREATE TABLE agent (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    passport_data VARCHAR(255) NOT NULL
);


CREATE OR REPLACE PROCEDURE add_agent(
    p_full_name VARCHAR,
    p_passport_data VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO agent (full_name, passport_data)
    VALUES (p_full_name, p_passport_data);
END;
$$;


CREATE OR REPLACE PROCEDURE update_agent(
    p_id INT,
    p_full_name VARCHAR,
    p_passport_data VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE agent
    SET
        full_name = CASE WHEN TRIM(p_full_name) <> '' THEN p_full_name ELSE full_name END,
        passport_data = CASE WHEN TRIM(p_passport_data) <> '' THEN p_passport_data ELSE passport_data END
    WHERE id = p_id;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_agent(p_id INT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM agent WHERE id = p_id;
END;
$$;


INSERT INTO agent (full_name, passport_data)
VALUES 
('John Smith', 'ABC123456'),
('Jane Doe', 'DEF789012'),
('Mike Brown', 'GHI345678'),
('Anna White', 'JKL901234'),
('Robert Black', 'MNO567890');

--------------------------------------------------------------------------

CREATE TABLE contract (
    id SERIAL PRIMARY KEY,
    agent_id INT REFERENCES agent(id) ON DELETE CASCADE,
    conclusion_date DATE NOT NULL,
    duration INTERVAL NOT NULL
);

CREATE INDEX idx_contract_conclusion_date
ON contract (conclusion_date);

INSERT INTO contract (agent_id, conclusion_date, duration)
VALUES 
(1, '2023-01-15', '2 years'),
(2, '2024-06-10', '1 year'),
(3, '2022-08-20', '3 years'),
(4, '2023-12-01', '1.5 years'),
(5, '2024-03-25', '1 year');

--------------------------------------------------------------------------

CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    risk_category INT REFERENCES risk_categories(id) NOT NULL,
    contract_id INT REFERENCES contract(id) ON DELETE CASCADE,
    amount INT NOT NULL
);

CREATE OR REPLACE FUNCTION check_duplicate_payment()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM payments
        WHERE risk_category = NEW.risk_category
          AND contract_id = NEW.contract_id
          AND id != NEW.id
    ) THEN
        RAISE NOTICE 'Duplicate entry with risk_category = % and contract_id = % already exists. Skipping the insertion.', 
            NEW.risk_category, NEW.contract_id;

        PERFORM setval(pg_get_serial_sequence('payments', 'id'), (SELECT MAX(id) FROM payments));

        RETURN NULL;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER check_duplicate_payment_insert
BEFORE INSERT ON payments
FOR EACH ROW
EXECUTE FUNCTION check_duplicate_payment();


CREATE OR REPLACE FUNCTION prevent_risk_contract_update()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.risk_category IS DISTINCT FROM OLD.risk_category OR
       NEW.contract_id IS DISTINCT FROM OLD.contract_id THEN
        RAISE  'Updating risk_category or contract_id is not allowed.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_risk_contract_update_trigger
BEFORE UPDATE ON payments
FOR EACH ROW
EXECUTE FUNCTION prevent_risk_contract_update();


INSERT INTO payments (risk_category, contract_id, amount)
VALUES 
(1, 1, 5000), (1, 1, 4500), (1, 1, 4700), (1, 1, 4800), (1, 1, 4900),
(2, 2, 3000), (2, 2, 3200), (2, 2, 3100), (2, 2, 3300), (2, 2, 3400),
(3, 3, 4000), (3, 3, 4200), (3, 3, 4100), (3, 3, 4300), (3, 3, 4400),
(4, 4, 2500), (4, 4, 2600), (4, 4, 2700), (4, 4, 2800), (4, 4, 2900),
(5, 5, 6000), (5, 5, 6100), (5, 5, 6200), (5, 5, 6300), (5, 5, 6400);

--------------------------------------------------------------------------

CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    risk_category INT REFERENCES risk_categories(id) ON DELETE CASCADE,
    contract_id INT REFERENCES contract(id) ON DELETE CASCADE,
    organization_id INT REFERENCES organization(id) ON DELETE CASCADE
);


CREATE OR REPLACE PROCEDURE add_employee(
    p_full_name VARCHAR,
    p_age INT,
    p_risk_category INT,
    p_contract_id INT,
    p_organization_id INT
)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO employee (full_name, age, risk_category, contract_id, organization_id)
    VALUES (p_full_name, p_age, p_risk_category, p_contract_id, p_organization_id);
END;
$$;

CREATE OR REPLACE PROCEDURE update_employee(
    p_id INT,
    p_full_name VARCHAR,
    p_age INT,
    p_risk_category INT,
    p_contract_id INT,
    p_organization_id INT
)
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE employee
    SET 
        full_name = CASE WHEN TRIM(p_full_name) <> '' THEN p_full_name ELSE full_name END,
        age = CASE WHEN p_age > 0 THEN p_age ELSE age END,
        risk_category = CASE WHEN p_risk_category >= 0 THEN p_risk_category ELSE risk_category END,
        contract_id = CASE WHEN p_contract_id > 0 THEN p_contract_id ELSE contract_id END,
        organization_id = CASE WHEN p_organization_id > 0 THEN p_organization_id ELSE organization_id END
    WHERE id = p_id;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_employee(p_id INT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM employee WHERE id = p_id;
END;
$$;


INSERT INTO employee (full_name, age, risk_category, contract_id, organization_id)
VALUES 
('Alice Johnson', 30, 1, 1, 1), 
('Bob Williams', 35, 1, 1, 1), 
('Clara Davis', 28, 2, 2, 1), 
('David Harris', 40, 2, 2, 1),

('Eve Taylor', 29, 3, 3, 2), 
('Frank Moore', 45, 3, 3, 2), 
('Grace Lee', 33, 4, 4, 2), 
('Henry Wilson', 50, 4, 4, 2),

('Ivy Hall', 31, 5, 5, 3), 
('Jack Young', 38, 5, 5, 3), 
('Karen Scott', 26, 5, 5, 3), 
('Liam Turner', 48, 5, 5, 3);

--------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION get_active_contracts_by_date(
    p_org_id INT,
    p_date DATE
)
RETURNS TABLE (
    organization_name VARCHAR,
    organization_address TEXT,
    contract_id INT,
    start_date DATE,
    end_date DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT 
        o.full_name AS organization_name,
        o.address AS organization_address,
        c.id::integer AS contract_id,
        c.conclusion_date::date AS start_date,
        (c.conclusion_date + c.duration)::date AS end_date
    FROM 
        organization o
    JOIN 
        employee e ON o.id = e.organization_id
    JOIN 
        contract c ON e.contract_id = c.id
    WHERE 
        o.id = p_org_id
        AND c.conclusion_date <= p_date
        AND (c.conclusion_date + c.duration) >= p_date;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_agents_for_organization_on_date(
    org_id INT, 
    chosen_date DATE
)
RETURNS TABLE(
    organization_name VARCHAR,
    agent_full_name VARCHAR,
    agent_passport_data VARCHAR,
    contract_conclusion_date DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        o.full_name AS organization_name,
        a.full_name AS agent_full_name,
        a.passport_data AS agent_passport_data,
        c.conclusion_date AS contract_conclusion_date
    FROM 
        contract c
    JOIN 
        agent a ON c.agent_id = a.id
    JOIN 
        employee e ON c.id = e.contract_id
    JOIN 
        organization o ON e.organization_id = o.id
    WHERE 
        e.organization_id = org_id
        AND c.conclusion_date <= chosen_date
        AND (c.conclusion_date + c.duration) >= chosen_date;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_insurance_payments_for_employees_on_date(
    chosen_date DATE
)
RETURNS TABLE(
    payment_date DATE,
    risk_category_name VARCHAR,
    payment_amount INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.payment_date AS payment_date,
        rc.risk_name AS risk_category_name,
        p.amount AS payment_amount
    FROM 
        payments p
    JOIN 
        risk_categories rc ON p.risk_category = rc.id
    JOIN 
        employee e ON e.id = p.employee_id
    WHERE 
        p.payment_date <= chosen_date
        AND (e.contract_id IS NOT NULL);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_insurance_payments(selected_date DATE)
RETURNS TABLE (
    risk_category VARCHAR,
    employee_name VARCHAR,
    payment_amount INT,
    contract_date DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        ec.risk_name AS risk_category,
        e.full_name AS employee_name,
        p.amount AS payment_amount,
        c.conclusion_date AS contract_date
    FROM 
        employee e
    JOIN 
        risk_categories ec ON e.risk_category = ec.id
    JOIN 
        contract c ON e.contract_id = c.id
    JOIN 
        payments p ON c.id = p.contract_id
    WHERE 
        c.conclusion_date <= selected_date
    ORDER BY 
        ec.risk_name, e.full_name;
END;
$$ LANGUAGE plpgsql;


--------------------------------------------------------------------------
