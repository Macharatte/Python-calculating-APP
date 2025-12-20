cat << 'EOF' > final_app.py
import streamlit as st
import math

st.set_page_config(page_title="Python Calculator", layout="centered")

st.markdown("""
<style>
    header {visibility: hidden;}
    .main .block-container {padding-top: 0.5rem !important; max-width: 480px !important;}
    
    .title-text {
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin-top: -20px;
        margin-bottom: 5px;
    }

    div.stButton > button {
        width: 100% !important;
        height: 52px !important;
        border: 2px solid #333 !important;
        border-radius: 8px !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        margin: 2px 0px !important;
    }

    /* ＋キー：SVGで絶対に消えないように描画 */
    button[key="k_+"] {
        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'><path d='M20 10 v20 M10 20 h20' stroke='black' stroke-width='5' stroke-linecap='round'/></svg>") !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        color: rgba(0,0,0,0) !important;
    }

    .display-box {
        font-size: 30px;
        font-weight: bold;
        text-align: right;
        padding: 10px;
        background: #f8f9fa;
        border: 2px solid #333;
        border-radius: 8px;
        min-height: 55px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">Python Calculator</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

st.markdown(f'<div class="display-box">{st.session_state.formula if st.session_state.formula else "0"}</div>', unsafe_allow_html=True)

# 入力制限リスト
BANNED_FIRST = ["+", "×", "÷", "^^", "/", ".", "＝", ","]

def press(char):
    curr = st.session_state.formula
    
    # Error時のガード
    if curr == "Error":
        if char == "C": st.session_state.formula = ""
        return 

    # 先頭入力制限
    if not curr and char in BANNED_FIRST: return
    
    if char == "＝":
        if not curr: return
        try:
            f = curr.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = f.replace('π', 'math.pi').replace('e', 'math.e').replace('√', 'math.sqrt').replace('i', '1j').replace('^^', '**').replace('∞', 'float("inf")')
            for func in ["sin", "cos", "tan", "log", "abs", "round", "min", "max"]:
                f = f.replace(f"{func}(", f"math.{func}(")
            units = {'y': '*1e-24', 'z': '*1e-21', 'a': '*1e-18', 'f': '*1e-15', 'p': '*1e-12', 'n': '*1e-9', 'μ': '*1e-6', 'm': '*1e-3', 'c': '*1e-2', 'd': '*1e-1', 'da': '*1e1', 'h': '*1e2', 'k': '*1e3', 'M': '*1e6', 'G': '*1e9', 'T': '*1e12', 'P': '*1e15', 'E': '*1e18', 'Z': '*1e21', 'Y': '*1e24'}
            for u, v in units.items(): f = f.replace(u, v)
            st.session_state.formula = str(eval(f))
        except: st.session_state.formula = "Error"
    elif char == "C": st.session_state.formula = ""
    else:
        # 演算子の連続制限
        OPS = BANNED_FIRST + ["−"]
        if curr != "" and char in OPS and curr[-1] in OPS:
            st.session_state.formula = curr[:-1] + char
        else:
            st.session_state.formula += str(char)

# 1つ前と同じ並び方（6列構成）
rows = [
    ["7", "8", "9", "π", "÷", "+"],
    ["4", "5", "6", "e", "√", "−"],
    ["1", "2", "3", "i", "^^", "×"],
    ["()", "(", ")", "0", ".", "/"]
]

for row in rows:
    cols = st.columns(6)
    for i, key in enumerate(row):
        with cols[i]:
            disabled = (st.session_state.formula == "Error")
            if st.button(key, key=f"k_{key}", disabled=disabled):
                press(key); st.rerun()

# 補助ボタン：カンマを左端に配置
c1, c2, c3, c4 = st.columns([1, 1, 1, 3])
with c1:
    # カンマを左端に
    if st.button(",", key="k_comma", disabled=(st.session_state.formula == "Error")):
        press(","); st.rerun()
with c2:
    if st.button("C", key="btn_c"): st.session_state.formula = ""; st.rerun()
with c3:
    if st.button("＝", key="btn_eq", disabled=(st.session_state.formula == "Error")):
        press("＝"); st.rerun()
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

if st.session_state.mode == "科学計算":
    st.markdown("### 科学関数 ( ) で閉じるのを忘れずに")
    for r in [["sin(", "cos(", "tan(", "log("], ["abs(", "round(", "min(", "max("]]:
        cols = st.columns(4)
        for i, k in enumerate(r):
            with cols[i]:
                if st.button(k, key=f"s_{k}", disabled=(st.session_state.formula == "Error")):
                    st.session_state.formula += k; st.rerun()
elif st.session_state.mode == "巨数":
    st.markdown("### 巨数 & ∞")
    # ∞をリストの最後に復帰
    u_list = ["y", "z", "a", "f", "p", "n", "μ", "m", "c", "d", "da", "h", "k", "M", "G", "T", "P", "E", "Z", "Y", "∞"]
    cols = st.columns(7)
    for i, u in enumerate(u_list):
        with cols[i % 7]:
            if st.button(u, key=f"u_{u}", disabled=(st.session_state.formula == "Error")):
                st.session_state.formula += u; st.rerun()
EOF
