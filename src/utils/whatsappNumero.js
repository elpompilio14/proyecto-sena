// Limpia el numero de WhatsApp guardado en admin (puede tener espacios, guiones,
// parentesis o venir sin el indicativo de pais) para que el link a wa.me funcione.
module.exports = function whatsappNumero(numero) {
    if (!numero) return null;
    const soloDigitos = numero.replace(/\D/g, '');
    if (soloDigitos.length === 10) return '57' + soloDigitos; // celular colombiano sin indicativo
    return soloDigitos;
};
