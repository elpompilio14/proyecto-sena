// Genera un link para incrustar Google Maps a partir de una direccion, sin necesitar API key.
module.exports = function googleMapsEmbedUrl(direccion) {
    if (!direccion) return null;
    return `https://www.google.com/maps?q=${encodeURIComponent(direccion)}&output=embed`;
};
