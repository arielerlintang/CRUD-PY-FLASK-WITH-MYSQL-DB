from flask import Flask, render_template, request, redirect, url_for
import os
import mysql.connector
from werkzeug.utils import secure_filename

app = Flask(__name__)

#koneksi ke database 
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="crud"
)

cursor = db.cursor(dictionary=True)

UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# konfigurasu rooting
@app.route('/')
def index():
    cursor.execute("SELECT * FROM produk")
    produk = cursor.fetchall()
    return render_template("index.html", data=produk)
    

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    # skrip untuk mendapatkan inputan dari formulir dan disimpan ke database 
    if request.method == 'POST':
        nama = request.form['nama_produk']
        deskripsi = request.form['deskripsi_produk']
        jenis = request.form['jenis_produk']
        
        foto = request.files['foto_produk']
        filename = secure_filename(foto.filename)
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        cursor.execute("INSERT INTO produk (nama_produk,deskripsi_produk,jenis_produk,foto_produk) VALUES(%s, %s, %s, %s)", 
                       (nama,deskripsi,jenis,filename))
        db.commit()
        return redirect(url_for('index'))
    return render_template("tambah.html")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cursor.execute("SELECT * FROM produk WHERE id_produk=%s", (id,))
    produk = cursor.fetchone()
    if request.method == 'POST':
        nama = request.form['nama_produk']
        deskripsi = request.form['deskripsi_produk']
        jenis = request.form['jenis_produk']
        
        foto = request.files['foto_produk']
        if foto and foto.filename != '':    
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = produk['foto_produk']
            
        cursor.execute("UPDATE produk SET nama_produk=%s, deskripsi_produk=%s, jenis_produk=%s, foto_produk=%s WHERE id_produk=%s", 
                       (nama,deskripsi,jenis,filename, id))
        db.commit()
        return redirect(url_for('index'))
    
    return render_template("edit.html", data=produk)


@app.route('/hapus/<int:id>')
def hapus(id):
    cursor.execute("SELECT * FROM produk WHERE id_produk=%s", (id,))
    produk = cursor.fetchone()
    if produk and produk['foto_produk']:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], produk['foto_produk']))
        except FileNotFoundError:
            pass
        
    cursor.execute("DELETE FROM produk WHERE id_produk=%s", (id,))
    db.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)