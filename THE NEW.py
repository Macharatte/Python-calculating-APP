import streamlit as st
import math
import statistics
import re

# --- ページ設定とスタイル調整（余白を破壊して全画面化） ---
st.set_page_config(page_title="Scientific Calculator Pro", layout="centered")

st.markdown("""
<style>
    /* 1. 左右の余白を強制撤廃 */
    header {visibility: hidden;}
    .main .block-container {
        padding: 0rem !important; 
        max-width: 100% !important;
        margin: 0px !important;
    }
    
    /* 2. ボタンを極太の正方形にする */
    div.stButton > button {
        width: 100% !important;
        height: 90px !important; /* 高さを大幅アップして1:1に近づける */
        font-size: 28px !important; /* 文字を極太に */
        font-weight: 900 !important;
        margin: 0px !important;
        padding: 0px !important;
        border: 2px solid #000 !important; /* 枠線を太くして存在感を出す */
        border-radius: 0px !important;
        background-color: #ffffff;
        color: #000000;
        display: block !important;
    }

    /* 3. ＝ と DELETE ボタン（画面の半分ずつを占有） */
    .wide-btn div.stButton > button {
        height: 110px !important;
        font-size: 35px !important;
        background-color: #e0e0e0 !important;
        color: #ff0000 !important; /* DELETEを目立たせる */
    }
    
    /* 4. カラムの隙間を完全にゼロにする */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }

    /* 5. ディスプレイ（計算結果） */
    .display-box { 
        font-size: 55px; font-weight: bold; text-align: right; 
        padding: 30px; background: #000000; color: #00ff00; 
        border-bottom: 5px solid #333; min-height: 140px;
        font-family: 'Courier New', monospace; word-wrap: break-word;
    }
    
    .calc-title {
        text-align: center; font-size: 28px; font-weight: bold;
        padding: 15px; background: #1a1a1a; color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# タイトル
st.markdown('<div class="calc-title">SCIENTIFIC CALCULATOR PRO</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

# ディスプレイ
st.markdown(f'<div class="display-box">{st.session_state.formula if st.session_state.formula else "0"}</div>', unsafe_allow_html=True)

# --- 計算ロジック ---
def on_click(char):
    if char == "＝":
        if not st.session_state.formula: return
        try:
            # ＋を含む全演算子の置換
            f = st.session_state.formula
            f = f.replace('×', '*').replace('÷', '/').replace('−', '-')
            # その他の数学関数
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('10^', '10**')
            f = f.replace('π', 'math.pi').replace('exp', 'math.e')
            # SI接頭辞
            u_map = {'Y':'1e24','Z':'1e21','E':'1e18','P':'1e15','T':'1e12','G':'1e9','M':'1e6','k':'1e3','m':'1e-3','μ':'1e-6','n':'1e-9','p':'1e-12'}
            for sym, val in u_map.items():
                f = re.sub(rf'(\d+){sym}', rf'(\1*{val})', f)
            
            context = {"math": math, "statistics": statistics}
            result = eval(f, {"__builtins__": None}, context)
            st.session_state.formula = format(result, '.10g')
        except:
            st.session_state.formula = "Error"
    elif char == "C": st.session_state.formula = ""
    elif char == "del": st.session_state.formula = st.session_state.formula[:-1]
    else: st.session_state.formula += str(char)

# --- ボタン配置（5列にして1つ1つを太くする） ---
def draw_calc_row(labels):
    cols = st.columns(len(labels))
    for i, label in enumerate(labels):
        if cols[i].button(label, key=f"btn_{label}_{i}_{st.session_state.mode}"):
            on_click(label); st.rerun()

# 1つ1つを太く見せるため、1行を5列に変更（＋を右端に配置）
draw_calc_row(["7", "8", "9", "÷", "+"])
draw_calc_row(["4", "5", "6", "×", "−"])
draw_calc_row(["1", "2", "3", "√", "π"])
draw_calc_row(["(", ")", "0", "00", "."])
draw_calc_row(["C", "i", "exp", "^^", "del"])

# ＝ と DELETE を画面下部に巨大配置
st.markdown('<div class="wide-btn">', unsafe_allow_html=True)
col_eq, col_del = st.columns(2)
with col_eq:
    if st.button("＝", key="eq_huge"): on_click("＝"); st.rerun()
with col_del:
    if st.button("DELETE", key="del_huge"): on_click("del"); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
m_cols = st.columns(4)
for i, m in enumerate(["通常", "科学計算", "巨数", "値数"]):
    if m_cols[i].button(m, key=f"mode_{m}"):
        st.session_state.mode = m; st.rerun()

# モード切替時のボタン
if st.session_state.mode == "科学計算":
    draw_calc_row(["sin(", "cos(", "tan(", "log(", "abs("])
elif st.session_state.mode == "巨数":
    draw_calc_row(["n", "μ", "m", "k", "M", "G", "T"])
elif st.session_state.mode == "値数":
    draw_calc_row(["平均(", "最頻値(", "中央値(", "max(", "min("])
