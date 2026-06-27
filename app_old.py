from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import requests

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


app = Flask(__name__)

# Secret Key for Sessions

app.secret_key = "my_secret_key"

# MySQL Configuration

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''      # Put your MariaDB password here
app.config['MYSQL_DB'] = 'ai_repository_db'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

# -------------------------

# HOME

# -------------------------

@app.route('/')
def home():


    if 'user_id' in session:
        return redirect('/dashboard')

    return redirect('/login')


# -------------------------

# REGISTER

# -------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():


    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        # Check if email already exists
        cur.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            return "Email already registered"

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur.execute(
            """
            INSERT INTO users(name,email,password_hash)
            VALUES(%s,%s,%s)
            """,
            (name, email, hashed_password)
        )

        mysql.connection.commit()
        cur.close()

        return redirect('/login')

    return render_template('register.html')


# -------------------------

# LOGIN

# -------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():


    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            """
            SELECT user_id,name,email,password_hash
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cur.fetchone()

        cur.close()

        if user:

            stored_hash = user[3]

            if bcrypt.check_password_hash(stored_hash, password):

                session['user_id'] = user[0]
                session['name'] = user[1]

                return redirect('/dashboard')

        return "Invalid Email or Password"

    return render_template('login.html')
   

# -------------------------

# DASHBOARD

# -------------------------

@app.route('/dashboard')
def dashboard():
    # 1. Enforce authentication guard clause
    if 'user_id' not in session:
        return redirect('/login')

    try:
        # 2. Initialize the flask_mysqldb cursor
        cur = mysql.connection.cursor()

        # 3. Optimize: Fetch all counts efficiently or run queries safely
        # Prompts Count
        cur.execute("""
            SELECT COUNT(*) 
            FROM prompts 
            WHERE user_id = %s
        """, (session['user_id'],))
        prompt_count = cur.fetchone()[0]

        # Projects Count
        cur.execute("""
            SELECT COUNT(*) 
            FROM projects 
            WHERE user_id = %s
        """, (session['user_id'],))
        project_count = cur.fetchone()[0]

        # Favorites Count
        cur.execute("""
            SELECT COUNT(*) 
            FROM favorites 
            WHERE user_id = %s
        """, (session['user_id'],))
        favorite_count = cur.fetchone()[0]

        # AI Executions Count
        cur.execute("""
            SELECT COUNT(*) 
            FROM prompt_executions 
            WHERE user_id = %s
        """, (session['user_id'],))
        execution_count = cur.fetchone()[0]

        # 4. Clean up cursor resource
        cur.close()

        # 5. Render standard unified interface view
        return render_template(
            'dashboard.html',
            name=session.get('name', 'Developer'),
            prompt_count=prompt_count,
            project_count=project_count,
            favorite_count=favorite_count,
            execution_count=execution_count
        )

    except Exception as e:
        # In case the database drops during deployment, catch the error gracefully
        print(f"Dashboard Query Failure: {str(e)}")
        flash("An error occurred while loading your metrics dashboard layout.", "error")
        return redirect('/')

# search route to allow users to search for prompts by title or category
@app.route('/search')
def search():

    if 'user_id' not in session:
        return redirect('/login')

    keyword = request.args.get('query', '')
    category = request.args.get('category', '')

    cur = mysql.connection.cursor()

    sql = """
    SELECT
        p.prompt_id,
        p.title,
        p.prompt_text,
        c.category_name

    FROM prompts p

    JOIN categories c
    ON p.category_id = c.category_id

    WHERE p.user_id=%s
    """

    values = [session['user_id']]

    if keyword:

        sql += """
        AND (
            p.title LIKE %s
            OR p.prompt_text LIKE %s
        )
        """

        values.append(f"%{keyword}%")
        values.append(f"%{keyword}%")

    if category:

        sql += " AND c.category_name=%s"
        values.append(category)

    sql += " ORDER BY p.created_at DESC"

    cur.execute(sql, tuple(values))

    prompts = cur.fetchall()

    cur.close()

    return render_template(
        "search_results.html",
        prompts=prompts,
        categories=get_categories(),
        keyword=keyword,
        category=category
    )

def get_categories():

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT *
    FROM categories
    ORDER BY category_name
    """)

    data = cur.fetchall()

    cur.close()

    return data

#view prompt route to allow users to view the details of a specific prompt
@app.route('/prompt/<int:prompt_id>')
def view_prompt(prompt_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            p.prompt_id,
            p.title,
            p.prompt_text,
            c.category_name,
            p.created_at

        FROM prompts p

        JOIN categories c
        ON p.category_id = c.category_id

        WHERE p.prompt_id=%s
        AND p.user_id=%s
    """,
    (prompt_id, session['user_id']))

    prompt = cur.fetchone()

    cur.close()

    if not prompt:
        flash("Prompt not found.", "danger")
        return redirect('/prompts')

    return render_template(
        'view_prompt.html',
        prompt=prompt
    )

#run project route to allow users to run all prompts in a specific project and get responses from the OpenRouter API
@app.route('/run_project/<int:project_id>', methods=['POST'])
def run_project(project_id):
    
    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()
    selected_model = request.form['model']
    cur.execute("""
        SELECT
            p.prompt_id,
            p.prompt_text
        FROM prompts p
        JOIN project_prompts pp
        ON p.prompt_id = pp.prompt_id
        WHERE pp.project_id=%s
    """, (project_id,))

    prompts = cur.fetchall()

    results = []

    for prompt in prompts:

        prompt_id = prompt[0]
        prompt_text = prompt[1]

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": selected_model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt_text
                    }
                ],
                "max_tokens": 1000
            }
        )

        if response.status_code == 200:

            data = response.json()

            ai_response = data["choices"][0]["message"]["content"]

        else:

            ai_response = f"Error: {response.json().get('error', {}).get('message', 'Unknown error')}"



        cur.execute("""
            INSERT INTO prompt_executions
            (
                prompt_id,
                model_id,
                user_id,
                response_text
            )
            VALUES (%s,%s,%s,%s)
        """,
        (
            prompt_id,
            selected_model,
            session['user_id'],
            ai_response
        ))

        results.append({
            "prompt_id": prompt_id,
            "prompt": prompt_text,
            "response": ai_response,
            "model": selected_model
        })

    mysql.connection.commit()
    cur.close()

    return render_template(
        "project_results.html",
        results=results
    )


#project details route to allow users to view the details of a specific project

@app.route('/project/<int:project_id>')
def project_detail(project_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT *
        FROM projects
        WHERE project_id=%s
    """,
    (project_id,))

    project = cur.fetchone()

    cur.execute("""
        SELECT
            p.prompt_id,
            p.title
        FROM prompts p

        JOIN project_prompts pp
        ON p.prompt_id = pp.prompt_id

        WHERE pp.project_id=%s
    """,
    (project_id,))

    prompts = cur.fetchall()

    cur.close()

    return render_template(
        'project_detail.html',
        project=project,
        prompts=prompts
    )
#add prompt to project route to allow users to add a prompt to a specific project

@app.route('/add_prompt_to_project/<int:project_id>',
           methods=['GET','POST'])
def add_prompt_to_project(project_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        prompt_id = request.form['prompt_id']

        cur.execute("""
            INSERT IGNORE INTO project_prompts
            (project_id,prompt_id)
            VALUES(%s,%s)
        """,
        (
            project_id,
            prompt_id
        ))

        mysql.connection.commit()

        return redirect(f'/project/{project_id}')

    cur.execute("""
        SELECT prompt_id,title
        FROM prompts
        WHERE user_id=%s
    """,
    (session['user_id'],))

    prompts = cur.fetchall()

    return render_template(
        'add_prompt_to_project.html',
        prompts=prompts,
        project_id=project_id
    )

# view projects route to display all projects created by the logged-in user
@app.route('/projects')
def projects():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            p.project_id,
            p.title,
            c.category_name,
            p.status
        FROM projects p
        JOIN categories c
            ON p.category_id = c.category_id
        WHERE p.user_id=%s
    """, (session['user_id'],))

    projects = cur.fetchall()

    cur.close()

    return render_template(
        'projects.html',
        projects=projects
    )

#add project route to allow users to add new projects
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        title = request.form['title']
        category_id = request.form['category_id']
        description = request.form['description']

        cur.execute("""
            INSERT INTO projects
            (
                title,
                description,
                category_id,
                user_id
            )
            VALUES (%s,%s,%s,%s)
        """,
        (
            title,
            description,
            category_id,
            session['user_id']
        ))

        mysql.connection.commit()

        return redirect('/projects')

    cur.execute(
        "SELECT category_id, category_name FROM categories"
    )

    categories = cur.fetchall()

    cur.close()

    return render_template(
        'add_project.html',
        categories=categories
    )
#update project route to allow users to update their existing projects
@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        title = request.form['title']
        category_id = request.form['category_id']
        description = request.form['description']
        status = request.form['status']

        cur.execute("""
            UPDATE projects
            SET
                title=%s,
                category_id=%s,
                description=%s,
                status=%s
            WHERE
                project_id=%s
                AND user_id=%s
        """,
        (
            title,
            category_id,
            description,
            status,
            project_id,
            session['user_id']
        ))

        mysql.connection.commit()

        return redirect('/projects')

    cur.execute("""
        SELECT
            project_id,
            title,
            category_id,
            description,
            status
        FROM projects
        WHERE
            project_id=%s
            AND user_id=%s
    """,
    (
        project_id,
        session['user_id']
    ))

    project = cur.fetchone()

    cur.execute(
        "SELECT category_id, category_name FROM categories"
    )

    categories = cur.fetchall()

    cur.close()

    return render_template(
        'edit_project.html',
        project=project,
        categories=categories
    )


#delete project route to allow users to delete their existing projects
@app.route('/delete_project/<int:project_id>')
def delete_project(project_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        DELETE FROM projects
        WHERE
            project_id=%s
            AND user_id=%s
    """,
    (
        project_id,
        session['user_id']
    ))

    mysql.connection.commit()

    cur.close()

    return redirect('/projects')


#favorites route to display all favorite prompts and projects of the logged-in user

@app.route('/add_favorite/<int:prompt_id>')
def add_favorite(prompt_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    try:

        cur.execute("""
            INSERT INTO favorites
            (prompt_id, user_id)
            VALUES (%s,%s)
        """,
        (
            prompt_id,
            session['user_id']
        ))

        mysql.connection.commit()

    except:
        pass

    cur.close()

    return redirect('/prompts')

#view favorites route to display all favorite prompts and projects of the logged-in user
@app.route('/favorites')
def favorites():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            p.title,
            c.category_name,
            f.favorite_id
        FROM favorites f
        JOIN prompts p
            ON f.prompt_id = p.prompt_id
        JOIN categories c
            ON p.category_id = c.category_id
        WHERE f.user_id=%s
    """,
    (
        session['user_id'],
    ))

    favorites = cur.fetchall()

    cur.close()

    return render_template(
        'favorites.html',
        favorites=favorites
    )
#remove favorite route to allow users to remove a prompt from their favorites
@app.route('/remove_favorite/<int:favorite_id>')
def remove_favorite(favorite_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        DELETE FROM favorites
        WHERE favorite_id=%s
    """,
    (
        favorite_id,
    ))

    mysql.connection.commit()

    cur.close()

    return redirect('/favorites')


# -------------------------

# LOGOUT

# -------------------------

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')


#prompts route to display all prompts created by the logged-in user

@app.route('/prompts')
def prompts():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            p.prompt_id,
            p.title,
            c.category_name,
            p.created_at
        FROM prompts p
        JOIN categories c
            ON p.category_id = c.category_id
        WHERE p.user_id = %s
        ORDER BY p.created_at DESC
    """, (session['user_id'],))

    prompts = cur.fetchall()

    cur.close()

    return render_template(
        'prompts.html',
        prompts=prompts
    )

#add prompt route to allow users to add new prompts

@app.route('/add_prompt', methods=['GET', 'POST'])
def add_prompt():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        title = request.form['title']
        category_id = request.form['category_id']
        prompt_text = request.form['prompt_text']

        cur.execute("""
            INSERT INTO prompts
            (
                title,
                prompt_text,
                category_id,
                user_id
            )
            VALUES (%s,%s,%s,%s)
        """,
        (
            title,
            prompt_text,
            category_id,
            session['user_id']
        ))

        mysql.connection.commit()

        return redirect('/prompts')

    cur.execute(
        "SELECT category_id, category_name FROM categories"
    )

    categories = cur.fetchall()

    cur.close()

    return render_template(
        'add_prompt.html',
        categories=categories
    )

#update prompt route to allow users to update their existing prompts
@app.route('/edit_prompt/<int:prompt_id>', methods=['GET', 'POST'])
def edit_prompt(prompt_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        title = request.form['title']
        category_id = request.form['category_id']
        prompt_text = request.form['prompt_text']

        cur.execute("""
            UPDATE prompts
            SET
                title=%s,
                category_id=%s,
                prompt_text=%s
            WHERE
                prompt_id=%s
                AND user_id=%s
        """,
        (
            title,
            category_id,
            prompt_text,
            prompt_id,
            session['user_id']
        ))

        mysql.connection.commit()

        return redirect('/prompts')

    cur.execute("""
        SELECT
            prompt_id,
            title,
            category_id,
            prompt_text
        FROM prompts
        WHERE prompt_id=%s
        AND user_id=%s
    """,
    (
        prompt_id,
        session['user_id']
    ))

    prompt = cur.fetchone()

    cur.execute(
        "SELECT category_id, category_name FROM categories"
    )

    categories = cur.fetchall()

    cur.close()

    return render_template(
        'edit_prompt.html',
        prompt=prompt,
        categories=categories
    )

#delete prompt route to allow users to delete their existing prompts
@app.route('/delete_prompt/<int:prompt_id>')
def delete_prompt(prompt_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        DELETE FROM prompts
        WHERE prompt_id=%s
        AND user_id=%s
    """,
    (
        prompt_id,
        session['user_id']
    ))

    mysql.connection.commit()

    cur.close()

    return redirect('/prompts')


#openrouter route to allow users to send a prompt to the OpenRouter API and get a response
@app.route('/run_prompt/<int:prompt_id>', methods=['GET', 'POST'])
def run_prompt(prompt_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT prompt_id, title, prompt_text
        FROM prompts
        WHERE prompt_id=%s
    """, (prompt_id,))

    prompt = cur.fetchone()

    if request.method == 'POST':

        model_id = request.form['model_id']

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model_id,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt[2]
                    }
                ],
                "max_tokens": 1000
                }
        )

        result = response.json()
        print(response.status_code)
        print(result)
        print(response.text)
        ai_response = result["choices"][0]["message"]["content"]

        cur.execute("""
            INSERT INTO prompt_executions
            (
                prompt_id,
                model_id,
                user_id,
                response_text
            )
            VALUES (%s,%s,%s,%s)
        """,
        (
            prompt_id,
            model_id,
            session['user_id'],
            ai_response
        ))

        mysql.connection.commit()

        return f"""
        <h2>AI Response</h2>
        <hr>
        <pre>{ai_response}</pre>
        <br>
        <a href='/prompts'>Back</a>
        """

    cur.execute("""
        SELECT model_id, model_name
        FROM models
    """)

    models = cur.fetchall()

    cur.close()

    return render_template(
        'run_prompt.html',
        prompt=prompt,
        models=models
    )


#execute prompt route to allow users to execute a prompt and get a response from the OpenRouter API
@app.route('/executions')
def executions():

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            pe.execution_id,
            p.title,
            pe.model_id,
            pe.response_text,
            pe.execution_time

        FROM prompt_executions pe

        JOIN prompts p
        ON pe.prompt_id = p.prompt_id

        WHERE pe.user_id=%s

        ORDER BY pe.execution_time DESC
    """,
    (session['user_id'],))

    executions = cur.fetchall()

    cur.close()

    return render_template(
        "executions.html",
        executions=executions
    )

#individual execution route to allow users to view the details of a specific prompt execution
@app.route('/execution/<int:execution_id>')
def execution_detail(execution_id):

    if 'user_id' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            p.title,
            m.model_name,
            pe.execution_time,
            pe.response_text
        FROM prompt_executions pe
        JOIN prompts p
            ON pe.prompt_id = p.prompt_id
        JOIN models m
            ON pe.model_id = m.model_id
        WHERE pe.execution_id=%s
        AND pe.user_id=%s
    """,
    (
        execution_id,
        session['user_id']
    ))

    execution = cur.fetchone()

    cur.close()

    return render_template(
        'execution_detail.html',
        execution=execution
    )



# -------------------------

# RUN APP

# -------------------------

if __name__ == '__main__':
    app.run(debug=True)
