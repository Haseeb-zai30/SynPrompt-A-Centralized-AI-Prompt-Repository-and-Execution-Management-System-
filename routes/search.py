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

search_bp = Blueprint("search", __name__)


# -------------------------
# SEARCH PROMPTS
# -------------------------

@search_bp.route("/search")
def search():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    try:

        keyword = request.args.get("query", "").strip()
        category = request.args.get("category", "").strip()

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

            WHERE p.user_id = %s
        """

        values = [session["user_id"]]

        if keyword:

            sql += """
                AND (
                    p.title LIKE %s
                    OR p.prompt_text LIKE %s
                )
            """

            values.extend([
                f"%{keyword}%",
                f"%{keyword}%"
            ])

        if category:

            sql += """
                AND c.category_name = %s
            """

            values.append(category)

        sql += """
            ORDER BY p.created_at DESC
        """

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

    except Exception as e:

        print(f"Search Error: {e}")

        flash(
            "Unable to perform search.",
            "danger"
        )

        return redirect(url_for("dashboard.dashboard"))


# -------------------------
# GET CATEGORIES
# -------------------------

def get_categories():

    try:

        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT
                category_id,
                category_name
            FROM categories
            ORDER BY category_name
        """)

        categories = cur.fetchall()

        cur.close()

        return categories

    except Exception as e:

        print(f"Category Error: {e}")

        return []