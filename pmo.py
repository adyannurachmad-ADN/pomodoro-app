import streamlit as st
import time

# ==========================================
# 0. KONFIGURASI HALAMAN
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
# 2. PROGRAM UTAMA
# ==========================================
if check_password():
    
    # Inisialisasi State Aplikasi
    if "pomo_state" not in st.session_state:
        st.session_state.pomo_state = "IDLE"  # IDLE, FOCUS, BREAK
    if "waktu_tersisa" not in st.session_state:
        st.session_state.waktu_tersisa = 25 * 60
    if "siklus_selesai" not in st.session_state:
        st.session_state.siklus_selesai = 0  
    if "durasi_istirahat" not in st.session_state:
        st.session_state.durasi_istirahat = 5 * 60

    # Kustomisasi CSS Spesial untuk Layar Blank Istirahat & Font Raksasa
    st.markdown("""
        <style>
        .timer-kerja {
            font-size: 80px !important;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
            color: #EF4444;
            margin: 20px 0;
        }
        
        /* GAYA BLANK SCREEN TOTAL SAAT ISTIRAHAT */
        .blank-screen-break {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: #090D16; 
            z-index: 9999; 
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        /* FONT RAKSASA DI TENGAH LAYAR */
        .timer-break-raksasa {
            font-size: 30vh !important; 
            font-weight: 100; 
            font-family: 'Helvetica Neue', Arial, sans-serif;
            color: #10B981; 
            margin: 0;
            line-height: 1;
        }
        
        .sub-text-break {
            font-size: 24px;
            color: #64748B;
            margin-top: 20px;
            letter-spacing: 2px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Link audio cadangan yang ringkas & kompatibel tinggi dengan browser (.mp3)
    url_audio_beep = "https://www.soundjay.com/buttons/sounds/button-10.mp3"

    # ------------------------------------------
    # JALANNYA PROGRAM BERDASARKAN MODE
    # ------------------------------------------
    
    # KONDISI A: JIKA MASUK MODE ISTIRAHAT (BREAK) -> LAYAR JADI BLANK TOTAL
    if st.session_state.pomo_state == "BREAK":
        layar_blank = st.empty()
        
        while st.session_state.waktu_tersisa > 0 and st.session_state.pomo_state == "BREAK":
            menit = st.session_state.waktu_tersisa // 60
            detik = st.session_state.waktu_tersisa % 60
            tipe_istirahat = "SHORT BREAK" if st.session_state.durasi_istirahat == 5 * 60 else "LONG BREAK"
            
            layar_blank.markdown(f"""
                <div class="blank-screen-break">
                    <p style="color: #10B981; font-size: 18px; letter-spacing: 5px;">☕ {tipe_istirahat}</p>
                    <h1 class="timer-break-raksasa">{menit:02d}:{detik:02d}</h1>
                    <p class="sub-text-break">Silakan sandarkan badan & rileks sejenak</p>
                </div>
            """, unsafe_allow_html=True)
            
            time.sleep(1)
            st.session_state.waktu_tersisa -= 1

        if st.session_state.waktu_tersisa <= 0 and st.session_state.pomo_state == "BREAK":
            st.session_state.pomo_state = "IDLE"
            st.session_state.waktu_tersisa = 25 * 60
            st.balloons() 
            st.rerun()

    # KONDISI B: MODE STANDBY ATAU MODE KERJA FOKUS (Tampilan Menu Normal)
    else:
        kolom_judul, kolom_aksi = st.columns([3, 1])
        with kolom_judul:
            st.title("⏱️ Pomodoro Timer")
            st.caption(f"Life Balance Technic | Siklus Fokus Berhasil: {st.session_state.siklus_selesai}")
            
        with kolom_aksi:
            st.write("") 
            sub_kolom1, sub_kolom2 = st.columns(2)
            with sub_kolom1:
                if st.button("🚀 DEPLOY", type="primary", use_container_width=True):
                    if st.session_state.pomo_state == "IDLE":
                        st.session_state.pomo_state = "FOCUS"
                        st.session_state.waktu_tersisa = 25 * 60
                        st.rerun()
            with sub_kolom2:
                if st.button("🛑 STOP", type="secondary", use_container_width=True):
                    st.session_state.pomo_state = "IDLE"
                    st.session_state.waktu_tersisa = 25 * 60
                    st.rerun()

        st.write("---")

        # Proses Countdown Mode Fokus Kerja
        if st.session_state.pomo_state == "FOCUS":
            st.info("🔴 Sesi Kerja Sedang Berjalan. Tetaplah Fokus.")
            tempat_timer = st.empty()
            tempat_audio = st.empty()
            
            while st.session_state.waktu_tersisa > 0 and st.session_state.pomo_state == "FOCUS":
                menit = st.session_state.waktu_tersisa // 60
                detik = st.session_state.waktu_tersisa % 60
                tempat_timer.markdown(f'<p class="timer-kerja">{menit:02d}:{detik:02d}</p>', unsafe_allow_html=True)
                
                # REPEATER BELL: Bunyi tepat di 5 detik terakhir (5, 4, 3, 2, 1)
                if st.session_state.waktu_tersisa <= 5:
                    # Menggunakan kombinasi audio HTML5 modern yang dipaksa reload per detik
                    tempat_audio.markdown(
                        f"""
                        <iframe src="{url_audio_beep}" allow="autoplay" style="display:none"></iframe>
                        <audio autoplay><source src="{url_audio_beep}" type="audio/mp3"></audio>
                        """, 
                        unsafe_allow_html=True
                    )
                
                time.sleep(1)
                st.session_state.waktu_tersisa -= 1
                
            # Logika Otomatis Perpindahan Setelah 25 Menit Selesai
            if st.session_state.waktu_tersisa <= 0 and st.session_state.pomo_state == "FOCUS":
                st.session_state.siklus_selesai += 1
                
                if st.session_state.siklus_selesai % 4 == 0:
                    st.session_state.durasi_istirahat = 15 * 60  
                else:
                    st.session_state.durasi_istirahat = 5 * 60   
                
                st.session_state.pomo_state = "BREAK"
                st.session_state.waktu_tersisa = st.session_state.durasi_istirahat
                st.rerun()

        # Mode Siap / Diam (IDLE)
        else:
            st.info("💡 Klik tombol **DEPLOY** di kanan atas untuk memulai siklus fokus 25 menit.")
            menit = st.session_state.waktu_tersisa // 60
            detik = st.session_state.waktu_tersisa % 60
            st.markdown(f'<div style="text-align:center;"><p class="timer-kerja" style="color: #94A3B8;">{menit:02d}:{detik:02d}</p></div>', unsafe_allow_html=True)
