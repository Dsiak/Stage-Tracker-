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