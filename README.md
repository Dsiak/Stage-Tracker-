# 🎯 Stage Tracker

**Organize internship opportunities, manage applications, and simplify your internship search.**

Stage Tracker is a Python-based application designed to help students organize their internship search in one place.

Instead of managing opportunities across spreadsheets, emails, and multiple job platforms, Stage Tracker provides a foundation for centralizing internship offers, organizing company information, and managing the skills associated with each opportunity.

The project aims to make the internship search more structured, efficient, and accessible.

## ✨ Features

Stage Tracker brings together several tools for internship management:

| Feature | Description |
|---|---|
| 🏢 Company Management | Organize company information, including names, websites, and locations. |
| 💼 Internship Offers | Store internship opportunities with job titles, descriptions, URLs, locations, and deadlines. |
| 🧠 Skills Management | Organize technical skills and associate them with internship opportunities. |
| 🗄️ Data Management | Create, retrieve, update, and delete records using a relational database. |
| 🔗 Database Relationships | Connect companies, internship offers, and technical skills. |
| 🧪 Automated Testing | Verify database operations and data integrity using automated tests. |
| 🖥️ Web Interface | Access the application through a Streamlit-based interface. |

## 🛠️ Technologies

**Programming Language**
- Python

**User Interface**
- Streamlit

**Database**
- SQLite
- SQL

**Testing**
- pytest

**Version Control**
- Git
- GitHub

## 🗄️ Database Architecture

Stage Tracker uses a relational SQLite database to organize internship opportunities and their associated information.

The database contains four interconnected tables:

| Table | Description |
|---|---|
| `companies` | Stores company names, websites, and locations. |
| `offers` | Stores internship offers and their associated companies. |
| `skills` | Stores technical skills such as Python, C++, SQL, and Git. |
| `offer_skills` | Establishes a many-to-many relationship between offers and skills. |

### Database Relationships

```text
        COMPANIES
        ─────────
        id
        name
        website
        location
            │
            │ 1
            │
            │ N
            ▼
          OFFERS
        ─────────
        id
        company_id
        title
        description
        url
        location
        deadline
            │
            │ 1
            │
            │ N
            ▼
       OFFER_SKILLS
       ────────────
       offer_id
       skill_id
            │
            │ N
            │
            │ 1
            ▼
          SKILLS
        ─────────
        id
        name
```

The database uses foreign keys to maintain relationships between records.

Additional constraints prevent duplicate company names, internship URLs, and skill names.

## 🧪 Automated Testing

Stage Tracker includes automated tests using **pytest**.

The test suite covers:

- Creating, updating, and deleting companies.
- Adding, retrieving, updating, and deleting internship offers.
- Managing technical skills.
- Associating multiple skills with internship offers.
- Preventing duplicate records.
- Validating foreign key relationships.
- Handling attempts to modify nonexistent records.

Tests use isolated SQLite databases to avoid modifying actual application data.

To run the tests:

```bash
python -m pytest -v
```

## 🚀 Getting Started

### Prerequisites

Before running Stage Tracker, make sure you have:

- Python 3 installed
- Git installed
- Streamlit
- pytest

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Dsiak/Stage-Tracker-.git
```

**2. Navigate to the project directory**

```bash
cd Stage-Tracker-
```

**3. Create a virtual environment**

```bash
python -m venv .venv
```

**4. Activate the virtual environment**

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

**5. Install dependencies**

```bash
python -m pip install streamlit pytest
```

**6. Initialize the database**

```bash
python db.py
```

**7. Optional: Add sample data**

```bash
python seed.py
```

The sample dataset includes fictional companies, internship opportunities, and technical skills for demonstration purposes.

**8. Launch the application**

```bash
python -m streamlit run app.py
```

Streamlit will open the application in your web browser.

## 📁 Project Structure

```text
Stage-Tracker-/
│
├── app.py
│   └── Streamlit application
│
├── db.py
│   └── Database schema and CRUD operations
│
├── seed.py
│   └── Sample data generation
│
├── tests/
│   ├── test_db.py
│   ├── test_offers.py
│   └── test_skills.py
│
├── .gitignore
├── LICENSE
└── README.md
```

A local `stages.db` file is generated when the database is initialized.

## 🎯 Project Objectives

Stage Tracker was created to address a common challenge faced by students: managing multiple internship opportunities throughout the recruitment process.

The project's main objectives are to:

1. Centralize internship information.
2. Simplify application organization.
3. Reduce missed deadlines and follow-ups.
4. Help students identify opportunities matching their skills.
5. Provide a clear overview of their internship search.

The project also demonstrates practical software development concepts, including database design, Python programming, automated testing, and user interface development.

## 🔮 Future Improvements

Potential future enhancements include:

- Application status tracking and history.
- Automated follow-up reminders.
- Skill-based compatibility scoring.
- Resume and job description comparison.
- Advanced filtering by location, skills, and deadlines.
- Application statistics and visualizations.
- Automatic internship offer collection from supported sources.
- Email notifications for important deadlines.
- Data export functionality.
- Improved mobile accessibility.

## 👨‍💻 Author

**Drissa Siaka Coulibaly**

Applied Computer Science Student  
Université de Moncton, Canada

## 📄 License

This project is licensed under the MIT License.

See the `LICENSE` file for details.