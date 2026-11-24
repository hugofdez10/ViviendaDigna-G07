import { computed, onMounted, ref } from "vue";
import { initializeApp } from "firebase/app";
import { signInAnonymously } from "firebase/auth";
import { addDoc, collection, deleteDoc, doc, orderBy, query, serverTimestamp } from "firebase/firestore";
import { useCollection, useCurrentUser, useFirebaseAuth, useFirestore, VueFire, VueFireAuth } from "vuefire";

export function instalarFirebase(app, configuracion) {
    app.use(VueFire, {
        firebaseApp: initializeApp(configuracion),
        modules: [VueFireAuth()],
    });
}

export function usarAgendaFirebase() {
    const auth = useFirebaseAuth();
    const usuario = useCurrentUser();
    const db = useFirestore();
    const errorSesion = ref("");
    const referencia = computed(() => usuario.value
        ? collection(db, "agendas", usuario.value.uid, "contactos")
        : null);
    const consulta = computed(() => referencia.value
        ? query(referencia.value, orderBy("nombre"))
        : null);
    const contactos = useCollection(consulta);
    const disponible = computed(() => Boolean(referencia.value && !contactos.pending.value && !contactos.error.value));

    onMounted(async () => {
        try {
            await auth.authStateReady();
            if (!auth.currentUser) await signInAnonymously(auth);
        } catch {
            errorSesion.value = "No se pudo abrir la sesión de Firebase.";
        }
    });

    return {
        contactos,
        disponible,
        estado: computed(() => !disponible.value && !errorSesion.value && !contactos.error.value
            ? "Conectando con Firebase…"
            : ""),
        error: computed(() => errorSesion.value || (contactos.error.value
            ? "No se pudieron cargar los contactos de Firebase."
            : "")),
        crear(datos) {
            return addDoc(referencia.value, { ...datos, creado: serverTimestamp() });
        },
        borrar(id) {
            return deleteDoc(doc(referencia.value, id));
        },
    };
}
