// Flujo de Google OAuth 2.0 hecho con fetch nativo, sin librerias extra.

exports.urlAutorizacionGoogle = function (state) {
    const params = new URLSearchParams({
        client_id: process.env.GOOGLE_CLIENT_ID,
        redirect_uri: process.env.GOOGLE_CALLBACK_URL,
        response_type: 'code',
        scope: 'openid email profile',
        prompt: 'select_account',
        state,
    });
    return `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
};

exports.obtenerPerfilGoogle = async function (code) {
    const respuestaToken = await fetch('https://oauth2.googleapis.com/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
            code,
            client_id: process.env.GOOGLE_CLIENT_ID,
            client_secret: process.env.GOOGLE_CLIENT_SECRET,
            redirect_uri: process.env.GOOGLE_CALLBACK_URL,
            grant_type: 'authorization_code',
        }),
    });

    const datosToken = await respuestaToken.json();
    if (!respuestaToken.ok) {
        throw new Error(datosToken.error_description || 'No se pudo validar con Google');
    }

    const respuestaPerfil = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
        headers: { Authorization: `Bearer ${datosToken.access_token}` },
    });

    const perfil = await respuestaPerfil.json();
    if (!respuestaPerfil.ok) {
        throw new Error('No se pudo obtener el perfil de Google');
    }

    return perfil; // { id, email, given_name, family_name, name, picture, verified_email }
};
