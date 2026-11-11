import sqlite3
import pytest
import db


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """Crée une base de données temporaire pour chaque test."""

    monkeypatch.setattr(db, "DB_NAME", tmp_path / "test_stages.db")

    db.create_tables()
    company_id = db.add_company("TechNova")

    return company_id


def test_add_offer(test_db):
    """Vérifie qu'une offre peut être ajoutée."""

    offer_id = db.add_offer(
        company_id=test_db,
        title="Python Developer",
        url="https://example.com/offer-1"
    )

    assert offer_id == 1

    offers = db.get_offers()

    assert len(offers) == 1
    assert offers[0][2] == "Python Developer"


def test_get_offers(test_db):
    """Vérifie la récupération des offres."""

    db.add_offer(
        company_id=test_db,
        title="Data Analyst",
        url="https://example.com/offer-2"
    )

    offers = db.get_offers()

    assert len(offers) == 1
    assert offers[0][1] == "TechNova"
    assert offers[0][2] == "Data Analyst"


def test_update_offer(test_db):
    """Vérifie la modification d'une offre."""

    offer_id = db.add_offer(
        company_id=test_db,
        title="Python Developer",
        url="https://example.com/offer-3"
    )

    updated = db.update_offer(
        offer_id=offer_id,
        company_id=test_db,
        title="Senior Python Developer",
        url="https://example.com/offer-3"
    )

    assert updated is True
    assert db.get_offers()[0][2] == "Senior Python Developer"


def test_delete_offer(test_db):
    """Vérifie la suppression d'une offre."""

    offer_id = db.add_offer(
        company_id=test_db,
        title="Web Developer",
        url="https://example.com/offer-4"
    )

    deleted = db.delete_offer(offer_id)

    assert deleted is True
    assert len(db.get_offers()) == 0


def test_update_nonexistent_offer(test_db):
    """Vérifie la modification d'une offre inexistante."""

    updated = db.update_offer(
        offer_id=999,
        company_id=test_db,
        title="Unknown",
        url="https://example.com/unknown"
    )

    assert updated is False


def test_delete_nonexistent_offer(test_db):
    """Vérifie la suppression d'une offre inexistante."""

    deleted = db.delete_offer(999)

    assert deleted is False


def test_duplicate_url(test_db):
    """Vérifie qu'une URL ne peut pas être utilisée deux fois."""

    db.add_offer(
        company_id=test_db,
        title="First Offer",
        url="https://example.com/duplicate"
    )

    with pytest.raises(sqlite3.IntegrityError):
        db.add_offer(
            company_id=test_db,
            title="Second Offer",
            url="https://example.com/duplicate"
        )


def test_invalid_company(test_db):
    """Vérifie qu'une offre doit appartenir à une entreprise existante."""

    with pytest.raises(sqlite3.IntegrityError):
        db.add_offer(
            company_id=999,
            title="Invalid Offer",
            url="https://example.com/invalid"
        )