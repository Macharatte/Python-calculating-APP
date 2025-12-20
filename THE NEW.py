import streamlit as st
import math

# --- ページ設定とカスタムデザイン ---
st.set_page_config(page_title="Scientific Calculator", layout="centered")

st.markdown("""
<style>
    header {visibility: hidden;}
    .main .block-container {padding-top: 0.5rem !important; max-width: 500px !important;}
    .title-text { font-size: 20px; font-weight: bold; text-align: center; margin-top: -20px; margin-bottom: 5px; }
    div.stButton > button {
        width: 100% !important; height: 50px !important;
        border: 2px solid #333 !important; border-radius: 8px !important;
        font-size: 18px !important; font-weight: 800 !important; margin: 2px 0px !important;
    }
    .display-box { 
        font-size: 30px; font-weight: bold; text-align: right; 
        padding: 10px; background: #f8f9fa; border: 2px solid #333; 
        border-radius: 8px; min-height: 55px; margin-bottom: 5px; 
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">Scientific Calculator</div>', unsafe_allow_html=True)

# 状態の初期化
if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

st.markdown(f'<div class="display-box">{st.session_state.formula if st.session_state.formula else "0"}</div>', unsafe_allow_html=True)

BANNED_FIRST = ["+", "×", "÷", "^^", "/", ".", "＝", ","]

# --- 計算ロジック ---
def press(char):
    curr = st.session_state.formula
    if curr == "Error":
        if char == "C": st.session_state.formula = ""
        return 
    if not curr and char in BANNED_FIRST: return
    
    if char == "＝":
        if not curr: return
        try:
            f = curr.replace('×', '*').replace('÷', '/').replace('−', '-')
            # 数学定数・関数の置換
            f = f.replace('π', 'math.pi').replace('exp(', 'math.exp(').replace('exp', 'math.e').replace('√', 'math.sqrt').replace('i', '1j').replace('^^', '**').replace('∞', 'float("inf")')
            f = f.replace('10^', '10**')
            
            for func in ["sin", "cos", "tan", "log", "abs", "round", "min", "max"]:
                f = f.replace(f"{func}(", f"math.{func}(")
            
            # SI接頭辞の変換
            units = {'y': '*1e-24', 'z': '*1e-21', 'a': '*1e-18', 'f': '*1e-15', 'p': '*1e-12', 'n': '*1e-9', 'μ': '*1e-6', 'm': '*1e-3', 'c': '*1e-2', 'd': '*1e-1', 'da': '*1e1', 'h': '*1e2', 'k': '*1e3', 'M': '*1e6', 'G': '*1e9', 'T': '*1e12', 'P': '*1e15', 'Exa': '*1e18', 'Z': '*1e21', 'Y': '*1e24'}
            for u, v in units.items(): f = f.replace(u, v)
            
            st.session_state.formula = str(eval(f))
        except: st.session_state.formula = "Error"
    elif char == "C": st.session_state.formula = ""
    else:
        OPS = BANNED_FIRST + ["−"]
        if curr != "" and char in OPS and curr[-1] in OPS:
            st.session_state.formula = curr[:-1] + char
        else:
            st.session_state.formula += str(char)

# --- ボタンレイアウト ---
rows = [
    ["7", "8", "9", "π", "÷", "+"],
    ["4", "5", "6", "exp", "√", "−"],
    ["1", "2", "3", "i", "^^", "×"],
    ["()", "(", ")", "0", ".", "/"]
]

for row in rows:
    cols = st.columns(6)
    for i, key in enumerate(row):
        with cols[i]:
            if st.button(key, key=f"k_{key}", disabled=(st.session_state.formula == "Error")):
                press(key); st.rerun()

c1, c2, c3, c4 = st.columns([1, 1, 1, 3])
with c1:
    if st.button(",", key="k_comma", disabled=(st.session_state.formula == "Error")): press(","); st.rerun()
with c2:
    if st.button("C", key="btn_c"): st.session_state.formula = ""; st.rerun()
with c3:
    if st.button("＝", key="btn_eq", disabled=(st.session_state.formula == "Error")): press("＝"); st.rerun()
with c4:
    if st.button("delete", key="del_main"):
        if st.session_state.formula == "Error": st.session_state.formula = ""
        else: st.session_state.formula = st.session_state.formula[:-1]
        st.rerun()

st.write("---")
m_cols = st.columns(3)
for i, m in enumerate(["通常", "科学計算", "巨数"]):
    with m_cols[i]:
        if st.button(m, key=f"mode_{m}"): st.session_state.mode = m; st.rerun()

# --- モード別機能 ---
if st.session_state.mode == "科学計算":
    st.markdown("### 科学関数 & 指数入力")
    c_idx = st.columns(2)
    with c_idx[0]:
        if st.button("10^n (10のべき乗)", key="btn_10n"): st.session_state.formula += "10^"; st.rerun()
    with c_idx[1]:
        if st.button("exp( ) (指数関数)", key="btn_expf"): st.session_state.formula += "exp("; st.rerun()
        
    for r in [["sin(", "cos(", "tan(", "log("], ["abs(", "round(", "min(", "max("]]:
        cols = st.columns(4)
        for i, k in enumerate(r):
            with cols[i]:
                if st.button(k, key=f"s_{k}", disabled=(st.session_state.formula == "Error")):
                    st.session_state.formula += k; st.rerun()
elif st.session_state.mode == "巨数":
    st.markdown("### 巨数(SI接頭辞) & ∞")
    u_list = ["y", "z", "a", "f", "p", "n", "μ", "m", "c", "d", "da", "h", "k", "M", "G", "T", "P", "Exa", "Z", "Y", "∞"]
    cols = st.columns(7)
    for i, u in enumerate(u_list):
        with cols[i % 7]:
            if st.button(u, key=f"u_{u}", disabled=(st.session_state.formula == "Error")):
                st.session_state.formula += u; st.rerun()
