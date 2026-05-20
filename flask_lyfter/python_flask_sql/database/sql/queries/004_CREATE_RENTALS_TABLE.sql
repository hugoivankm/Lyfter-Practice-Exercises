SET search_path TO lyfter_car_rental;

CREATE TABLE rentals (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    users_id INT NOT NULL,
    vehicles_id INT NOT NULL,
    rental_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rental_status VARCHAR(20) NOT NULL,

    CONSTRAINT fk_usuario FOREIGN KEY (users_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_vehicle FOREIGN KEY (vehicles_id)
        REFERENCES vehicles(id)
        ON DELETE CASCADE
);