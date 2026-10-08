<?php
/**
 * Page d'accueil du catalogue : liste des espèces filtrable par écosystème,
 * avec recherche par nom (commun ou latin).
 *
 * Couvre les 3 écosystèmes "non-aviaires" du zoo : marin, forestier,
 * pollinisateurs. Le pavillon des oiseaux migrateurs a sa propre encyclopédie
 * (livrable 1, demande 1).
 */

require_once __DIR__ . '/AccesseurEspece.php';

$ecosystemeFiltre = $_GET['ecosysteme'] ?? '';
$termeRecherche = trim($_GET['recherche'] ?? '');

try {
    $accesseurEspece = new AccesseurEspece();
    if (!$accesseurEspece->ecosystemeEstValide($ecosystemeFiltre)) {
        $ecosystemeFiltre = '';
    }
    $especes = $accesseurEspece->chercherListe($ecosystemeFiltre, $termeRecherche);
    $erreurChargement = null;
} catch (Throwable $erreurAttrapee) {
    $accesseurEspece = null;
    $especes = [];
    $erreurChargement = $erreurAttrapee->getMessage();
}

$nombreEspeces = count($especes);
?>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Catalogue des espèces - Zoo maritime</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="decoration/decoration-catalogue.css">
</head>
<body>

<header id="entete">
  <span id="entete-tag">Catalogue interactif</span>
  <h1 id="entete-titre">Le catalogue <span>vivant</span> du zoo</h1>
  <p id="entete-sous-titre">Douze espèces emblématiques des écosystèmes marin, forestier et pollinisateurs du Bas-Saint-Laurent. Filtrez, cherchez, explorez.</p>
</header>

<main id="contenu">

  <?php if ($erreurChargement !== null): ?>
    <section id="erreur">
      <p class="erreur-titre">La base de données ne répond pas</p>
      <p class="erreur-detail"><?= htmlspecialchars($erreurChargement) ?></p>
      <p class="erreur-aide">Si c'est le tout premier démarrage, attendez quelques secondes et rechargez la page : MariaDB peut prendre 5 à 10 secondes pour s'initialiser au premier lancement.</p>
    </section>
  <?php else: ?>

    <form id="recherche-formulaire" method="get" action="">
      <?php if ($ecosystemeFiltre !== ''): ?>
        <input type="hidden" name="ecosysteme" value="<?= htmlspecialchars($ecosystemeFiltre) ?>">
      <?php endif; ?>
      <div id="barre-recherche">
        <input id="champs-recherche" type="search" name="recherche" placeholder="Chercher par nom commun ou nom latin..." value="<?= htmlspecialchars($termeRecherche) ?>" autocomplete="off">
      </div>
    </form>

    <section id="filtres">
      <p class="section-titre">Filtrer par écosystème</p>
      <nav id="filtres-actions">
        <a class="filtre-action" href="?<?= $termeRecherche !== '' ? 'recherche=' . urlencode($termeRecherche) : '' ?>" <?= $ecosystemeFiltre === '' ? 'data-actif="oui"' : '' ?>>Tous écosystèmes</a>
        <a class="filtre-action" data-couleur="marin" href="?ecosysteme=marin<?= $termeRecherche !== '' ? '&recherche=' . urlencode($termeRecherche) : '' ?>" <?= $ecosystemeFiltre === 'marin' ? 'data-actif="oui"' : '' ?>>Marin</a>
        <a class="filtre-action" data-couleur="forestier" href="?ecosysteme=forestier<?= $termeRecherche !== '' ? '&recherche=' . urlencode($termeRecherche) : '' ?>" <?= $ecosystemeFiltre === 'forestier' ? 'data-actif="oui"' : '' ?>>Forestier</a>
        <a class="filtre-action" data-couleur="pollinisateurs" href="?ecosysteme=pollinisateurs<?= $termeRecherche !== '' ? '&recherche=' . urlencode($termeRecherche) : '' ?>" <?= $ecosystemeFiltre === 'pollinisateurs' ? 'data-actif="oui"' : '' ?>>Pollinisateurs</a>
      </nav>
    </section>

    <section id="especes-section">
      <h2 class="section-grand-titre"><?= $nombreEspeces ?> espèce<?= $nombreEspeces > 1 ? 's' : '' ?> trouvée<?= $nombreEspeces > 1 ? 's' : '' ?></h2>

      <?php if (empty($especes)): ?>
        <div id="message-vide">
          <p>Aucune espèce ne correspond à ces critères.</p>
        </div>
      <?php else: ?>
        <div id="especes-grille">
          <?php foreach ($especes as $espece):
            $infosEcosysteme = $accesseurEspece->decrireEcosysteme($espece['ecosysteme']);
          ?>
            <a class="espece-vignette" data-couleur="<?= $infosEcosysteme['couleur'] ?>" href="fiche.php?identifiant=<?= (int) $espece['identifiant'] ?>">
              <p class="espece-vignette-ecosysteme"><?= htmlspecialchars($infosEcosysteme['nom']) ?></p>
              <h3 class="espece-vignette-nom"><?= htmlspecialchars($espece['nom_commun']) ?></h3>
              <p class="espece-vignette-latin"><?= htmlspecialchars($espece['nom_latin']) ?></p>
              <p class="espece-vignette-statut"><?= htmlspecialchars($espece['statut_residence']) ?></p>
            </a>
          <?php endforeach; ?>
        </div>
      <?php endif; ?>
    </section>

  <?php endif; ?>

</main>

<footer id="pied">
  <p>Catalogue interactif - <a href="index.php">Zoo maritime du Bas-Saint-Laurent</a></p>
</footer>

<script>
  // Soumission automatique de la recherche après une courte pause de frappe.
  const champsRecherche = document.getElementById('champs-recherche');
  const formulaireRecherche = document.getElementById('recherche-formulaire');
  let minuterieRecherche = null;

  if (champsRecherche && formulaireRecherche) {
    champsRecherche.addEventListener('input', function() {
      clearTimeout(minuterieRecherche);
      minuterieRecherche = setTimeout(function() {
        formulaireRecherche.submit();
      }, 350);
    });
  }
</script>

</body>
</html>
