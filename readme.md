# Recensement - Application Flask & PostgreSQL

Cette application permet de collecter des données de recensement via un formulaire web et de les enregistrer dans une base PostgreSQL.  
**La base de données PostgreSQL est hébergée sur Supabase.**

---

## Fonctionnalités

- Formulaire web complet pour saisir les informations d’un individu et de son foyer
- Enregistrement sécurisé des données dans une base PostgreSQL distante (hébergée sur Supabase)
- Affichage d’un récapitulatif des données soumises après validation
- Gestion des champs complexes (cases à cocher, listes, dates, etc.)

---

## Prérequis

- Python 3.8 ou supérieur
- [pipenv](https://pipenv.pypa.io/en/latest/) pour la gestion des dépendances
- Un compte Supabase avec une base PostgreSQL configurée

---

## Installation

1. **Clone le dépôt :**
   ```bash
   git clone <url-du-repo>
   cd recensement
   ```

2. **Installe les dépendances :**
   ```bash
   pipenv install flask psycopg2-binary python-dotenv
   ```

3. **Configure la base de données :**
   - Crée un fichier `.env` à la racine du projet avec :
     ```
     DATABASE_URL=postgresql://<utilisateur>:<motdepasse>@<hôte>:<port>/<nom_base>
     ```
   - Exemple pour Supabase :
     ```
     DATABASE_URL=postgresql://postgres.puybzvngwxhacahahxrs:Merveil1234@aws-0-us-east-2.pooler.supabase.com:6543/postgres
     ```

4. **Crée la table `individus` dans ta base PostgreSQL Supabase** (exemple de structure) :
   ```sql
   CREATE TABLE individus (
       household_id TEXT,
       individual_sequence INTEGER,
       last_name TEXT,
       first_name TEXT,
       sex TEXT,
       dob DATE,
       age INTEGER,
       birth_country TEXT,
       birth_region TEXT,
       birth_city TEXT,
       nationality TEXT,
       marital_status TEXT,
       relationship_to_head TEXT,
       address_street_number TEXT,
       address_quarter TEXT,
       address_city TEXT,
       address_region TEXT,
       address_country TEXT,
       address_postal_code TEXT,
       housing_type TEXT,
       occupancy_status TEXT,
       num_rooms INTEGER,
       water_source TEXT,
       toilet_type TEXT,
       lighting_energy TEXT,
       cooking_energy TEXT,
       waste_disposal TEXT,
       education_level TEXT,
       school_status TEXT,
       school_type TEXT,
       activity_status TEXT,
       main_profession TEXT,
       economic_sector TEXT,
       employment_status TEXT,
       workplace TEXT,
       residence_status TEXT,
       residence_duration INTEGER,
       prev_residence_country TEXT,
       prev_residence_region TEXT,
       prev_residence_city TEXT,
       reason_for_move TEXT,
       health_status TEXT,
       difficulty_vision BOOLEAN,
       difficulty_vision_level TEXT,
       difficulty_hearing BOOLEAN,
       difficulty_hearing_level TEXT,
       difficulty_mobility BOOLEAN,
       difficulty_mobility_level TEXT,
       difficulty_cognition BOOLEAN,
       difficulty_cognition_level TEXT,
       difficulty_selfcare BOOLEAN,
       difficulty_selfcare_level TEXT,
       difficulty_communication BOOLEAN,
       difficulty_communication_level TEXT,
       healthcare_access TEXT,
       ethnic_origin TEXT,
       religion TEXT,
       spoken_languages TEXT,
       num_mobile_phones INTEGER,
       internet_access TEXT
   );
   ```

---

## Utilisation

1. **Lance l’application :**
   ```bash
   pipenv run python app.py
   ```

2. **Accède au formulaire :**
   - Ouvre [http://127.0.0.1:5000](http://127.0.0.1:5000) dans ton navigateur.

3. **Remplis et soumets le formulaire.**
   - Les données sont enregistrées dans la base PostgreSQL hébergée sur Supabase.
   - Un récapitulatif des données soumises s’affiche sur la page de succès.

---

## Personnalisation

- Modifie le fichier `templates/formulaire.html` pour adapter le formulaire à tes besoins.
- Modifie la structure de la table `individus` si tu ajoutes ou retires des champs.
- Le fichier `templates/success.html` affiche le récapitulatif des données.

---

## Dépannage

- Si tu rencontres une erreur de base de données, vérifie la variable `DATABASE_URL` dans `.env` et la structure de ta table sur Supabase.
- Pour afficher les erreurs détaillées, le code affiche temporairement les messages d’erreur PostgreSQL dans la réponse JSON.

---

## Licence

Projet open source sous licence MIT.