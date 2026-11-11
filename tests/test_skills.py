import sqlite3
import pytest
import db


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """Crée une base de données temporaire pour chaque test."""

    monkeypatch.setattr(db, "DB_NAME", tmp_path / "test_stages.db")

    db.create_tables()

    company_id = db.add_company("TechNova")

    offer_id = db.add_offer(
        company_id=company_id,
        title="Python Developer",
        url="https://example.com/offer-1"
    )

    return offer_id


def test_add_skill(test_db):
    """Vérifie l'ajout d'une compétence."""

    skill_id = db.add_skill("Python")

    assert skill_id == 1
    assert db.get_skills() == [(1, "Python")]


def test_get_skills(test_db):
    """Vérifie la récupération et le tri des compétences."""

    db.add_skill("Python")
    db.add_skill("Git")
    db.add_skill("SQL")

    skills = db.get_skills()

    assert [skill[1] for skill in skills] == [
        "Git", "Python", "SQL"
    ]


def test_add_offer_skill(test_db):
    """Vérifie l'association d'une compétence à une offre."""

    skill_id = db.add_skill("Python")

    added = db.add_offer_skill(test_db, skill_id)

    assert added is True
    assert db.get_offer_skills(test_db) == [(skill_id, "Python")]


def test_multiple_skills(test_db):
    """Vérifie qu'une offre peut avoir plusieurs compétences."""

    python_id = db.add_skill("Python")
    git_id = db.add_skill("Git")

    db.add_offer_skill(test_db, python_id)
    db.add_offer_skill(test_db, git_id)

    skills = db.get_offer_skills(test_db)

    assert skills == [
        (git_id, "Git"),
        (python_id, "Python")
    ]


def test_duplicate_skill(test_db):
    """Vérifie qu'une compétence ne peut pas être ajoutée deux fois."""

    db.add_skill("Python")

    with pytest.raises(sqlite3.IntegrityError):
        db.add_skill("Python")


def test_duplicate_association(test_db):
    """Vérifie qu'une association ne peut pas être dupliquée."""

    skill_id = db.add_skill("Python")

    first = db.add_offer_skill(test_db, skill_id)
    second = db.add_offer_skill(test_db, skill_id)

    assert first is True
    assert second is False


def test_invalid_skill_association(test_db):
    """Vérifie qu'une compétence inexistante ne peut pas être associée."""

    with pytest.raises(sqlite3.IntegrityError):
        db.add_offer_skill(test_db, 999)


def test_invalid_offer_association(test_db):
    """Vérifie qu'une offre inexistante ne peut pas être associée."""

    skill_id = db.add_skill("Python")

    with pytest.raises(sqlite3.IntegrityError):
        db.add_offer_skill(999, skill_id)