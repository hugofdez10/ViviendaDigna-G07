import { computed, createApp, reactive, ref } from "vue";
import { firebaseConfig } from "./firebase-config.js";

const vistaPrevia = new URLSearchParams(window.location.search).get("demo") === "1";
const tieneConfiguracion = ["apiKey", "authDomain", "projectId", "appId"]
    .every((campo) => firebaseConfig[campo]);

async function iniciarAgenda() {
    const app = createApp({
        template: "#plantilla-agenda",
        setup() {
            const formulario = reactive({ nombre: "", email: "", telefono: "" });
            const operacion = ref(false);
            const aviso = ref("");
            const errorOperacion = ref("");
            const agenda = !vistaPrevia && tieneConfiguracion
                ? usarAgendaFirebase()
                : usarVistaPrevia();

            async function crearContacto() {
                if (!agenda.disponible.value || operacion.value) return;
                if (Object.values(formulario).some((dato) => !dato)) {
                    errorOperacion.value = "Rellena los tres campos del contacto.";
                    return;
                }
                operacion.value = true;
                errorOperacion.value = "";
                try {
                    await agenda.crear({ ...formulario });
                    Object.assign(formulario, { nombre: "", email: "", telefono: "" });
                    aviso.value = "Contacto añadido.";
                } catch {
                    errorOperacion.value = "No se pudo guardar el contacto. Inténtalo de nuevo.";
                } finally {
                    operacion.value = false;
                }
            }

            async function borrarContacto(id) {
                if (!agenda.disponible.value || operacion.value) return;
                operacion.value = true;
                errorOperacion.value = "";
                try {
                    await agenda.borrar(id);
                    aviso.value = "Contacto borrado.";
                } catch {
                    errorOperacion.value = "No se pudo borrar el contacto. Inténtalo de nuevo.";
                } finally {
                    operacion.value = false;
                }
            }

            return {
                formulario,
                operacion,
                disponible: agenda.disponible,
                puedePrevisualizar: !vistaPrevia && !tieneConfiguracion,
                contactos: agenda.contactos,
                aviso: computed(() => [agenda.estado.value, aviso.value].filter(Boolean).join(" ")),
                error: computed(() => errorOperacion.value || agenda.error.value),
                crearContacto,
                borrarContacto,
            };
        },
    });

    let usarAgendaFirebase;
    if (!vistaPrevia && tieneConfiguracion) {
        const firebase = await import("./agenda-firebase.js");
        usarAgendaFirebase = firebase.usarAgendaFirebase;
        firebase.instalarFirebase(app, firebaseConfig);
    }
    app.mount("#agenda");
}

function usarVistaPrevia() {
    const contactos = ref([]);
    return {
        contactos,
        disponible: ref(vistaPrevia),
        estado: ref(vistaPrevia
            ? "Vista previa local. Los contactos se borran al recargar."
            : ""),
        error: ref(vistaPrevia
            ? ""
            : "Falta configurar Firebase."),
        crear(datos) {
            contactos.value.push({ ...datos, id: crypto.randomUUID() });
        },
        borrar(id) {
            contactos.value = contactos.value.filter((contacto) => contacto.id !== id);
        },
    };
}

iniciarAgenda().catch(() => {
    const estado = document.querySelector("#agenda");
    estado.textContent = "No se pudo iniciar la agenda. Recarga la página para volver a intentarlo.";
    estado.setAttribute("role", "alert");
});
