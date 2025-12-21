import streamlit as st
import math
import statistics
import re

# --- ページ設定 ---
st.set_page_config(page_title="Python Calculator", layout="centered")

# --- 画像デザインを再現するCSS ---
st.markdown("""
<style>
    header {visibility: hidden;}
    .main .block-container { padding-top: 2rem; max-width: 600px; }
    
    /* タイトル：画像通りのフォント感 */
    .calc-title { 
        text-align: center; font-size: 48px; font-weight: 800; 
        color: #2D3748; margin-bottom: 30px; font-family: sans-serif; 
    }
    
    /* ディスプレイ部分 */
    .display-container {
        display: flex; align-items: center; justify-content: flex-start;
        font-size: 50px; font-weight: bold; color: #2D3748;
        margin-bottom: 20px; padding-left: 10px;
    }
    .play-icon { color: #718096; margin-right: 15px; font-size: 40px; }

    /* 基本ボタン：白背景・細い枠線・角丸 */
    div.stButton > button {
        width: 100% !important; height: 55px !important;
        font-size: 18px !important; border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important; background-color: #fff !important;
        color: #4A5568 !important; transition: 0.2s;
    }

    /* ＝ ボタン：横長（3カラム分） */
    .eq-container div.stButton > button {
        height: 55px !important;
    }

    /* 赤い DELETE ボタン：最下部で横幅いっぱい */
    .delete-btn div.stButton > button {
        background-color: #FF4D4D !important; color: white !important;
        border: none !important; height: 60px !important;
        font-size: 20px !important; font-weight: bold !important;
        margin-top: 20px !important;
    }

    /* モードボタン：デザインを邪魔しないようシンプルに */
    .mode-section { margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px; }
    .mode-btn div.stButton > button {
        height: 40px !important; font-size: 14px !important;
        background-color: #F7FAFC !important;
    }

    /* カラムの隙間調整 */
    [data-testid="column"] { padding: 5px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
</style>
""", unsafe_allow_html=True)

# タイトル
st.markdown('<div class="calc-title">python calculator</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

# ディスプレイ（再生アイコン付き）
st.markdown(f'''
    <div class="display-container">
        <span class="play-icon">▶</span>
        <span>{st.session_state.formula if st.session_state.formula else "0"}</span>
    </div>
''', unsafe_allow_html=True)

# --- ロジック ---
def on_click(char):
    current = st.session_state.formula
    if current == "Error":
        st.session_state.formula = ""
        if char in ["=", "delete"]: return
        current = ""

    if char == "=":
        if not current: return
        try:
            f = current.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('π', 'math.pi').replace('e', 'math.e')
            res = eval(f, {"__builtins__": None}, {"math": math, "statistics": statistics})
            st.session_state.formula = format(res, '.10g')
        except: st.session_state.formula = "Error"
    elif char == "delete":
        st.session_state.formula = ""
    else:
        # 演算子連続入力制限
        ops = ["+", "×", "÷", "^^"]
        if current and current[-1] in (ops + ["−", "."]) and char in (ops + ["−", "."]): return
        st.session_state.formula += str(char)

def draw_row(labels):
    cols = st.columns(len(labels))
    for i, l in enumerate(labels):
        if cols[i].button(l, key=f"btn_{l}_{i}_{st.session_state.mode}"):
            on_click(l); st.rerun()

# --- 画像通りのボタン配置（6列） ---
draw_row(["7", "8", "9", "π", "÷", "+"])
draw_row(["4", "5", "6", "e", "√", "−"])
draw_row(["1", "2", "3", "i", "^^", "×"])

# 4段目：() 0 . と 横長の ＝
c1, c2, c3, c4 = st.columns([1, 1, 1, 3])
with c1: 
    if st.button("()"): on_click("()"); st.rerun()
with c2: 
    if st.button("0"): on_click("0"); st.rerun()
with c3: 
    if st.button("."): on_click("."); st.rerun()
with c4:
    st.markdown('<div class="eq-container">', unsafe_allow_html=True)
    if st.button("＝"): on_click("="); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 赤い DELETE ボタン
st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
if st.button("delete"): on_click("delete"); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- モード切替（機能維持のため下部に配置） ---
st.markdown('<div class="mode-section">', unsafe_allow_html=True)
m_cols = st.columns(4)
modes = ["通常", "科学計算", "巨数", "値数"]
for i, m in enumerate(modes):
    with m_cols[i]:
        st.markdown('<div class="mode-btn">', unsafe_allow_html=True)
        if st.button(m): st.session_state.mode = m; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# 追加機能の表示
if st.session_state.mode != "通常":
    st.write(f"**{st.session_state.mode}モードの追加機能:**")
    if st.session_state.mode == "科学計算":
        draw_row(["sin(", "cos(", "tan(", "log(", "exp(", "abs("])
    elif st.session_state.mode == "巨数":
        draw_row(["k", "M", "G", "T", "P", "E"])
    elif st.session_state.mode == "値数":
        draw_row(["平均(", "中央値(", "最大(", "最小(", "合計(", "分散("])
