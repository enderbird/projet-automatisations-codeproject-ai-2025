<?php
/**
 * Fiche détaillée d'une espèce.
 */

require_once __DIR__ . '/AccesseurEspece.php';

$identifiantBrut = $_GET['identifiant'] ?? '';
$identifiantEspece = (int) $identifiantBrut;

if ($identifiantEspece <= 0) {
    http_response_code(400);
    echo 'Identifiant manquant ou invalide.';
    exit;
}

try {
    $accesseurEspece = new AccesseurEspece();
    $espece = $accesseurEspece->chercherParIdentifiant($identifiantEspece);
} catch (Throwable $erreurAttrapee) {
    http_response_code(500);
    echo 'Base de données inaccessible : ' . htmlspecialchars($erreurAttrapee->getMessage());
    exit;
}

if ($espece === null) {
    http_response_code(404);
    echo 'Espèce introuvable.';
    exit;
}

$infosEcosysteme = $accesseurEspece->decrireEcosysteme($espece['ecosysteme']);
?>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title><?= htmlspecialchars($espece['nom_commun']) ?> - Catalogue</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="decoration/decoration-catalogue.css">
</head>
<body>

<header id="fiche-entete" data-couleur="<?= $infosEcosysteme['couleur'] ?>">
  <a id="fiche-retour" href="index.php?ecosysteme=<?= urlencode($espece['ecosysteme']) ?>">&lt;- Retour au catalogue</a>
  <p id="fiche-ecosysteme"><?= htmlspecialchars($infosEcosysteme['nom']) ?></p>
  <h1 id="fiche-titre"><?= htmlspecialchars($espece['nom_commun']) ?></h1>
  <p id="fiche-latin"><?= htmlspecialchars($espece['nom_latin']) ?></p>
  <p id="fiche-statut"><?= htmlspecialchars($espece['statut_residence']) ?></p>
</header>

<main id="fiche-corps">

  <section class="fiche-section">
    <p class="fiche-section-titre">Description</p>
    <p><?= nl2br(htmlspecialchars($espece['description'])) ?></p>
  </section>

  <?php if (!empty($espece['fait_marquant'])): ?>
    <section class="fiche-section" data-theme="curiosite">
      <p class="fiche-section-titre">Le saviez-vous</p>
      <p><?= nl2br(htmlspecialchars($espece['fait_marquant'])) ?></p>
    </section>
  <?php endif; ?>

</main>

<footer id="pied">
  <p>Catalogue interactif - <a href="index.php">Retour</a></p>
</footer>

</body>
</html>
