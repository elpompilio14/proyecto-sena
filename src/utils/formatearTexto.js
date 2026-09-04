function escaparHtml(texto) {
    return texto
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

// Convierte *texto* o **texto** en negrilla, como en WhatsApp.
// El texto se escapa primero para que no se pueda inyectar HTML.
module.exports = function formatearTexto(texto) {
    if (!texto) return '';
    const escapado = escaparHtml(texto);
    return escapado
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.+?)\*/g, '<strong>$1</strong>');
};
