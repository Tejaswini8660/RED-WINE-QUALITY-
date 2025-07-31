from flask import Flask, render_template, request, redirect, jsonify
from utils.db import db
from models.wine import Wine

# Initialize Flask App
app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Wine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

# ------------------- ROUTES -------------------

@app.route('/')
def index():
    """Homepage that displays all wine records."""
    wines = Wine.query.all()
    return render_template('index.html', content=wines)


@app.route('/dashboard')
def dashboard():
    """Renders the dashboard page."""
    wines = Wine.query.all()

    # Prepare data for Chart.js
    data = {
        "fixed_acidity": [wine.fixed_acidity for wine in wines],
        "volatile_acidity": [wine.volatile_acidity for wine in wines],
        "citric_acid": [wine.citric_acid for wine in wines],
        "residual_sugar": [wine.residual_sugar for wine in wines],
        "chlorides": [wine.chlorides for wine in wines],
        "ids": [wine.id for wine in wines],
    }

    return render_template('dashboard.html', data=data)





@app.route('/about')
def about():
    """Renders the About Us page."""
    return render_template('about.html')


@app.route('/winepark')
def winepark():
    """Renders the About Us page."""
    return render_template('winepark.html')

@app.route('/winepark/redwinequalitybrand')
def redwinequalitybrand():
    """Renders the About Us page."""
    return render_template('redwinequalitybrand.html')

@app.route('/winepark/frenchwinesquality')
def frenchwinesquality():
    """Renders the About Us page."""
    return render_template('frenchwinesquality.html')

@app.route('/winepark/indianwinequality')
def indianwinequality():
    """Renders the About Us page."""
    return render_template('indianwinequality.html')

@app.route('/winepark/rosewinequalitybrand')
def rosewinequalitybrand():
    """Renders the About Us page."""
    return render_template('rosewinequalitybrand.html')

@app.route('/winepark/sweetwinequality')
def sweetwinequality():
    """Renders the About Us page."""
    return render_template('sweetwinequality.html')

@app.route('/winepark/whitewinequalitybrand')
def whitewinequalitybrand():
    """Renders the About Us page."""
    return render_template('whitewinequalitybrand.html')

@app.route('/winepark/document')
def document():
    """Renders the About Us page."""
    return render_template('document.html')


@app.route('/add_wine')
def add_wine():
    """Renders the 'Add Wine' page."""
    return render_template('add_wine.html')


@app.route('/contact')
def contact():
    """Renders the Contact Us page."""
    return render_template('contact.html')





@app.route('/submit', methods=['POST'])
def submit():
    """Handles form submission for adding a new wine."""
    form_data = request.form.to_dict()
    print(f"Form Data: {form_data}")

    try:
        wine = Wine(
            id=form_data.get('id'),
            fixed_acidity=form_data.get('fixed_acidity'),
            volatile_acidity=form_data.get('volatile_acidity'),
            citric_acid=form_data.get('citric_acid'),
            residual_sugar=form_data.get('residual_sugar'),
            chlorides=form_data.get('chlorides')
        )
        db.session.add(wine)
        db.session.commit()
        print("Wine submitted successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error during wine submission: {e}")
        return jsonify({'error': 'Failed to add wine.'}), 500

    return redirect('/')

#
# @app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
# def delete(id):
#     """Handles deletion of a wine record by ID."""
#     wine = Wine.query.get(id)
#
#     if not wine:
#         return jsonify({'message': 'Wine not found'}), 404
#
#     try:
#         db.session.delete(wine)
#         db.session.commit()
#         return jsonify({'message': 'Wine deleted successfully'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': f'Error during deletion: {e}'}), 500

@app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
def delete(id):
    """Handles deletion of a wine record by ID."""
    wine = Wine.query.get(id)

    if not wine:
        return jsonify({'message': 'Wine not found'}), 404

    try:
        db.session.delete(wine)
        db.session.commit()

        # Reassign IDs to maintain consecutive order
        wines = Wine.query.order_by(Wine.id).all()
        for index, wine in enumerate(wines, start=1):
            wine.id = index
        db.session.commit()

        return jsonify({'message': 'Wine deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error during deletion: {e}'}), 500


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    """Handles updating a wine record by ID."""
    wine = Wine.query.get_or_404(id)

    if request.method == 'POST':
        # Update wine properties from form data
        try:
            wine.fixed_acidity = request.form['fixed_acidity']
            wine.volatile_acidity = request.form['volatile_acidity']
            wine.citric_acid = request.form['citric_acid']
            wine.residual_sugar = request.form['residual_sugar']
            wine.chlorides = request.form['chlorides']

            db.session.commit()
            print("Wine updated successfully.")
            return redirect('/')
        except Exception as e:
            db.session.rollback()
            print(f"Error during wine update: {e}")
            return "An error occurred while updating the record."

    return render_template('update.html', wine=wine)


# ------------------- MAIN -------------------

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003, debug=True)
