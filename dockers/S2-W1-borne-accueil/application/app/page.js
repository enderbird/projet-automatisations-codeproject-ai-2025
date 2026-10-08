"use client";

import { useEffect, useMemo, useState } from "react";

const pavillons = [
  {
    cle: "foret",
    titre: "FORET",
    sousTitre: "Foret boreale quebecoise",
    description:
      "Orignaux, ours, lievres, oiseaux forestiers et champignons. Sentiers ombrages a l'interieur du pavillon.",
    couleur: "#82a04c",
  },
  {
    cle: "marin",
    titre: "MARIN",
    sousTitre: "Faune du Saint-Laurent",
    description:
      "Belugas, phoques, poissons et oiseaux marins. Bassins ouverts et fenetres sous-marines.",
    couleur: "#3d96bd",
  },
  {
    cle: "prairie",
    titre: "PRAIRIE",
    sousTitre: "Pollinisateurs et jardins",
    description:
      "Abeilles, papillons, fleurs sauvages, plantes medicinales et savoirs traditionnels.",
    couleur: "#bd953a",
  },
  {
    cle: "voyageurs",
    titre: "VOYAGEURS",
    sousTitre: "Oiseaux migrateurs",
    description:
      "Voliere et observatoire des especes locales et exotiques en escale sur le Saint-Laurent.",
    couleur: "#97633a",
  },
];

const arbres = [
  { x: 130, y: 130 },
  { x: 220, y: 105 },
  { x: 310, y: 95 },
  { x: 400, y: 110 },
  { x: 480, y: 130 },
  { x: 110, y: 220 },
  { x: 180, y: 250 },
  { x: 285, y: 235 },
  { x: 405, y: 250 },
  { x: 130, y: 320 },
  { x: 215, y: 350 },
  { x: 310, y: 360 },
  { x: 410, y: 355 },
  { x: 270, y: 460 },
  { x: 350, y: 465 },
];

const vagues = [
  { x: 700, y: 130 },
  { x: 820, y: 130 },
  { x: 880, y: 240 },
  { x: 920, y: 350 },
];

const herbes = [
  { x: 130, y: 615 },
  { x: 200, y: 615 },
  { x: 270, y: 615 },
  { x: 340, y: 615 },
  { x: 410, y: 615 },
  { x: 700, y: 415 },
  { x: 770, y: 430 },
  { x: 820, y: 460 },
  { x: 870, y: 480 },
  { x: 920, y: 470 },
  { x: 720, y: 555 },
  { x: 800, y: 575 },
  { x: 870, y: 565 },
  { x: 920, y: 590 },
  { x: 540, y: 605 },
  { x: 600, y: 615 },
  { x: 670, y: 615 },
];

const fleurs = [
  { x: 100, y: 555, couleur: "#e8528c" },
  { x: 165, y: 540, couleur: "#fbcf3d" },
  { x: 240, y: 555, couleur: "#a96bd4" },
  { x: 300, y: 540, couleur: "#fbcf3d" },
  { x: 370, y: 555, couleur: "#e8528c" },
  { x: 430, y: 540, couleur: "#a96bd4" },
  { x: 80, y: 590, couleur: "#fbcf3d" },
  { x: 220, y: 590, couleur: "#e8528c" },
  { x: 360, y: 590, couleur: "#a96bd4" },
];

const abeilles = [
  { x: 195, y: 510 },
  { x: 320, y: 505 },
  { x: 130, y: 580 },
  { x: 405, y: 580 },
  { x: 270, y: 525 },
];

const oiseaux = [
  { x: 600, y: 180 },
  { x: 540, y: 250 },
  { x: 540, y: 320 },
  { x: 690, y: 440 },
  { x: 760, y: 470 },
  { x: 830, y: 440 },
  { x: 900, y: 470 },
  { x: 615, y: 530 },
  { x: 875, y: 605 },
  { x: 770, y: 615 },
];

function dessinerArbre(positionX, positionY, indexArbre) {
  return (
    <g key={`arbre-${indexArbre}`} className="decor-arbre">
      <rect
        x={positionX - 4}
        y={positionY + 18}
        width="8"
        height="22"
        fill="#5a3819"
        rx="1"
      />
      <ellipse cx={positionX} cy={positionY + 4} rx="22" ry="26" fill="#2a4d1f" />
    </g>
  );
}

function dessinerVague(positionX, positionY, indexVague) {
  return (
    <g key={`vague-${indexVague}`} className="decor-vague">
      <path
        d={`M ${positionX} ${positionY} q 14 -10 28 0 t 28 0`}
        fill="none"
        stroke="#ffffff"
        strokeWidth="4"
        strokeLinecap="round"
      />
      <path
        d={`M ${positionX + 4} ${positionY + 12} q 14 -10 28 0 t 28 0`}
        fill="none"
        stroke="#ffffff"
        strokeWidth="4"
        strokeLinecap="round"
      />
    </g>
  );
}

function dessinerHerbe(positionX, positionY, indexHerbe) {
  return (
    <g key={`herbe-${indexHerbe}`} className="decor-herbe">
      <line
        x1={positionX}
        y1={positionY + 14}
        x2={positionX - 8}
        y2={positionY}
        stroke="#f3e6c8"
        strokeWidth="3"
        strokeLinecap="round"
      />
      <line
        x1={positionX}
        y1={positionY + 14}
        x2={positionX + 8}
        y2={positionY}
        stroke="#f3e6c8"
        strokeWidth="3"
        strokeLinecap="round"
      />
      <line
        x1={positionX}
        y1={positionY + 14}
        x2={positionX}
        y2={positionY - 4}
        stroke="#f3e6c8"
        strokeWidth="3"
        strokeLinecap="round"
      />
    </g>
  );
}

function dessinerFleur(positionX, positionY, couleur, indexFleur) {
  return (
    <g key={`fleur-${indexFleur}`} className="decor-fleur">
      <circle cx={positionX} cy={positionY - 4} r="3" fill={couleur} />
      <circle cx={positionX - 4} cy={positionY - 1} r="3" fill={couleur} />
      <circle cx={positionX + 4} cy={positionY - 1} r="3" fill={couleur} />
      <circle cx={positionX - 2.5} cy={positionY + 3} r="3" fill={couleur} />
      <circle cx={positionX + 2.5} cy={positionY + 3} r="3" fill={couleur} />
      <circle cx={positionX} cy={positionY} r="2" fill="#fff4ad" />
      <line
        x1={positionX}
        y1={positionY + 5}
        x2={positionX}
        y2={positionY + 12}
        stroke="#3f7a2b"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
    </g>
  );
}

function dessinerAbeille(positionX, positionY, indexAbeille) {
  return (
    <g key={`abeille-${indexAbeille}`} className="decor-abeille">
      <ellipse cx={positionX - 2} cy={positionY - 3} rx="3.5" ry="2" fill="#ffffff" opacity="0.9" />
      <ellipse cx={positionX + 2} cy={positionY - 3} rx="3.5" ry="2" fill="#ffffff" opacity="0.9" />
      <ellipse cx={positionX} cy={positionY} rx="5" ry="3.5" fill="#fbcf3d" />
      <line
        x1={positionX - 2}
        y1={positionY - 3}
        x2={positionX - 2}
        y2={positionY + 3}
        stroke="#000000"
        strokeWidth="1"
      />
      <line
        x1={positionX + 1.5}
        y1={positionY - 3}
        x2={positionX + 1.5}
        y2={positionY + 3}
        stroke="#000000"
        strokeWidth="1"
      />
    </g>
  );
}

function dessinerOiseau(positionX, positionY, indexOiseau) {
  return (
    <path
      key={`oiseau-${indexOiseau}`}
      className="decor-oiseau"
      d={`M ${positionX - 9} ${positionY + 4} q 4.5 -6 9 0 q 4.5 -6 9 0`}
      fill="none"
      stroke="#2a2a2a"
      strokeWidth="2"
      strokeLinecap="round"
    />
  );
}

function genererCheminAvecCoinsRonds(waypoints, rayonCoin = 28) {
  if (!waypoints || waypoints.length < 2) {
    return "";
  }
  if (waypoints.length === 2) {
    return `M ${waypoints[0].x} ${waypoints[0].y} L ${waypoints[1].x} ${waypoints[1].y}`;
  }

  let chaineChemin = `M ${waypoints[0].x} ${waypoints[0].y}`;

  for (let position = 1; position < waypoints.length - 1; position += 1) {
    const pointPrecedent = waypoints[position - 1];
    const pointActuel = waypoints[position];
    const pointSuivant = waypoints[position + 1];

    const deltaXEntrant = pointActuel.x - pointPrecedent.x;
    const deltaYEntrant = pointActuel.y - pointPrecedent.y;
    const deltaXSortant = pointSuivant.x - pointActuel.x;
    const deltaYSortant = pointSuivant.y - pointActuel.y;

    const longueurEntrante = Math.hypot(deltaXEntrant, deltaYEntrant);
    const longueurSortante = Math.hypot(deltaXSortant, deltaYSortant);

    const rayonEntrant = Math.min(rayonCoin, longueurEntrante / 2);
    const rayonSortant = Math.min(rayonCoin, longueurSortante / 2);

    const pointApproche = {
      x: pointActuel.x - (deltaXEntrant / longueurEntrante) * rayonEntrant,
      y: pointActuel.y - (deltaYEntrant / longueurEntrante) * rayonEntrant,
    };
    const pointDepart = {
      x: pointActuel.x + (deltaXSortant / longueurSortante) * rayonSortant,
      y: pointActuel.y + (deltaYSortant / longueurSortante) * rayonSortant,
    };

    chaineChemin += ` L ${pointApproche.x.toFixed(2)} ${pointApproche.y.toFixed(2)}`;
    chaineChemin += ` Q ${pointActuel.x} ${pointActuel.y} ${pointDepart.x.toFixed(2)} ${pointDepart.y.toFixed(2)}`;
  }

  const dernierPoint = waypoints[waypoints.length - 1];
  chaineChemin += ` L ${dernierPoint.x} ${dernierPoint.y}`;

  return chaineChemin;
}

const horairesDuJour = [
  { heure: "09:30", titre: "Ouverture du parc", pavillonCle: null, pavillon: null },
  {
    heure: "10:00",
    titre: "Nourrissage des belugas",
    pavillonCle: "marin",
    pavillon: "Pavillon marin",
  },
  {
    heure: "10:30",
    titre: "Promenade contee : la riviere qui chante",
    pavillonCle: "foret",
    pavillon: "Pavillon foret",
  },
  {
    heure: "11:00",
    titre: "Demonstration de plongee sous-marine",
    pavillonCle: "marin",
    pavillon: "Pavillon marin",
  },
  {
    heure: "12:30",
    titre: "Visite guidee : corridor de migration",
    pavillonCle: "voyageurs",
    pavillon: "Pavillon voyageurs",
  },
  {
    heure: "13:00",
    titre: "Atelier pollinisation pour enfants",
    pavillonCle: "prairie",
    pavillon: "Pavillon prairie",
  },
  {
    heure: "14:00",
    titre: "Lecture jeunesse sur la foret boreale",
    pavillonCle: "foret",
    pavillon: "Pavillon foret",
  },
  {
    heure: "14:30",
    titre: "Rencontre des biologistes",
    pavillonCle: "voyageurs",
    pavillon: "Pavillon voyageurs",
  },
  {
    heure: "15:30",
    titre: "Nourrissage des phoques",
    pavillonCle: "marin",
    pavillon: "Pavillon marin",
  },
  {
    heure: "16:00",
    titre: "Atelier savoirs traditionnels (plantes)",
    pavillonCle: "prairie",
    pavillon: "Pavillon prairie",
  },
  {
    heure: "17:00",
    titre: "Fermeture des pavillons exterieurs",
    pavillonCle: null,
    pavillon: null,
  },
];

const sentiers = [
  {
    id: "sentier-avenue",
    nom: "Avenue principale",
    decalageNom: "8%",
    waypoints: [
      { x: 100, y: 200 },
      { x: 920, y: 200 },
    ],
  },
  {
    id: "sentier-canopee",
    nom: "Boucle de la canopee",
    decalageNom: "40%",
    waypoints: [
      { x: 300, y: 200 },
      { x: 300, y: 350 },
      { x: 500, y: 350 },
      { x: 500, y: 200 },
    ],
  },
  {
    id: "sentier-allee-centrale",
    nom: "Allee centrale",
    decalageNom: "30%",
    waypoints: [
      { x: 500, y: 350 },
      { x: 500, y: 460 },
    ],
  },
  {
    id: "sentier-marin",
    nom: "Promenade des belugas",
    decalageNom: "30%",
    waypoints: [
      { x: 700, y: 200 },
      { x: 700, y: 100 },
      { x: 880, y: 100 },
      { x: 880, y: 360 },
      { x: 700, y: 360 },
    ],
  },
  {
    id: "sentier-prairie",
    nom: "Sentier des fleurs",
    decalageNom: "20%",
    waypoints: [
      { x: 130, y: 530 },
      { x: 500, y: 530 },
      { x: 500, y: 460 },
    ],
  },
  {
    id: "sentier-voyageurs",
    nom: "Boulevard des voyageurs",
    decalageNom: "20%",
    waypoints: [
      { x: 500, y: 460 },
      { x: 880, y: 460 },
      { x: 880, y: 600 },
      { x: 600, y: 600 },
    ],
  },
];

function dessinerPavillonBatiment(positionX, positionY, largeur, hauteur, indexPavillon) {
  const xCentre = positionX + largeur / 2;
  return (
    <g key={`batiment-${indexPavillon}`} className="batiment">
      <path
        d={`M ${positionX - 6} ${positionY + hauteur * 0.35} L ${xCentre} ${positionY} L ${positionX + largeur + 6} ${positionY + hauteur * 0.35} Z`}
        fill="#1f3a5e"
      />
      <rect
        x={positionX}
        y={positionY + hauteur * 0.35}
        width={largeur}
        height={hauteur * 0.65}
        fill="#1f3a5e"
      />
      <rect
        x={xCentre - 8}
        y={positionY + hauteur * 0.6}
        width="16"
        height={hauteur * 0.4}
        fill="#f3e6c8"
      />
      <rect x={positionX + 10} y={positionY + hauteur * 0.45} width="10" height="10" fill="#f3e6c8" />
      <rect
        x={positionX + largeur - 20}
        y={positionY + hauteur * 0.45}
        width="10"
        height="10"
        fill="#f3e6c8"
      />
    </g>
  );
}

function dessinerCarteIcone(positionX, positionY, couleurFond, contenuIcone, cleIcone) {
  return (
    <g key={cleIcone} className="icone-service">
      <rect
        x={positionX}
        y={positionY}
        width="34"
        height="34"
        rx="4"
        fill={couleurFond}
      />
      {contenuIcone}
    </g>
  );
}

function iconeFamille(positionX, positionY) {
  return (
    <g pointerEvents="none">
      <circle cx={positionX + 11} cy={positionY + 11} r="3" fill="#ffffff" />
      <path
        d={`M ${positionX + 7} ${positionY + 14} L ${positionX + 7} ${positionY + 24} L ${positionX + 15} ${positionY + 24} L ${positionX + 15} ${positionY + 14} Z`}
        fill="#ffffff"
      />
      <circle cx={positionX + 23} cy={positionY + 11} r="3" fill="#ffffff" />
      <path
        d={`M ${positionX + 19} ${positionY + 14} L ${positionX + 19} ${positionY + 24} L ${positionX + 27} ${positionY + 24} L ${positionX + 27} ${positionY + 14} Z`}
        fill="#ffffff"
      />
    </g>
  );
}

function iconePersonne(positionX, positionY) {
  return (
    <g pointerEvents="none">
      <circle cx={positionX + 17} cy={positionY + 10} r="3.5" fill="#ffffff" />
      <path
        d={`M ${positionX + 12} ${positionY + 14} L ${positionX + 12} ${positionY + 26} L ${positionX + 22} ${positionY + 26} L ${positionX + 22} ${positionY + 14} Z`}
        fill="#ffffff"
      />
    </g>
  );
}

function iconeGoutte(positionX, positionY) {
  return (
    <path
      pointerEvents="none"
      d={`M ${positionX + 17} ${positionY + 7} C ${positionX + 11} ${positionY + 14} ${positionX + 9} ${positionY + 19} ${positionX + 9} ${positionY + 22} A 8 8 0 0 0 ${positionX + 25} ${positionY + 22} C ${positionX + 25} ${positionY + 19} ${positionX + 23} ${positionY + 14} ${positionX + 17} ${positionY + 7} Z`}
      fill="#ffffff"
    />
  );
}

function iconeBol(positionX, positionY) {
  return (
    <g pointerEvents="none">
      <path
        d={`M ${positionX + 8} ${positionY + 16} A 9 9 0 0 0 ${positionX + 26} ${positionY + 16} L ${positionX + 26} ${positionY + 18} A 9 9 0 0 1 ${positionX + 8} ${positionY + 18} Z`}
        fill="#ffffff"
      />
      <ellipse cx={positionX + 17} cy={positionY + 16} rx="9" ry="2.5" fill="#ffffff" />
    </g>
  );
}

function iconeMouton(positionX, positionY) {
  return (
    <g pointerEvents="none">
      <ellipse cx={positionX + 17} cy={positionY + 18} rx="10" ry="6" fill="#ffffff" />
      <circle cx={positionX + 9} cy={positionY + 16} r="3.5" fill="#ffffff" />
      <line
        x1={positionX + 12}
        y1={positionY + 24}
        x2={positionX + 12}
        y2={positionY + 28}
        stroke="#ffffff"
        strokeWidth="1.5"
      />
      <line
        x1={positionX + 22}
        y1={positionY + 24}
        x2={positionX + 22}
        y2={positionY + 28}
        stroke="#ffffff"
        strokeWidth="1.5"
      />
    </g>
  );
}

function iconeCouteau(positionX, positionY) {
  return (
    <g pointerEvents="none">
      <path
        d={`M ${positionX + 9} ${positionY + 22} L ${positionX + 22} ${positionY + 9} L ${positionX + 26} ${positionY + 13} L ${positionX + 13} ${positionY + 26} Z`}
        fill="#ffffff"
      />
      <line
        x1={positionX + 9}
        y1={positionY + 22}
        x2={positionX + 5}
        y2={positionY + 27}
        stroke="#ffffff"
        strokeWidth="3"
      />
    </g>
  );
}

function iconeAssiette(positionX, positionY) {
  return (
    <g pointerEvents="none">
      <ellipse cx={positionX + 17} cy={positionY + 18} rx="11" ry="3" fill="#ffffff" />
      <ellipse cx={positionX + 17} cy={positionY + 17} rx="7" ry="2" fill="none" stroke="#ffffff" strokeWidth="1.5" />
    </g>
  );
}

function iconeFunic(positionX, positionY) {
  return (
    <g pointerEvents="none">
      <line
        x1={positionX + 6}
        y1={positionY + 10}
        x2={positionX + 28}
        y2={positionY + 14}
        stroke="#ffffff"
        strokeWidth="1.5"
      />
      <rect x={positionX + 11} y={positionY + 14} width="14" height="10" rx="2" fill="#ffffff" />
      <line
        x1={positionX + 13}
        y1={positionY + 12}
        x2={positionX + 13}
        y2={positionY + 14}
        stroke="#ffffff"
        strokeWidth="1.5"
      />
      <line
        x1={positionX + 23}
        y1={positionY + 13}
        x2={positionX + 23}
        y2={positionY + 14}
        stroke="#ffffff"
        strokeWidth="1.5"
      />
    </g>
  );
}

function iconeRandonneur(positionX, positionY, couleurFigure) {
  return (
    <g key={`rando-${positionX}-${positionY}`} className="figure-randonneur" pointerEvents="none">
      <circle cx={positionX} cy={positionY} r="4" fill={couleurFigure} />
      <path
        d={`M ${positionX - 4} ${positionY + 4} L ${positionX - 6} ${positionY + 18} L ${positionX - 2} ${positionY + 26} L ${positionX + 2} ${positionY + 18} L ${positionX + 6} ${positionY + 26} L ${positionX + 4} ${positionY + 18} L ${positionX + 4} ${positionY + 4} Z`}
        fill={couleurFigure}
      />
      <line
        x1={positionX + 8}
        y1={positionY + 6}
        x2={positionX + 12}
        y2={positionY + 26}
        stroke={couleurFigure}
        strokeWidth="2"
        strokeLinecap="round"
      />
    </g>
  );
}

function formaterDate(date) {
  const jours = [
    "dimanche",
    "lundi",
    "mardi",
    "mercredi",
    "jeudi",
    "vendredi",
    "samedi",
  ];
  const mois = [
    "janvier",
    "fevrier",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "aout",
    "septembre",
    "octobre",
    "novembre",
    "decembre",
  ];
  return `${jours[date.getDay()]} ${date.getDate()} ${mois[date.getMonth()]}`;
}

function formaterHeureCourante(date) {
  const heures = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  return `${heures}:${minutes}`;
}

function trouverIndexProchaineActivite(horaires, heureCourante) {
  for (let position = 0; position < horaires.length; position += 1) {
    if (horaires[position].heure.localeCompare(heureCourante) >= 0) {
      return position;
    }
  }
  return -1;
}

export default function PageBorneAccueil() {
  const [pavillonOuvert, definirPavillonOuvert] = useState(null);
  const [maintenant, definirMaintenant] = useState(() => new Date());
  const [vueActive, definirVueActive] = useState("carte");

  useEffect(() => {
    const minuterie = setInterval(() => {
      definirMaintenant(new Date());
    }, 30 * 1000);
    return () => clearInterval(minuterie);
  }, []);

  const heureCourante = formaterHeureCourante(maintenant);
  const indexProchaine = useMemo(
    () => trouverIndexProchaineActivite(horairesDuJour, heureCourante),
    [heureCourante],
  );

  function ouvrirPavillon(cle) {
    definirPavillonOuvert(cle);
  }

  function fermerPavillon() {
    definirPavillonOuvert(null);
  }

  const pavillonAffiche =
    pavillons.find((unPavillon) => unPavillon.cle === pavillonOuvert) || null;

  return (
    <div id="borne">
      <header id="entete">
        <div>
          <div id="entete-titre">Zoo maritime du Bas-Saint-Laurent</div>
          <div id="entete-sous-titre">
            {vueActive === "carte"
              ? "Plan du parc - touchez un pavillon pour le decouvrir"
              : "Horaires des activites du jour"}
          </div>
        </div>
        <div id="entete-bascule" role="tablist" aria-label="Choix de la vue">
          <button
            type="button"
            role="tab"
            aria-selected={vueActive === "carte"}
            className={`bascule-action ${vueActive === "carte" ? "bascule-action-actif" : ""}`}
            onClick={() => definirVueActive("carte")}
          >
            Carte
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={vueActive === "horaires"}
            className={`bascule-action ${vueActive === "horaires" ? "bascule-action-actif" : ""}`}
            onClick={() => definirVueActive("horaires")}
          >
            Horaires
          </button>
        </div>
        <div id="entete-date">
          {formaterDate(maintenant)} - {heureCourante}
        </div>
      </header>

      <main id="contenu">
        {vueActive === "horaires" ? (
          <section id="horaires">
            <h2 id="horaires-titre">Horaires du jour</h2>
            <div id="horaires-sous-titre">Activites et nourrissages</div>
            <ul id="horaires-liste">
              {horairesDuJour.map((unHoraire, indexHoraire) => {
                const estBientot = indexHoraire === indexProchaine;
                const classeLigne = estBientot ? "horaire horaire-bientot" : "horaire";
                const classePastille = unHoraire.pavillonCle
                  ? `horaire-pastille pavillon-${unHoraire.pavillonCle}`
                  : null;
                return (
                  <li className={classeLigne} key={`${unHoraire.heure}-${indexHoraire}`}>
                    <div className="horaire-heure">{unHoraire.heure}</div>
                    <div>
                      <div className="horaire-titre">{unHoraire.titre}</div>
                      {unHoraire.pavillon ? (
                        <div className="horaire-pavillon">
                          <span className={classePastille} aria-hidden="true" />
                          {unHoraire.pavillon}
                        </div>
                      ) : null}
                    </div>
                  </li>
                );
              })}
            </ul>
          </section>
        ) : (
          <>
        <section id="carte">
          <svg
            id="carte-svg"
            viewBox="0 0 1024 686"
            preserveAspectRatio="xMidYMid meet"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g
              className={`pavillon ${pavillonOuvert === "voyageurs" ? "pavillon-actif" : ""}`}
              onClick={() => ouvrirPavillon("voyageurs")}
            >
              <rect
                id="carte-fond"
                className="pavillon-corps"
                x="60"
                y="40"
                width="900"
                height="600"
                rx="30"
                ry="30"
                fill="#97633a"
              />
            </g>

            <g
              className={`pavillon ${pavillonOuvert === "foret" ? "pavillon-actif" : ""}`}
              onClick={() => ouvrirPavillon("foret")}
            >
              <path
                className="pavillon-corps"
                d="M 60 60 Q 60 40 80 40 L 540 40 Q 580 40 580 90 L 580 280 Q 580 360 520 380 L 480 390 Q 380 410 340 480 L 320 510 Q 280 540 220 530 L 100 510 Q 60 500 60 460 Z"
                fill="#82a04c"
              />
            </g>

            <g
              className={`pavillon ${pavillonOuvert === "marin" ? "pavillon-actif" : ""}`}
              onClick={() => ouvrirPavillon("marin")}
            >
              <path
                className="pavillon-corps"
                d="M 580 80 Q 580 40 620 40 L 920 40 Q 960 40 960 80 L 960 380 Q 960 420 920 420 L 800 420 Q 720 420 680 360 L 620 280 Q 580 220 580 160 Z"
                fill="#3d96bd"
              />
            </g>

            <g
              className={`pavillon ${pavillonOuvert === "prairie" ? "pavillon-actif" : ""}`}
              onClick={() => ouvrirPavillon("prairie")}
            >
              <path
                className="pavillon-corps"
                d="M 60 470 Q 60 440 100 435 L 220 425 Q 280 415 320 450 L 380 510 Q 440 560 480 555 L 520 555 Q 560 555 560 600 L 560 620 Q 560 640 540 640 L 80 640 Q 60 640 60 620 Z"
                fill="#bd953a"
              />
            </g>

            <g id="decor-foret">
              {arbres.map((unArbre, indexArbre) =>
                dessinerArbre(unArbre.x, unArbre.y, indexArbre),
              )}
            </g>

            <g id="decor-mer">
              {vagues.map((uneVague, indexVague) =>
                dessinerVague(uneVague.x, uneVague.y, indexVague),
              )}
            </g>

            <g id="decor-herbes">
              {herbes.map((uneHerbe, indexHerbe) =>
                dessinerHerbe(uneHerbe.x, uneHerbe.y, indexHerbe),
              )}
            </g>

            <g id="decor-fleurs">
              {fleurs.map((uneFleur, indexFleur) =>
                dessinerFleur(uneFleur.x, uneFleur.y, uneFleur.couleur, indexFleur),
              )}
            </g>

            <g id="decor-abeilles">
              {abeilles.map((uneAbeille, indexAbeille) =>
                dessinerAbeille(uneAbeille.x, uneAbeille.y, indexAbeille),
              )}
            </g>

            <g id="decor-oiseaux">
              {oiseaux.map((unOiseau, indexOiseau) =>
                dessinerOiseau(unOiseau.x, unOiseau.y, indexOiseau),
              )}
            </g>

            <g id="sentiers" pointerEvents="none">
              {sentiers.map((unSentier) => (
                <path
                  key={unSentier.id}
                  id={unSentier.id}
                  className="sentier-trace"
                  d={genererCheminAvecCoinsRonds(unSentier.waypoints, 28)}
                  fill="none"
                  stroke="rgba(243, 230, 200, 0.45)"
                  strokeWidth="22"
                  strokeLinecap="round"
                  pathLength="1"
                />
              ))}
            </g>

            <g id="sentiers-noms" pointerEvents="none">
              {sentiers.map((unSentier) => (
                <text key={`nom-${unSentier.id}`} className="sentier-nom">
                  <textPath href={`#${unSentier.id}`} startOffset={unSentier.decalageNom}>
                    {unSentier.nom}
                  </textPath>
                </text>
              ))}
            </g>

            <g id="batiments" pointerEvents="none">
              {dessinerPavillonBatiment(490, 360, 80, 80, "central")}
              {dessinerPavillonBatiment(450, 460, 80, 80, "secondaire")}
            </g>

            <text
              className="zone-titre"
              x="270"
              y="205"
              textAnchor="middle"
              pointerEvents="none"
            >
              FORET
            </text>
            <text
              className="zone-titre"
              x="780"
              y="225"
              textAnchor="middle"
              pointerEvents="none"
            >
              MARIN
            </text>
            <text
              className="zone-titre zone-titre-prairie"
              x="200"
              y="565"
              textAnchor="middle"
              pointerEvents="none"
            >
              PRAIRIE
            </text>
            <text
              className="zone-titre"
              x="700"
              y="530"
              textAnchor="middle"
              pointerEvents="none"
            >
              VOYAGEURS
            </text>

            <g id="icones-services">
              {dessinerCarteIcone(415, 175, "#1f3a8a", iconeGoutte(415, 175), "icone-eau")}
              {dessinerCarteIcone(420, 305, "#1f3a8a", iconeBol(420, 305), "icone-bol-foret")}
              {dessinerCarteIcone(285, 405, "#a83232", iconeCouteau(285, 405), "icone-couteau")}
              {dessinerCarteIcone(105, 475, "#a83232", iconeMouton(105, 475), "icone-mouton-prairie")}
              {dessinerCarteIcone(275, 380, "#1f3a8a", iconeFamille(275, 380), "icone-famille-foret")}
              {dessinerCarteIcone(575, 245, "#1f3a8a", iconeFamille(575, 245), "icone-famille-pavillon-1")}
              {dessinerCarteIcone(680, 270, "#1f3a8a", iconeFamille(680, 270), "icone-famille-pavillon-2")}
              {dessinerCarteIcone(785, 320, "#1f3a8a", iconeMouton(785, 320), "icone-mouton-voyageurs")}
              {dessinerCarteIcone(610, 280, "#1f3a8a", iconeFunic(610, 280), "icone-funiculaire")}
              {dessinerCarteIcone(710, 320, "#a83232", iconeAssiette(710, 320), "icone-assiette")}
              {dessinerCarteIcone(545, 510, "#1f3a8a", iconePersonne(545, 510), "icone-personne-prairie")}
              {dessinerCarteIcone(640, 530, "#a83232", iconeAssiette(640, 530), "icone-assiette-bas")}
              {dessinerCarteIcone(750, 555, "#1f3a8a", iconePersonne(750, 555), "icone-personne-voyageurs")}
            </g>

            <g id="randonneurs" pointerEvents="none">
              {iconeRandonneur(135, 595, "#ffffff")}
              {iconeRandonneur(180, 595, "#ffffff")}
              {iconeRandonneur(490, 595, "#ffffff")}
            </g>

            <g id="vous-etes-ici" pointerEvents="none">
              <text id="vous-etes-ici-etiquette" x="530" y="350" textAnchor="middle">
                Vous etes ici
              </text>
              <path
                id="vous-etes-ici-pin"
                d="M 530 360 C 515 360 503 372 503 388 C 503 410 530 445 530 445 C 530 445 557 410 557 388 C 557 372 545 360 530 360 Z"
              />
              <circle cx="530" cy="388" r="8" fill="#ffffff" />
            </g>
          </svg>
        </section>

        {pavillonAffiche ? (
          <aside
            id="fiche-pavillon"
            style={{ borderTopColor: pavillonAffiche.couleur }}
          >
            <button
              id="fiche-pavillon-fermer"
              type="button"
              aria-label="Fermer la fiche"
              onClick={fermerPavillon}
            >
              x
            </button>
            <div id="fiche-pavillon-sous-titre">{pavillonAffiche.sousTitre}</div>
            <div id="fiche-pavillon-titre">{pavillonAffiche.titre}</div>
            <p id="fiche-pavillon-description">{pavillonAffiche.description}</p>
          </aside>
        ) : null}
        </>
        )}
      </main>
    </div>
  );
}
