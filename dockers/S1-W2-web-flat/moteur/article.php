<?php
/**
 * Affichage d'un article unique.
 * Lit le fichier .html correspondant dans fp-content/articles/, en extrait
 * les métadonnées et le corps, puis enrobe le tout du gabarit du site.
 */

$identifiantBrut = $_GET['identifiant'] ?? '';
$identifiantArticle = basename(preg_replace('/[^a-z0-9-]/i', '', $identifiantBrut));

if ($identifiantArticle === '') {
    http_response_code(400);
    echo 'Identifiant manquant.';
    exit;
}

$cheminArticle = __DIR__ . '/fp-content/articles/' . $identifiantArticle . '.html';
if (!file_exists($cheminArticle)) {
    http_response_code(404);
    echo 'Article introuvable.';
    exit;
}

$contenuFichier = file_get_contents($cheminArticle);

$titreArticle = 'Sans titre';
$dateArticle = '';
$ecosystemeArticle = '';

if (preg_match('/<!--\s*METADONNEES(.*?)-->/s', $contenuFichier, $blocCorrespondance)) {
    $blocMeta = $blocCorrespondance[1];
    if (preg_match('/TITRE\s*:\s*(.+)/', $blocMeta, $titreCorrespondance)) {
        $titreArticle = trim($titreCorrespondance[1]);
    }
    if (preg_match('/DATE\s*:\s*(.+)/', $blocMeta, $dateCorrespondance)) {
        $dateArticle = trim($dateCorrespondance[1]);
    }
    if (preg_match('/ECOSYSTEME\s*:\s*(.+)/', $blocMeta, $ecosystemeCorrespondance)) {
        $ecosystemeArticle = trim($ecosystemeCorrespondance[1]);
    }
}

$corpsArticle = preg_replace('/<!--\s*METADONNEES.*?-->/s', '', $contenuFichier);

function decrireEcosysteme(string $cle): array {
    $catalogue = [
        'marin' => ['nom' => 'Écosystème marin', 'couleur' => 'marin'],
        'forestier' => ['nom' => 'Écosystème forestier', 'couleur' => 'forestier'],
        'pollinisateurs' => ['nom' => 'Pollinisateurs et jardins', 'couleur' => 'pollinisateurs'],
        'oiseaux-migrateurs' => ['nom' => 'Oiseaux migrateurs', 'couleur' => 'migrateurs'],
    ];
    return $catalogue[$cle] ?? ['nom' => '', 'couleur' => 'general'];
}

$infosEcosysteme = decrireEcosysteme($ecosystemeArticle);
?>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title><?= htmlspecialchars($titreArticle) ?> - Zoo maritime</title>
<link rel="stylesheet" href="decoration/decoration-evenements.css">
</head>
<body>

<header id="article-entete" data-couleur="<?= $infosEcosysteme['couleur'] ?>">
  <a id="article-retour" href="index.php">&lt;- Retour aux événements</a>
  <?php if ($infosEcosysteme['nom'] !== ''): ?>
    <p id="article-ecosysteme"><?= htmlspecialchars($infosEcosysteme['nom']) ?></p>
  <?php endif; ?>
  <h1 id="article-titre"><?= htmlspecialchars($titreArticle) ?></h1>
  <?php if ($dateArticle !== ''): ?>
    <p id="article-date"><?= htmlspecialchars($dateArticle) ?></p>
  <?php endif; ?>
</header>

<main id="article-corps">
  <?= $corpsArticle ?>
</main>

<footer id="pied">
  <p>Mini-sites événementiels - <a href="index.php">Retour</a></p>
</footer>

</body>
</html>
