from flask import Flask, request, redirect, url_for, render_template, jsonify, send_from_directory, flash
from flask_mail import Mail, Message
import mysql.connector
import stripe
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages
# Configure St
stripe.api_key = 'your_stripe_secret_key'

# Configuration
UPLOAD_FOLDER = 'uploads'
GALLERY_FOLDER = 'gallery'
MAX_VIDEO_SIZE_MB = 500
MAX_TOTAL_SIZE_GB = 16
MAX_GALLERY_SIZE = 16 * 1024 * 1024 * 1024  # 16 GB
MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500 MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mkv',"docx", 'pdf'}
# Fixed amount (in paise) to be charged (e.g., Rs 500 = 50000 paise)
FIXED_AMOUNT = 50000  # Rs 500


PERMANENT_FILES = [
    'school_books.pdf', 'school_fees.pdf', 'bus_fees.pdf','topers_last.pdf',
    'admission.jpg'
    'bg-image1.jpg', 'bg-image2.jpg', 'bg-image3.jpg', 'bg-image4.jpg',
    'image1.jpg', 'image2.jpg', 'image3.jpg',
    'video1.mp4', 'video2.mp4', 'video3.mp4', 
    'computer_lab.jpg', 'library.jpg', 'halping-hands.jpg', 'teachers.jpg',
    'play_ground.jpg', 'science_lab.jpg', 'bus_services.jpg', 'school-image.jpg',
    'school_1st.jpg', 'school_2nd.jpg','school_3rd.jpg',
    'nursary_first.jpg' , 'nursary_second.jpg', 'nursary_third.jpg',
    'kg1_first.jpg' , 'kg1_second.jpg', 'kg1_third.jpg', 'kg2_first.jpg' , 'kg2_second.jpg', 'kg2_third.jpg',
    '1st_first.jpg' , '1st_second.jpg', '1st_third.jpg', '2nd_first.jpg' , '2nd_second.jpg', '2nd_third.jpg',
    '3rd_first.jpg' , '3rd_second.jpg', '3rd_third.jpg', '4th_first.jpg' , '4th_second.jpg', '4th_third.jpg',
    '5th_first.jpg' , '5th_second.jpg', '5th_third.jpg', '6th_first.jpg' , '6th_second.jpg', '6th_third.jpg',
    '7th_first.jpg' , '7th_second.jpg', '7th_third.jpg', '8th_first.jpg' , '8th_second.jpg', '8th_third.jpg',
    '9th_first.jpg' , '9th_second.jpg', '9th_third.jpg', '10th_first.jpg' , '10th_second.jpg', '10th_third.jpg',
    '11th_first.jpg' , '11th_second.jpg', '11th_third.jpg', '12th_first.jpg' , '12th_second.jpg', '12th_third.jpg'
]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GALLERY_FOLDER'] = GALLERY_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_VIDEO_SIZE_MB * 1024 * 1024  # 500 MB
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your email provider's SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'your_email_password'  # Your email password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Ensure the upload and gallery directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GALLERY_FOLDER, exist_ok=True)

# Function to check the total size of files in a directory
def total_size(directory):
    total = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            total += os.path.getsize(filepath)
    return total

# Database Configuration
db_config = {
    'user': 'root',
    'password': 'ro11@777#777',  # Replace with your MySQL password
    'host': 'localhost',
    'database': 'contact_db'
}

# Function to create a connection to the database
def create_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_contact_table():
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(200),
            email VARCHAR(200),
            phone VARCHAR(200),
            message TEXT
        )
        """)
        print("Contact table created successfully.")
        cursor.close()
        connection.close()

# Create Registration Table
def create_registration_table():
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            father_first_name VARCHAR(255),
            father_last_name VARCHAR(255),
            mother_first_name VARCHAR(255),
            mother_last_name VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(20),
            class VARCHAR(10),
            dob DATE,
            payment_method VARCHAR(50),
            payment_status BOOLEAN
        )
        """)
        print("Registration table created successfully.")
        cursor.close()
        connection.close()

# Route to check MySQL connection
@app.route('/check-mysql-connection')
def check_mysql_connection():
    connection = create_db_connection()
    if connection:
        connection.close()
        return "Connected successfully to MySQL!"
    else:
        return "Failed to connect to MySQL."

# Check if the uploaded file has an allowed extension
def allowed_file(filename):
    return filename in PERMANENT_FILES or ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

# Route to display the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and save data to the database
@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']

    # Save to the database
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO contacts (name, email, phone, message) VALUES (%s, %s, %s, %s)", 
                   (name, email, phone, message))
    connection.commit()
    connection.close()

    flash('Form submitted successfully!', 'success')
    return redirect(url_for('index'))

# Route to upload files
@app.route('/upload_gallery', methods=['GET', 'POST'])
def upload_gallery_file():
    if request.method == 'POST':
        files = request.files.getlist('files')
        for file in files:
            if file and allowed_file(file.filename):
                if file.content_length > MAX_VIDEO_SIZE and file.filename.rsplit('.', 1)[1].lower() in ['mp4']:
                    flash('File is too large! Videos must be under 500 MB.', 'danger')
                    continue
                filename = file.filename
                filepath = os.path.join(app.config['GALLERY_FOLDER'], filename)
                file.save(filepath)
                flash('File uploaded successfully!', 'success')
            else:
                flash('Invalid file type!', 'danger')
        return redirect(url_for('upload_gallery_file'))
    return render_template('upload_gallery.html')

#Route for the calendar page
@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/fastival')
def calender():
    return render_template('fastival.html')

# Route to display the gallery
@app.route('/gallery')
def gallery():
    image_files = [f for f in os.listdir(app.config['GALLERY_FOLDER']) if allowed_file(f) and f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
    video_files = [f for f in os.listdir(app.config['GALLERY_FOLDER']) if allowed_file(f) and f.lower().endswith('mp4')]
    return render_template('gallery.html', images=image_files, videos=video_files)

@app.route('/gallery_files/<filename>')
def gallery_file(filename):
    return send_from_directory(app.config['GALLERY_FOLDER'], filename)
    

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Route to handle file upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            filename = request.form.get('filename')  # File name should be provided from form input

            if filename not in PERMANENT_FILES:
                flash('Invalid filename!', 'danger')
                return jsonify({"error": "Invalid filename"}), 400

            if file and allowed_file(file.filename):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                flash('File uploaded successfully!', 'success')
                return redirect(url_for('upload_file'))

        if 'delete_filename' in request.form:
            filename = request.form['delete_filename']

            if filename in PERMANENT_FILES:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                    flash('File deleted successfully!', 'success')
                    return redirect(url_for('upload_file'))

    # Get existing files
    uploaded_files = {f: os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], f)) for f in PERMANENT_FILES}
    return render_template('upload.html', files=PERMANENT_FILES, uploaded_files=uploaded_files)

# Route to view and delete files
@app.route('/delete_page', methods=['GET', 'POST'])
def delete_page():
    if request.method == 'POST':
        file_to_delete = request.form.get('file_to_delete')
        if file_to_delete:
            file_path = os.path.join(app.config['GALLERY_FOLDER'], file_to_delete)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    flash(f'File {file_to_delete} deleted successfully!', 'success')
                except Exception as e:
                    flash(f'Error deleting file: {e}', 'danger')
            else:
                flash(f'File {file_to_delete} does not exist.', 'danger')
        return redirect(url_for('delete_page'))

    # List files in the upload directory
    files = [f for f in os.listdir(app.config['GALLERY_FOLDER']) if allowed_file(f)]
    return render_template('delete_page.html', files=files)


@app.route('/register_page')
def register_page():
    # Render the registration page
    return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        class_name = request.form.get('class')
        dob = request.form.get('dob')

        # Process the payment data here (usually, you would need to send the payment data to Google Pay API or another payment processor)

        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO registrations (first_name, last_name, email, phone, class, dob, payment_method, payment_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, email, phone, class_name, dob, 'google_pay', False))
            connection.commit()
            connection.close()

            # Send confirmation email
            msg = Message('Registration Confirmation',
                          sender='your_email@gmail.com',  # Your email address
                          recipients=[email])
            msg.body = f'Hi {first_name},\n\nThank you for registering. Your registration is successful!\n\nBest regards,\nYour Company'
            mail.send(msg)

            return redirect(url_for('payment_success'))
        else:
            flash('Failed to connect to the database.', 'danger')

    return render_template('register.html')

@app.route('/payment_success')
def payment_success():
    return render_template('payment_success.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

# Route to display the contacts
@app.route('/display_contacts')
def display_contacts():
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch all contacts from the 'contacts' table
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()

    cursor.close()
    connection.close()

    # Pass the contacts data to the HTML template
    return render_template('contacts.html', contacts=contacts)

# Customer Support Route
@app.route('/support')
def support():
    # Customer support details
    support_url = "https://www.yourwebsite.com/support"
    support_email = "support@yourwebsite.com"
    support_phone = "+1 (123) 456-7890"
    return render_template('support.html', url=support_url, email=support_email, phone=support_phone)

@app.route('/privacy')
def privacy_polices():
    return render_template('privacy.html')

# Route to handle deleting a contact
@app.route('/delete_contact/<int:id>')
def delete_contact(id):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
        connection.close()
        flash('Contact deleted successfully!', 'success')
    else:
        flash('Failed to connect to the database.', 'danger')
    
    return redirect(url_for('display_contacts'))

# Route to serve the PDF file
@app.route('/view_pdf')
def view_pdf():
    return render_template('pdf_viewer.html')

# Route to handle the actual PDF file download
@app.route('/pdf/<filename>')
def pdf_view(filename):
    return send_from_directory('pdfs', filename)

if __name__ == "__main__":
    # Call the functions to create the necessary tables
    create_contact_table()
    create_registration_table()
    
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000, debug=True)
