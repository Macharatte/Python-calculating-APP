import streamlit as st
import math
import statistics
import re

# --- ページ設定と超強力なスタイル調整（画面全体を使う設定） ---
st.set_page_config(page_title="Scientific Calculator Pro", layout="centered")

st.markdown("""
<style>
    /* 1. タイトルと全体の余白設定 */
    header {visibility: hidden;}
    .main .block-container {
        padding: 0rem !important; 
        max-width: 100% !important; /* 横幅いっぱいに広げる */
        margin-top: -50px;
    }
    
    /* 2. ボタンを1:1(正方形)かつ極太にする設定 */
    div.stButton > button {
        width: 100% !important;
        height: 80px !important; /* 高さを出して正方形に近づける */
        font-size: 24px !important;
        font-weight: 900 !important;
        margin: 0px !important;
        padding: 0px !important;
        border: 1px solid #000 !important;
        border-radius: 0px !important;
        background-color: #ffffff;
        color: #000000;
    }

    /* 3. ＝ と delete ボタンを横いっぱいに広げる設定 */
    .wide-btn div.stButton > button {
        height: 90px !important;
        font-size: 30px !important;
        background-color: #f0f0f0 !important;
    }
    
    /* 4. 隙間を完全にゼロにする */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }

    /* 5. ディスプレイ（計算結果） */
    .display-box { 
        font-size: 45px; font-weight: bold; text-align: right; 
        padding: 30px; background: #000000; color: #00ff00; 
        border: 2px solid #333; border-radius: 0px; min-height: 120px;
        font-family: 'Courier New', monospace; word-wrap: break-word;
    }
    
    /* 6. タイトルの装飾 */
    .calc-title {
        text-align: center; font-size: 24px; font-weight: bold;
        padding: 10px; background: #222; color: white;
    }
</style>
""", unsafe_allow_html=True)

# タイトルの表示
st.markdown('<div class="calc-title">SCIENTIFIC CALCULATOR PRO</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

# ディスプレイ表示
st.markdown(f'<div class="display-box">{st.session_state.formula if st.session_state.formula else "0"}</div>', unsafe_allow_html=True)

# --- 計算ロジック ---
def on_click(char):
    if char == "＝":
        if not st.session_state.formula: return
        try:
            f = st.session_state.formula
            f = f.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('10^', '10**')
            f = f.replace('π', 'math.pi').replace('exp', 'math.e').replace('∞', 'float("inf")')

            # SI接頭辞の置換
            u_map = {'Y':'1e24','Z':'1e21','E':'1e18','P':'1e15','T':'1e12','G':'1e9','M':'1e6','k':'1e3','h':'1e2','da':'1e1','d':'1e-1','c':'1e-2','m':'1e-3','μ':'1e-6','n':'1e-9','p':'1e-12','f':'1e-15','a':'1e-18','z':'1e-21','y':'1e-24'}
            for sym, val in u_map.items():
                f = re.sub(rf'(\d+){sym}', rf'(\1*{val})', f)

            context = {"math": math, "平均": lambda x: statistics.mean(x), "中央値": lambda x: statistics.median(x), "最頻値": lambda x: statistics.mode(x), "abs": abs, "max": max, "min": min, "round": round, "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log}
            result = eval(f, {"__builtins__": None}, context)
            st.session_state.formula = format(result, '.10g')
        except:
            st.session_state.formula = "Error"
    elif char == "C": st.session_state.formula = ""
    elif char == "del": st.session_state.formula = st.session_state.formula[:-1]
    else: st.session_state.formula += str(char)

def draw_row(labels):
    cols = st.columns(len(labels))
    for i, label in enumerate(labels):
        if cols[i].button(label, key=f"btn_{label}_{i}"):
            on_click(label); st.rerun()

# --- メインレイアウト ---
# 1-4行目（正方形ボタン群）
draw_row(["7", "8", "9", "π", "÷", "+"])
draw_row(["4", "5", "6", "exp", "√", "−"])
draw_row(["1", "2", "3", "i", "^^", "×"])
draw_row(["(", ")", "0", "00", ".", "C"])

# ＝ と delete ボタン（横長、画面を二分割して埋め尽くす）
st.markdown('<div class="wide-btn">', unsafe_allow_html=True)
col_eq, col_del = st.columns(2)
with col_eq:
    if st.button("＝", key="eq_wide"): on_click("＝"); st.rerun()
with col_del:
    if st.button("DELETE", key="del_wide"): on_click("del"); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin:20px;'></div>", unsafe_allow_html=True)
# モード切替
m_cols = st.columns(4)
for i, m in enumerate(["通常", "科学計算", "巨数", "値数"]):
    if m_cols[i].button(m, key=f"mode_{m}"):
        st.session_state.mode = m; st.rerun()

# 各モードの追加ボタン
if st.session_state.mode == "科学計算":
    draw_row(["sin(", "cos(", "tan(", "log("])
    draw_row(["abs(", "round(", "min(", "max("])
elif st.session_state.mode == "巨数":
    draw_row(["y", "z", "a", "f", "p", "n"])
    draw_row(["μ", "m", "k", "M", "G", "T"])
    draw_row(["P", "E", "Z", "Y", "∞", "i"])
elif st.session_state.mode == "値数":
    draw_row(["平均(", "最頻値(", "中央値(", "偏差値("])
    draw_row(["極大値", "境界値", "初期値", "abs("])
