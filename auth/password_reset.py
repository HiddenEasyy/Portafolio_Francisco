import streamlit as st

def show_password_reset():
    # --- CSS personalizado solo para recuperación ---
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
    st.markdown('<div class="login-logo">🔐</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Recuperar contraseña</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">Ingresa tu correo y te enviaremos instrucciones para restablecer tu contraseña.</div>', unsafe_allow_html=True)
    st.markdown('<hr class="login-separator" />', unsafe_allow_html=True)

    correo = st.text_input('Correo electrónico', key='reset_email', placeholder='Correo electrónico')
    st.markdown('<div class="login-input"><span class="input-icon">📧</span></div>', unsafe_allow_html=True)

    reset_btn = st.container()
    with reset_btn:
        reset_clicked = st.button('Enviar instrucciones', key='btn_reset')

    if reset_clicked:
        st.info('Si el correo está registrado, se enviará un enlace de recuperación (simulado).')

    st.markdown('<div class="login-links">', unsafe_allow_html=True)
    if st.button('Volver al login', key='btn_goto_login_reset'):
        st.session_state['auth_page'] = 'login'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
