import os
import psycopg2
from flask import Flask, request, jsonify, render_template, redirect, url_for
from dotenv import load_dotenv
import uuid
from datetime import datetime

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def index():
    return render_template('formulaire.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        # Correction : gérer les listes (spoken_languages) et booléens
        data = request.form.to_dict(flat=False)
        # spoken_languages peut être une liste, les autres sont uniques
        data = {k: (v[0] if len(v) == 1 else v) for k, v in data.items()}

        if 'household_id' not in data or not data['household_id'] or data['household_id'] == 'AUTO-GÉNÉRÉ':
            data['household_id'] = str(uuid.uuid4())

        conn = get_db_connection()
        cur = conn.cursor()

        columns = []
        values_placeholders = []
        values_data = []

        field_mapping = {
            'household_id': 'household_id',
            'individual_sequence': 'individual_sequence',
            'last_name': 'last_name',
            'first_name': 'first_name',
            'sex': 'sex',
            'dob': 'dob',
            'age': 'age',
            'birth_country': 'birth_country',
            'birth_region': 'birth_region',
            'birth_city': 'birth_city',
            'nationality': 'nationality',
            'marital_status': 'marital_status',
            'relationship_to_head': 'relationship_to_head',
            'address_street_number': 'address_street_number',
            'address_quarter': 'address_quarter',
            'address_city': 'address_city',
            'address_region': 'address_region',
            'address_country': 'address_country',
            'address_postal_code': 'address_postal_code',
            'housing_type': 'housing_type',
            'occupancy_status': 'occupancy_status',
            'num_rooms': 'num_rooms',
            'water_source': 'water_source',
            'toilet_type': 'toilet_type',
            'lighting_energy': 'lighting_energy',
            'cooking_energy': 'cooking_energy',
            'waste_disposal': 'waste_disposal',
            'education_level': 'education_level',
            'school_status': 'school_status',
            'school_type': 'school_type',
            'activity_status': 'activity_status',
            'main_profession': 'main_profession',
            'economic_sector': 'economic_sector',
            'employment_status': 'employment_status',
            'workplace': 'workplace',
            'residence_status': 'residence_status',
            'residence_duration': 'residence_duration',
            'prev_residence_country': 'prev_residence_country',
            'prev_residence_region': 'prev_residence_region',
            'prev_residence_city': 'prev_residence_city',
            'reason_for_move': 'reason_for_move',
            'health_status': 'health_status',
            'difficulty_vision': 'difficulty_vision',
            'difficulty_vision_level': 'difficulty_vision_level',
            'difficulty_hearing': 'difficulty_hearing',
            'difficulty_hearing_level': 'difficulty_hearing_level',
            'difficulty_mobility': 'difficulty_mobility',
            'difficulty_mobility_level': 'difficulty_mobility_level',
            'difficulty_cognition': 'difficulty_cognition',
            'difficulty_cognition_level': 'difficulty_cognition_level',
            'difficulty_selfcare': 'difficulty_selfcare',
            'difficulty_selfcare_level': 'difficulty_selfcare_level',
            'difficulty_communication': 'difficulty_communication',
            'difficulty_communication_level': 'difficulty_communication_level',
            'healthcare_access': 'healthcare_access',
            'ethnic_origin': 'ethnic_origin',
            'religion': 'religion',
            'spoken_languages': 'spoken_languages',
            'num_mobile_phones': 'num_mobile_phones',
            'internet_access': 'internet_access'
        }

        difficulty_fields = [
            'difficulty_vision', 'difficulty_hearing', 'difficulty_mobility',
            'difficulty_cognition', 'difficulty_selfcare', 'difficulty_communication'
        ]

        for html_name, db_column in field_mapping.items():
            if html_name in data:
                value = data[html_name]
                if db_column not in columns:
                    columns.append(db_column)
                    # Conversion des types
                    if html_name in ['individual_sequence', 'age', 'residence_duration', 'num_rooms', 'num_mobile_phones']:
                        try:
                            values_data.append(int(value) if value else None)
                        except ValueError:
                            values_data.append(None)
                    elif html_name in difficulty_fields:
                        values_data.append(value == 'on' or value is True)
                    elif html_name == 'dob':
                        try:
                            if value:
                                datetime.strptime(value, "%Y-%m-%d")
                                values_data.append(value)
                            else:
                                values_data.append(None)
                        except ValueError:
                            values_data.append(None)
                    elif html_name == 'spoken_languages':
                        if isinstance(value, list):
                            values_data.append(','.join(value))
                        else:
                            values_data.append(value)
                    else:
                        values_data.append(value)
                    values_placeholders.append('%s')
            elif html_name in difficulty_fields:
                if db_column not in columns:
                    columns.append(db_column)
                    values_data.append(False)
                    values_placeholders.append('%s')
                level_field = f'{html_name}_level'
                if level_field in field_mapping and field_mapping[level_field] not in columns:
                    columns.append(field_mapping[level_field])
                    values_data.append(data[level_field] if level_field in data else None)
                    values_placeholders.append('%s')
            elif html_name.endswith('_level') and html_name not in data and field_mapping[html_name] not in columns:
                columns.append(field_mapping[html_name])
                values_data.append(None)
                values_placeholders.append('%s')

        insert_query = f"INSERT INTO individus ({', '.join(columns)}) VALUES ({', '.join(values_placeholders)})"
        cur.execute(insert_query, values_data)
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('success'))

    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    except Exception:
        return jsonify({'error': "Erreur inattendue."}), 500

if __name__ == '__main__':
    app.run(debug=True)