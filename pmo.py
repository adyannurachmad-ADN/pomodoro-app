import streamlit as st
import time

# ==========================================
# 0. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Life Balance Technic by Adyan.Dev", 
    page_icon="⏱️", 
    layout="wide"
)

# ==========================================
# 1. SISTEM KEAMANAN (LOGIN PASSWORD)
# ==========================================
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    st.markdown("<h2 style='text-align: center; margin-top: 50px;'>🔒 Akses Terbatas</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Silakan masukkan password untuk mengakses Aplikasi Pomodoro</p>", unsafe_allow_html=True)
    
    _, kol_tengah, _ = st.columns([1, 2, 1])
    with kol_tengah:
        st.write("---")
        password = st.text_input("Password Akses:", type="password")
        tombol_masuk = st.button("Masuk Aplikasi", use_container_width=True)
        
        if tombol_masuk:
            if password == "#4dy4n#": 
                st.session_state.password_correct = True
                st.success("Login Berhasil!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ Password salah!")
        st.write("---")
    return False

# ==========================================
# 2. PROGRAM UTAMA POMODORO
# ==========================================
if check_password():
    
    # Inisialisasi State Aplikasi (Penyimpanan Memori Internal)
    if "pomo_state" not in st.session_state:
        st.session_state.pomo_state = "IDLE"  # Status awal: IDLE (Diam)
    if "waktu_tersisa" not in st.session_state:
        st.session_state.waktu_tersisa = 25 * 60  # Standar fokus 25 menit
    if "siklus_selesai" not in st.session_state:
        st.session_state.siklus_selesai = 0  
    if "durasi_istirahat" not in st.session_state:
        st.session_state.durasi_istirahat = 5 * 60

    # Tautan Animasi Alam (GIF) - Pemandangan Aliran Air Sungai yang Rileks
    url_animasi_air = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3M5dzR0bm5jM2ZpYndhZ3N0bm9mY3ZsczB0Z3R4dzR0bm5jM2ZpYndhZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YmYAMDycV5FzO/giphy.gif"

    # Tautan Efek Suara Alam (.MP3) - Aliran Air Sungai Pilihan Anda dari SoundJay
    url_suara_air = "https://www.soundjay.com/nature/sounds/stream-3.mp3"

    # Kustomisasi Desain Tampilan (CSS Injection)
    st.markdown(f"""
        <style>
        .timer-kerja {{
            font-size: 80px !important;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
            color: #EF4444;
            margin: 20px 0;
        }}
        
        /* LAYAR ANIMASI FULLSCREEN SAAT ISTIRAHAT */
        .blank-screen-break {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            /* Menggabungkan efek gelap transparan 60% dan latar belakang animasi air mengalir */
            background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                        url('{url_animasi_air}');
            background-size: cover;
            background-position: center;
            z-index: 9999; 
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
        }}
        
        /* TIMER HIJAU RAKSASA DI TENGAH LAYAR */
        .timer-break-raksasa {{
            font-size: 25vh !important; 
            font-weight: 200; 
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: #10B981; 
            margin: 0;
            line-height: 1;
            text-shadow: 0px 0px 30px rgba(0, 0, 0, 0.8);
        }}
        
        .sub-text-break {{
            font-size: 24px;
            color: #F8FAFC;
            margin-top: 20px;
            letter-spacing: 3px;
            text-shadow: 2px 2px 10px rgba(0,0,0,1);
            text-transform: uppercase;
        }}
        </style>
    """, unsafe_allow_html=True)

    # Wadah kosong khusus untuk memicu suara otomatis di latar belakang web
    pemicu_audio = st.empty()

    # ------------------------------------------------------------
    # KONDISI A: MODE ISTIRAHAT (BREAK) -> TAMPILKAN LAYAR ANIMASI + SUARA
    # ------------------------------------------------------------
    if st.session_state.pomo_state == "BREAK":
        layar_blank = st.empty()
        
        # Deteksi otomatis teks judul berdasarkan durasi istirahat
        tipe_break = "LONG BREAK" if st.session_state.durasi_istirahat == 15 * 60 else "SHORT BREAK"
        pesan_break = "Saatnya istirahat panjang, nikmati teh hangat Anda" if tipe_break == "LONG BREAK" else "Rileks sejenak, sandarkan badan & ambil napas"
        
        while st.session_state.waktu_tersisa > 0 and st.session_state.pomo_state == "BREAK":
            menit = st.session_state.waktu_tersisa // 60
            detik = st.session_state.waktu_tersisa % 60
            
            # Memunculkan layar animasi air penuh + angka hitung mundur raksasa
            layar_blank.markdown(f"""
                <div class="blank-screen-break">
                    <p style="color: #10B981; font-size: 18px; letter-spacing: 5px; font-weight: bold;">☕ {tipe_break}</p>
                    <h1 class="timer-break-raksasa">{menit:02d}:{detik:02d}</h1>
                    <p class="sub-text-break">{pesan_break}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Pemicu suara air otomatis berbunyi di 5 detik terakhir sesi istirahat
            if st.session_state.waktu_tersisa <= 5:
                pemicu_audio.markdown(
                    f"""<iframe src="{url_suara_air}" allow="autoplay" style="display:none"></iframe>
                        <audio autoplay><source src="{url_suara_air}" type="audio/mp3"></audio>""", 
                    unsafe_allow_html=True
                )
            
            time.sleep(1)
            st.session_state.waktu_tersisa -= 1

        # Jika waktu istirahat habis, reset otomatis kembali ke Mode Kerja
        if st.session_state.waktu_tersisa <= 0 and st.session_state.pomo_state == "BREAK":
            st.session_state.pomo_state = "FOCUS"
            st.session_state.waktu_tersisa = 25 * 60
            st.balloons()  # Efek balon perayaan kembali kerja
            st.rerun()

    # ------------------------------------------------------------
    # KONDISI B: MODE STANDBY / MODE KERJA FOKUS (Tampilan Menu Normal)
    # ------------------------------------------------------------
    else:
        # Tata Letak Header Atas
        kolom_judul, kolom_aksi = st.columns([3, 1])
        with kolom_judul:
            st.title("⏱️ Pomodoro Timer")
            st.caption(f"Life Balance Technic | Siklus Kerja Berhasil Dilalui: {st.session_state.siklus_selesai}")
            
        with kolom_aksi:
            st.write("") 
            sub_tombol1, sub_tombol2 = st.columns(2)
            with sub_tombol1:
                if st.button("🚀 DEPLOY", type="primary", use_container_width=True):
                    if st.session_state.pomo_state == "IDLE":
                        st.session_state.pomo_state = "FOCUS"
                        st.session_state.waktu_tersisa = 25 * 60
                        # Trik bypass aturan privasi browser agar suara diizinkan berbunyi otomatis nanti
                        st.markdown(f'<iframe src="{url_suara_air}" allow="autoplay" style="display:none"></iframe>', unsafe_allow_html=True)
                        st.rerun()
            with sub_tombol2:
                if st.button("🛑 STOP", type="secondary", use_container_width=True):
                    st.session_state.pomo_state = "IDLE"
                    st.session_state.waktu_tersisa = 25 * 60
                    st.rerun()

        st.write("---")

        # Jalannya Hitung Mundur Waktu Kerja Fokus
        if st.session_state.pomo_state == "FOCUS":
            st.info("🔴 Sesi Kerja Sedang Berjalan. Tetaplah Fokus.")
            tempat_timer = st.empty()
            
            while st.session_state.waktu_tersisa > 0 and st.session_state.pomo_state == "FOCUS":
                menit = st.session_state.waktu_tersisa // 60
                detik = st.session_state.waktu_tersisa % 60
                tempat_timer.markdown(f'<p class="timer-kerja">{menit:02d}:{detik:02d}</p>', unsafe_allow_html=True)
                
                # Suara air berbunyi di 5 detik terakhir kerja (Penanda masuk waktu rileks)
                if st.session_state.waktu_tersisa <= 5:
                    pemicu_audio.markdown(
                        f"""<iframe src="{url_suara_air}" allow="autoplay" style="display:none"></iframe>
                            <audio autoplay><source src="{url_suara_air}" type="audio/mp3"></audio>""", 
                        unsafe_allow_html=True
                    )
                
                time.sleep(1)
                st.session_state.waktu_tersisa -= 1
                
            # Logika Otomatis Perpindahan Sesi Setelah Kerja Selesai
            if st.session_state.waktu_tersisa <= 0 and st.session_state.pomo_state == "FOCUS":
                st.session_state.siklus_selesai += 1
                
                # Logika Modulo 4: Siklus ke-4, 8, 12 dapat istirahat panjang 15 menit
                if st.session_state.siklus_selesai % 4 == 0:
                    st.session_state.durasi_istirahat = 15 * 60  
                else:
                    st.session_state.durasi_istirahat = 5 * 60   
                
                st.session_state.pomo_state = "BREAK"
                st.session_state.waktu_tersisa = st.session_state.durasi_istirahat
                st.rerun()
                
        # Tampilan Awal Menu Saat Aplikasi Diam / Belum Mulai
        else:
            st.info("💡 Klik tombol **DEPLOY** di kanan atas untuk memulai siklus fokus otomatis 25 menit.")
            menit = st.session_state.waktu_tersisa // 60
            detik = st.session_state.waktu_tersisa % 60
            st.markdown(f'<div style="text-align:center;"><p class="timer-kerja" style="color: #94A3B8;">{menit:02d}:{detik:02d}</p></div>', unsafe_allow_html=True)
