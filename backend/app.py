from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)


# =========================
# HOME PAGE
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# MATRIX CALCULATIONS
# =========================
@app.route("/calculate", methods=["POST"])
def calculate():

    try:
        # Get JSON data from frontend
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No data received."
            }), 400

        # Get matrices and operation
        matrix_a = np.array(data["matrixA"], dtype=float)
        matrix_b = np.array(data["matrixB"], dtype=float)

        operation = data["operation"]

        # =========================
        # ADDITION
        # =========================
        if operation == "addition":

            if matrix_a.shape != matrix_b.shape:
                return jsonify({
                    "error": "Matrices must have the same dimensions for addition."
                }), 400

            result = matrix_a + matrix_b

            return jsonify({
                "result": result.tolist()
            })


        # =========================
        # SUBTRACTION
        # =========================
        elif operation == "subtraction":

            if matrix_a.shape != matrix_b.shape:
                return jsonify({
                    "error": "Matrices must have the same dimensions for subtraction."
                }), 400

            result = matrix_a - matrix_b

            return jsonify({
                "result": result.tolist()
            })


        # =========================
        # MULTIPLICATION
        # =========================
        elif operation == "multiplication":

            if matrix_a.shape[1] != matrix_b.shape[0]:
                return jsonify({
                    "error": (
                        "Matrix multiplication is not possible. "
                        "Number of columns of Matrix A must equal "
                        "number of rows of Matrix B."
                    )
                }), 400

            result = matrix_a @ matrix_b

            return jsonify({
                "result": result.tolist()
            })


        # =========================
        # DETERMINANT
        # =========================
        elif operation == "determinant":

            if matrix_a.shape[0] != matrix_a.shape[1]:
                return jsonify({
                    "error": "Matrix A must be square to calculate its determinant."
                }), 400

            if matrix_b.shape[0] != matrix_b.shape[1]:
                return jsonify({
                    "error": "Matrix B must be square to calculate its determinant."
                }), 400

            det_a = np.linalg.det(matrix_a)
            det_b = np.linalg.det(matrix_b)

            return jsonify({
                "result": (
                    f"Determinant of A = {det_a:.4f}<br>"
                    f"Determinant of B = {det_b:.4f}"
                )
            })


        # =========================
        # INVERSE
        # =========================
        elif operation == "inverse":

            if matrix_a.shape[0] != matrix_a.shape[1]:
                return jsonify({
                    "error": "Matrix A must be square to calculate its inverse."
                }), 400

            if matrix_b.shape[0] != matrix_b.shape[1]:
                return jsonify({
                    "error": "Matrix B must be square to calculate its inverse."
                }), 400

            det_a = np.linalg.det(matrix_a)
            det_b = np.linalg.det(matrix_b)

            if np.isclose(det_a, 0):
                return jsonify({
                    "error": "Matrix A does not have an inverse because its determinant is 0."
                }), 400

            if np.isclose(det_b, 0):
                return jsonify({
                    "error": "Matrix B does not have an inverse because its determinant is 0."
                }), 400

            inverse_a = np.linalg.inv(matrix_a)
            inverse_b = np.linalg.inv(matrix_b)

            return jsonify({
                "result": (
                    "<b>Inverse of Matrix A:</b><br>"
                    f"{inverse_a.tolist()}<br><br>"
                    "<b>Inverse of Matrix B:</b><br>"
                    f"{inverse_b.tolist()}"
                )
            })


        # =========================
        # INVALID OPERATION
        # =========================
        else:

            return jsonify({
                "error": "Invalid operation selected."
            }), 400


    # =========================
    # ERROR HANDLING
    # =========================
    except KeyError as e:

        return jsonify({
            "error": f"Missing required field: {e}"
        }), 400


    except ValueError:

        return jsonify({
            "error": "Invalid matrix values. Please enter valid numbers."
        }), 400


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


# =========================
# RUN FLASK SERVER
# =========================
if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False
    )
