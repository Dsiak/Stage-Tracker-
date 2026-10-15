from db import get_connection, create_tables


def seed_database():
    create_tables()

    conn = get_connection()
    cursor = conn.cursor()


    # Ajouter les entreprises fictives
    companies = [
        ("TechNova", "https://technova.example", "Moncton"),
        ("DataVision", "https://datavision.example", "Montréal"),
        ("CyberPlus", "https://cyberplus.example", "Québec")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO companies (name, website, location)
        VALUES (?, ?, ?)
    """, companies)


    # Ajouter les compétences fictives
    skills = [
        ("Python",),
        ("C++",),
        ("SQL",),
        ("Git",),
        ("Linux",)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO skills (name)
        VALUES (?)
    """, skills)


    # Ajouter les offres de stage fictives
    offers = [
        (
            "Stage développeur Python",
            "Développer des fonctionnalités en Python.",
            "https://example.com/offre-1",
            "Moncton",
            "2027-02-28",
            "TechNova"
        ),
        (
            "Stage développeur C++",
            "Participer au développement d'applications en C++.",
            "https://example.com/offre-2",
            "Moncton",
            "2027-03-15",
            "TechNova"
        ),
        (
            "Stage analyste de données",
            "Analyser des données avec Python et SQL.",
            "https://example.com/offre-3",
            "Montréal",
            "2027-03-30",
            "DataVision"
        ),
        (
            "Stage administrateur Linux",
            "Participer à la gestion des systèmes Linux.",
            "https://example.com/offre-4",
            "Québec",
            "2027-04-15",
            "CyberPlus"
        ),
        (
            "Stage développeur web",
            "Participer au développement et aux tests d'une application web.",
            "https://example.com/offre-5",
            "Montréal",
            "2027-04-30",
            "DataVision"
        )
    ]

    for title, description, url, location, deadline, company_name in offers:
        cursor.execute("""
            INSERT OR IGNORE INTO offers (
                company_id, title, description, url, location, deadline
            )
            VALUES (
                (SELECT id FROM companies WHERE name = ?),
                ?, ?, ?, ?, ?
            )
        """, (
            company_name,
            title,
            description,
            url,
            location,
            deadline
        ))


    # Associer les offres aux compétences
    associations = {
        "Stage développeur Python": ["Python", "SQL", "Git"],
        "Stage développeur C++": ["C++", "Git"],
        "Stage analyste de données": ["Python", "SQL"],
        "Stage administrateur Linux": ["Linux"],
        "Stage développeur web": ["Python", "SQL", "Git"]
    }

    for offer_title, skill_names in associations.items():

        # Récupérer l'identifiant de l'offre
        cursor.execute(
            "SELECT id FROM offers WHERE title = ?",
            (offer_title,)
        )
        offer = cursor.fetchone()

        if offer is None:
            continue

        offer_id = offer[0]

        for skill_name in skill_names:

            # Récupérer l'identifiant de la compétence
            cursor.execute( 
                "SELECT id FROM skills WHERE name = ?",
                (skill_name,)
            )
            skill = cursor.fetchone()

            if skill is None:
                continue

            skill_id = skill[0]

            # Créer l'association
            cursor.execute("""
                INSERT OR IGNORE INTO offer_skills (offer_id, skill_id)
                VALUES (?, ?)
            """, (offer_id, skill_id))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_database()
    print("Les données fictives ont été ajoutées !") 