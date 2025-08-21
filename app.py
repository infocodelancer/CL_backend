from flask import Flask, request, jsonify
from flask_cors import CORS
from models.customer import Customer
from services.db_service import insert_customer
from services.email_service import send_confirmation_email
from config import settings

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["ENV"] = settings.ENV
    app.config["DEBUG"] = settings.DEBUG

    # CORS for your frontend origin(s); adjust as needed
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "customer_backend"}), 200

    @app.post("/api/register")
    def register_customer():
        try:
            if request.is_json:
                payload = request.get_json(silent=True) or {}
            else:
                # accept form submissions
                payload = request.form.to_dict()

            # Validate with Pydantic
            customer = Customer(**payload)

            # Store in MongoDB
            customer_id = insert_customer(customer.model_dump())

            # Send confirmation email
            email_sent = send_confirmation_email(customer.email, customer.firstName)

            return jsonify({
                "message": "Customer registered successfully",
                "customer_id": customer_id,
                "email_sent": email_sent
            }), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=settings.DEBUG)
