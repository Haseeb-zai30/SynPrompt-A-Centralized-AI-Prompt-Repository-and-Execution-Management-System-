from flask import Blueprint, render_template, redirect, session
from extensions import mysql

dashboard_bp = Blueprint('dashboard', __name__)


# DASHBOARD

# -------------------------

@dashboard_bp.route('/dashboard')
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