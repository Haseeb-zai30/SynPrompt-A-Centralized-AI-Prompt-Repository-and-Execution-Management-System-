from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for,
    flash
)

from extensions import mysql

favorite_bp = Blueprint("favorite", __name__)


# -------------------------
# ADD FAVORITE
# -------------------------

@favorite_bp.route("/add_favorite/<int:prompt_id>")
def add_favorite(prompt_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:

        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO favorites
            (
                prompt_id,
                user_id
            )
            VALUES
            (
                %s,
                %s
            )
        """,
        (
            prompt_id,
            session["user_id"]
        ))

        mysql.connection.commit()
        cur.close()

        flash(
            "Prompt added to favorites.",
            "success"
        )

    except Exception:

        flash(
            "Prompt is already in your favorites.",
            "warning"
        )

    return redirect(url_for("prompt.prompts"))


# -------------------------
# VIEW FAVORITES
# -------------------------

@favorite_bp.route("/favorites")
def favorites():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:

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

            WHERE f.user_id = %s
        """,
        (session["user_id"],))

        favorites = cur.fetchall()

        cur.close()

        return render_template(
            "favorites.html",
            favorites=favorites
        )

    except Exception as e:

        print(f"Favorites Error: {e}")

        flash(
            "Unable to load favorites.",
            "danger"
        )

        return redirect(url_for("dashboard.dashboard"))


# -------------------------
# REMOVE FAVORITE
# -------------------------

@favorite_bp.route("/remove_favorite/<int:favorite_id>")
def remove_favorite(favorite_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:

        cur = mysql.connection.cursor()

        cur.execute("""
            DELETE FROM favorites
            WHERE
                favorite_id = %s
                AND user_id = %s
        """,
        (
            favorite_id,
            session["user_id"]
        ))

        mysql.connection.commit()

        cur.close()

        flash(
            "Favorite removed successfully.",
            "success"
        )

    except Exception as e:

        print(f"Remove Favorite Error: {e}")

        flash(
            "Unable to remove favorite.",
            "danger"
        )

    return redirect(url_for("favorite.favorites"))