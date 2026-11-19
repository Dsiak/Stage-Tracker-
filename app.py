import streamlit as st
import pandas as pd
import sqlite3

from urllib.parse import urlsplit

from db import (
    create_tables,
    get_or_create_company,
    add_offer,
    get_offers_with_status,
    get_or_create_skill,
    add_offer_skill,
    get_offer_skills,
    prepare_tracking,
    update_offer_status,
    get_offer_history
)



# CONFIGURATION
st.set_page_config(
    page_title="Stage Tracker",
    page_icon="🎯",
    layout="wide"
)

create_tables()
prepare_tracking()

STATUTS = [
    "À postuler",
    "Candidature envoyée",
    "Entretien",
    "Acceptée",
    "Refusée"
]


# VALIDATION DES LIENS
def valid_url(url):
    """Vérifie le format d'une URL web."""

    try:
        adresse = urlsplit(url)

        return (
            adresse.scheme in ("http", "https")
            and bool(adresse.hostname)
            and "." in adresse.hostname
            and not any(c.isspace() for c in url)
        )

    except ValueError:
        return False


# INTERFACE PRINCIPALE
st.title("🎯 Stage Tracker")
st.write("Bienvenue dans ton gestionnaire de candidatures de stage !")

page = st.sidebar.radio(
    "Navigation",
    ["Accueil", "Offres", "Candidatures", "Statistiques"]
)


# PAGE ACCUEIL
if page == "Accueil":

    st.header("🏠 Tableau de bord")

    offres = get_offers_with_status()

    total = len(offres)

    candidatures = sum(
        1 for offre in offres
        if offre[7] != "À postuler"
    )

    entretiens = sum(
        1 for offre in offres
        if offre[7] == "Entretien"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Offres enregistrées", total)
    col2.metric("Candidatures", candidatures)
    col3.metric("Entretiens", entretiens)


# PAGE OFFRES
elif page == "Offres":

    st.header("💼 Offres de stage")

    # FORMULAIRE D'AJOUT
    st.subheader("➕ Ajouter une offre")

    with st.form("formulaire_offre"):

        entreprise = st.text_input("Entreprise *")
        titre = st.text_input("Titre du poste *")
        lien = st.text_input("Lien de l'offre *")
        lieu = st.text_input("Lieu")

        description = st.text_area(
            "Description du poste"
        )

        date_limite = st.date_input(
            "Date limite",
            value=None
        )

        competences = st.text_input(
            "Compétences requises",
            placeholder="Python, SQL, JavaScript"
        )

        ajouter = st.form_submit_button(
            "Ajouter l'offre"
        )

    # ENREGISTREMENT
    if ajouter:

        entreprise = entreprise.strip()
        titre = titre.strip()
        lien = lien.strip()
        lieu = lieu.strip()
        description = description.strip()

        if not entreprise or not titre or not lien:

            st.error(
                "Veuillez remplir tous les champs obligatoires."
            )

        elif not valid_url(lien):

            st.error(
                "Veuillez entrer un lien web valide."
            )

        else:

            try:

                company_id = get_or_create_company(
                    entreprise
                )

                deadline = (
                    date_limite.isoformat()
                    if date_limite is not None
                    else None
                )

                offer_id = add_offer(
                    company_id=company_id,
                    title=titre,
                    url=lien,
                    description=description or None,
                    location=lieu or None,
                    deadline=deadline
                )

                # Enregistrer les compétences
                liste_competences = {
                    competence.strip()
                    for competence in competences.split(",")
                    if competence.strip()
                }

                for competence in liste_competences:

                    skill_id = get_or_create_skill(
                        competence
                    )

                    add_offer_skill(
                        offer_id,
                        skill_id
                    )

                st.success(
                    "Offre enregistrée avec succès !"
                )

            except sqlite3.IntegrityError:

                st.error(
                    "Cette offre existe peut-être déjà."
                )

   
    # TABLEAU DES OFFRES
    st.divider()
    st.subheader("📄 Liste des offres")

    offres = get_offers_with_status()

    if offres:

        donnees = []

        for offre in offres:

            skills = get_offer_skills(offre[0])

            noms_skills = ", ".join(
                skill[1] for skill in skills
            )

            donnees.append(
                list(offre) + [noms_skills]
            )

        df = pd.DataFrame(
            donnees,
            columns=[
                "ID",
                "Entreprise",
                "Poste",
                "Description",
                "Lien",
                "Lieu",
                "Date limite",
                "Statut",
                "Compétences"
            ]
        )

        # FILTRES
        st.subheader("🔍 Rechercher une offre")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            recherche = st.text_input(
                "Rechercher un poste"
            )

        with col2:
            entreprises = ["Toutes"] + sorted(
                df["Entreprise"].dropna().unique().tolist()
            )

            filtre_entreprise = st.selectbox(
                "Entreprise",
                entreprises
            )

        with col3:
            lieux = ["Tous"] + sorted(
                df["Lieu"].dropna().unique().tolist()
            )

            filtre_lieu = st.selectbox(
                "Lieu",
                lieux
            )

        with col4:
            filtre_statut = st.selectbox(
                "Statut",
                ["Tous"] + STATUTS
            )

        # APPLIQUER LES FILTRES
        df_filtre = df.copy()

        if recherche:

            df_filtre = df_filtre[
                df_filtre["Poste"].str.contains(
                    recherche,
                    case=False,
                    na=False,
                    regex=False
                )
            ]

        if filtre_entreprise != "Toutes":

            df_filtre = df_filtre[
                df_filtre["Entreprise"] == filtre_entreprise
            ]

        if filtre_lieu != "Tous":

            df_filtre = df_filtre[
                df_filtre["Lieu"] == filtre_lieu
            ]

        if filtre_statut != "Tous":

            df_filtre = df_filtre[
                df_filtre["Statut"] == filtre_statut
            ]

        # AFFICHER LES RÉSULTATS
        st.dataframe(
            df_filtre,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Lien": st.column_config.LinkColumn(
                    "Lien de l'offre"
                )
            }
        )

        st.caption(
            f"{len(df_filtre)} offre(s) trouvée(s) "
            f"sur {len(df)}"
        )

    else:

        st.info(
            "Aucune offre enregistrée pour le moment."
        )


# PAGE CANDIDATURES
elif page == "Candidatures":

    st.header("📋 Mes candidatures")

    if st.session_state.pop("candidature_saved", False):
        st.success("Candidature mise à jour avec succès !")

    offres = get_offers_with_status()

    if offres:

        # AFFICHER LES CANDIDATURES
        df = pd.DataFrame(
            offres,
            columns=[
                "ID",
                "Entreprise",
                "Poste",
                "Description",
                "Lien",
                "Lieu",
                "Date limite",
                "Statut"
            ]
        )

        candidatures = df[
            df["Statut"] != "À postuler"
        ]

        st.subheader("📄 Candidatures enregistrées")

        if not candidatures.empty:

            st.dataframe(
                candidatures[
                    [
                        "Entreprise",
                        "Poste",
                        "Statut",
                        "Date limite"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Aucune candidature envoyée."
            )

        st.divider()

        # MODIFIER UNE CANDIDATURE
        st.subheader("✏️ Gérer une candidature")

        # Sélectionner une offre
        options = {
            offre[0]: f"{offre[1]} - {offre[2]} (ID {offre[0]})"
            for offre in offres
        }

        offer_id = st.selectbox(
            "Sélectionner une offre",
            list(options.keys()),
            format_func=lambda x: options[x]
        )

        # Récupérer son statut actuel
        offre_selectionnee = next(
            offre for offre in offres
            if offre[0] == offer_id
        )

        statut_actuel = offre_selectionnee[7]

        with st.form("formulaire_candidature"):

            nouveau_statut = st.selectbox(
                "Statut de la candidature",
                STATUTS,
                index=STATUTS.index(statut_actuel)
            )

            note = st.text_area(
                "Ajouter une note",
                placeholder="Exemple : Entretien prévu vendredi."
            )

            enregistrer = st.form_submit_button(
                "Enregistrer les modifications"
            )

        if enregistrer:

            if (
                nouveau_statut == statut_actuel
                and not note.strip()
            ):

                st.warning(
                    "Aucune modification à enregistrer."
                )

            else:

                updated = update_offer_status(
                    offer_id,
                    nouveau_statut,
                    note
                )

                if updated:
                    st.session_state["candidature_saved"] = True
                    st.rerun()

                else:
                    st.error(
                        "Impossible de modifier cette candidature."
                    )

        # HISTORIQUE
        st.divider()

        st.subheader("🕒 Historique de la candidature")

        historique = get_offer_history(
            offer_id
        )

        if historique:

            df_historique = pd.DataFrame(
                historique,
                columns=[
                    "Date (UTC)",
                    "Ancien statut",
                    "Nouveau statut",
                    "Note"
                ]
            )

            st.dataframe(
                df_historique,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "Aucun historique disponible."
            )

    else:

        st.info(
            "Ajoutez d'abord une offre de stage."
        )


# ==========================================
# PAGE STATISTIQUES
# ==========================================

elif page == "Statistiques":

    st.header("📊 Statistiques")

    offres = get_offers_with_status()

    if offres:

        statuts = [
            offre[7] for offre in offres
        ]

        df = pd.DataFrame({
            "Statut": statuts
        })

        statistiques = (
            df["Statut"]
            .value_counts()
        )

        st.bar_chart(statistiques)

    else:

        st.info(
            "Aucune donnée disponible."
        )