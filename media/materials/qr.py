import qrcode as qr

img = qr.make("https://github.com/yugbhuva747-byte?tab=repositories")

img.save("pythonQR.png")

print("QR code generated and saved as w3python.png")    
