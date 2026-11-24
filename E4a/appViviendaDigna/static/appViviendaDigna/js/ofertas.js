if (window.jQuery) {
    jQuery(function ($) {
        const formulario = $("#filtro-ofertas");
        const estado = $("#estado-ofertas");
        let peticion;

        formulario.on("submit", function (evento) {
            evento.preventDefault();
            if (peticion) peticion.abort();

            const datos = formulario.serialize();
            const resultados = $("#resultados-ofertas");
            resultados.attr("aria-busy", "true");
            estado.text(formulario.data("cargando"));

            peticion = $.ajax({
                url: formulario.data("resultados-url"),
                data: datos,
                dataType: "html"
            }).done(function (html) {
                const fragmento = $($.parseHTML(html)).filter("#resultados-ofertas");
                const urlListado = formulario.attr("action") + (datos ? "?" + datos : "");
                if (!fragmento.length) {
                    window.location.assign(urlListado);
                    return;
                }
                resultados.replaceWith(fragmento);
                if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
                    fragmento.hide().fadeIn(160);
                }
                window.history.replaceState(null, "", urlListado);
                estado.text(formulario.data("actualizado"));
            }).fail(function (_respuesta, motivo) {
                if (motivo !== "abort") {
                    resultados.removeAttr("aria-busy");
                    estado.text(formulario.data("error"));
                }
            });
        });
    });
}
