<?php
/**
 * Accesseur de données pour la table espece.
 * Centralise la connexion à MariaDB et les requêtes utilisées par les pages.
 *
 * Conventions : nom de classe en PascalCase, méthodes commencent par une
 * minuscule, variables en mixedCase, aucune abréviation.
 */

class AccesseurEspece
{
    private PDO $connexion;

    private const ECOSYSTEMES_VALIDES = ['marin', 'forestier', 'pollinisateurs'];

    private const CATALOGUE_ECOSYSTEMES = [
        'marin' => ['nom' => 'Écosystème marin', 'couleur' => 'marin'],
        'forestier' => ['nom' => 'Écosystème forestier', 'couleur' => 'forestier'],
        'pollinisateurs' => ['nom' => 'Pollinisateurs et jardins', 'couleur' => 'pollinisateurs'],
    ];

    public function __construct()
    {
        // 127.0.0.1 force une connexion TCP. Avec 'localhost', PDO essaie le
        // socket Unix dont le chemin par défaut peut différer du socket réel
        // de MariaDB (cause classique de "No such file or directory").
        $hote = '127.0.0.1';
        $nomBase = 'catalogue_especes';
        $utilisateur = 'catalogue_app';
        $motDePasse = 'pavillon-bsl';

        $chaineConnexion = "mysql:host={$hote};dbname={$nomBase};charset=utf8mb4";
        $optionsConnexion = [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        ];

        $this->connexion = new PDO(
            $chaineConnexion,
            $utilisateur,
            $motDePasse,
            $optionsConnexion
        );
    }

    /**
     * Liste les espèces, filtrées par écosystème et/ou par terme de recherche.
     * Un filtre vide est ignoré.
     */
    public function chercherListe(string $ecosystemeFiltre, string $termeRecherche): array
    {
        $clauses = [];
        $parametres = [];

        if (in_array($ecosystemeFiltre, self::ECOSYSTEMES_VALIDES, true)) {
            $clauses[] = 'ecosysteme = :ecosysteme';
            $parametres[':ecosysteme'] = $ecosystemeFiltre;
        }
        if ($termeRecherche !== '') {
            // Deux placeholders distincts car PDO en mode prépare natif
            // (EMULATE_PREPARES = false) refuse de réutiliser un paramètre
            // nommé dans la même requête. Erreur SQLSTATE[HY093] sinon.
            $clauses[] = '(nom_commun LIKE :rechercheNomCommun OR nom_latin LIKE :rechercheNomLatin)';
            $motifRecherche = '%' . $termeRecherche . '%';
            $parametres[':rechercheNomCommun'] = $motifRecherche;
            $parametres[':rechercheNomLatin'] = $motifRecherche;
        }

        $sql = 'SELECT * FROM espece';
        if (!empty($clauses)) {
            $sql .= ' WHERE ' . implode(' AND ', $clauses);
        }
        $sql .= ' ORDER BY ecosysteme, nom_commun';

        $requete = $this->connexion->prepare($sql);
        $requete->execute($parametres);
        return $requete->fetchAll();
    }

    /**
     * Cherche une espèce par son identifiant. Retourne null si introuvable.
     */
    public function chercherParIdentifiant(int $identifiantEspece): ?array
    {
        $requete = $this->connexion->prepare(
            'SELECT * FROM espece WHERE identifiant = :identifiant'
        );
        $requete->execute([':identifiant' => $identifiantEspece]);
        $resultat = $requete->fetch();
        return $resultat !== false ? $resultat : null;
    }

    /**
     * Donne le nom affichable et la clé de couleur d'un écosystème.
     */
    public function decrireEcosysteme(string $cleEcosysteme): array
    {
        return self::CATALOGUE_ECOSYSTEMES[$cleEcosysteme]
            ?? ['nom' => $cleEcosysteme, 'couleur' => 'general'];
    }

    /**
     * Vérifie qu'un écosystème fait partie des valeurs reconnues.
     */
    public function ecosystemeEstValide(string $cleEcosysteme): bool
    {
        return in_array($cleEcosysteme, self::ECOSYSTEMES_VALIDES, true);
    }
}
