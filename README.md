Nama : Daffa Akmal Mahadaya Pasaribu

NPM : 2506584451

Kelas : PBP D

Website portofolio pribadi berbasis Django yang menampilkan profil, pengalaman,
proyek, dan pendidikan. Bagian Education adalah model pilihan Tugas 3–6;
Projects digunakan untuk mengikuti tutorial.

### Tugas 1
https://pbp.cs.ui.ac.id/assignments/individual/tugas-1.html#pertanyaan-reflektif

1. Saya menggunakan elemen <section> untuk membuat suatu section atau area yang terpisah secara terstruktur. Walaupun saya belum 100% mengerti kegunaannya, saya merasa bahwa elemen ini penting dan baik digunakan karena bisa modular.

2. Bagi saya, tantangan yang saya temukan merupakan seberapa unintuitive peletakan elemen pada css. Saya masih belum mengerti cara-cara yang baik dan benar untuk menata elemen-element dalam web design. Sebagai anak design, saya biasanya hanya drag-n-drop elemen-elemen pada suatu layar, tapi dengan css, saya belum mengerti penuh caranya bagaimana. Until tampilan mobile saya merasa sudah cukup rapih, jadi saya tidak mengubah apapun dari template kecuali section skills.

3. Saya belum merasakan terlalu banyak batasan, tapi mungkin di masa depan jika saya sudah melakukan banyak proyek, lebih enak kalau misalnya saya bisa update secara langsung apa saja yang saya buat.

KETERANGAN AI: Saya menggunakan AI untuk menambahkan beberapa fitur seperti caption gambar dan section skills. Hanya menggunakan GPT 5.6 Luna (Gratis) untuk membantu saya saat saya kebingungan bagaimana menstruktur CSS saya dengan benar.

### Tugas 2
https://pbp.cs.ui.ac.id/assignments/individual/tugas-2.html#pertanyaan-reflektif

1. Saat pengguna membuka halaman proyek, request tersebut akan diterima urls.py proyek. Pada urls.py proyek akan ditentukan aplikasi mana yang bakal menangani URL tersebut. Selanjutnya request akan diteruskan ke urls.py milik main, di mana ada path("project/", show_project, name="show_project") yang membuat Django mengetahui bahwa project/ harus ditangani oleh funcion show_experience di views.py. Di dalam view.py ada return render(request, "project.html", context) di mana function render adalah untuk merender atau menggambarkan HTML yang ada di template.
2. Jawaban singkatnya adalah scalability dan modularity. Jika kita langsung menulis data secara langsung ke template tanpa menggunakan model, kita harus mengisinya satu per satu dengan data yang sama. Jika pada suatu saat kita harus mengubah data tersebut, kita harus mengubah semuanya secara manual dan mungkin saja kita salah input dan secara tidak sengaja membuat inkonsistensi pada template tersebut.
3. makemigration digunakan untuk membuat file migration berdasarkan perubahan pada model Django. Misal pada awalnya pada models.py pada main hanya ada class Experience, lalu kita menambah class Project. Setelah mengubah model kita menjalankan python manage.py makemigrations dan Django  akan membuat file migration yang berisi instruksi-instruksi, tetapi database belum berubah. Setelah itu kita menggunakan migrate untuk menerapkan migration ke database. Jadi perubahan yang sebelumnya hanya tercatat dalam file migration menjadi masuk ke database, sehingga sekarang ada Project.

Simpelnya: 
makemigration -> membuat migration berdasarkan perubahan di models.py
migrate       -> menerapkan migration ke database

KETERANGAN AI: Saya menggunakan AI untuk menjelaskan lebih dalam alur jalannya urls dan migration pada Django. Saya juga menggunakan AI untuk fact-checking jawaban saya pada pertanyaan refleksi. Saya hanya menggunakan GPT 5.6 Luna (Gratis)

### Tugas 3
https://pbp.cs.ui.ac.id/assignments/individual/tugas-3.html#pertanyaan-reflektif

1. Kita menggunakan ModelForm agar bisa lebih cepat membuat kolom kolom form sesuai dengan model yang udah dibuat. Ada juga fitur-fitur tambahan yang bisa development lebih efisien tanpa meng-rewrite code kita. 

{% csrf_token %} wajib dipakai di form untuk memverify bahwa POST asli berasal dari form yang dirender dari server kita sendiri, bukan thirdparty

2. Karena JSON lebih simpel dan lebih mudah digunakan dibandingkan XML. XML memerlukan aturan-aturan yang lebih rumit dibandingkan JSON yang hanya terdiri dari sekumpulan map/dictionary yang mudah terpakai pada JavaScript.

3. Saat fungsi view seperti get_education_json di call, alurnya dimulai dari view yang mengambil data dari database melalui django ORM, yang menghasilkan queryset berisi objek-objeck model python. Karena objek-objek ini kompleks, tidak bisa dikirim melalui HTTP sebagai teks. Maka harus diubah menjadi JSON melalui serialization. Setelah diubah menjadi JSON maka bisa dikirim melalui HTTP.

KETERANGAN AI: Saya menggunakan AI untuk membuat model baru "Education" karena saya rasa task ini tidak memerlukan daya pikir yang terlalu dalam karena semua fiturnya sudah saya kembangkan di dalam Experience dan Project. Saya juga mendapat bantuan dalam membuat fitur Update dan saat mengerjakan soal refleksi 3. Saya menggunakan GPT 5.6 Luna (Gratis) dan Claude Sonnet 5 (Gratis).

### Tutorial 7 — Django REST Framework

DRF memakai model dan database yang sudah ada. Project menggunakan `category`
(`project-small` atau `project-big`), bukan `tech_stack`, dan tidak memiliki
`project_image_url`. API menyediakan `category_display` untuk label kartu.
Tidak ada perubahan model atau migrasi baru.

| Resource | Daftar / tambah | Detail / ubah / hapus | Star |
| --- | --- | --- | --- |
| Project | `/api/v1/projects/` | `/api/v1/projects/<uuid>/` | `/api/v1/projects/<uuid>/star/` |
| Education | `/api/v1/education/` | `/api/v1/education/<uuid>/` | `/api/v1/education/<uuid>/star/` |

Daftar mendukung `?title=...`. GET publik; POST membuat data; PUT/PATCH
memperbarui data; DELETE mengembalikan 204 tanpa body. Star memakai POST dan
membutuhkan login. ID dan informasi star bersifat read-only.

Hanya superuser dapat mengelola Project. Education mengikuti bagian Editor
pada tutorial: Editor dapat PUT/PATCH, sedangkan create dan delete khusus
superuser. Grup `Editor`, permission `main.change_education`, dan permission
`main.change_project` dari implementasi Editor sebelumnya didukung untuk
update Education.

Halaman `/project/` dan `/education/` memakai API baru untuk daftar, pencarian,
tambah, hapus, dan star. Setelah Tugas 6, form Edit Education mengirim PATCH
ke API tanpa reload. Session login yang
sudah ada tetap digunakan, dengan CSRF pada operasi tulis. Browsable API
tersedia di endpoint API, dengan login di `/api-auth/login/`.

Jalankan dari environment proyek:

```sh
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py test main.tests_api
python manage.py test main
```

Pengujian mencakup 13 test Project dari tutorial, 10 test Education, dan 9 test
halaman/model sebelumnya. Test Education juga memeriksa permission Editor,
field star read-only, dan token CSRF dari halaman portofolio.

### Tugas 4
https://pbp.cs.ui.ac.id/assignments/individual/tugas-4.html

Pada tugas kali ini tidak ada pertanyaan reflektif. 

KETERANGAN AI: Saya menggunakan AI untuk membantu debugging hal-hal yang terlewatkan. Pada tugas kali ini saya mendapat beberapa eror yang saya memang saya sulit temukan dan terlewat tanpa bantuan AI. Saya hanya menggunakan GPT 5.6 Luna (Gratis).

### Tugas 6

1. REST (Representational State Transfer) adalah gaya arsitektur yang memperlakukan data sebagai resource dengan antarmuka yang konsisten. URL seperti `/api/v1/education/<uuid>/` menunjuk resource, sedangkan method HTTP menyatakan tindakan terhadapnya. JSON hanya format representasi; endpoint yang selalu memakai POST untuk semua tindakan belum otomatis mengikuti REST. REST juga mencakup batasan seperti client-server, stateless, caching, dan uniform interface. API proyek ini memakai pola resource dan method HTTP, tetapi session Django menyimpan state autentikasi di server sehingga tidak sepenuhnya stateless. PUT digunakan untuk mengirim representasi pengganti, misalnya seluruh field wajib sebuah Education. PATCH digunakan untuk perubahan sebagian, misalnya hanya `{"title": "Universitas Indonesia"}`. Pada implementasi ini PUT mewajibkan title, description, level, dan started_at; PATCH mempertahankan field yang tidak dikirim. Field opsional yang tidak dikirim pada PUT mengikuti perilaku serializer, bukan otomatis dikosongkan.

2. Serializer mengubah objek model menjadi tipe data Python yang dapat dirender sebagai JSON, sekaligus memvalidasi input sebelum disimpan. `ModelSerializer` mengambil aturan dasar field dari model, sementara `validate_title` dan `validate_description` membersihkan tag HTML dan menolak teks kosong. Dibandingkan merakit dictionary dengan `JsonResponse`, aturan representasi, validasi, create, dan update menjadi lebih terpusat. Daftar field eksplisit membatasi data yang keluar; `star_count`, `is_starred`, dan `starred_by_names` bersifat read-only. Serializer tidak menjalankan `ModelForm.clean_*`, jadi aturan input harus tersedia di jalur serializer juga. Pembersihan tag bukan pengganti escaping saat data ditampilkan.

3. Autentikasi menentukan siapa pengirim request; `SessionAuthentication` memakai session login Django untuk mengisi `request.user`. Otorisasi menentukan tindakan yang boleh dilakukan akun tersebut. Pada Education, pengunjung hanya membaca, pengguna login juga boleh star, Editor boleh PUT/PATCH, dan superuser boleh membuat serta menghapus. Permission class memeriksa aturan di server sebelum perubahan dilakukan. Menyembunyikan tombol hanya membantu tampilan: pengguna tetap bisa mengirim request langsung melalui alat HTTP atau JavaScript. Karena itu API dan view lama harus sama-sama menolak tindakan terlarang, dan test juga memeriksa bahwa database tidak berubah.

4. Browser mengirim cookie session secara otomatis dalam kondisi yang berlaku, sehingga cookie saja tidak membuktikan bahwa sebuah operasi tulis memang berasal dari halaman aplikasi yang diizinkan. Token CSRF, bersama pemeriksaan origin/referer oleh Django, melindungi operasi tersebut dari request lintas situs yang tidak sah. Fetch untuk POST, PUT, PATCH, dan DELETE menyertakan `X-CSRFToken`; halaman merender token agar cookie tersedia. `force_authenticate` melewati autentikasi session sehingga tidak membuktikan pemeriksaan CSRF bekerja. Test menggunakan `APIClient(enforce_csrf_checks=True)` dan `.login()`, memastikan operasi tanpa token menghasilkan 403 serta database tetap sama, lalu memastikan operasi dengan token sah berhasil.

Implementasi Education:

- API daftar/detail/star menggunakan model dan data Education yang sudah ada, dengan pencarian `?title=...` dan empat peran akses.
- Daftar, pencarian, tambah, hapus, dan star berjalan melalui fetch tanpa reload di `/education/`.
- Tombol Edit untuk Editor/pemilik membuka form yang mengirim PATCH melalui fetch. Error 400/403 ditampilkan lewat toast; input tetap tersedia untuk diperbaiki. Penyimpanan berhasil tidak memuat ulang halaman.
- Field teks dan star menggunakan validasi bersama pada `PortfolioItemSerializer`; masing-masing serializer tetap memiliki daftar field eksplisit.
- Test mencakup keadaan database setelah penolakan, izin view lama, format tanggal edit, dan session/CSRF dengan login sungguhan.

Menjalankan secara lokal di Windows, setelah clone dan masuk ke folder proyek:

```powershell
py -m venv env
.\env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PRODUCTION = 'False'
python manage.py migrate
python manage.py createsuperuser
python manage.py test main
python manage.py runserver
```

Jika environment sudah ada, cukup aktifkan environment tersebut. Buka
`http://127.0.0.1:8000/education/` untuk halaman dan
`http://127.0.0.1:8000/api/v1/education/` untuk Browsable API. Gunakan akun
superuser untuk mengelola data. Editor dapat memakai grup `Editor` atau
permission Education/permission lama yang dijelaskan pada bagian Tutorial 7.
Database SQLite dan file `.env` tetap lokal dan tidak dimasukkan ke Git.

KETERANGAN AI TUGAS 6: Codex membantu membaca checklist tugas, membandingkannya
dengan implementasi Tutorial 7, menambahkan form fetch/PATCH, merapikan
serializer bersama, memperkuat test permission/CSRF, dan menyusun jawaban
reflektif serta dokumentasi ini. Jawaban reflektif ini merupakan draf yang
disusun dengan bantuan AI, bukan catatan pengalaman pribadi yang diverifikasi.

Log prompt ringkas dari sesi pengerjaan:

- `Implement tutorial 7 first`
- `Implement tugas 6`

Strategi pengerjaan: dokumen tutorial dan tugas diberikan sebagai referensi,
lalu implementasi diperiksa terhadap model Education yang sudah ada.
Keterbatasan yang perlu diperhatikan: test otomatis tidak menjamin seluruh
perilaku browser atau deployment. Pemeriksaan kode menemukan bahwa form edit
lama belum memakai API dan test CSRF Education masih memakai `force_login`;
keduanya diperbaiki pada pengerjaan ini. Tidak ada klaim bahwa pengguna telah
melakukan perbaikan manual atau bahwa deployment/submisi telah selesai.
