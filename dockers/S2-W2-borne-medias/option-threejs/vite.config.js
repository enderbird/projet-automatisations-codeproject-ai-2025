import { defineConfig } from "vite";

// Les variables d'environnement injectees au build du Dockerfile
// (BUILD_DATE, NOM_ETUDIANT, MATRICULE) sont remplacees a la compilation
// Vite par les valeurs litterales correspondantes. C'est le mecanisme
// equivalent aux ARG du Dockerfile, cote frontend.
export default defineConfig({
  define: {
    __BUILD_DATE__: JSON.stringify(process.env.BUILD_DATE || "inconnu"),
    __NOM_ETUDIANT__: JSON.stringify(process.env.NOM_ETUDIANT || "anonyme"),
    __MATRICULE__: JSON.stringify(process.env.MATRICULE || "000000"),
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
    sourcemap: false,
    target: "es2022",
  },
});
