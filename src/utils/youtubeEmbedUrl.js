const patrones = [
    /youtu\.be\/([a-zA-Z0-9_-]{11})/,
    /youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})/,
    /youtube\.com\/embed\/([a-zA-Z0-9_-]{11})/,
    /youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})/,
];

// Convierte un link normal de YouTube (watch, youtu.be, shorts) en su URL de incrustar (embed)
module.exports = function youtubeEmbedUrl(url) {
    if (!url) return null;
    for (const patron of patrones) {
        const coincidencia = url.match(patron);
        if (coincidencia) return `https://www.youtube.com/embed/${coincidencia[1]}`;
    }
    return null;
};
