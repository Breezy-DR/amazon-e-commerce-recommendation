# Sistem Rekomendasi Produk E-Commerce Amazon

## Muhammad Farrel Danendra Rachim

Proyek ini adalah sistem rekomendasi Streamlit berbasis *embedding retrieval* dari [dataset produk Amazon](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset/data) yang terdiri atas 
berbagai fitur (harga, rating, kategori, dll) untuk menyarankan produk 
yang 
sesuai dengan preferensi pengguna pada saat itu juga. Sistem rekomendasi tidak menggunakan model machine learning 
(ML) secara eksplisit, namun membuat representasi vektor (embedding) dari kueri produk yang diinginkan pengguna dan menghitung semantic similarity antara keduanya. Sekumpulan produk dengan selisih embedding antara kueri pengguna yang paling dekat akan menjadi prioritas utama dalam daftar rekomendasi.

Tidak hanya itu, saya juga mengusulkan dan mengembangkan fitur chatbot yang dispesialisasi untuk menjawab 
rekomendasi produk yang tersedia di Amazon. Jawaban yang disediakan chatbot ini sangat membantu pengguna dalam 
membandingkan produk-produk yang ada beserta justifikasi mengapa produk-produk tersebut direkomendasikan berdasarkan kualitasnya. Model untuk chatbot menggunakan pendekatan berbasis _generative question answering_ menggunakan LLM dari Google Gemini.

Evaluasi model sistem rekomendasi menggunakan gabungan cosine similarity antar teks, precision@k, dan evaluasi 
manual (khusus untuk chatbot).

**Bahasa pemrograman**: Python 3.12 \
**Platform aplikasi**: Streamlit

Link dashboard: https://amazon-e-commerce-recommendation.streamlit.app

### [Instalasi](https://docs.streamlit.io/get-started/installation/command-line)
1. Buat folder virtual environment `.venv` 
2. Aktifkan `.venv` 
3. Masukkan perintah `streamlit run website.py`