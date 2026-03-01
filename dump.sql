-- Nuage

-- Drop Nuage
DROP TABLE IF EXISTS entreprise CASCADE;
DROP TABLE IF EXISTS genre CASCADE;
DROP TABLE IF EXISTS jeux CASCADE;
DROP TABLE IF EXISTS joueur CASCADE;
DROP TABLE IF EXISTS succes CASCADE;
DROP TABLE IF EXISTS monnaie CASCADE;
DROP TABLE IF EXISTS developpe CASCADE;
DROP TABLE IF EXISTS edite CASCADE;
DROP TABLE IF EXISTS appartient CASCADE;
DROP TABLE IF EXISTS note CASCADE;
DROP TABLE IF EXISTS partage CASCADE;
DROP TABLE IF EXISTS achete CASCADE;
DROP TABLE IF EXISTS reussi CASCADE;
DROP TABLE IF EXISTS amis CASCADE;
DROP VIEW IF EXISTS rapport_ventes CASCADE;

/*
Schema relationnel:

Jeux(idJ, titre, prix, dateSortie, ageRequis, descriptionJ)
  PK: idJ

Entreprise(idE, nom, pays)
  PK: idE

Genre(idG, nom)
  PK: idG

Monnaie(idM, solde)
  PK: idM

Joueur(idP, pseudo, nom, email, dateN, idM)
  PK: idP
  FK: idM REFERENCES Monnaie(idM)

Succes(code, intitule, descriptionS, idJ)
  PK: code
  FK: idJ REFERENCES Jeux(idJ)

developpe(idE, idJ)
  PK: (idE, idJ)
  FK: idE REFERENCES Entreprise(idE)
  FK: idJ REFERENCES Jeux(idJ)

edite(idE, idJ)
  PK: (idE, idJ)
  FK: idE REFERENCES Entreprise(idE)
  FK: idJ REFERENCES Jeux(idJ)

appartient(idG, idJ)
  PK: (idG, idJ)
  FK: idG REFERENCES Genre(idG)
  FK: idJ REFERENCES Jeux(idJ)

note(idJ, idP, commentaire)
  PK: (idJ, idP)
  FK: idJ REFERENCES Jeux(idJ)
  FK: idP REFERENCES Joueur(idP)

achete(idJ, idP, dateA)
  PK: (idJ, idP, dateA)
  FK: idJ REFERENCES Jeux(idJ)
  FK: idP REFERENCES Joueur(idP)

partage(idJ, idP1, idP2)
  PK: (idJ, idP1, idP2)
  FK: idJ REFERENCES Jeux(idJ)
  FK: idP1 REFERENCES Joueur(idP)
  FK: idP2 REFERENCES Joueur(idP)

reussi(idP, code, dateR)
  PK: (idP, code)
  FK: idP REFERENCES Joueur(idP)
  FK: code REFERENCES Succes(code)

amis(idP1, idP2, demande)
  PK: (idP1, idP2)
  FK: idP1 REFERENCES Joueur(idP)
  FK: idP2 REFERENCES Joueur(idP)
*/

-- Création des tables

CREATE TABLE jeux (
	idJ serial PRIMARY KEY,
	titre varchar(20),
	prix numeric(5, 2),
	dateSortie date,
	ageRequis int,
	descriptionJ text
);

CREATE TABLE entreprise (
	idE serial PRIMARY KEY,
	nom varchar(20),
	pays varchar(20)
);

CREATE TABLE genre (
	idG serial PRIMARY KEY,
	nom varchar(20)
);

CREATE TABLE monnaie (
	idM serial PRIMARY KEY,
	solde numeric(6, 2) DEFAULT 0.00
);

CREATE TABLE joueur (
	idP serial PRIMARY KEY,
	pseudo varchar(10),
	nom varchar(20),
	email varchar(100),
	dateN date,
	idM int REFERENCES monnaie(idM),
	mdp varchar(100)
);

CREATE TABLE succes (
	code serial PRIMARY KEY,
	intitule varchar(100),
	descriptionS text,
	idJ int REFERENCES jeux(idJ)
);

-- Création des associations

CREATE TABLE developpe (
	idE int,
	idJ int,
	PRIMARY KEY (idE, idJ),
	FOREIGN KEY (idE) REFERENCES entreprise(idE),
	FOREIGN KEY (idJ) REFERENCES jeux(idJ)
);

CREATE TABLE edite (
	idE int,
	idJ int,
	PRIMARY KEY (idE, idJ),
	FOREIGN KEY (idE) REFERENCES entreprise(idE),
	FOREIGN KEY (idJ) REFERENCES jeux(idJ)
);

CREATE TABLE appartient (
	idG int,
	idJ int,
	PRIMARY KEY (idG, idJ),
	FOREIGN KEY (idG) REFERENCES genre(idG),
	FOREIGN KEY (idJ) REFERENCES jeux(idJ)
);

CREATE TABLE note (
	idJ int,
	idP int,
	commentaire text,
	note int check (note <= 10),
	PRIMARY KEY (idJ, idP),
	FOREIGN KEY (idJ) REFERENCES jeux(idJ),
	FOREIGN KEY (idP) REFERENCES joueur(idP) ON DELETE CASCADE
);

CREATE TABLE achete (
	idJ int,
	idP int,
	dateA date,
	PRIMARY KEY (idJ, idP, dateA),
	FOREIGN KEY (idJ) REFERENCES jeux(idJ),
	FOREIGN KEY (idP) REFERENCES joueur(idP) ON DELETE CASCADE
);

CREATE TABLE partage (
	idJ int,
	idP1 int,
	idP2 int,
	PRIMARY KEY (idJ, idP1, idP2),
	FOREIGN KEY (idJ) REFERENCES jeux(idJ),
	FOREIGN KEY (idP1) REFERENCES joueur(idP) ON DELETE CASCADE,
	FOREIGN KEY (idP2) REFERENCES joueur(idP) ON DELETE CASCADE
);

CREATE TABLE reussi (
	idP int,
	code int,
	dateR date,
	PRIMARY KEY (idP, code),
	FOREIGN KEY (idP) REFERENCES joueur(idP) ON DELETE CASCADE,
	FOREIGN KEY (code) REFERENCES succes(code)
);

CREATE TABLE amis (
	idP1 int,
	idP2 int,
	demande int,
	PRIMARY KEY (idP1, idP2),
	FOREIGN KEY (idP1) REFERENCES joueur(idP) ON DELETE CASCADE,
	FOREIGN KEY (idP2) REFERENCES joueur(idP) ON DELETE CASCADE
);

-- Remplissage des tables 

-- Insertion dans la table Jeux
INSERT INTO jeux (titre, prix, dateSortie, ageRequis, descriptionJ) VALUES
('Adventure Quest', 19.99, '2023-06-12', 12, 'Une aventure épique.'),
('Battle Stars', 39.99, '2022-10-05', 16, 'Jeu de combat intense.'),
('Mystic World', 29.99, '2021-11-23', 10, 'Explorez un monde mystique.'),
('Space Explorer', 49.99, '2024-01-15', 18, 'Voyagez dans un espace infini.'),
('Fantasy Fighters', 34.99, '2020-05-21', 14, 'Combattez dans un monde fantastique.'),
('Pixel Jump', 14.99, '2019-09-09', 8, 'Sautez et évitez les obstacles.'),
('Maze Runner', 24.99, '2018-12-17', 10, 'Courez à travers un labyrinthe.'),
('Kingdom Quest', 44.99, '2023-03-14', 12, 'Quête royale dans un royaume.'),
('Racing Pro', 39.99, '2017-08-30', 10, 'Course automobile rapide.'),
('Zombie Survival', 29.99, '2021-06-05', 18, 'Survivez dans un monde de zombies.');

-- Insertion dans la table Entreprise
INSERT INTO entreprise (nom, pays) VALUES
('TechGames', 'USA'),
('PlayFun', 'Canada'),
('EpicWorks', 'France'),
('PixelArt', 'Japan'),
('AdventureSoft', 'UK'),
('MegaPlay', 'Germany'),
('BattleZone', 'Italy'),
('FutureGames', 'Spain'),
('OldSchool', 'Poland'),
('GamePlus', 'South Korea');

-- Insertion dans la table Genre
INSERT INTO genre (nom) VALUES
('Action'),
('Adventure'),
('RPG'),
('Simulation'),
('Horror'),
('Racing'),
('Strategy'),
('Sports'),
('Puzzle'),
('Platformer'),
('Shooter'),
('Fighting'),
('Survival'),
('Open World'),
('Stealth');

-- Insertion dans la table Monnaie
INSERT INTO monnaie (solde) VALUES
(100.00),
(150.50),
(200.75),
(50.25),
(75.00),
(120.50),
(60.00),
(90.25),
(300.00),
(180.75);

-- Insertion dans la table Joueur
INSERT INTO joueur (pseudo, nom, email, dateN, idM) VALUES
('Player1', 'Dupont', 'player1@mail.com', '1990-02-15', 1),
('Gamer2', 'Durand', 'gamer2@mail.com', '1995-07-24', 2),
('Ace3', 'Martin', 'ace3@mail.com', '2000-11-12', 3),
('Noob4', 'Bernard', 'noob4@mail.com', '1988-04-23', 4),
('Pro5', 'Moreau', 'pro5@mail.com', '1992-10-30', 5),
('Star6', 'Petit', 'star6@mail.com', '1998-06-11', 6),
('Champ7', 'Lemoine', 'champ7@mail.com', '1991-03-05', 7),
('Hero8', 'Blanc', 'hero8@mail.com', '1993-12-20', 8),
('Boss9', 'Giraud', 'boss9@mail.com', '1985-05-16', 9),
('King10', 'Roux', 'king10@mail.com', '1999-09-10', 10);

-- Insertion dans la table Succes
INSERT INTO succes (intitule, descriptionS, idJ) VALUES
('First Victory', 'Remporter une première victoire', 1),
('Master Explorer', 'Explorer tous les niveaux', 1),
('Legend Status', 'Atteindre le niveau maximum', 1),
('First Blood', 'Gagner votre premier combat', 2),
('Strategist', 'Gagner sans perdre de vie', 2),
('Champion', 'Remporter le tournoi mondial', 2),
('Apprentice', 'Apprendre votre première magie', 3),
('Archmage', 'Maîtriser toutes les magies', 3),
('World Savior', 'Terminer l''histoire principale', 3),
('Take Off', 'Quitter l''atmosphère', 4),
('Galaxy Mapper', 'Découvrir 50 systèmes solaires', 4),
('Universal Peace', 'Unifier toutes les races', 4),
('First Strike', 'Gagner un combat', 5),
('Combo Master', 'Réaliser un combo de 100 coups', 5),
('Ultimate Fighter', 'Débloquer tous les personnages', 5),
('First Jump', 'Terminer le niveau 1', 6),
('Perfect Run', 'Finir un niveau sans mourir', 6),
('Speed Runner', 'Finir le jeu en moins de 30 minutes', 6),
('Escape Artist', 'Sortir du premier labyrinthe', 7),
('Ghost', 'Finir un niveau sans être vu', 7),
('Maze Master', 'Terminer tous les labyrinthes', 7),
('Squire', 'Devenir écuyer', 8),
('Knight', 'Être adoubé chevalier', 8),
('King', 'Monter sur le trône', 8),
('Rookie', 'Gagner votre première course', 9),
('Speed Demon', 'Battre un record de piste', 9),
('World Champion', 'Gagner le championnat du monde', 9),
('Survivor', 'Survivre une journée', 10),
('Zombie Slayer', 'Tuer 1000 zombies', 10),
('Last Man Standing', 'Survivre 100 jours', 10);

-- Insertion dans la table Developpe
INSERT INTO developpe (idE, idJ) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

-- Insertion dans la table Edite
INSERT INTO edite (idE, idJ) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

-- Insertion dans la table Appartient
INSERT INTO appartient (idG, idJ) VALUES
(1, 1), (2, 1), (3, 1),
(1, 2), (12, 2), (7, 2),
(2, 3), (3, 3), (14, 3),
(4, 4), (11, 4), (14, 4),
(1, 5), (3, 5), (12, 5),
(10, 6), (9, 6), (2, 6),
(2, 7), (15, 7), (9, 7),
(2, 8), (3, 8), (14, 8),
(6, 9), (4, 9), (8, 9),
(5, 10), (13, 10), (1, 10);

-- Insertion dans la table Note
INSERT INTO note (idJ, idP, commentaire, note) VALUES
(1, 1, 'Très amusant !', 8),
(2, 2, 'Bon jeu de combat.', 7),
(3, 3, 'Très immersif.', 8),
(4, 4, 'Excellente expérience.', 9),
(5, 5, 'Amusant et captivant.', 9),
(6, 6, 'Très difficile.', 5),
(7, 7, 'Un vrai challenge.', 6),
(8, 8, 'À essayer absolument.', 8),
(9, 9, 'Beau graphisme.', 7),
(10, 10, 'Bon jeu pour se détendre.', 6);

-- Insertion dans la table Achete
INSERT INTO achete (idJ, idP, dateA) VALUES
(1, 1, '2023-06-12'),
(2, 2, '2023-07-05'),
(3, 3, '2023-08-11'),
(4, 4, '2023-09-15'),
(5, 5, '2023-10-20'),
(6, 6, '2023-11-22'),
(7, 7, '2023-12-25'),
(8, 8, '2024-01-01'),
(9, 9, '2024-01-15'),
(10, 10, '2024-02-05');

-- Insertion dans la table Partage
INSERT INTO partage (idJ, idP1, idP2) VALUES
(1, 1, 2),
(2, 2, 3),
(3, 3, 4),
(4, 4, 5),
(5, 5, 6),
(6, 6, 7),
(7, 7, 8),
(8, 8, 9),
(9, 9, 10),
(10, 10, 1);

-- Insertion dans la table Reussi
INSERT INTO reussi (idP, code, dateR) VALUES
(1, 1, '2023-07-01'),
(1, 2, '2023-07-15'),
(2, 4, '2023-08-01'),
(3, 7, '2023-09-01'),
(3, 8, '2023-09-15'),
(3, 9, '2023-09-30'),
(4, 10, '2023-10-01'),
(5, 13, '2023-11-01'),
(5, 14, '2023-11-15'),
(6, 16, '2023-12-01'),
(6, 17, '2023-12-15'),
(6, 18, '2023-12-30'),
(7, 19, '2024-01-01'),
(8, 22, '2024-02-01'),
(8, 23, '2024-02-15'),
(9, 25, '2024-03-01'),
(9, 26, '2024-03-15'),
(9, 27, '2024-03-30'),
(10, 28, '2024-04-01'),
(10, 29, '2024-04-15');

-- Insertion dans la table Amis
INSERT INTO amis (idP1, idP2, demande) VALUES
(1, 2, 1),
(2, 3, 1),
(3, 4, 1),
(4, 5, 1),
(5, 6, 1),
(6, 7, 1),
(7, 8, 1),
(8, 9, 1),
(9, 10, 1),
(10, 1, 1);

-- Vue
CREATE VIEW rapport_ventes AS
SELECT
    e.nom AS editeur,
    j.idJ,
    j.titre,
    COUNT(ach.idJ) AS nombre_ventes,
    COUNT(part.idJ) AS nombre_prets,
    SUM(j.prix * (CASE WHEN ach.idJ IS NOT NULL THEN 1 ELSE 0 END)) AS chiffre_affaires,
    round(AVG(n.note), 2) AS note_moyenne,
    COUNT(DISTINCT s.code) AS total_succes,
    DATE(ach.dateA) AS date
FROM
    jeux j
    JOIN edite ed ON j.idJ = ed.idJ
    JOIN entreprise e ON ed.idE = e.idE
    LEFT JOIN achete ach ON j.idJ = ach.idJ
    LEFT JOIN partage part ON j.idJ = part.idJ
    LEFT JOIN note n ON j.idJ = n.idJ
    LEFT JOIN succes s ON j.idJ = s.idJ
    LEFT JOIN reussi r ON s.code = r.code
GROUP BY
    e.nom,
    j.idJ,
    j.titre,
    DATE(ach.dateA);
