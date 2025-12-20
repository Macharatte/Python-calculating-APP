import streamlit as st
import math
import statistics
import re

# --- ページ設定と超強力なスタイル調整 ---
st.set_page_config(page_title="Scientific Calculator Pro", layout="centered")

st.markdown("""
<style>
    header {visibility: hidden;}
    /* 全体の余白を削る */
    .main .block-container {padding: 0.5rem !important; max-width: 550px !important;}
    
    /* ボタン同士の間隔をなくし、大きくする */
    div.stButton > button {
        width: 100% !important;
        height: 65px !important; /* ボタンの高さをアップ */
        font-size: 20px !important; /* 文字を大きく */
        font-weight: 900 !important;
        margin: 0px !important; /* 隙間をゼロに */
        padding: 0px !important;
        border: 1px solid #333 !important; /* 境界線を細く */
        border-radius: 0px !important; /* 四角くして密着させる */
        background-color: #fcfcfc;
    }
    
    /* ボタンの列(Column)自体の隙間も消す */
    [data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
    }
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important;
    }

    .display-box { 
        font-size: 35px; font-weight: bold; text-align: right; 
        padding: 20px; background: #202124; color: #00ff00; /* 緑文字で視認性アップ */
        border: 2px solid #555; border-radius: 5px; min-height: 80px; margin-bottom: 10px;
        font-family: 'Courier New', monospace; word-wrap: break-word;
    }
</style>
""", unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

st.markdown(f'<div class="display-box">{st.session_state.formula if st.session_state.formula else "0"}</div>', unsafe_allow_html=True)

# --- 計算ロジック（エラー完全ガード） ---
def on_click(char):
    if char == "＝":
        if not st.session_state.formula: return
        try:
            # 1. 単位を「保護記号」に一時変換（干渉防止）
            f = st.session_state.formula
            f = f.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('10^', '10**')
            f = f.replace('π', 'math.pi').replace('exp', 'math.e').replace('∞', 'float("inf")')

            # 2. 単位を安全に置換
            u_map = {
                'Y': '1e24', 'Z': '1e21', 'E': '1e18', 'P': '1e15', 'T': '1e12', 
                'G': '1e9', 'M': '1e6', 'k': '1e3', 'h': '1e2', 'da': '1e1',
                'd': '1e-1', 'c': '1e-2', 'm': '1e-3', 'μ': '1e-6', 'n': '1e-9', 
                'p': '1e-12', 'f': '1e-15', 'a': '1e-18', 'z': '1e-21', 'y': '1e-24'
            }
            for sym, val in u_map.items():
                # 数字の直後にある単位記号だけを (*1eX) に置換
                f = re.sub(rf'(\d+){sym}', rf'(\1*{val})', f)

            context = {
                "math": math,
                "平均": lambda x: statistics.mean(x) if x else 0,
                "中央値": lambda x: statistics.median(x) if x else 0,
                "最頻値": lambda x: statistics.mode(x) if x else 0,
                "偏差値": lambda x, v: ((v - statistics.mean(x)) / (statistics.stdev(x) if len(x)>1 else 1)) * 10 + 50 if x else 0,
                "abs": abs, "max": max, "min": min, "round": round,
                "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log
            }
            result = eval(f, {"__builtins__": None}, context)
            st.session_state.formula = format(result, '.10g')
        except:
            st.session_state.formula = "Error"
    elif char == "C": st.session_state.formula = ""
    elif char == "del": st.session_state.formula = st.session_state.formula[:-1]
    else: st.session_state.formula += str(char)

# --- UI レイアウト（ボタン密着配置） ---
def draw_row(labels):
    cols = st.columns(len(labels))
    for i, label in enumerate(labels):
        if cols[i].button(label, key=f"btn_{label}_{st.session_state.mode}"):
            on_click(label); st.rerun()

draw_row(["7", "8", "9", "π", "÷", "+"])
draw_row(["4", "5", "6", "exp", "√", "−"])
draw_row(["1", "2", "3", "i", "^^", "×"])
draw_row(["(", ")", "0", "00", ".", "C"])

# ＝ と delete を大きく配置
col_eq, col_del = st.columns(2)
if col_eq.button("＝", key="eq_big"): on_click("＝"); st.rerun()
if col_del.button("delete", key="del_big"): on_click("del"); st.rerun()

st.markdown("<div style='margin:10px;'></div>", unsafe_allow_html=True)
m_cols = st.columns(4)
for i, m in enumerate(["通常", "科学計算", "巨数", "値数"]):
    if m_cols[i].button(m, key=f"mode_{m}"):
        st.session_state.mode = m; st.rerun()

# --- 各モード表示 ---
if st.session_state.mode == "科学計算":
    draw_row(["sin(", "cos(", "tan(", "log("])
    draw_row(["abs(", "round(", "min(", "max("])
elif st.session_state.mode == "巨数":
    draw_row(["n", "μ", "m", "k", "M", "G"])
    draw_row(["T", "P", "E", "Z", "Y", "∞"])
elif st.session_state.mode == "値数":
    draw_row(["平均(", "最頻値(", "中央値(", "偏差値("])
    draw_row(["極大値", "境界値", "初期値", "abs("])
    draw_row(["[", "]", ",", "sin("])
