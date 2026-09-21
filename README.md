Nama : Daffa Akmal Mahadaya Pasaribu

NPM : 2506584451

Kelas : PBP D

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