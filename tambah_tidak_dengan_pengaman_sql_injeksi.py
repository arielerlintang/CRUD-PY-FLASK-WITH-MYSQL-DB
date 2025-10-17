@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nama = request.form['nama_produk']
        deskripsi = request.form['deskripsi_produk']
        jenis = request.form['jenis_produk']

        foto = request.files['foto_produk']
        filename = secure_filename(foto.filename)
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        sql = f"INSERT INTO produk (nama_produk, deskripsi_produk, jenis_produk, foto_produk) VALUES ('{nama}', '{deskripsi}', '{jenis}', '{filename}')"
        cursor.execute(sql)
        db.commit()

        return redirect(url_for('index'))
    return render_template("tambah.html")
