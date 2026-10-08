import "./globals.css";

export const metadata = {
  title: "Zoo maritime du Bas-Saint-Laurent - Borne d'accueil",
  description: "Carte interactive et horaires des activites du jour",
};

export default function rootLayout({ children }) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
