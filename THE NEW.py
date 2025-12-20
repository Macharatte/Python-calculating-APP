import streamlit as st
import math

# --- ページ設定とデザイン ---
st.set_page_config(page_title="Scientific Calculator", layout="centered")
st.markdown("""
<style>
    .main .block-container {padding-top: 1rem; max-width: 500px;}
    .display-box { 
        font-size: 32px; font-weight: bold; text-align: right; 
        padding: 15px; background: #f1f3f4; border: 2px solid #202124; 
        border-radius: 10px; min-height: 60px; margin-bottom: 20px;
        color: #202124; font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# 状態の初期化
if 'formula' not in st.session_state:
    st.session_state.formula = ""

# 表示部
st.title("🧪 化学・科学計算電卓")
st.markdown(f'<div class="display-box">{st.session_state.formula if st.session_state.formula else "0"}</div>', unsafe_allow_html=True)

# --- 計算ロジック ---
def press(char):
    if char == "＝":
        try:
            # 表示用記号を計算用記号に置換
            f = st.session_state.formula
            f = f.replace('×', '*').replace('÷', '/').replace('−', '-')
            # 科学計算用の置換
            f = f.replace('exp(', 'math.exp(')
            f = f.replace('10^', '10**')
            
            result = eval(f)
            # 指数表記が必要なほど大きい/小さい場合は指数表記にする
            if abs(result) > 1e6 or (0 < abs(result) < 1e-4):
                st.session_state.formula = f"{result:.4e}"
            else:
                st.session_state.formula = str(result)
        except Exception:
            st.session_state.formula = "Error"
    elif char == "C":
        st.session_state.formula = ""
    else:
        st.session_state.formula += str(char)

# --- ボタン配置 ---
# 通常の数字と演算子
rows = [
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "−"],
    ["0", ".", "C", "＝"]
]

for row in rows:
    cols = st.columns(4)
    for i, key in enumerate(row):
        if cols[i].button(key, use_container_width=True):
            press(key)
            st.rerun()

st.markdown("---")
st.write("🔬 **科学計算ツール**")
c1, c2 = st.columns(2)
if c1.button("exp (自然対数の底e)", use_container_width=True):
    st.session_state.formula += "exp("
    st.rerun()
if c2.button("10^n (10のべき乗)", use_container_width=True):
    st.session_state.formula += "10^"
    st.rerun()
