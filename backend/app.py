from flask import Flask, jsonify, request
from flask_cors import CORS
from db import db, cursor

app = Flask(__name__)
CORS(app)

projects = [
    {
        "title": "CI/CD Pipeline on Amazon EKS",
        "description": "Built an end-to-end CI/CD pipeline integrating GitHub, Jenkins, Docker Hub and Amazon EKS.",
        "github": "https://github.com/YOUR_USERNAME/repo1",
        "image": "assets/eks.png"
    },
    {
        "title": "End-to-End CI/CD Pipeline with Terraform",
        "description": "Provisioned AWS infrastructure using Terraform and deployed Flask applications on Kubernetes.",
        "github": "https://github.com/YOUR_USERNAME/repo2",
        "image": "assets/terraform.png"
    },
    {
        "title": "AWS Infrastructure Dashboard",
        "description": "Flask dashboard for monitoring EC2 instances using AWS Boto3.",
        "github": "https://github.com/YOUR_USERNAME/repo3",
        "image": "assets/dashboard.png"
    }
]


@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "message": "Portfolio Backend Running"
    })


@app.route("/api/projects", methods=["GET"])
def get_projects():
    return jsonify(projects)


@app.route("/api/contact", methods=["POST"])
def contact():

    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        cursor.execute(
            """
            INSERT INTO contacts
            (name, email, message)
            VALUES (%s, %s, %s)
            """,
            (name, email, message)
        )

        db.commit()

        return jsonify({
            "success": True,
            "message": "Message stored successfully"
        }), 201

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/messages", methods=["GET"])
def get_messages():

    try:

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                message,
                created_at
            FROM contacts
            ORDER BY created_at DESC
            """
        )

        rows = cursor.fetchall()

        messages = []

        for row in rows:

            messages.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "message": row[3],
                "created_at": str(row[4])
            })

        return jsonify(messages)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/message/<int:id>", methods=["GET"])
def get_message(id):

    try:

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                message,
                created_at
            FROM contacts
            WHERE id = %s
            """,
            (id,)
        )

        row = cursor.fetchone()

        if not row:
            return jsonify({
                "success": False,
                "message": "Message not found"
            }), 404

        return jsonify({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "message": row[3],
            "created_at": str(row[4])
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )