const extensionesVideo = ['.mp4', '.webm', '.mov', '.ogg'];

module.exports = function esVideo(url) {
    if (!url) return false;
    const minuscula = url.toLowerCase();
    return extensionesVideo.some((ext) => minuscula.endsWith(ext));
};
