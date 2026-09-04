const nodemailer = require('nodemailer');

const transportador = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.GMAIL_USER,
        pass: process.env.GMAIL_APP_PASSWORD,
    },
});

exports.enviarCodigoVerificacion = async function (destinatario, nombre, codigo) {
    await transportador.sendMail({
        from: `"IED Talento Humano" <${process.env.GMAIL_USER}>`,
        to: destinatario,
        subject: 'Verifica tu correo - IED Talento Humano',
        html: `
            <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;">
                <h2 style="color: #073d82;">Hola, ${nombre}</h2>
                <p>Usa este código para confirmar tu correo en la página del colegio:</p>
                <p style="font-size: 32px; font-weight: bold; letter-spacing: 6px; color: #0a5ec4; text-align: center; padding: 16px; background: #e6f1ff; border-radius: 10px;">${codigo}</p>
                <p>Este código vence en 15 minutos. Si no creaste esta cuenta, ignora este mensaje.</p>
            </div>
        `,
    });
};

exports.enviarCodigoRecuperacion = async function (destinatario, nombre, codigo) {
    await transportador.sendMail({
        from: `"IED Talento Humano" <${process.env.GMAIL_USER}>`,
        to: destinatario,
        subject: 'Restablece tu contraseña - IED Talento Humano',
        html: `
            <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;">
                <h2 style="color: #073d82;">Hola, ${nombre}</h2>
                <p>Recibimos una solicitud para restablecer tu contraseña. Usa este código para continuar:</p>
                <p style="font-size: 32px; font-weight: bold; letter-spacing: 6px; color: #0a5ec4; text-align: center; padding: 16px; background: #e6f1ff; border-radius: 10px;">${codigo}</p>
                <p>Este código vence en 15 minutos. Si tú no pediste esto, ignora este mensaje y tu contraseña seguirá igual.</p>
            </div>
        `,
    });
};
