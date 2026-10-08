/**
 * Borne medias - jeu 3D "Repere les belugas dans le Saint-Laurent".
 *
 * Le visiteur est sur le pont d'un bateau. Une dizaine de belugas nagent
 * autour de lui en surface. Il fait pivoter la camera avec la souris et
 * clique sur les belugas pour les "reperer" (compteur a l'ecran).
 *
 * three.js gere le rendu 3D ; un raycaster traduit la position du clic 2D
 * en intersection 3D pour detecter le beluga touche.
 */

import * as THREE from "three";

// Variables remplacees par Vite a la build (voir vite.config.js).
// Pas de risque qu'elles soient indefinies en runtime : Vite injecte
// les chaines litterales avant minification.
const BUILD_DATE = __BUILD_DATE__;
const NOM_ETUDIANT = __NOM_ETUDIANT__;
const MATRICULE = __MATRICULE__;

const NOMBRE_BELUGAS = 12;
const RAYON_ZONE_SPAWN = 60;

const COULEUR_CIEL = 0x9bcfe8;
const COULEUR_MER_HAUTE = 0x4ea7ce;
const COULEUR_MER_BASSE = 0x1f5a78;
const COULEUR_BELUGA = 0xf2efe7;
const COULEUR_BELUGA_REPERE = 0xfbcf3d;
const COULEUR_BATEAU = 0x6b4226;
const COULEUR_PONT = 0xd9b88a;

const elementCanevas = document.getElementById("canevas-jeu");
const elementBanniereIdentite = document.getElementById("banniere-identite");
const elementScoreTrouves = document.getElementById("score-trouves");
const elementScoreTotal = document.getElementById("score-total");
const elementMessageFinal = document.getElementById("message-final");
const actionRejouer = document.getElementById("action-rejouer");

elementBanniereIdentite.textContent =
  `${NOM_ETUDIANT} - ${MATRICULE} - build ${BUILD_DATE}`;
elementScoreTotal.textContent = String(NOMBRE_BELUGAS);

const scene = new THREE.Scene();
scene.background = new THREE.Color(COULEUR_CIEL);
scene.fog = new THREE.Fog(COULEUR_CIEL, 80, 180);

const camera = new THREE.PerspectiveCamera(
  60,
  window.innerWidth / window.innerHeight,
  0.1,
  500,
);
camera.position.set(0, 4.5, 0);
camera.lookAt(0, 2, -10);

const moteurRendu = new THREE.WebGLRenderer({
  canvas: elementCanevas,
  antialias: true,
});
moteurRendu.setPixelRatio(window.devicePixelRatio);
moteurRendu.setSize(window.innerWidth, window.innerHeight);

const lumiereAmbiante = new THREE.HemisphereLight(0xffffff, 0xb1cfd8, 0.85);
scene.add(lumiereAmbiante);

const lumiereSoleil = new THREE.DirectionalLight(0xfff2cc, 0.9);
lumiereSoleil.position.set(50, 80, 30);
scene.add(lumiereSoleil);

// -----------------------------------------------------------------------------
// Mer : plan subdivise dont on anime les sommets avec des sinusoides en Z.
// -----------------------------------------------------------------------------
const geometrieMer = new THREE.PlaneGeometry(400, 400, 80, 80);
geometrieMer.rotateX(-Math.PI / 2);
const materiauMer = new THREE.MeshStandardMaterial({
  color: COULEUR_MER_HAUTE,
  roughness: 0.85,
  metalness: 0.1,
});
const surfaceMer = new THREE.Mesh(geometrieMer, materiauMer);
surfaceMer.position.y = 0;
scene.add(surfaceMer);

const positionsMer = geometrieMer.attributes.position;
const positionsMerOrigine = positionsMer.array.slice();

function animerVagues(temps) {
  for (let indexSommet = 0; indexSommet < positionsMer.count; indexSommet += 1) {
    const indexX = indexSommet * 3;
    const indexY = indexSommet * 3 + 1;
    const indexZ = indexSommet * 3 + 2;
    const xOrigine = positionsMerOrigine[indexX];
    const zOrigine = positionsMerOrigine[indexZ];
    const onde =
      Math.sin(xOrigine * 0.1 + temps * 1.4) * 0.35 +
      Math.cos(zOrigine * 0.13 + temps * 1.1) * 0.3;
    positionsMer.array[indexY] = onde;
  }
  positionsMer.needsUpdate = true;
  geometrieMer.computeVertexNormals();
}

// -----------------------------------------------------------------------------
// Bateau : un demi-pont visible devant la camera pour ancrer le visiteur.
// -----------------------------------------------------------------------------
function fabriquerBateau() {
  const groupeBateau = new THREE.Group();

  const coque = new THREE.Mesh(
    new THREE.CylinderGeometry(2.6, 2.0, 5, 18, 1, false, 0, Math.PI),
    new THREE.MeshStandardMaterial({ color: COULEUR_BATEAU, roughness: 0.7 }),
  );
  coque.rotation.z = Math.PI / 2;
  coque.position.set(0, 1.2, -2.0);
  groupeBateau.add(coque);

  const pont = new THREE.Mesh(
    new THREE.BoxGeometry(5, 0.25, 4.5),
    new THREE.MeshStandardMaterial({ color: COULEUR_PONT, roughness: 0.8 }),
  );
  pont.position.set(0, 2.4, -2.0);
  groupeBateau.add(pont);

  const balustrade = new THREE.Mesh(
    new THREE.TorusGeometry(2.3, 0.07, 8, 32, Math.PI),
    new THREE.MeshStandardMaterial({ color: 0xffffff }),
  );
  balustrade.rotation.x = Math.PI / 2;
  balustrade.position.set(0, 3.0, -2.0);
  groupeBateau.add(balustrade);

  return groupeBateau;
}

scene.add(fabriquerBateau());

// -----------------------------------------------------------------------------
// Belugas : capsules blanches qui flottent et plongent. Chaque beluga porte
// un index, une phase et un decalage de profondeur pour eviter la synchronie.
// -----------------------------------------------------------------------------
const groupeBelugas = new THREE.Group();
scene.add(groupeBelugas);

const geometrieBeluga = new THREE.CapsuleGeometry(0.9, 2.4, 6, 14);
geometrieBeluga.rotateZ(Math.PI / 2);

function fabriquerBeluga(positionX, positionZ, phase) {
  const materiau = new THREE.MeshStandardMaterial({
    color: COULEUR_BELUGA,
    roughness: 0.6,
    metalness: 0.05,
  });
  const corps = new THREE.Mesh(geometrieBeluga, materiau);
  corps.position.set(positionX, 0.6, positionZ);
  corps.userData.estBeluga = true;
  corps.userData.estRepere = false;
  corps.userData.phaseBobbing = phase;
  corps.userData.phaseRotation = phase * 1.3;
  corps.userData.amplitudeBobbing = 0.4 + Math.random() * 0.3;
  corps.userData.materiau = materiau;
  return corps;
}

function semerBelugas() {
  while (groupeBelugas.children.length > 0) {
    const enfant = groupeBelugas.children[0];
    groupeBelugas.remove(enfant);
    enfant.geometry?.dispose?.();
    enfant.userData.materiau?.dispose?.();
  }
  for (let indexBeluga = 0; indexBeluga < NOMBRE_BELUGAS; indexBeluga += 1) {
    const angle = Math.random() * Math.PI * 2;
    const distance = 12 + Math.random() * (RAYON_ZONE_SPAWN - 12);
    const positionX = Math.cos(angle) * distance;
    const positionZ = Math.sin(angle) * distance;
    const phase = Math.random() * Math.PI * 2;
    groupeBelugas.add(fabriquerBeluga(positionX, positionZ, phase));
  }
}

function animerBelugas(temps) {
  for (const unBeluga of groupeBelugas.children) {
    const phaseBobbing = unBeluga.userData.phaseBobbing;
    const amplitude = unBeluga.userData.amplitudeBobbing;
    unBeluga.position.y =
      0.5 + Math.sin(temps * 1.5 + phaseBobbing) * amplitude;
    unBeluga.rotation.x = Math.sin(temps * 1.2 + phaseBobbing) * 0.18;
    if (!unBeluga.userData.estRepere) {
      unBeluga.rotation.y =
        unBeluga.userData.phaseRotation + Math.sin(temps * 0.4) * 0.4;
    }
  }
}

// -----------------------------------------------------------------------------
// Score
// -----------------------------------------------------------------------------
let nombreReperes = 0;

function reinitialiserPartie() {
  nombreReperes = 0;
  elementScoreTrouves.textContent = "0";
  elementMessageFinal.classList.remove("message-final-actif");
  semerBelugas();
}

function reperer(unBeluga) {
  if (unBeluga.userData.estRepere) {
    return;
  }
  unBeluga.userData.estRepere = true;
  unBeluga.userData.materiau.color.setHex(COULEUR_BELUGA_REPERE);
  unBeluga.userData.materiau.emissive = new THREE.Color(0xffe082);
  unBeluga.userData.materiau.emissiveIntensity = 0.4;
  nombreReperes += 1;
  elementScoreTrouves.textContent = String(nombreReperes);
  if (nombreReperes >= NOMBRE_BELUGAS) {
    elementMessageFinal.classList.add("message-final-actif");
  }
}

actionRejouer.addEventListener("click", reinitialiserPartie);

// -----------------------------------------------------------------------------
// Controle camera : drag pour pivoter (yaw + pitch limite).
// -----------------------------------------------------------------------------
let yawCamera = 0;
let pitchCamera = -0.05;
let estEnTrainDeGlisser = false;
let positionXSourisDernier = 0;
let positionYSourisDernier = 0;
const PITCH_MAX = 0.6;
const PITCH_MIN = -0.4;

function appliquerOrientationCamera() {
  const distance = 1;
  const cibleX = Math.sin(yawCamera) * Math.cos(pitchCamera) * distance;
  const cibleZ = -Math.cos(yawCamera) * Math.cos(pitchCamera) * distance;
  const cibleY = camera.position.y + Math.sin(pitchCamera) * distance;
  camera.lookAt(camera.position.x + cibleX, cibleY, camera.position.z + cibleZ);
}

elementCanevas.addEventListener("mousedown", (evenement) => {
  estEnTrainDeGlisser = true;
  positionXSourisDernier = evenement.clientX;
  positionYSourisDernier = evenement.clientY;
});

window.addEventListener("mouseup", () => {
  estEnTrainDeGlisser = false;
});

window.addEventListener("mousemove", (evenement) => {
  if (!estEnTrainDeGlisser) {
    return;
  }
  const deltaX = evenement.clientX - positionXSourisDernier;
  const deltaY = evenement.clientY - positionYSourisDernier;
  positionXSourisDernier = evenement.clientX;
  positionYSourisDernier = evenement.clientY;
  yawCamera -= deltaX * 0.005;
  pitchCamera -= deltaY * 0.003;
  if (pitchCamera > PITCH_MAX) pitchCamera = PITCH_MAX;
  if (pitchCamera < PITCH_MIN) pitchCamera = PITCH_MIN;
});

elementCanevas.addEventListener("touchstart", (evenement) => {
  if (evenement.touches.length !== 1) return;
  estEnTrainDeGlisser = true;
  positionXSourisDernier = evenement.touches[0].clientX;
  positionYSourisDernier = evenement.touches[0].clientY;
});
elementCanevas.addEventListener("touchend", () => {
  estEnTrainDeGlisser = false;
});
elementCanevas.addEventListener("touchmove", (evenement) => {
  if (!estEnTrainDeGlisser || evenement.touches.length !== 1) return;
  const deltaX = evenement.touches[0].clientX - positionXSourisDernier;
  const deltaY = evenement.touches[0].clientY - positionYSourisDernier;
  positionXSourisDernier = evenement.touches[0].clientX;
  positionYSourisDernier = evenement.touches[0].clientY;
  yawCamera -= deltaX * 0.005;
  pitchCamera -= deltaY * 0.003;
  if (pitchCamera > PITCH_MAX) pitchCamera = PITCH_MAX;
  if (pitchCamera < PITCH_MIN) pitchCamera = PITCH_MIN;
});

// -----------------------------------------------------------------------------
// Detection de clic sur un beluga via raycaster.
// -----------------------------------------------------------------------------
const raycaster = new THREE.Raycaster();
const positionSourisNormalisee = new THREE.Vector2();

function gererClicSurCanevas(evenement) {
  const rectangleCanevas = elementCanevas.getBoundingClientRect();
  positionSourisNormalisee.x =
    ((evenement.clientX - rectangleCanevas.left) / rectangleCanevas.width) * 2 - 1;
  positionSourisNormalisee.y =
    -((evenement.clientY - rectangleCanevas.top) / rectangleCanevas.height) * 2 + 1;
  raycaster.setFromCamera(positionSourisNormalisee, camera);
  const intersections = raycaster.intersectObjects(groupeBelugas.children, false);
  if (intersections.length > 0) {
    reperer(intersections[0].object);
  }
}

// On fait la difference entre clic et drag : si la souris s'est deplacee de
// moins de 5 pixels entre mousedown et mouseup, on considere que c'est un clic.
let positionXClicDebut = 0;
let positionYClicDebut = 0;
elementCanevas.addEventListener("mousedown", (evenement) => {
  positionXClicDebut = evenement.clientX;
  positionYClicDebut = evenement.clientY;
});
elementCanevas.addEventListener("mouseup", (evenement) => {
  const deltaX = Math.abs(evenement.clientX - positionXClicDebut);
  const deltaY = Math.abs(evenement.clientY - positionYClicDebut);
  if (deltaX < 5 && deltaY < 5) {
    gererClicSurCanevas(evenement);
  }
});

// -----------------------------------------------------------------------------
// Adaptation au redimensionnement.
// -----------------------------------------------------------------------------
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  moteurRendu.setSize(window.innerWidth, window.innerHeight);
});

// -----------------------------------------------------------------------------
// Boucle d'animation.
// -----------------------------------------------------------------------------
const horloge = new THREE.Clock();

function boucleAnimation() {
  const tempsEcoule = horloge.getElapsedTime();
  animerVagues(tempsEcoule);
  animerBelugas(tempsEcoule);
  appliquerOrientationCamera();
  moteurRendu.render(scene, camera);
  requestAnimationFrame(boucleAnimation);
}

semerBelugas();
boucleAnimation();
