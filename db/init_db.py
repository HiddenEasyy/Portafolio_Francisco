from .connection import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(150) NOT NULL,
        correo VARCHAR(150) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        rol ENUM('paciente', 'medico', 'administrador') DEFAULT 'paciente',
        activo BOOLEAN DEFAULT TRUE,
        intentos_fallidos INT DEFAULT 0,
        bloqueado BOOLEAN DEFAULT FALSE,
        fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sesiones (
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario_id INT,
        token VARCHAR(500),
        fecha_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
        activa BOOLEAN DEFAULT TRUE,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
