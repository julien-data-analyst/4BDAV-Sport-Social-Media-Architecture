INSERT INTO "User" (id, firstname, lastname, description, email, password)
VALUES ('1', 'John', 'Doe', 'Sportif professionnel qui fait de la natation', 'john@example.com', '12345'),
        ('2', 'Jul', 'JJ', 'Professionnel sportif de haut niveau dans la course', 'jul@example.com', '23456'),
        ('3', 'Louise', 'LL', 'Sportive occasionnelle, faits course à pieds et nattation', 'louise@example.com', '34567')
;

INSERT INTO "Sport" (id, name, description) 
VALUES 
('1', 'Natation', 'Parmi les activités humaines, la natation regroupe le déplacement à la surface de l''eau et sous l''eau (plongée, mermaiding, natation synchronisée, water-polo), le plongeon et divers jeux pratiqués dans l''eau.'),
('2', 'Course à pieds (Trail)', 'Le trail, la course nature ou plus rarement la course en sentier, est un sport de course à pied, en milieu naturel, généralement sur des chemins de terre et des sentiers de randonnée en plaine, en forêt ou en montagne.');

INSERT INTO "Metric" (id, name, unity)
VALUES ('1', 'Distance parcourue', 'km'),
('2', 'Vitesse de course', 'km/h'),
('3', 'Nombre de mouvements', NULL),
('4', 'SWOLF', NULL),
('5', 'Nombre de longueurs', NULL),
('6', 'Temps de la longueur', 'secondes');

INSERT INTO "User_Sports" (id, user_id, sport_id) 
VALUES ('1', '1', '1'),
        ('2', '2', '2'),
        ('3', '2', '1'),
        ('4', '3', '1'),
        ('5', '3', '2')
;

INSERT INTO "Professionnal" (id, user_sport_id, title, description) 
VALUES ('1', '1', 'Sportif professionnel de nattation dans le club de cherbourg',
'Premier de son club'),
('2', '2', 'Sportif professionnel de la course à pieds dans le club de cherbourg', 
'Dixième de son club + remporter une médaille d''or lors d''une compétition')
;

INSERT INTO "Sensor" (id, name, type, formula, unity) VALUES
('1', 'capteur de course à pieds', 'montre', NULL, NULL),
('2', 'détection de mouvement dans la piscine', 'bracelet', 'SWOLF', NULL),
('3', 'capteur fixe pour compter les longueurs', 'capteur fixe', NULL, NULL);

INSERT INTO "Apparatus" (id, name, type) VALUES
('1', 'montre numérique', 'montre'),
('2', 'Samsung A52', 'mobile'),
('3', 'Iphone 10', 'mobile'),
('4', 'Galacy tab A9+', 'tablette')
;

INSERT INTO "Sensors_Apparatus" (id, sensor_id, apparatus_id) VALUES
('1', '1', '1'),
('2', '2', '4'),
('3', '2', '2'),
('4', '3', '4'),
('5', '3', '3'),
('6', '3', '2')
;

INSERT INTO "Aggregation" (id, name) VALUES
('1', 'min'),
('2', 'max'),
('3', 'mean'),
('4', 'median'),
('5', 'Q1'),
('6', 'Q3'),
('7', 'standard deviation'),
('8', 'variability')
;

INSERT INTO "Aggregation_Metric" (id, name, id_metric, id_aggregation) VALUES
('1', 'Distance parcourue (km)','1', '2'),
('2', 'Moyenne de la vitesse de course (km/h)', '2', '3'),
('3', 'Médiane de la vitesse de course (km/h)', '2', '4'),
('4', 'Q1 de la vitesse de course (km/h)', '2', '5'),
('5', 'Q3 de la vitesse de course (km/h)', '2', '6'),
('6', 'Variation de la vitesse de course (km/h)', '2', '8'),
('7', 'Ecart-type de la vitesse de course (km/h)', '2', '7'),
('8', 'Nombre de mouvements', '3', '2'),
('9', 'Moyenne du SWOLF', '4', '3'),
('10', 'Médiane du SWOLF', '4', '4'),
('11', 'Q1 SWOLF', '4', '5'),
('12', 'Q3 SWLOF', '4', '6'),
('13', 'Nombre de longueurs', '5', '2'),
('14', 'Temps maximum pour une longueur', '6', '2'),
('15', 'Temps minimum pour une longueur', '6', '1'),
('16', 'Moyenne de temps pour une longueur', '6', '3')
;

INSERT INTO "Sensors_Metrics" (id, id_sensor, id_metric) VALUES
('1', '1', '1'),
('2', '1', '2'),
('3', '2', '3'),
('4', '2', '4'),
('5', '3', '5'),
('6', '3', '6');

INSERT INTO "Sports_Metrics" (id, sport_id, metric_id) VALUES
('1', '1', '4'),
('2', '1', '5'),
('3', '1', '6'),
('4', '2', '1');

