import streamlit as st
import math
import statistics
import re
import datetime

# --- ページ設定 ---
st.set_page_config(page_title="Python Calculator", layout="centered")

# --- 色彩反転（ライト/ダーク対応）＆ 1行表示CSS ---
st.markdown("""
<style>
    /* 1. 基本カラー変数の定義（システム設定に合わせて反転） */
    :root {
        --text-color: #000000;
        --bg-color: #FFFFFF;
        --border-color: #000000;
    }
    @media (prefers-color-scheme: dark) {
        :root {
            --text-color: #FFFFFF;
            --bg-color: #000000;
            --border-color: #FFFFFF;
        }
    }

    /* 2. 画面全体の背景と文字色 */
    .main .block-container {
        max-width: 95% !important; 
        padding: 5px 2px !important;
    }
    header {visibility: hidden;}
    
    /* 3. タイトルとディスプレイ */
    .calc-title {
        text-align: center;
        font-weight: 900 !important;
        font-size: 26px !important;
        color: var(--text-color) !important;
        margin-bottom: 10px !important;
        white-space: nowrap !important; /* 改行防止 */
    }

    .display-container {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-end !important;
        font-size: 55px !important;
        font-weight: 900 !important;
        margin-bottom: 15px !important;
        padding: 10px !important; 
        border-bottom: 5px solid var(--border-color) !important;
        min-height: 100px !important;
        color: var(--text-color) !important;
        word-break: break-all !important;
    }

    /* 4. ボタンデザイン（枠線色を自動反転） */
    div.stButton > button {
        width: 100% !important;
        height: 75px !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        border-radius: 8px !important;
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
        border: 2px solid var(--border-color) !important;
        transition: none !important;
        animation: none !important;
    }
    
    /* ボタン内テキストの改行を絶対に防止 */
    div.stButton > button p {
        color: var(--text-color) !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: clip !important;
        font-size: 18px !important; /* 科学計算などの長い文字用 */
    }

    /* 数字ボタンは大きく表示 */
    [data-testid="column"]:nth-child(-n+3) div.stButton > button p {
        font-size: 28px !important;
    }

    /* 5. 特殊ボタンの配色 */
    .del-btn div.stButton > button { background-color: #FF4B4B !important; border-color: var(--border-color) !important; }
    .eq-btn div.stButton > button { background-color: #2e7d32 !important; border-color: var(--border-color) !important; }
    
    .del-btn div.stButton > button p, .eq-btn div.stButton > button p { color: #FFFFFF !important; }

    /* モード切替エリアのテキスト1行強制 */
    .mode-text {
        color: var(--text-color) !important;
        font-weight: bold;
        margin-bottom: 8px;
        white-space: nowrap !important;
    }
</style>
""", unsafe_allow_html=True)

# タイトル
st.markdown('<div class="calc-title">PYTHON CALCULATOR</div>', unsafe_allow_html=True)

# --- 状態管理 ---
ss = st.session_state
if 'formula' not in ss: ss.formula = ""
if 'mode' not in ss: ss.mode = "通常"
if 'last_was_equal' not in ss: ss.last_was_equal = False
if 'history' not in ss: ss.history = []

# ディスプレイ表示
st.markdown(f'<div class="display-container"><span>{ss.formula if ss.formula else "0"}</span></div>', unsafe_allow_html=True)

# --- ロジック ---
def on_click(char):
    operators = ["+", "−", "×", "÷", "^^", ".", "°"]
    if ss.formula == "Error" or ss.last_was_equal:
        if char in operators and ss.formula != "Error": ss.last_was_equal = False
        else: ss.formula = ""; ss.last_was_equal = False

    if char == "＝":
        if not ss.formula: return
        try:
            f = ss.formula.replace('×', '*').replace('÷', '/').replace('−', '-').replace('m', '-')
            res = eval(f, {"math": math, "statistics": statistics, "abs": abs})
            res_str = format(res, '.10g')
            ss.history.insert(0, {"f": ss.formula, "r": res_str, "t": datetime.datetime.now().strftime("%H:%M")})
            ss.formula = res_str; ss.last_was_equal = True
        except: ss.formula = "Error"
    elif char == "delete": ss.formula = ""
    elif char == "(-)":
        if not ss.formula or ss.formula[-1] in ["+", "−", "×", "÷", "(", "^^"]: ss.formula += "−"
        else: on_click("−")
    else:
        if not ss.formula and char in operators: return
        if ss.formula and ss.formula[-1] in operators and char in operators:
            ss.formula = ss.formula[:-1] + str(char)
        else: ss.formula += str(char)

# --- キーパッド ---
main_btns = [
    "7", "8", "9", "π", "√",  "+",
    "4", "5", "6", "e", "^^", "−",
    "1", "2", "3", "i", "(-)", "×",
    "0", "00", ".", "(", ")", "÷"
]

cols = st.columns(6)
for i, b in enumerate(main_btns):
    with cols[i % 6]:
        if st.button(b, key=f"k{i}"): on_click(b); st.rerun()

# --- 下部ボタン ---
st.write("") 
bot_c1, bot_c2 = st.columns(2)
with bot_c1:
    st.markdown('<div class="del-btn">', unsafe_allow_html=True)
    if st.button("delete", use_container_width=True, key="btn_del"): on_click("delete"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with bot_c2:
    st.markdown('<div class="eq-btn">', unsafe_allow_html=True)
    if st.button("＝", use_container_width=True, key="btn_eq"): on_click("＝"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr style="margin:15px 0; border-color:var(--border-color); opacity:0.3;">', unsafe_allow_html=True)

# --- モード切替（1行表示を維持） ---
m_cols = st.columns(5)
modes = ["通常", "科学計算", "巨数", "値数", "履歴"]
for i, m in enumerate(modes):
    if m_cols[i].button(m, key=f"m{i}"):
        ss.mode = m
        st.rerun()

# モード別表示
if ss.mode != "通常":
    st.markdown(f'<div class="mode-text">MODE: {ss.mode}</div>', unsafe_allow_html=True)
    if ss.mode == "履歴":
        for i, item in enumerate(ss.history[:5]):
            if st.button(f"{item['f']} = {item['r']}", key=f"h{i}", use_container_width=True):
                ss.formula = item['r']; ss.mode = "通常"; st.rerun()
    else:
        if ss.mode == "巨数":
            extra = ["Q", "R", "Y", "Z", "E", "P", "T", "G", "M", "k", "h", "da", "d", "c", "m", "μ", "n", "p", "f", "a", "z", "y", "r", "q"]
        elif ss.mode == "科学計算":
            extra = ["sin(", "cos(", "tan(", "°", "abs(", "log("]
        elif ss.mode == "値数":
            extra = ["平均([", "中央値([", "最頻値([", "最大([", "最小([", "])", "偏差値(", "期待値(", ","]
        
        e_cols = st.columns(6)
        for i, b in enumerate(extra):
            with e_cols[i % 6]:
                if st.button(b, key=f"e{i}"): on_click(b); st.rerun()
