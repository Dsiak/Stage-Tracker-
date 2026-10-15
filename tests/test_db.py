import sqlite3
import uuid

import pytest
import db


@pytest.fixture
def database(monkeypatch):
    # Créer une base temporaire en mémoire partagée
    db_uri = f"file:{uuid.uuid4().hex}?mode=memory&cache=shared"

    monkeypatch.setattr(db, "DB_NAME", db_uri)

    # Garder une connexion ouverte pendant le test
    keeper = sqlite3.connect(db_uri, uri=True)

    # Créer les quatre tables
    db.create_tables()

    yield

    # Fermer la connexion après le test
    keeper.close()
    

def test_add_company(database):
    company_id = db.add_company(
        "TechNova",
        "https://technova.example",
        "Moncton"
    )

    companies = db.get_companies()

    assert company_id > 0
    assert len(companies) == 1
    assert companies[0][1] == "TechNova"


def test_update_company(database):
    company_id = db.add_company("TechNova")

    updated = db.update_company(
        company_id,
        "TechNova Canada",
        location="Moncton"
    )

    companies = db.get_companies()

    assert updated is True
    assert len(companies) == 1
    assert companies[0][1] == "TechNova Canada"


def test_delete_company(database):
    company_id = db.add_company("TechNova")

    deleted = db.delete_company(company_id)

    companies = db.get_companies()

    assert deleted is True
    assert len(companies) == 0