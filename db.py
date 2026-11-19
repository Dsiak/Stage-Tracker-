import sqlite3

from pathlib import Path

DB_NAME = Path(__file__).resolve().parent / "stages.db"

def get_connection():
    """Ouvre une connexion a la base de donnees"""
    conn= sqlite3.connect(DB_NAME, uri=True)

    #Active la vérification des clés étrangères
    conn.execute("PRAGMA Foreign_Keys = ON ")
    return conn

def create_tables():
    """Crée les 4 tables de la base de donnée"""
    conn= get_connection()
    cursor= conn.cursor()


    #Table 1 : entreprises
    cursor.execute(""" CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            website TEXT,
            location TEXT
        )
    """)


    #Table 2 : Offres de stage
    cursor.execute(""" CREATE TABLE IF NOT EXISTS offers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    url TEXT NOT NULL UNIQUE,
    location TEXT,
    deadline TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (company_id) 
        REFERENCES companies (id)
        ON DELETE CASCADE

    )
    """)


    #Table 3 : Competences
    cursor.execute("""CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE 
    )
    """)


    #Tablr 4 : Association entre offres et compétences
    cursor.execute(""" CREATE TABLE IF NOT EXISTS offer_skills ( 
    offer_id INTEGER NOT NULL, 
    skill_id INTEGER NOT NULL,

    PRIMARY KEY (offer_id, skill_id), 

    FOREIGN KEY (offer_id) 
        REFERENCES offers(id) 
        ON DELETE CASCADE, 

    FOREIGN KEY (skill_id) 
        REFERENCES skills(id) 
        ON DELETE CASCADE 
    ) 
    """)
 
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Les 4 tables sont prêtes !")

def add_company(name, website=None, location=None):
    """Ajoute une entreprise à la base de données"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO companies (name, website, location)
        VALUES (?, ?, ?)
    """, (name, website, location))

    company_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return company_id


def get_companies():
    """Récupère toutes les entreprises."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, website, location
        FROM companies
        ORDER BY name
    """)

    companies = cursor.fetchall()

    conn.close()

    return companies

def get_or_create_company(name):
    """Récupère l'identifiant d'une entreprise ou la crée"""
    conn= get_connection()
    cursor=  conn.cursor()
    
    #chercher l'entreprise
    cursor.execute("""
    SELECT id
    FROM companies
    WHERE name = ? COLLATE NOCASE
""", (name,))
    company = cursor.fetchone()

    conn.close()

    #Si l'entreprise existe déjà
    if company : 
        return company[0]

    #Sinon, créer l'entreprise 
    return add_company(name)

def update_company(company_id, name, website=None, location=None):
    """Modifie une entreprise existante."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE companies
        SET name = ?, website = ?, location = ?
        WHERE id = ?
    """, (name, website, location, company_id))

    updated = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return updated

def delete_company(company_id):
    """Supprime une entreprise."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM companies
        WHERE id = ?
    """, (company_id,))

    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted

def add_offer ( company_id, title, url, description= None, location=None, deadline=None):
    """Ajoute une offre de stage à la base de données"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO offers (company_id, title, description, url, location, deadline)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        company_id,
        title,
        description,
        url,
        location,
        deadline
    ))

    offer_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return offer_id

def get_offers():
    """"Récupéré toutes les offres avec le nom de leur entreprise """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        offers.id,
        companies.name,
        offers.title,
        offers.description,
        offers.url,
        offers.location,
        offers.deadline
    FROM offers 
    JOIN companies
        ON offers.company_id = companies.id
    ORDER BY offers.deadline
    """)

    offers = cursor.fetchall()

    conn.close()

    return offers 

def update_offer(offer_id, company_id, title, url, description= None, location= None, deadline= None ):
    """Modifier les offres de stages existant """

    conn = get_connection()
    cursor= conn.cursor()

    cursor.execute("""
        UPDATE offers
        SET company_id =?,
            title = ? ,
            description =?,
            url = ? ,
            location =?,
            deadline= ?
        WHERE id = ?
    """,(
        company_id,
        title,
        description,
        url,
        location,
        deadline,
        offer_id
    ))
    updated = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return updated

def delete_offer(offer_id):
    """Supprimer une offre de stage. """
   
    conn = get_connection()
    cursor= conn.cursor()

    cursor.execute("""
        DELETE FROM offers
        WHERE id = ?""", (offer_id,))

    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted

def add_skill(name):
    """Ajoute une compétence à la base de données"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO skills (name)
        VALUES (?)
    """, (name,))

    skill_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return skill_id

def get_skills():
    """Récupère toutes les compétences."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name
        FROM skills
        ORDER BY name
    """)

    skills = cursor.fetchall()

    conn.close()

    return skills

def add_offer_skill(offer_id, skill_id):
    """Associe une compétence à une offre de stage."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO offer_skills (offer_id, skill_id)
        VALUES (?, ?)
    """, (offer_id, skill_id))

    added = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return added

def get_offer_skills(offer_id):
    """Récupère toutes les compétences associées à une offre de stage."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT skills.id, skills.name
        FROM skills
        JOIN offer_skills ON skills.id = offer_skills.skill_id
        WHERE offer_skills.offer_id = ?
        ORDER BY skills.name
    """, (offer_id,))

    skills = cursor.fetchall()

    conn.close()

    return skills

#Gestion des compétences associées à une offre de stage
def get_or_create_skill(name):
    """Récupère l'identifiant d'une compétence ou la crée"""
    name -name.strip()
    conn = get_connection()
    cursor = conn.cursor()

    # Chercher la compétence
    cursor.execute("""
        SELECT id
        FROM skills
        WHERE name = ? COLLATE NOCASE
    """, (name,))
    skill = cursor.fetchone()

    conn.close()

    # Si la compétence existe déjà
    if skill:
        return skill[0]

    # Sinon, créer la compétence
    return add_skill(name)

# Initialisation du suivi des candidatures
def prepare_tracking():
    """Ajoute le statut et l'historique sans supprimer les offres existantes."""
    conn= get_connection()
    cursor= conn.cursor()

    #Vérifier si la colonne "status" existe déjà
    cursor.execute("""
        PRAGMA table_info(offers)
    """)
    columns = [column[1] for column in cursor.fetchall()]

    if "status" not in columns:
        cursor.execute("""
            ALTER TABLE offers
            ADD COLUMN status TEXT NOT NULL DEFAULT 'À postuler'
        """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS offer_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            offer_id INTEGER NOT NULL,
            old_status TEXT,
            new_status TEXT NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (offer_id)
                REFERENCES offers (id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()

#Offres avec statut
def get_offers_with_status():
    """Récupère toutes les offres avec le nom de leur entreprise et leur statut"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            offers.id,
            companies.name,
            offers.title,
            offers.description,
            offers.url,
            offers.location,
            offers.deadline,
            offers.status
        FROM offers
        JOIN companies ON offers.company_id = companies.id
        ORDER BY offers.id DESC
    """)

    offers = cursor.fetchall()

    conn.close()

    return offers

#Modification d'une candidature
def update_offer_status(offer_id, new_status, note=""):
    """Modifie le statut et conserve un historique."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status
        FROM offers
        WHERE id = ?
    """, (offer_id,))

    result = cursor.fetchone()

    if result is None:
        conn.close()
        return False

    old_status = result[0]
    note = note.strip()

    if old_status == new_status and not note:
        conn.close()
        return False

    try:
        # Modifier le statut
        cursor.execute("""
            UPDATE offers
            SET status = ?
            WHERE id = ?
        """, (new_status, offer_id))

        # Enregistrer l'historique
        cursor.execute("""
            INSERT INTO offer_history
            (offer_id, old_status, new_status, note)
            VALUES (?, ?, ?, ?)
        """, (
            offer_id,
            old_status,
            new_status,
            note
        ))

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

#Historique des candidatures
def get_offer_history(offer_id):
    """Récupère l'historique des statuts d'une offre de stage."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT old_status, new_status, note, created_at
        FROM offer_history
        WHERE offer_id = ?
        ORDER BY created_at DESC
    """, (offer_id,))

    history = cursor.fetchall()

    conn.close()

    return history 
