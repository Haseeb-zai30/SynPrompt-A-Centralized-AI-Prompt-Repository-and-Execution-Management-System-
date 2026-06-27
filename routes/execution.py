from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for,
    flash
)

from extensions import mysql

execution_bp = Blueprint("execution", __name__)


# -------------------------
# ALL EXECUTIONS
# -------------------------

@execution_bp.route("/executions")
def executions():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:

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

            WHERE pe.user_id = %s

            ORDER BY pe.execution_time DESC
        """, (session["user_id"],))

        executions = cur.fetchall()

        cur.close()

        return render_template(
            "executions.html",
            executions=executions
        )

    except Exception as e:

        print(f"Execution List Error: {e}")

        flash(
            "Unable to load execution history.",
            "danger"
        )

        return redirect(url_for("dashboard.dashboard"))


# -------------------------
# EXECUTION DETAILS
# -------------------------

@execution_bp.route("/execution/<int:execution_id>")
def execution_detail(execution_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:

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

            WHERE
                pe.execution_id = %s
                AND pe.user_id = %s
        """, (
            execution_id,
            session["user_id"]
        ))

        execution = cur.fetchone()

        cur.close()

        if not execution:

            flash(
                "Execution record not found.",
                "warning"
            )

            return redirect(url_for("execution.executions"))

        return render_template(
            "execution_detail.html",
            execution=execution
        )

    except Exception as e:

        print(f"Execution Detail Error: {e}")

        flash(
            "Unable to load execution details.",
            "danger"
        )

        return redirect(url_for("execution.executions"))