import streamlit as st
import math

# --- ページ設定 ---
st.set_page_config(page_title="Scientific Calculator", layout="centered")

# デザインの調整（ボタンの反応を視覚的にも分かりやすくします）
st.markdown("""
<style>
    header {visibility: hidden;}
    .main .block-container {padding-top: 1rem !important; max-width: 500px !important;}
    div.stButton > button {
        width: 100% !important; height: 50px !important;
        font-size: 18px !important; font-weight: bold !important;
    }
    .display-box { 
        font-size: 32px; font-weight: bold; text-align: right; 
        padding: 15px; background: #202124; color: #ffffff;
        border-radius: 8px; min-height: 65px; margin-bottom: 15px;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# 状態の初期化（ここが反応の肝です）
if 'formula' not in st.session_state:
    st.session_state.formula = ""
if 'mode' not in st.session_state:
    st.session_state.mode = "通常"

st.markdown('<div style="text-align:center; font-weight:bold;">Scientific Calculator</div>', unsafe_allow_html=True)
# 現在の式を表示
st.markdown(f'<div class="display-box">{st.session_state.formula if st.session_state.formula else "0"}</div>', unsafe_allow_html=True)

# --- 計算・処理関数 ---
def on_click(char):
    if char == "＝":
        if not st.session_state.formula: return
        try:
            # 計算用の置換
            f = st.session_state.formula.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = f.replace('π', 'math.pi').replace('exp(', 'math.exp(').replace('exp', 'math.e')
            f = f.replace('√', 'math.sqrt').replace('i', '1j').replace('^^', '**').replace('∞', 'float("inf")')
            f = f.replace('10^', '10**')
            
            # SI接頭辞の置換
            units = {'y': '*1e-24', 'z': '*1e-21', 'a': '*1e-18', 'f': '*1e-15', 'p': '*1e-12', 'n': '*1e-9', 'μ': '*1e-6', 'm': '*1e-3', 'c': '*1e-2', 'd': '*1e-1', 'da': '*1e1', 'h': '*1e2', 'k': '*1e3', 'M': '*1e6', 'G': '*1e9', 'T': '*1e12', 'P': '*1e15', 'Exa': '*1e18', 'Z': '*1e21', 'Y': '*1e24'}
            for u, v in units.items():
                if u in f: f = f.replace(u, v)
            
            # 安全な計算実行
            result = eval(f, {"__builtins__": None}, {"math": math, "float": float, "complex": complex})
            st.session_state.formula = str(result)
        except:
            st.session_state.formula = "Error"
    elif char == "C":
        st.session_state.formula = ""
    elif char == "del":
        st.session_state.formula = st.session_state.formula[:-1]
    else:
        st.session_state.formula += str(char)

# --- レイアウト構築 ---
# ボタンを押した瞬間に callback を使って状態を更新するように変更
def create_button(label, key=None):
    button_key = key if key else f"btn_{label}"
    if st.button(label, key=button_key, use_container_width=True):
        on_click(label)
        st.rerun()

# メインボタン
rows = [
    ["7", "8", "9", "π", "÷", "C"],
    ["4", "5", "6", "exp", "√", "−"],
    ["1", "2", "3", "i", "^^", "×"],
    ["(", "0", ")", ".", "＝", "del"]
]

for row in rows:
    cols = st.columns(len(row))
    for i, label in enumerate(row):
        with cols[i]:
            create_button(label)

st.write("---")
m_cols = st.columns(3)
with m_cols[0]:
    if st.button("通常", use_container_width=True): st.session_state.mode = "通常"; st.rerun()
with m_cols[1]:
    if st.button("科学計算", use_container_width=True): st.session_state.mode = "科学計算"; st.rerun()
with m_cols[2]:
    if st.button("巨数", use_container_width=True): st.session_state.mode = "巨数"; st.rerun()

# モード別ボタン
if st.session_state.mode == "科学計算":
    st.caption("科学関数")
    c_idx = st.columns(2)
    with c_idx[0]: create_button("10^")
    with c_idx[1]: create_button("exp(")
    
    for r in [["sin(", "cos(", "tan(", "log("], ["abs(", "round(", "min(", "max("]]:
        cols = st.columns(4)
        for i, k in enumerate(r):
            with cols[i]: create_button(k)

elif st.session_state.mode == "巨数":
    st.caption("SI接頭辞")
    u_list = ["y", "z", "a", "f", "p", "n", "μ", "m", "c", "d", "da", "h", "k", "M", "G", "T", "P", "Exa", "Z", "Y", "∞"]
    cols = st.columns(7)
    for i, u in enumerate(u_list):
        with cols[i % 7]: create_button(u)
