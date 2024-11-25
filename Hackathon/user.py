
import psycopg2
import bcrypt  # Importation de la bibliothèque bcrypt

class User:
    def __init__(self, username, password, user_id=None):
        """Initialiser un objet utilisateur avec les détails fournis."""
        self.username = username
        self.password = password
        self.user_id = user_id

    @staticmethod
    def connect_db():
        """Établir et retourner une connexion à la base de données PostgreSQL."""
        try:
            connection = psycopg2.connect(
                dbname='hangman_game',  # Nom de ta base de données
                user='postgres',        # Nom d'utilisateur de ta base de données
                password='1004',        # Mot de passe de ta base de données
                host='localhost',       # Hôte de ta base de données
                port='5432'             # Port de ta base de données
            )
            return connection
        except Exception as e:
            print(f"Erreur de connexion à la base de données: {e}")
            return None

    @classmethod
    def create_tables(cls):
        """Créer les tables 'users' et 'scores' si elles n'existent pas."""
        connection = cls.connect_db()
        cursor = connection.cursor()

        # Création de la table des joueurs
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        ''')

        # Création de la table des scores
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS scores (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                score INTEGER
            );
        ''')

        connection.commit()
        cursor.close()
        connection.close()

    @classmethod
    def register_user(cls, username, password):
        """Enregistrer un nouvel utilisateur avec un mot de passe hashé."""
        connection = cls.connect_db()
        cursor = connection.cursor()

        # Vérifier si l'utilisateur existe déjà
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            print(f"L'utilisateur {username} existe déjà.")
            cursor.close()
            connection.close()
            return None

        # Hachage du mot de passe avant de le stocker
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insérer l'utilisateur dans la table 'users' avec le mot de passe hashé
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id", (username, hashed_password))
        user_id = cursor.fetchone()[0]

        connection.commit()
        cursor.close()
        connection.close()

        # Retourner un objet User avec les détails de l'utilisateur créé
        return cls(username, hashed_password, user_id)

    @classmethod
    def check_login(cls, username, password):
        """Vérifier si un utilisateur existe et si le mot de passe correspond, sinon l'enregistrer."""
        connection = cls.connect_db()
        if not connection:
            print("Échec de la connexion à la base de données.")
            return None
        
        cursor = connection.cursor()

        # Récupérer l'utilisateur en fonction du nom d'utilisateur
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()

        if not user_data:
            print(f"Aucun utilisateur trouvé avec le nom d'utilisateur : {username}")
            print(f"Enregistrement de l'utilisateur {username}...")
            # Enregistrer un nouvel utilisateur si l'utilisateur n'existe pas
            return cls.register_user(username, password)
        
        print(f"Utilisateur trouvé : {user_data}")  # Affiche les données de l'utilisateur
        cursor.close()
        connection.close()

        # Comparaison du mot de passe
        stored_password_hash = user_data[2]  # Mot de passe hashé dans la base de données
        if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
            print("Le mot de passe correspond !")  # Afficher si le mot de passe correspond
            return cls(user_data[1], stored_password_hash, user_data[0])
        else:
            print("Le mot de passe ne correspond pas.")  # Message si le mot de passe ne correspond pas
        return None

    def save_score(self, score):
        """Sauvegarder le score de l'utilisateur actuel dans la base de données."""
        connection = self.connect_db()
        cursor = connection.cursor()

        # Insérer le score de l'utilisateur dans la table 'scores'
        cursor.execute("INSERT INTO scores (user_id, score) VALUES (%s, %s)", (self.user_id, score))
        connection.commit()

        cursor.close()
        connection.close()

    def update_score(self, score):
        """Mettre à jour le score de l'utilisateur dans la table 'users'."""
        connection = self.connect_db()
        cursor = connection.cursor()

        # Mettre à jour le score de l'utilisateur
        cursor.execute("UPDATE users SET score = %s WHERE id = %s", (score, self.user_id))
        connection.commit()

        cursor.close()
        connection.close()

    @classmethod
    def get_all_users(cls):
         """Récupérer tous les utilisateurs et leurs informations depuis la base de données."""
         connection = cls.connect_db()
         cursor = connection.cursor()

         # Requête mise à jour pour joindre la table scores
         cursor.execute("""
        SELECT u.id, u.username, u.password, s.score
        FROM users u
        LEFT JOIN scores s ON u.id = s.user_id
        """)
         users_data = cursor.fetchall()

         cursor.close()
         connection.close()

         return users_data



