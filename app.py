from flask import Flask, request, jsonify
from flask_cors import CORS
from models.customer import Customer
from services.db_service import insert_customer, get_super_admin_emails
from services.email_service import send_confirmation_email, send_super_admin_notification
from config import settings


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["ENV"] = settings.ENV
    app.config["DEBUG"] = settings.DEBUG

    CORS(app)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "customer_backend"}), 200

    @app.post("/api/register")
    def register_customer():
        try:
            if request.is_json:
                payload = request.get_json(silent=True) or {}
            else:
                payload = request.form.to_dict()

            customer = Customer(**payload)
            customer_id = insert_customer(customer.model_dump())

            # Customer confirmation email
            email_sent = send_confirmation_email(customer.email, customer.firstName)

            # Notify all super admins
            super_admins = get_super_admin_emails()
            for admin_email in super_admins:
                send_super_admin_notification(admin_email, customer.model_dump())

            return jsonify({
                "message": "Customer registered successfully",
                "customer_id": customer_id,
                "email_sent": email_sent
            }), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return app


app = create_app()
