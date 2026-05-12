import qrcode

def generate_qr(data, filename):
    img = qrcode.make(data)
    img.save("static/" + filename)
    return filename