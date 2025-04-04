from flask import Flask, request, send_file
import qrcode
import io
import os
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h2>QR Code Generator</h2>
    <form action="/generate" method="post">
        <input type="text" name="data" placeholder="Enter AR menu URL" required>
        <button type="submit">Generate QR Code</button>
    </form>
    '''

@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.form.get('data')
    if not data:
        return "Error: No data provided", 400

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    # Save to an in-memory file
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 10000))  # Get port from Render
    app.run(host="0.0.0.0", port=port, debug=True)



