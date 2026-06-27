from flask import Blueprint, render_template, request, redirect, session
from extensions import mysql

project_bp = Blueprint('project', __name__)

#run project route to allow users to run all prompts in a specific project and get responses from the OpenRouter API
@project_bp.route('/run_project/<int:project_id>', methods=['POST'])
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

@project_bp.route('/project/<int:project_id>')
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

@project_bp.route('/add_prompt_to_project/<int:project_id>',
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
@project_bp.route('/projects')
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
@project_bp.route('/add_project', methods=['GET', 'POST'])
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
@project_bp.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
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
@project_bp.route('/delete_project/<int:project_id>')
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

