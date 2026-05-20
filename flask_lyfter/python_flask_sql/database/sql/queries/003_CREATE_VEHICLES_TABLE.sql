SET search_path TO lyfter_car_rental;

BEGIN;

CREATE TABLE vehicles (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    model_year INT NOT NULL,
    vehicle_status VARCHAR(20) NOT NULL
    CONSTRAINT valid_status CHECK (vehicle_status IN ('rented', 'in_maintenance', 'available', 'unavailable', 'reserved'))
);

INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Mitsubishi', 'GTO', 1994, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Isuzu', 'Ascender', 2006, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Jaguar', 'S-Type', 2004, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Scion', 'xD', 2009, 'in_maintenance');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Dodge', 'Challenger', 2010, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Volkswagen', 'New Beetle', 2006, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Lincoln', 'Mark VIII', 1996, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Ford', 'Windstar', 2002, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Volvo', '850', 1996, 'in_maintenance');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Chevrolet', 'Monte Carlo', 1973, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Mitsubishi', 'Challenger', 2002, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Subaru', 'Forester', 2002, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Pontiac', 'Aztek', 2003, 'in_maintenance');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Chevrolet', 'Suburban 1500', 1993, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Chevrolet', 'Tahoe', 2010, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('GMC', 'Suburban 1500', 1999, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Mercedes-Benz', 'SLK-Class', 2003, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Volkswagen', 'Touareg', 2008, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Daewoo', 'Nubira', 2000, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Nissan', '240SX', 1997, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Infiniti', 'J', 1993, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('GMC', 'Sierra 1500', 2007, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Toyota', 'Land Cruiser', 2010, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Acura', 'MDX', 2009, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Suzuki', 'Sidekick', 1997, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Suzuki', 'Cultus', 1985, 'in_maintenance');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('GMC', 'Sierra 1500', 2002, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Hyundai', 'Santa Fe', 2012, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Saab', '9-3', 2010, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('BMW', 'Z4 M', 2006, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Lincoln', 'MKZ', 2011, 'in_maintenance');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Land Rover', 'Discovery', 1994, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Mitsubishi', 'Mirage', 1988, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Mazda', 'RX-7', 1988, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Mazda', 'Millenia', 1996, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Oldsmobile', 'Bravada', 2004, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Ford', 'Mustang', 1986, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Volkswagen', 'Cabriolet', 1990, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Isuzu', 'i-370', 2007, 'in_maintenance');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Chevrolet', 'Corvair', 1960, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Honda', 'Ridgeline', 2010, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Buick', 'Electra', 1985, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('GMC', 'Yukon XL 1500', 2009, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('BMW', '325', 2006, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Dodge', 'Ram Van 3500', 2003, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Dodge', 'Stealth', 1993, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Lotus', 'Exige', 2009, 'available');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Oldsmobile', 'Bravada', 1997, 'in_maintenance');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Dodge', 'Ram 1500 Club', 1996, 'rented');
INSERT INTO vehicles (make, model, model_year, vehicle_status) VALUES ('Isuzu', 'Space', 1992, 'rented');

COMMIT;