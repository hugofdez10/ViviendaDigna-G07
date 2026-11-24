import { copyFile, mkdir } from "node:fs/promises";

const destino = new URL("./publicacion/", import.meta.url);
const archivos = ["index.html", "agenda.css", "agenda.js", "agenda-firebase.js", "firebase-config.js"];
await mkdir(destino, { recursive: true });
await Promise.all(archivos.map((archivo) =>
    copyFile(new URL(archivo, import.meta.url), new URL(archivo, destino))
));
