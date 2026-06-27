from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for
)

from extensions import mysql
from services.openrouter_service import ask_ai

prompt_bp = Blueprint("prompt", __name__)

# -------------------------
# VIEW PROMPT
# -------------------------

@prompt_bp.route("/prompt/<int:prompt_id>")
def view_prompt(prompt_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:

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

            WHERE
                p.prompt_id = %s
                AND p.user_id = %s
        """,
        (
            prompt_id,
            session["user_id"]
        ))

        prompt = cur.fetchone()

        cur.close()

        if not prompt:

            flash(
                "Prompt not found.",
                "warning"
            )

            return redirect(url_for("prompt.prompts"))

        return render_template(
            "view_prompt.html",
            prompt=prompt
        )

    except Exception as e:

        print(f"View Prompt Error: {e}")

        flash(
            "Unable to load prompt.",
            "danger"
        )

        return redirect(url_for("prompt.prompts"))


# -------------------------
# VIEW PROMPTS
# -------------------------

@prompt_bp.route("/prompts")
def prompts():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:

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
        """,
        (session["user_id"],))

        prompts = cur.fetchall()

        cur.close()

        return render_template(
            "prompts.html",
            prompts=prompts
        )

    except Exception as e:

        print(f"Prompts Error: {e}")

        flash(
            "Unable to load prompts.",
            "danger"
        )

        return redirect(url_for("dashboard.dashboard"))


# -------------------------
# ADD PROMPT
# -------------------------

@prompt_bp.route("/add_prompt", methods=["GET", "POST"])
def add_prompt():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:

        cur = mysql.connection.cursor()

        if request.method == "POST":

            title = request.form["title"]
            category_id = request.form["category_id"]
            prompt_text = request.form["prompt_text"]

            cur.execute("""
                INSERT INTO prompts
                (
                    title,
                    prompt_text,
                    category_id,
                    user_id
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
            """,
            (
                title,
                prompt_text,
                category_id,
                session["user_id"]
            ))

            mysql.connection.commit()

            cur.close()

            flash(
                "Prompt created successfully.",
                "success"
            )

            return redirect(url_for("prompt.prompts"))

        cur.execute("""
            SELECT
                category_id,
                category_name
            FROM categories
        """)

        categories = cur.fetchall()

        cur.close()

        return render_template(
            "add_prompt.html",
            categories=categories
        )

    except Exception as e:

        print(f"Add Prompt Error: {e}")

        flash(
            "Unable to create prompt.",
            "danger"
        )

        return redirect(url_for("prompt.prompts"))






# -------------------------
# EDIT PROMPT
# -------------------------

@prompt_bp.route("/edit_prompt/<int:prompt_id>", methods=["GET", "POST"])
def edit_prompt(prompt_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:

        cur = mysql.connection.cursor()

        if request.method == "POST":

            title = request.form["title"]
            category_id = request.form["category_id"]
            prompt_text = request.form["prompt_text"]

            cur.execute("""
                UPDATE prompts
                SET
                    title = %s,
                    category_id = %s,
                    prompt_text = %s
                WHERE
                    prompt_id = %s
                    AND user_id = %s
            """,
            (
                title,
                category_id,
                prompt_text,
                prompt_id,
                session["user_id"]
            ))

            mysql.connection.commit()
            cur.close()

            flash(
                "Prompt updated successfully.",
                "success"
            )

            return redirect(url_for("prompt.prompts"))

        cur.execute("""
            SELECT
                prompt_id,
                title,
                category_id,
                prompt_text

            FROM prompts

            WHERE
                prompt_id = %s
                AND user_id = %s
        """,
        (
            prompt_id,
            session["user_id"]
        ))

        prompt = cur.fetchone()

        if not prompt:

            cur.close()

            flash(
                "Prompt not found.",
                "warning"
            )

            return redirect(url_for("prompt.prompts"))

        cur.execute("""
            SELECT
                category_id,
                category_name
            FROM categories
        """)

        categories = cur.fetchall()

        cur.close()

        return render_template(
            "edit_prompt.html",
            prompt=prompt,
            categories=categories
        )

    except Exception as e:

        print(f"Edit Prompt Error: {e}")

        flash(
            "Unable to update prompt.",
            "danger"
        )

        return redirect(url_for("prompt.prompts"))


# -------------------------
# DELETE PROMPT
# -------------------------

@prompt_bp.route("/delete_prompt/<int:prompt_id>")
def delete_prompt(prompt_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:

        cur = mysql.connection.cursor()

        cur.execute("""
            DELETE FROM prompts
            WHERE
                prompt_id = %s
                AND user_id = %s
        """,
        (
            prompt_id,
            session["user_id"]
        ))

        mysql.connection.commit()
        cur.close()

        flash(
            "Prompt deleted successfully.",
            "success"
        )

    except Exception as e:

        print(f"Delete Prompt Error: {e}")

        flash(
            "Unable to delete prompt.",
            "danger"
        )

    return redirect(url_for("prompt.prompts"))


# -------------------------
# RUN PROMPT
# -------------------------

@prompt_bp.route("/run_prompt/<int:prompt_id>", methods=["GET", "POST"])
def run_prompt(prompt_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:

        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT
                prompt_id,
                title,
                prompt_text

            FROM prompts

            WHERE
                prompt_id = %s
                AND user_id = %s
        """,
        (
            prompt_id,
            session["user_id"]
        ))

        prompt = cur.fetchone()

        if not prompt:

            cur.close()

            flash(
                "Prompt not found.",
                "warning"
            )

            return redirect(url_for("prompt.prompts"))

        if request.method == "POST":

            model_id = request.form["model_id"]

            ai_response = ask_ai(
                prompt[2],
                model_id
            )

            cur.execute("""
                INSERT INTO prompt_executions
                (
                    prompt_id,
                    model_id,
                    user_id,
                    response_text
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
            """,
            (
                prompt_id,
                model_id,
                session["user_id"],
                ai_response
            ))

            mysql.connection.commit()
            
            cur.close()

            return render_template(
                "prompt_result.html",
                prompt=prompt,
                response=ai_response,
                model=model_id
            )

        cur.execute("""
            SELECT
                model_id,
                model_name
            FROM models
        """)

        models = cur.fetchall()

        cur.close()

        return render_template(
            "run_prompt.html",
            prompt=prompt,
            models=models
        )

    except Exception as e:

        print(f"Run Prompt Error: {e}")

        flash(
            "Unable to execute prompt.",
            "danger"
        )

        return redirect(url_for("prompt.prompts"))