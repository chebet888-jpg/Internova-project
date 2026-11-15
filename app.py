from flask import Flask, render_template, request, redirect, url_for, session, flash
app = Flask(__name__)
app.secret_key = "internova_secret_key"
ADMIN_EMAIL = "admin@internova.com"
ADMIN_PASSWORD = "admin123"
students = [
    {
        'id': 1,
        'name': 'Elizabeth Ngotho',
        'email': 'elizabeth@example.com',
        'reg_number': 'CSCI/2025/001',
        'status': 'Active'
    },
    {
        'id': 2,
        'name': 'Taffny Chepkoech',
        'email': 'taffny@example.com',
        'reg_number': 'CSCI/2025/002',
        'status': 'Active'
    },
    {
        'id': 3,
        'name': 'Tonny Ryan',
        'email': 'tonny@example.com',
        'reg_number': 'CSCI/2025/003',
        'status': 'Inactive'
    }
]
companies = [
    {
        'id': 1,
        'name': 'Safaricom',
        'email': 'info@safaricom.co.ke',
        'industry': 'Telecommunications',
        'status': 'Active'
    },
    {
        'id': 2,
        'name': 'Equity Bank',
        'email': 'info@equitybank.co.ke',
        'industry': 'Banking',
        'status': 'Active'
    },
    {
        'id': 3,
        'name': 'Tech Solutions',
        'email': 'info@techsolutions.com',
        'industry': 'Information Technology',
        'status': 'Inactive'
    }
]
internships = [
    {
        'id': 1,
        'title': 'Software Developer Intern',
        'company': 'Safaricom',
        'location': 'Nairobi',
        'deadline': '2026-12-15',
        'status': 'Active'
    },
    {
        'id': 2,
        'title': 'Data Analyst Intern',
        'company': 'Equity Bank',
        'location': 'Nairobi',
        'deadline': '2026-12-20',
        'status': 'Active'
    },
    {
        'id': 3,
        'title': 'IT Support Intern',
        'company': 'Tech Solutions',
        'location': 'Kiambu',
        'deadline': '2026-12-10',
        'status': 'Inactive'
    }
]
applications = [
    {
        'id': 1,
        'student': 'Elizabeth Ngotho',
        'company': 'Safaricom',
        'position': 'Software Developer Intern',
        'date': '2026-11-05',
        'status': 'Pending'
    },
    {
        'id': 2,
        'student': 'Taffny Chepkoech',
        'company': 'Equity Bank',
        'position': 'Data Analyst Intern',
        'date': '2026-11-06',
        'status': 'Approved'
    },
    {
        'id': 3,
        'student': 'Tonny Ryan',
        'company': 'Tech Solutions',
        'position': 'IT Support Intern',
        'date': '2026-11-07',
        'status': 'Rejected'
    }
]
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin'] = email
            return redirect(url_for('dashboard'))

        else:
            flash("Invalid email or password. Please try again.")

    return render_template('login.html')
@app.route('/dashboard')
def dashboard():

    if 'admin' not in session:
        return redirect(url_for('login'))
    stats = {
    'students': len(students),
    'companies': len(companies),
    'internships': len(internships),
    'applications': len(applications)
}
    recent_applications = list(reversed(applications[-5:]))

    return render_template(
        'dashboard.html',
        stats=stats,
        recent_applications=recent_applications
    )
# Manage Students
@app.route('/students')
def manage_students():

    if 'admin' not in session:
        return redirect(url_for('login'))

    search = request.args.get('search', '')

    filtered_students = [
        student for student in students
        if search.lower() in student['name'].lower()
        or search.lower() in student['email'].lower()
    ]

    return render_template(
        'students.html',
        students=filtered_students,
        search=search
    )


# Add Student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():

    if 'admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        new_student = {
            'id': max([s['id'] for s in students], default=0) + 1,
            'name': request.form['name'],
            'email': request.form['email'],
            'reg_number': request.form['reg_number'],
            'status': request.form['status']
        }

        students.append(new_student)

        flash('Student added successfully!')

        return redirect(url_for('manage_students'))

    return render_template('add_student.html')


# Activate or Deactivate Student
@app.route('/toggle_student/<int:student_id>')
def toggle_student(student_id):

    if 'admin' not in session:
        return redirect(url_for('login'))

    for student in students:
        if student['id'] == student_id:

            if student['status'] == 'Active':
                student['status'] = 'Inactive'
            else:
                student['status'] = 'Active'

            break

    return redirect(url_for('manage_students'))
@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):

    if 'admin' not in session:
        return redirect(url_for('login'))

    for student in students:
        if student['id'] == student_id:
            students.remove(student)
            flash('Student deleted successfully!')
            break

    return redirect(url_for('manage_students'))
@app.route('/companies')
def manage_companies():
    if 'admin' not in session:
        return redirect(url_for('login'))

    search = request.args.get('search', '')

    filtered_companies = [
        company for company in companies
        if search.lower() in company['name'].lower()
        or search.lower() in company['email'].lower()
    ]

    return render_template(
        'companies.html',
        companies=filtered_companies,
        search=search
    )


@app.route('/add_company', methods=['GET', 'POST'])
def add_company():
    if 'admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_company = {
            'id': max([c['id'] for c in companies], default=0) + 1,
            'name': request.form['name'],
            'email': request.form['email'],
            'industry': request.form['industry'],
            'status': request.form['status']
        }

        companies.append(new_company)
        flash('Company added successfully!')
        return redirect(url_for('manage_companies'))

    return render_template('add_company.html')


@app.route('/toggle_company/<int:company_id>')
def toggle_company(company_id):
    if 'admin' not in session:
        return redirect(url_for('login'))

    for company in companies:
        if company['id'] == company_id:
            if company['status'] == 'Active':
                company['status'] = 'Inactive'
            else:
                company['status'] = 'Active'
            break

    return redirect(url_for('manage_companies'))
@app.route('/delete_company/<int:company_id>', methods=['POST'])
def delete_company(company_id):

    if 'admin' not in session:
        return redirect(url_for('login'))

    for company in companies:
        if company['id'] == company_id:
            companies.remove(company)
            flash('Company deleted successfully!')
            break

    return redirect(url_for('manage_companies'))
@app.route('/internships')
def manage_internships():
    if 'admin' not in session:
        return redirect(url_for('login'))

    search = request.args.get('search', '')

    filtered_internships = [
        internship for internship in internships
        if search.lower() in internship['title'].lower()
        or search.lower() in internship['company'].lower()
    ]

    return render_template(
        'internships.html',
        internships=filtered_internships,
        search=search
    )


@app.route('/add_internship', methods=['GET', 'POST'])
def add_internship():
    if 'admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_internship = {
            'id': max([i['id'] for i in internships], default=0) + 1,
            'title': request.form['title'],
            'company': request.form['company'],
            'location': request.form['location'],
            'deadline': request.form['deadline'],
            'status': request.form['status']
        }

        internships.append(new_internship)
        flash('Internship added successfully!')
        return redirect(url_for('manage_internships'))

    return render_template('add_internship.html')


@app.route('/toggle_internship/<int:internship_id>')
def toggle_internship(internship_id):
    if 'admin' not in session:
        return redirect(url_for('login'))

    for internship in internships:
        if internship['id'] == internship_id:
            if internship['status'] == 'Active':
                internship['status'] = 'Inactive'
            else:
                internship['status'] = 'Active'
            break

    return redirect(url_for('manage_internships'))
@app.route('/delete_internship/<int:internship_id>', methods=['POST'])
def delete_internship(internship_id):

    if 'admin' not in session:
        return redirect(url_for('login'))

    for internship in internships:
        if internship['id'] == internship_id:
            internships.remove(internship)
            flash('Internship deleted successfully!')
            break

    return redirect(url_for('manage_internships'))

@app.route('/applications')
def manage_applications():
    if 'admin' not in session:
        return redirect(url_for('login'))

    search = request.args.get('search', '')
    print("SEARCH VALUE:", search)

    filtered_applications = [
        application for application in applications
        if search.lower() in application['student'].lower()
        or search.lower() in application['company'].lower()
        or search.lower() in application['position'].lower()
    ]

    return render_template(
        'applications.html',
        applications=filtered_applications,
        search=search
    )
@app.route('/application_details/<int:application_id>')
def application_details(application_id):
    if 'admin' not in session:
        return redirect(url_for('login'))

    selected_application = None

    for application in applications:
        if application['id'] == application_id:
            selected_application = application
            break

    if selected_application is None:
        flash('Application not found!')
        return redirect(url_for('manage_applications'))

    return render_template(
        'application_details.html',
        application=selected_application
    )
@app.route('/update_application/<int:application_id>/<status>', methods=['POST'])
def update_application(application_id, status):
    if 'admin' not in session:
        return redirect(url_for('login'))

    if status not in ['Approved', 'Rejected']:
        return redirect(url_for('manage_applications'))

    for application in applications:
        if application['id'] == application_id:
            application['status'] = status
            flash(f'Application {status.lower()} successfully!')
            break

    return redirect(url_for('manage_applications'))
@app.route('/delete_application/<int:application_id>', methods=['POST'])
def delete_application(application_id):

    if 'admin' not in session:
        return redirect(url_for('login'))

    for application in applications:
        if application['id'] == application_id:
            applications.remove(application)
            flash('Application deleted successfully!')
            break

    return redirect(url_for('manage_applications'))
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    global ADMIN_PASSWORD

    if 'admin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if current_password != ADMIN_PASSWORD:
            flash('Current password is incorrect!')
            return redirect(url_for('reset_password'))

        if new_password != confirm_password:
            flash('New passwords do not match!')
            return redirect(url_for('reset_password'))

        if len(new_password) < 8:
            flash('Password must be at least 8 characters long!')
            return redirect(url_for('reset_password'))

        ADMIN_PASSWORD = new_password

        flash('Password updated successfully!')
        return redirect(url_for('reset_password'))

    return render_template('reset_password.html')
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)
    # Temporary student records
