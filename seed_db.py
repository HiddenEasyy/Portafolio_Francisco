import bcrypt
from db.connection import get_connection 

def seed_users():
    users = [
        {'nombre': 'Ana García', 'correo': 'ana@demo.com', 'password': 'ana123', 'rol': 'paciente'},
        {'nombre': 'Dr. Luis Pérez', 'correo': 'luis@demo.com', 'password': 'luis123', 'rol': 'medico'},
        {'nombre': 'Admin', 'correo': 'admin@demo.com', 'password': 'admin123', 'rol': 'administrador'},
    ]
    conn = get_connection()
    cursor = conn.cursor()
    for user in users:
        password_hash = bcrypt.hashpw(user['password'].encode(), bcrypt.gensalt()).decode()
        try:
            cursor.execute('INSERT INTO usuarios (nombre, correo, password_hash, rol) VALUES (%s, %s, %s, %s)',
                           (user['nombre'], user['correo'], password_hash, user['rol']))
        except Exception as e:
            print(f"Usuario {user['correo']} ya existe o error: {e}")
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    seed_users()
