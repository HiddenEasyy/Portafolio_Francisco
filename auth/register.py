import streamlit as st
import bcrypt
from db.connection import get_connection

def show_register():
    # --- CSS personalizado solo para registro ---
    st.markdown("""
        <style>
        body, .stApp {
            background: linear-gradient(135deg, #EBF3FB 0%, #D4EDDA 100%) !important;
        }
        .login-card {
            max-width: 420px;
            margin: 5vh auto 0 auto;
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 6px 32px 0 rgba(46,117,182,0.10), 0 1.5px 6px 0 rgba(15,110,86,0.10);
            padding: 2.5rem 2rem 2rem 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .login-logo {
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
            filter: drop-shadow(0 2px 8px #2E75B633);
        }
        .login-title {
            font-size: 2rem;
            font-weight: 700;
            color: #1F2937;
            margin-bottom: 0.2rem;
            text-align: center;
        }
        .login-subtitle {
            color: #6B7280;
            font-size: 1.05rem;
            margin-bottom: 1.2rem;
            text-align: center;
        }
        .login-separator {
            width: 100%;
            border: none;
            border-top: 1px solid #E5E7EB;
            margin: 1.2rem 0 1.2rem 0;
        }
        .login-input input {
            border-radius: 8px !important;
            border: 1.5px solid #D1D5DB !important;
            padding-left: 2.2rem !important;
            background: #F9FAFB !important;
        }
        .login-input {
            position: relative;
            width: 100%;
            margin-bottom: 1.1rem;
        }
        .login-input .input-icon {
            position: absolute;
            left: 0.7rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 1.2rem;
            color: #2E75B6;
            opacity: 0.85;
        }
        .login-btn button {
            width: 100%;
            background: #2E75B6 !important;
            color: #fff !important;
            font-weight: 600;
            border-radius: 8px !important;
            padding: 0.7rem 0;
            font-size: 1.1rem;
            margin-top: 0.2rem;
            margin-bottom: 0.7rem;
            box-shadow: 0 2px 8px #2E75B633;
            border: none;
            transition: background 0.2s;
        }
        .login-btn button:hover {
            background: #1F4E79 !important;
        }
        .login-or {
            color: #6B7280;
            font-size: 0.95rem;
            margin: 0.7rem 0 0.7rem 0;
            width: 100%;
            text-align: center;
            letter-spacing: 0.1em;
        }
        .login-links {
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
            margin-top: 0.2rem;
        }
        .login-link {
            color: #0F6E56;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.98rem;
            transition: color 0.2s;
            cursor: pointer;
        }
        .login-link:hover {
            color: #2E75B6;
            text-decoration: underline;
        }
        header, footer {visibility: hidden !important; height: 0 !important;}
        @media (max-width: 500px) {
            .login-card { padding: 1.2rem 0.5rem; }
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-logo">⚕️</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Crear cuenta</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Plataforma de Monitoreo de Salud</div>', unsafe_allow_html=True)
    st.markdown('<hr class="login-separator" />', unsafe_allow_html=True)

    nombre = st.text_input('Nombre completo', key='register_nombre', placeholder='Nombre completo')
    st.markdown('<div class="login-input"><span class="input-icon">👤</span></div>', unsafe_allow_html=True)
    correo = st.text_input('Correo electrónico', key='register_email', placeholder='Correo electrónico')
    st.markdown('<div class="login-input"><span class="input-icon">📧</span></div>', unsafe_allow_html=True)
    password = st.text_input('Contraseña', type='password', key='register_password', placeholder='Contraseña')
    st.markdown('<div class="login-input"><span class="input-icon">🔒</span></div>', unsafe_allow_html=True)
    password2 = st.text_input('Confirmar contraseña', type='password', key='register_password2', placeholder='Confirmar contraseña')
    st.markdown('<div class="login-input"><span class="input-icon">🔒</span></div>', unsafe_allow_html=True)
    rol = st.selectbox('Rol', ['paciente', 'medico'], key='register_rol')

    register_btn = st.container()
    with register_btn:
        register_clicked = st.button('Crear cuenta', key='btn_register')

    if register_clicked:
        if not (nombre and correo and password and password2):
            st.error('Todos los campos son obligatorios')
            return
        if '@' not in correo or '.' not in correo:
            st.error('Correo electrónico inválido')
            return
        if password != password2:
            st.error('Las contraseñas no coinciden')
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM usuarios WHERE correo=%s', (correo,))
        if cursor.fetchone():
            st.error('El correo ya está registrado')
            cursor.close()
            conn.close()
            return
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cursor.execute('INSERT INTO usuarios (nombre, correo, password_hash, rol) VALUES (%s, %s, %s, %s)', (nombre, correo, password_hash, rol))
        conn.commit()
        cursor.close()
        conn.close()
        st.success('Registro exitoso. Ahora puedes iniciar sesión.')
        st.session_state['auth_page'] = 'login'
        st.rerun()

    st.markdown('<div class="login-links">', unsafe_allow_html=True)
    if st.button('¿Ya tienes cuenta? Inicia sesión', key='btn_goto_login'):
        st.session_state['auth_page'] = 'login'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
