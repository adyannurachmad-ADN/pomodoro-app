import streamlit as st
import time

# ==========================================
# 0. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Life Balance by Adyan.Dev", 
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

    # Kustomisasi CSS Spesial & INJEKSI JAVASCRIPT AUDIO BROWSER (Mengatasi Blokir Autoplay)
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

        <script>
        // Fungsi Web Audio API untuk menghasilkan bunyi Beep murni secara lokal tanpa file eksternal
        function bunyikanBeep() {
            try {
                var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                var oscillator = audioCtx.createOscillator();
                var gainNode = audioCtx.createGain();
                
                oscillator.type = 'sine';
                oscillator.frequency.value = 880; // Frekuensi nada tinggi (A5)
                gainNode.gain.setValueAtTime(0.5, audioCtx.currentTime); // Volume 50%
                
                oscillator.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                
                oscillator.start();
                oscillator.stop(audioCtx.currentTime + 0.3); // Durasi bunyi 0.3 detik
            } catch(e) {
                console.log("AudioContext diblokir, butuh interaksi user klik pertama kali.");
            }
        }
        
        // Daftarkan fungsi ke window parent global agar bisa dipanggil dari sandbox iframe Streamlit
        window.mainbunyikanBeep = bunyikanBeep;
        </script>
    """, unsafe_allow_html=True)

    # Wadah kosong khusus untuk memicu skrip audio otomatis
    pemicu_audio = st.empty()

    # ------------------------------------------
    # JALANNYA PROGRAM BERDASARKAN MODE
    # ------------------------------------------
    
    # KONDISI A: JIKA MASUK MODE ISTIRAHAT (BREAK) -> LAYAR JADI BLANK TOTAL
    if st.session_state.pomo_state == "BREAK":
        layar_blank = st.empty()
        
        # Penyesuaian teks dinamis berdasarkan durasi istirahat yang sedang aktif
        if st.session_state.durasi_istirahat == 15 * 60:
            tipe_istirahat = "LONG BREAK"
            pesan_break = "Luar biasa! Nikmati istirahat panjang Anda sekarang."
        else:
            tipe_istirahat = "SHORT BREAK"
            pesan_break = "Silakan sandarkan badan & rileks sejenak"
        
        while st.session_state.waktu_tersisa > 0 and st.session_state.pomo_state == "BREAK":
            menit = st.session_state.waktu_tersisa // 60
            detik = st.session_state.waktu_tersisa % 60
            
            layar_blank.markdown(f"""
                <div class="blank-screen-break">
                    <p style="color: #10B981; font-size: 18px; letter-spacing: 5px;">☕ {tipe_istirahat}</p>
                    <h1 class="timer-break-raksasa">{menit:02d}:{detik:02d}</h1>
                    <p class="sub-text-break">{pesan_break}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Bunyi beep aba-aba pada 5 detik terakhir masa istirahat
            if st.session_state.waktu_tersisa <= 5:
                pemicu_audio.markdown("<script>window.parent.mainbunyikanBeep();</script>", unsafe_allow_html=True)
            
            time.sleep(1)
            st.session_state.waktu_tersisa -= 1

        # PERBAIKAN TOTAL: Begitu istirahat habis, langsung lempar kembali ke sesi FOCUS berikutnya secara otomatis!
        if st.session_state.waktu_tersisa <= 0 and st.session_state.pomo_state == "BREAK":
            st.session_state.pomo_state = "FOCUS"
            st.session_state.waktu_tersisa = 25 * 60  # Kembalikan ke durasi kerja 25 menit
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
                # Tombol deploy sekaligus berfungsi membuka segel (unlock) audio browser lewat interaksi klik pertama
                if st.button("🚀 DEPLOY", type="primary", use_container_width=True):
                    if st.session_state.pomo_state == "IDLE":
                        st.session_state.pomo_state = "FOCUS"
                        st.session_state.waktu_tersisa = 25 * 60
                        # Test bunyi sekali saat klik awal untuk memicu izin browser
                        st.markdown("<script>window.parent.mainbunyikanBeep();</script>", unsafe_allow_html=True)
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
            
            while st.session_state.waktu_tersisa > 0 and st.session_state.pomo_state == "FOCUS":
                menit = st.session_state.waktu_tersisa // 60
                detik = st.session_state.waktu_tersisa % 60
                tempat_timer.markdown(f'<p class="timer-kerja">{menit:02d}:{detik:02d}</p>', unsafe_allow_html=True)
                
                # Bunyi Beep berulang pada 5 detik terakhir sesi kerja
                if st.session_state.waktu_tersisa <= 5:
                    pemicu_audio.markdown("<script>window.parent.mainbunyikanBeep();</script>", unsafe_allow_html=True)
                
                time.sleep(1)
                st.session_state.waktu_tersisa -= 1
                
            # Logika Otomatis Perpindahan Setelah 25 Menit Selesai Kerja
            if st.session_state.waktu_tersisa <= 0 and st.session_state.pomo_state == "FOCUS":
                st.session_state.siklus_selesai += 1
                
                # Cek Modulo: Jika kelipatan 4, set ke istirahat panjang (15 Menit), sisanya istirahat pendek (5 Menit)
                if st.session_state.siklus_selesai % 4 == 0:
                    st.session_state.durasi_istirahat = 15 * 60  
                else:
                    st.session_state.durasi_istirahat = 5 * 60   
                
                # Langsung aktifkan mode break tanpa kembali ke mode IDLE
                st.session_state.pomo_state = "BREAK"
                st.session_state.waktu_tersisa = st.session_state.durasi_istirahat
                st.rerun()

        # Mode Siap / Diam (IDLE) - Hanya muncul saat aplikasi pertama kali dimuat
        else:
            st.info("💡 Klik tombol **DEPLOY** di kanan atas untuk memulai siklus fokus otomatis 25 menit.")
            menit = st.session_state.waktu_tersisa // 60
            detik = st.session_state.waktu_tersisa % 60
            st.markdown(f'<div style="text-align:center;"><p class="timer-kerja" style="color: #94A3B8;">{menit:02d}:{detik:02d}</p></div>', unsafe_allow_html=True)
