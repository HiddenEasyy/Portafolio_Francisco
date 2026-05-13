import streamlit as st

def login_user(user_id, user_name, user_role):
    st.session_state['authenticated'] = True
    st.session_state['user_id'] = user_id
    st.session_state['user_name'] = user_name
    st.session_state['user_role'] = user_role

def logout_user():
    st.session_state.clear()
    st.session_state['authenticated'] = False

def is_authenticated():
    return st.session_state.get('authenticated', False)

def get_current_user():
    return {
        'id': st.session_state.get('user_id'),
        'name': st.session_state.get('user_name'),
        'role': st.session_state.get('user_role')
    }
