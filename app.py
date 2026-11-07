from flask import Flask, abort, redirect, url_for, request

app = Flask(__name__)

# Data simulasi akun pengguna (Member Zakiya Scents)
USERS = ["admin", "member01", "member02"]

# Data simulasi produk parfum (Bagian 1: Kamus Sederhana)
PRODUCTS = {
    1: {"nama": "Bohe Sage Green Tea EDP 35ml", "harga": "Rp 145.000", "stok": 24},
    2: {"nama": "Bohe Faye Floral Musk EDP 35ml", "harga": "Rp 149.000", "stok": 15},
    3: {"nama": "SAFF & Co. S.O.T.B Extrait 30ml", "harga": "Rp 199.000", "stok": 32},
    4: {"nama": "SAFF & Co. LOUI Fresh Fruity 30ml", "harga": "Rp 185.000", "stok": 19},
}

# =========================================================================
# POIN 1: Minimal 4 Route Statis (beranda, tentang, produk, kontak)
# =========================================================================

@app.route("/")
def beranda():
    link_produk = url_for("produk")
    link_cek = url_for("form_cek")
    link_tentang = url_for("tentang")
    link_kontak = url_for("kontak")
    
    return f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <title>Beranda — Zakiya Scents</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; padding: 40px; background: #f8fafc; color: #0f172a; line-height: 1.6; }}
            nav a {{ margin-right: 15px; color: #0f766e; text-decoration: none; font-weight: 600; }}
            .card {{ background: white; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>✨ Zakiya Scents — Artisan Perfumery</h1>
        <p><em>Tugas Individu 5 (Bagian 1): Implementasi Routing Flask Dasar</em></p>
        <nav>
            <a href="{link_produk}">Katalog Produk</a> |
            <a href="{link_cek}">Pengecekan Member</a> |
            <a href="{link_tentang}">Tentang Brand</a> |
            <a href="{link_kontak}">Kontak Kami</a>
        </nav>
        <div class="card">
            <h3>Selamat Datang di Butik Parfum Zakiya Scents</h3>
            <p>Eksplorasi koleksi aroma teh, matcha, dan citrus tropis pilihan untuk kebutuhan kampus dan harian.</p>
        </div>
    </body>
    </html>
    """

@app.route("/tentang")
def tentang():
    return f"""
    <h2>Tentang Zakiya Scents</h2>
    <p>Zakiya Scents adalah butik parfum lokal yang mengedepankan formulasi artisan berkualitas tinggi dengan sentuhan kesegaran khas iklim tropis.</p>
    <p><a href="{url_for('beranda')}">&larr; Kembali ke Beranda</a></p>
    """

@app.route("/kontak")
def kontak():
    return f"""
    <h2>Kontak & Layanan Konsumen</h2>
    <p><strong>Butik:</strong> Kota Surabaya, Jawa Timur</p>
    <p><strong>WhatsApp Support:</strong> +62 812-3456-7890</p>
    <p><a href="{url_for('beranda')}">&larr; Kembali ke Beranda</a></p>
    """

@app.route("/produk")
def produk():
    daftar = ""
    for id_prod, item in PRODUCTS.items():
        link_detail = url_for("detail_produk", id=id_prod)
        daftar += f"<li><a href='{link_detail}'><strong>{item['nama']}</strong></a> — {item['harga']} (Stok: {item['stok']})</li>"
        
    return f"""
    <h2>Koleksi Parfum Zakiya Scents</h2>
    <ul>
        {daftar}
    </ul>
    <p><a href="{url_for('beranda')}">&larr; Kembali ke Beranda</a></p>
    """

# =========================================================================
# POIN 2: Dynamic Route /cek/<username> dan /user/<username> dengan Validasi
# POIN 4: Gunakan url_for dan redirect minimal satu kali
# =========================================================================

@app.route("/cek")
def form_cek():
    username = request.args.get("username", "").strip()
    pesan = ""
    
    if username:
        if len(username) < 4:
            pesan = f"<p style='color: #b45309;'>⚠️ <strong>Username '{username}' tidak valid!</strong> Minimal harus 4 karakter.</p>"
        elif username.lower() in [u.lower() for u in USERS]:
            link_profil = url_for("profil_user", username=username)
            pesan = f"<p style='color: #b91c1c;'>❌ <strong>Username '{username}' sudah dipakai!</strong> <a href='{link_profil}'>Lihat Profil</a></p>"
        else:
            pesan = f"<p style='color: #047857;'>✅ <strong>Username '{username}' tersedia</strong> dan dapat digunakan.</p>"
            
    return f"""
    <h2>Pengecekan Ketersediaan Member</h2>
    <form action="{url_for('form_cek')}" method="GET">
        <label>Ketik Username:</label><br>
        <input type="text" name="username" value="{username}" placeholder="Contoh: virazakiya" required style="padding: 8px; width: 250px;">
        <button type="submit" style="padding: 8px 16px;">Cek</button>
    </form>
    {pesan}
    <p><a href="{url_for('beranda')}">&larr; Kembali ke Beranda</a></p>
    """

@app.route("/cek/<username>")
def cek_langsung(username):
    # Mengarahkan parameter dynamic route langsung ke form_cek menggunakan redirect & url_for
    return redirect(url_for("form_cek", username=username))

@app.route("/user/<username>")
def profil_user(username):
    if username.lower() not in [u.lower() for u in USERS]:
        abort(404)
        
    return f"""
    <h2>Profil Akun Member: {username}</h2>
    <p>Status: Terdaftar Aktif di Database Zakiya Scents</p>
    <p><a href="{url_for('form_cek')}">&larr; Kembali ke Pengecekan</a> | <a href="{url_for('beranda')}">Beranda</a></p>
    """

# =========================================================================
# POIN 3: Minimal 1 Route Converter Int (/produk/<int:id>) beserta abort(404)
# =========================================================================

@app.route("/produk/<int:id>")
def detail_produk(id):
    if id not in PRODUCTS:
        abort(404)
        
    item = PRODUCTS[id]
    return f"""
    <h2>Detail Produk: {item['nama']}</h2>
    <p><strong>Harga:</strong> {item['harga']}</p>
    <p><strong>Stok Tersedia:</strong> {item['stok']} botol</p>
    <p><a href="{url_for('produk')}">&larr; Kembali ke Katalog</a></p>
    """

# =========================================================================
# POIN 5: Custom Halaman Error 404
# =========================================================================

@app.errorhandler(404)
def halaman_error_404(e):
    return f"""
    <div style="text-align: center; padding: 50px; font-family: sans-serif;">
        <h1 style="color: #dc2626; font-size: 48px;">404 — Tidak Ditemukan</h1>
        <p>Maaf, halaman atau produk parfum yang Anda cari tidak tersedia di sistem Zakiya Scents.</p>
        <p><a href="{url_for('beranda')}">&larr; Kembali ke Halaman Utama</a></p>
    </div>
    """, 404

if __name__ == "__main__":
    # Jalankan di port 5002 agar tidak bentrok dengan bagian 2 (port 5001)
    app.run(debug=True, port=5002)