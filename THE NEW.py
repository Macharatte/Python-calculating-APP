import streamlit as st
import math
import statistics
import re

# --- ページ設定とスタイル調整 ---
st.set_page_config(page_title="Scientific Calculator Pro", layout="centered")

st.markdown("""
<style>
    /* 1. 全体の余白を完全にゼロにして画面幅いっぱいに使う */
    header {visibility: hidden;}
    .main .block-container {
        padding: 0rem !important; 
        max-width: 100% !important;
        margin: 0px !important;
    }
    
    /* 2. ボタンを正方形(1:1)にするための高さ設定 */
    div.stButton > button {
        width: 100% !important;
        height: 85px !important; /* 1:1に近づけるため高さを確保 */
        font-size: 26px !important; /* 数字を見やすく大きく */
        font-weight: 900 !important;
        margin: 0px !important;
        padding: 0px !important;
        border: 1px solid #000 !important;
        border-radius: 0px !important;
        background-color: #ffffff;
        color: #000000;
    }

    /* 3. ＝ と DELETE ボタンを横いっぱいに広げるための特別な高さ */
    .wide-btn div.stButton > button {
        height: 100px !important;
        font-size: 32px !important;
        background-color: #e0e0e0 !important;
    }
    
    /* 4. カラム間の隙間を完全に除去 */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }

    /* 5. ディスプレイ（計算結果表示部） */
    .display-box { 
        font-size: 50px; font-weight: bold; text-align: right; 
        padding: 30px; background: #000000; color: #00ff00; 
        border-bottom: 3px solid #333; min-height: 130px;
        font-family: 'Courier New', monospace; word-wrap: break-word;
    }
    
    /* 6. タイトル */
    .calc-title {
        text-align: center; font-size: 26px; font-weight: bold;
        padding: 15px; background: #1a1a1a; color: #ffffff;
        border-bottom: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)

# タイトル
st.markdown('<div class="calc-title">SCIENTIFIC CALCULATOR PRO</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

# ディスプレイ
st.markdown(f'<div class="display-box">{st.session_state.formula if st.session_state.formula else "0"}</div>', unsafe_allow_html=True)

# --- 計算・処理ロジック ---
def on_click(char):
    if char == "＝":
        if not st.session_state.formula: return
        try:
            f = st.session_state.formula
            f = f.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('10^', '10**')
            f = f.replace('π', 'math.pi').replace('exp', 'math.e').replace('∞', 'float("inf")')
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

# --- ボタン配置 ---
# 6列構成で + を確実に右端へ
def draw_calc_row(labels):
    cols = st.columns(6) # 6列固定
    for i, label in enumerate(labels):
        if cols[i].button(label, key=f"btn_{label}_{i}"):
            on_click(label); st.rerun()

draw_calc_row(["7", "8", "9", "π", "÷", "+"])
draw_calc_row(["4", "5", "6", "exp", "√", "−"])
draw_calc_row(["1", "2", "3", "i", "^^", "×"])
draw_calc_row(["(", ")", "0", "00", ".", "C"])

# ＝ と DELETE ボタン（画面下部を2分割で占有）
st.markdown('<div class="wide-btn">', unsafe_allow_html=True)
col_eq, col_del = st.columns(2)
with col_eq:
    if st.button("＝", key="eq_w"): on_click("＝"); st.rerun()
with col_del:
    if st.button("DELETE", key="del_w"): on_click("del"); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
# モード切替
m_cols = st.columns(4)
for i, m in enumerate(["通常", "科学計算", "巨数", "値数"]):
    if m_cols[i].button(m, key=f"mode_{m}"):
        st.session_state.mode = m; st.rerun()

# 各モードのボタン
if st.session_state.mode == "科学計算":
    draw_calc_row(["sin(", "cos(", "tan(", "log(", "abs(", "round("])
elif st.session_state.mode == "巨数":
    draw_calc_row(["y", "z", "a", "f", "p", "n"])
    draw_calc_row(["μ", "m", "k", "M", "G", "T"])
elif st.session_state.mode == "値数":
    draw_calc_row(["平均(", "最頻値(", "中央値(", "偏差値(", "max(", "min("])
