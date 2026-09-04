// Genera un codigo numerico de 6 digitos como texto (con ceros a la izquierda si hace falta)
module.exports = function generarCodigo() {
    return String(Math.floor(Math.random() * 1000000)).padStart(6, '0');
};
