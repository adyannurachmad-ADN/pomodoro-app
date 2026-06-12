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
    
    # Inisialisasi State Aplikasi
    if "pomo_state" not in st.session_state:
        st.session_state.pomo_state = "IDLE" 
    if "waktu_tersisa" not in st.session_state:
        st.session_state.waktu_tersisa = 25 * 60  
    if "siklus_selesai" not in st.session_state:
        st.session_state.siklus_selesai = 0  
    if "durasi_istirahat" not in st.session_state:
        st.session_state.durasi_istirahat = 5 * 60

    # JALUR DIREKTORI RAW GITHUB MILIK ANDA
    url_animasi_air = "https://raw.githubusercontent.com/adyannurachmad-ADN/pomodoro-app/main/assets/river-flow.gif"
    url_suara_air = "https://raw.githubusercontent.com/adyannurachmad-ADN/pomodoro-app/main/assets/stream-3.mp3"
    url_suara_es = "https://raw.githubusercontent.com/adyannurachmad-ADN/pomodoro-app/main/assets/ice-cracking-01.mp3"

    # Desain Gaya Font Mode Kerja & Mode Istirahat
    st.markdown("""
        <style>
        .timer-kerja {
            font-size: 100px !important;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
            color: #EF4444;
            margin: 10px 0;
        }
        .timer-break-layar {
            /* SOLUSI PERTAMA: Memperkecil angka jam agar setara dengan tinggi gambar baru */
            font-size: 100px !important; 
            font-weight: bold;
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: #10B981;
            text-align: center;
            margin: 0px 0;
            padding-top: 10px; /* Menyesuaikan jarak vertikal */
        }
        </style>
    """, unsafe_allow_html=True)

    # ------------------------------------------------------------
    # KONDISI A: MODE ISTIRAHAT (BREAK) - BERDAMPINGAN Side-by-Side (TERBARU)
    # ------------------------------------------------------------
    if st.session_state.pomo_state == "BREAK":
        
        tipe_break = "LONG BREAK" if st.session_state.durasi_istirahat == 15 * 60 else "SHORT BREAK"
        st.markdown(f"<h3 style='text-align: center; color: #10B981; letter-spacing: 3px; padding-bottom: 20px;'>☕ {tipe_break} ACTIVE</h3>", unsafe_allow_html=True)
        
        # Kita bagi layar menjadi dua kolom yang seimbang secara proporsional
        kolom_kiri_timer, kolom_kanan_animasi = st.columns([1, 1])
        
        # Wadah countdown diletakkan di KOLOM KIRI
        with kolom_kiri_timer:
            tempat_timer_break = st.empty()
            st.write("") 

        # Animasi dan Audio diletakkan di KOLOM KANAN
        with kolom_kanan_animasi:
            try:
                # SOLUSI KEDUA & KETIGA: use_container_width=False
                # Ini akan memuat gambar dengan skala aslinya, sehingga tinggi gambar proporsional
                # dan seluruh frame sungai akan terlihat jelas tanpa terpotong bagian bawahnya.
                st.image(url_animasi_air, use_container_width=False, caption="Rileks sejenak, nikmati aliran air sungai pegunungan...")
            except Exception:
                st.caption("Memuat gambar animasi lokal...")
            
            try:
                st.audio(url_suara_air, format="audio/mp3", autoplay=True, loop=True)
            except Exception:
                st.warning("⚠️ Suara latar belakang tidak dapat dimuat.")
            
        # Perulangan detik tetap berjalan
        while st.session_state.waktu_tersisa > 0 and st.session_state.pomo_state == "BREAK":
            menit = st.session_state.waktu_tersisa // 60
            detik = st.session_state.waktu_tersisa % 60
            # Jam berdetak di wadah di kolom kiri
            tempat_timer_break.markdown(f'<p class="timer-break-layar">{menit:02d}:{detik:02d}</p>', unsafe_allow_html=True)
            
            time.sleep(1)
            st.session_state.waktu_tersisa -= 1

        if st.session_state.waktu_tersisa <= 0 and st.session_state.pomo_state == "BREAK":
            st.session_state.pomo_state = "FOCUS"
            st.session_state.waktu_tersisa = 25 * 60
            st.balloons() 
            st.rerun()

    # ------------------------------------------------------------
    # KONDISI B: MODE STANDBY / MODE KERJA FOKUS
    # ------------------------------------------------------------
    else:
        kolom_judul, kolom_aksi = st.columns([3, 1])
        with kolom_judul:
            st.title("⏱️ Pomodoro Timer")
            st.caption(f"Life Balance Technic | Siklus Fokus Sukses: {st.session_state.siklus_selesai}")
            
        with kolom_aksi:
            st.write("") 
            sub1, sub2 = st.columns(2)
            with sub1:
                if st.button("🚀 DEPLOY", type="primary", use_container_width=True):
                    if st.session_state.pomo_state == "IDLE":
                        st.session_state.pomo_state = "FOCUS"
                        st.session_state.waktu_tersisa = 25 * 60
                        st.rerun()
            with sub2:
                if st.button("🛑 STOP", type="secondary", use_container_width=True):
                    st.session_state.pomo_state = "IDLE"
                    st.session_state.waktu_tersisa = 25 * 60
                    st.rerun()

        st.write("---")

        if st.session_state.pomo_state == "FOCUS":
            st.info("🔴 Sesi Kerja Sedang Berjalan. Fokus pada prioritas Anda.")
            tempat_timer = st.empty()
            
            # Wadah tersembunyi khusus untuk memicu efek suara es retak pengingat transisi
            wadah_audio_es = st.empty()
            es_played = False
            
            while st.session_state.waktu_tersisa > 0 and st.session_state.pomo_state == "FOCUS":
                menit = st.session_state.waktu_tersisa // 60
                detik = st.session_state.waktu_tersisa % 60
                tempat_timer.markdown(f'<p class="timer-kerja">{menit:02d}:{detik:02d}</p>', unsafe_allow_html=True)
                
                # --- MEMUTAR SUARA ES RETAK PADA 5 DETIK TERAKHIR ---
                if st.session_state.waktu_tersisa == 5 and not es_played:
                    try:
                        with wadah_audio_es:
                            st.audio(url_suara_es, format="audio/mp3", autoplay=True)
                        es_played = True
                    except Exception:
                        pass
                
                time.sleep(1)
                st.session_state.waktu_tersisa -= 1
                
            if st.session_state.waktu_tersisa <= 0 and st.session_state.pomo_state == "FOCUS":
                st.session_state.siklus_selesai += 1
                st.session_state.durasi_istirahat = 15 * 60 if st.session_state.siklus_selesai % 4 == 0 else 5 * 60
                st.session_state.pomo_state = "BREAK"
                st.session_state.waktu_tersisa = st.session_state.durasi_istirahat
                st.rerun()
                
        else:
            st.info("💡 Klik tombol **DEPLOY** untuk memulai siklus fokus otomatis 25 menit.")
            menit = st.session_state.waktu_tersisa // 60
            detik = st.session_state.waktu_tersisa % 60
            st.markdown(f'<div style="text-align:center;"><p class="timer-kerja" style="color: #94A3B8;">{menit:02d}:{detik:02d}</p></div>', unsafe_allow_html=True)
