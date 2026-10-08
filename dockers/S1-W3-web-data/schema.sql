-- Schéma initial du catalogue des espèces (hors oiseaux migrateurs).
-- Le pavillon des oiseaux migrateurs a sa propre encyclopédie (livrable 1, demande 1).
-- Ce catalogue couvre les 3 autres écosystèmes : marin, forestier, pollinisateurs.
-- Joué une seule fois au premier démarrage du container par demarrer-services.sh.

CREATE DATABASE IF NOT EXISTS catalogue_especes
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE catalogue_especes;

CREATE TABLE IF NOT EXISTS espece (
    identifiant INT AUTO_INCREMENT PRIMARY KEY,
    nom_commun VARCHAR(120) NOT NULL,
    nom_latin VARCHAR(120) NOT NULL,
    ecosysteme ENUM('marin', 'forestier', 'pollinisateurs') NOT NULL,
    statut_residence VARCHAR(80) NOT NULL,
    description TEXT NOT NULL,
    fait_marquant TEXT,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ecosysteme (ecosysteme)
);

-- ----- 12 espèces : 4 par écosystème, aucun oiseau -----

INSERT INTO espece (nom_commun, nom_latin, ecosysteme, statut_residence, description, fait_marquant) VALUES

-- Écosystème marin (4)
('Béluga du Saint-Laurent', 'Delphinapterus leucas', 'marin', 'Résidence permanente', 'Petite baleine blanche emblématique de l''estuaire et du golfe du Saint-Laurent. Population isolée et menacée d''environ 900 individus. Communique par un large répertoire de sifflements et de claquements.', 'Surnommé le canari des mers pour son chant audible à plusieurs kilomètres sous l''eau.'),
('Phoque commun', 'Phoca vitulina', 'marin', 'Résidence permanente', 'Plus petit des phoques du Saint-Laurent, présent toute l''année sur les rochers du Bas-Saint-Laurent et de la Gaspésie. Se reconnaît à son museau court et à ses taches sombres irrégulières.', 'Peut rester jusqu''à 30 minutes sous l''eau et plonger à 200 mètres de profondeur.'),
('Crabe des neiges', 'Chionoecetes opilio', 'marin', 'Résidence permanente', 'Crustacé des fonds froids du golfe et de l''estuaire, à pattes longues et fines. Pêche commerciale majeure de la Côte-Nord et de la Gaspésie. Vit entre 50 et 300 mètres de profondeur.', 'Migre verticalement dans la colonne d''eau au gré des saisons.'),
('Étoile de mer commune', 'Asterias rubens', 'marin', 'Résidence permanente', 'Échinoderme à cinq bras radiaux, couleurs orangées à brunes, présent sur les fonds rocheux du Saint-Laurent. Capable de régénérer un bras perdu, et même un disque central s''il reste un seul bras.', 'Mange ses proies en projetant son estomac à l''extérieur de son corps pour digérer une moule sur place.'),

-- Écosystème forestier (4)
('Orignal', 'Alces americanus', 'forestier', 'Résidence permanente', 'Plus grand cervidé du continent. Abondant dans la forêt boréale du Bas-Saint-Laurent, des Hautes-Terres et de la Gaspésie. Solitaire la majeure partie de l''année, sauf en saison du brame en automne.', 'Le mâle perd ses bois chaque hiver et en repousse une nouvelle paire au printemps.'),
('Lièvre d''Amérique', 'Lepus americanus', 'forestier', 'Résidence permanente', 'Petit lièvre forestier qui change de couleur selon la saison : brun roux l''été, blanc l''hiver pour se camoufler dans la neige. Le poids des pattes lui permet de marcher sur la neige sans s''enfoncer.', 'Sa population suit un cycle de 10 ans, lié à celui du lynx du Canada qui s''en nourrit.'),
('Lynx du Canada', 'Lynx canadensis', 'forestier', 'Résidence permanente', 'Félin discret de la forêt boréale, plus petit que le couguar. Reconnaissable à ses oreilles surmontées de pinceaux noirs et à ses pattes énormes qui lui servent de raquettes naturelles dans la neige profonde.', 'Sa population suit fidèlement celle du lièvre d''Amérique avec un cycle de dix ans, parfaitement documenté par les archives de fourrure.'),
('Renard roux', 'Vulpes vulpes', 'forestier', 'Résidence permanente', 'Petit canidé adaptable, présent en forêt comme en milieu agricole. Pelage orangé à blanc selon la sous-espèce. Excellent chasseur de petits rongeurs grâce à une ouïe extraordinaire.', 'Capable de localiser une souris sous la neige uniquement à l''oreille, et de plonger pour la capturer en sautant tête première.'),

-- Écosystème pollinisateurs et jardins (4)
('Papillon monarque', 'Danaus plexippus', 'pollinisateurs', 'Migration estivale', 'Papillon orange et noir emblématique. Effectue une migration de plusieurs générations entre le Mexique et le sud du Québec, en suivant la croissance de l''asclépiade, sa plante hôte.', 'Aucun individu ne fait le voyage aller-retour : ce sont les arrière-arrière-petits-enfants qui reviennent au point de départ de leurs ancêtres.'),
('Bourdon fébrile', 'Bombus impatiens', 'pollinisateurs', 'Résidence permanente', 'Bourdon indigène de l''Est canadien, très bon pollinisateur des plantes à corolle tubulaire. Peut voler par temps frais, contrairement aux abeilles domestiques. Niche au sol, dans des abris naturels.', 'Sa langue mesure presque la longueur de son corps, lui permettant d''atteindre le nectar des trèfles.'),
('Asclépiade incarnate', 'Asclepias incarnata', 'pollinisateurs', 'Plante indigène', 'Plante mellifère vivace des prairies humides du Bas-Saint-Laurent. Fleurs roses regroupées en ombelles parfumées. Plante hôte essentielle du papillon monarque qui y dépose ses oeufs.', 'Sa sève blanche contient des cardénolides qui rendent les chenilles de monarque toxiques pour leurs prédateurs.'),
('Abeille charpentière', 'Xylocopa virginica', 'pollinisateurs', 'Résidence permanente', 'Grosse abeille solitaire au corps noir et brillant, sans rayures. Creuse ses galeries de nidification dans le bois mort, sans causer de dégâts structurels significatifs. Forte pollinisatrice des fleurs profondes.', 'Pratique parfois le vol-pollinisation : elle perce la base des fleurs trop profondes pour atteindre le nectar sans passer par les étamines.');
