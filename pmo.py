import streamlit as st
import time

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Pomodoro Studio by 4dy4n.Dev",
    page_icon="⏱️",
    layout="centered"
)

# ==========================================
# INISIALISASI STATE (Manajemen Memori RAM)
# ==========================================
if "current_time" not in st.session_state:
    st.session_state.current_time = 25 * 60
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "session_type" not in st.session_state:
    st.session_state.session_type = "Fokus Kerja"

# Kontainer dinamis tunggal untuk memisahkan rendering
blank_container = st.empty()

# ==========================================
# CUSTOM CSS (STRUKTUR BASE TEMA GELAP)
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background-color: #12161a !important;
        color: #e3e8ed !important;
    }
    .stDeployButton { display:none; }
    footer { visibility: hidden; }
    
    .timer-display {
        font-family: 'Courier New', Courier, monospace;
        font-size: 6rem;
        font-weight: bold;
        color: #00f0ff;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
        text-align: center;
        background-color: #1a2129;
        border: 1px solid #2d3846;
        padding: 15px;
        border-radius: 18px;
        margin: 20px 0;
    }
    
    h1, h2, h3, h4, h5, h6, p, span {
        color: #e3e8ed !important;
    }
    
    .stButton>button {
        background-color: #1a2129 !important;
        color: #e3e8ed !important;
        border: 1px solid #2d3846 !important;
        border-radius: 10px !important;
    }
    .stButton>button:hover {
        border-color: #00f0ff !important;
        color: #00f0ff !important;
    }

    /* ──► GAYA LOCK SCREEN UTAMA (Z-INDEX ABSOLUT) ◄── */
    .cyber-blank-overlay {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        background-color: #000000 !important;
        z-index: 999999 !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-family: 'Courier New', Courier, monospace;
    }
    
    .blank-status {
        font-size: 2vw;
        color: #ffffff !important;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 10px;
    }
    
    .mega-countdown {
        font-size: 14vw;
        font-weight: bold;
        color: #00f0ff !important;
        text-shadow: 0 0 35px rgba(0, 240, 255, 0.9), 0 0 10px rgba(0, 240, 255, 0.6);
        line-height: 1;
        margin-bottom: 20px;
    }
    
    .blank-instruction {
        font-size: 1.5vw;
        color: #888888 !important;
        letter-spacing: 1px;
    }
    
    .top-right-panel {
        position: absolute;
        top: 30px;
        right: 40px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .btn-stop {
        border: 2px solid #ffffff !important;
        color: #ffffff !important;
        background: transparent;
        padding: 8px 18px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 14px;
        letter-spacing: 1px;
    }
    .btn-deploy {
        border: 2px solid #00f0ff !important;
        color: #00f0ff !important;
        background: transparent;
        padding: 8px 18px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 14px;
        letter-spacing: 1px;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
    }
    .divider-dots {
        color: #666666 !important;
        font-weight: bold;
        font-size: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# ANTARMUKA MODE NORMAL (MENU DASHBOARD)
# ==========================================
if not ("Istirahat" in st.session_state.session_type and st.session_state.timer_running):
    st.title("⏱️ Pomodoro Studio")
    st.write("Kelola ritme kerja dan relaksasi Anda dengan antarmuka gelap yang nyaman di mata.")
    st.divider()

    col_mode1, col_mode2, col_mode3 = st.columns(3)
    with col_mode1:
        if st.button("🎯 Sesi Fokus (25 Menit)", key="fokus_btn"):
            st.session_state.current_time = 25 * 60
            st.session_state.session_type = "Fokus Kerja"
            st.session_state.timer_running = False
            st.rerun()
    with col_mode2:
        if st.button("☕ Istirahat Pendek (5 Menit)", key="rehat_p_btn"):
            st.session_state.current_time = 5 * 60
            st.session_state.session_type = "Istirahat Pendek"
            st.session_state.timer_running = False
            st.rerun()
    with col_mode3:
        if st.button("🌳 Istirahat Panjang (15 Menit)", key="rehat_j_btn"):
            st.session_state.current_time = 15 * 60
            st.session_state.session_type = "Istirahat Panjang"
            st.session_state.timer_running = False
            st.rerun()

    st.subheader(f"Status Sesi: {st.session_state.session_type}")
    
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        if st.button("▶️ Mulai Sesi", key="start_btn"): 
            st.session_state.timer_running = True
            st.rerun()
    with col_ctrl2:
        if st.button("⏸️ Jeda (Pause)", key="pause_btn"): 
            st.session_state.timer_running = False
            st.rerun()

# ==========================================
# LOGIKA INTI SIKLUS WAKTU (WHILE LOOP)
# ==========================================
while st.session_state.timer_running and st.session_state.current_time > 0:
    mins, secs = divmod(st.session_state.current_time, 60)
    
    if "Istirahat" in st.session_state.session_type:
        blank_container.markdown(f"""
            <div class="cyber-blank-overlay">
                <div class="top-right-panel">
                    <button class="btn-stop">🏃 STOP</button>
                    <span class="divider-dots">:</span>
                    <button class="btn-deploy">🚀 DEPLOY</button>
                </div>
                <div class="blank-status">SESSION: {st.session_state.session_type.upper()} ACTIVE 🔔</div>
                <div class="mega-countdown">{mins:02d}:{secs:02d}</div>
                <div class="blank-instruction">Pejamkan mata sejenak...</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        blank_container.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
        
    time.sleep(1)
    st.session_state.current_time -= 1
    
    # TRANSISI MANAJEMEN WAKTU HABIS
    if st.session_state.current_time == 0:
        st.session_state.timer_running = False
        blank_container.empty() 
        
        if st.session_state.session_type == "Fokus Kerja":
            # ──► INTERSEPTOR AUDIO: Pemicu Efek Bunyi Alarm 5 Kali ◄──
            # Membuat sintaks Audio Sintetis Web browser (Frekuensi 800Hz selama 0.15 detik sebanyak 5 putaran)
            st.components.v1.html("""
                <script>
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                let count = 0;
                function playBeep() {
                    if(count >= 5) return;
                    const oscillator = audioCtx.createOscillator();
                    const gainNode = audioCtx.createGain();
                    oscillator.type = 'sine';
                    oscillator.frequency.value = 800; 
                    gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
                    oscillator.connect(gainNode);
                    gainNode.connect(audioCtx.destination);
                    oscillator.start();
                    oscillator.stop(audioCtx.currentTime + 0.15);
                    count++;
                    setTimeout(playBeep, 400); // Jeda antar bunyi bip (400ms)
                }
                playBeep();
                </script>
            """, height=0, width=0)
            
            # Berikan waktu 2 detik agar browser menyelesaikan putaran lagunya sebelum pindah screen
            time.sleep(2)
            
            st.session_state.session_type = "Istirahat Pendek"
            st.session_state.current_time = 5 * 60
            st.session_state.timer_running = True 
        else:
            st.session_state.session_type = "Fokus Kerja"
            st.session_state.current_time = 25 * 60
            st.session_state.timer_running = False 
            st.balloons()
            
        st.rerun()

# Tampilan Kondisi Jeda / Statis (Saat posisi Timer Berhenti)
if not ("Istirahat" in st.session_state.session_type and st.session_state.timer_running):
    mins, secs = divmod(st.session_state.current_time, 60)
    blank_container.markdown(f'<div class="timer-display">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)