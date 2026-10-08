<?php
/**
 * Page d'accueil du mini-CMS flat-file.
 * Liste tous les articles trouvés dans /var/www/html/fp-content/articles/.
 */

$dossierArticles = __DIR__ . '/fp-content/articles';
$fichiersArticles = is_dir($dossierArticles) ? glob($dossierArticles . '/*.html') : [];

function lireMetadonnees(string $cheminFichier): array {
    $contenuFichier = file_get_contents($cheminFichier);
    $metadonnees = [
        'titre' => 'Sans titre',
        'date' => '',
        'ecosysteme' => '',
    ];
    if (preg_match('/<!--\s*METADONNEES(.*?)-->/s', $contenuFichier, $blocCorrespondance)) {
        $blocMeta = $blocCorrespondance[1];
        if (preg_match('/TITRE\s*:\s*(.+)/', $blocMeta, $titreCorrespondance)) {
            $metadonnees['titre'] = trim($titreCorrespondance[1]);
        }
        if (preg_match('/DATE\s*:\s*(.+)/', $blocMeta, $dateCorrespondance)) {
            $metadonnees['date'] = trim($dateCorrespondance[1]);
        }
        if (preg_match('/ECOSYSTEME\s*:\s*(.+)/', $blocMeta, $ecosystemeCorrespondance)) {
            $metadonnees['ecosysteme'] = trim($ecosystemeCorrespondance[1]);
        }
    }
    return $metadonnees;
}

function decrireEcosysteme(string $cle): array {
    $catalogue = [
        'marin' => ['nom' => 'Écosystème marin', 'couleur' => 'marin'],
        'forestier' => ['nom' => 'Écosystème forestier', 'couleur' => 'forestier'],
        'pollinisateurs' => ['nom' => 'Pollinisateurs et jardins', 'couleur' => 'pollinisateurs'],
        'oiseaux-migrateurs' => ['nom' => 'Oiseaux migrateurs', 'couleur' => 'migrateurs'],
    ];
    return $catalogue[$cle] ?? ['nom' => 'Toutes les sections', 'couleur' => 'general'];
}

$articles = [];
foreach ($fichiersArticles as $cheminFichier) {
    $identifiantArticle = basename($cheminFichier, '.html');
    $metadonneesArticle = lireMetadonnees($cheminFichier);
    $articles[] = [
        'identifiant' => $identifiantArticle,
        'titre' => $metadonneesArticle['titre'],
        'date' => $metadonneesArticle['date'],
        'ecosysteme' => $metadonneesArticle['ecosysteme'],
    ];
}

usort($articles, fn($premier, $second) => strcmp($second['date'], $premier['date']));
?>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mini-sites événementiels - Zoo maritime</title>
<link rel="stylesheet" href="decoration/decoration-evenements.css">
</head>
<body>

<header id="entete">
  <span id="entete-tag">Sites événementiels</span>
  <h1 id="entete-titre">Les rendez-vous du zoo</h1>
  <p id="entete-sous-titre">Festivals, journées thématiques, nuits des musées : retrouvez tous les événements du Zoo maritime du Bas-Saint-Laurent.</p>
</header>

<main id="contenu">

  <section id="articles-section">
    <p class="section-titre">À l'affiche</p>
    <h2 class="section-grand-titre"><?= count($articles) ?> événement<?= count($articles) > 1 ? 's' : '' ?> publié<?= count($articles) > 1 ? 's' : '' ?></h2>

    <?php if (empty($articles)): ?>
      <div id="message-vide">
        <p>Aucun article publié pour le moment.</p>
        <p class="message-vide-aide">Le studio créatif local peut déposer ses livraisons HTML dans le dossier <code>fp-content/articles/</code>. Le moteur les détectera automatiquement.</p>
      </div>
    <?php else: ?>
      <div id="articles-grille">
        <?php foreach ($articles as $articleEnCours):
          $infosEcosysteme = decrireEcosysteme($articleEnCours['ecosysteme']);
        ?>
          <a class="article-vignette" data-couleur="<?= $infosEcosysteme['couleur'] ?>" href="article.php?identifiant=<?= htmlspecialchars($articleEnCours['identifiant']) ?>">
            <p class="article-vignette-ecosysteme"><?= htmlspecialchars($infosEcosysteme['nom']) ?></p>
            <h3 class="article-vignette-titre"><?= htmlspecialchars($articleEnCours['titre']) ?></h3>
            <p class="article-vignette-date"><?= htmlspecialchars($articleEnCours['date']) ?></p>
          </a>
        <?php endforeach; ?>
      </div>
    <?php endif; ?>
  </section>

  <section id="explication">
    <p class="section-titre">Pour les rédacteurs et le studio créatif</p>
    <p>Pour publier un nouvel événement, déposez un fichier <code>.html</code> dans <code>fp-content/articles/</code>. Le fichier doit commencer par un bloc de métadonnées comme suit, suivi du contenu HTML libre.</p>
    <pre><code>&lt;!-- METADONNEES
TITRE: Mon nouvel événement
DATE: 2026-08-15
ECOSYSTEME: marin
--&gt;
&lt;p&gt;Le contenu de l'article ici...&lt;/p&gt;</code></pre>
    <p>Aucun rebuild Docker n'est nécessaire : le contenu vit dans un volume monté au démarrage. Mettre à jour un article = sauvegarder le fichier, recharger la page.</p>
  </section>

</main>

<footer id="pied">
  <p>Mini-sites événementiels - <a href="../index.html">Zoo maritime du Bas-Saint-Laurent</a></p>
</footer>

</body>
</html>
