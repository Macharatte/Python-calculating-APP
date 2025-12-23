import streamlit as st
import math
import statistics
import re
import datetime

# --- ページ設定（高速化のため静的な設定を優先） ---
st.set_page_config(page_title="Python Calculator", layout="centered")

# --- デザインCSS（描画速度と可視性の向上） ---
st.markdown("""
<style>
    /* 全体のマージンを最小化して反応を速く見せる */
    .block-container { padding: 1rem 0.5rem !important; max-width: 600px !important; }
    header {visibility: hidden;}
    
    /* ボタンの基本スタイル（影を消して描画を速く） */
    div.stButton > button {
        width: 100% !important; height: 65px !important;
        font-size: 20px !important; border-radius: 12px !important;
        font-weight: bold !important; background-color: var(--bg-color) !important;
        color: var(--text-color) !important; border: 2px solid var(--border-color) !important;
        transition: none !important; /* アニメーションを無効化して高速化 */
    }

    /* 6列グリッドの強制維持（+キーの消失防止） */
    [data-testid="stHorizontalBlock"] {
        gap: 4px !important;
    }

    .display-container {
        display: flex; align-items: center; justify-content: flex-end;
        font-size: 40px; font-weight: bold; margin-bottom: 15px; padding: 15px; 
        border-bottom: 4px solid currentColor; min-height: 80px; word-break: break-all;
    }

    :root { --bg-color: #000000; --text-color: #ffffff; --border-color: #333333; }
    @media (prefers-color-scheme: dark) { :root { --bg-color: #ffffff; --text-color: #000000; --border-color: #dddddd; } }
    
    .delete-btn-style div.stButton > button { background-color: #FF0000 !important; color: white !important; border: none !important; }
    .equal-btn-style div.stButton > button { background-color: #2e7d32 !important; color: white !important; border: none !important; }
    
    .mode-divider { margin: 8px 0 !important; opacity: 0.3; }
    .calc-title { text-align: center; font-size: 28px; font-weight: 800; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="calc-title">python calculator</div>', unsafe_allow_html=True)

# --- 状態管理の高速アクセス ---
ss = st.session_state
if 'formula' not in ss: ss.formula = ""
if 'mode' not in ss: ss.mode = "通常"
if 'last_was_equal' not in ss: ss.last_was_equal = False
if 'history' not in ss: ss.history = []

st.markdown(f'<div class="display-container"><span>{ss.formula if ss.formula else "0"}</span></div>', unsafe_allow_html=True)

# --- 高速計算ロジック ---
def on_click(char):
    operators = ["+", "−", "×", "÷", "^^", ".", "°"]
    
    if ss.formula == "Error" or ss.last_was_equal:
        if char in operators and ss.formula != "Error":
            ss.last_was_equal = False
        else:
            ss.formula = ""; ss.last_was_equal = False

    if char == "＝":
        if not ss.formula: return
        try:
            f = ss.formula.replace('×', '*').replace('÷', '/').replace('−', '-').replace('m', '-')
            f = f.replace(')]', '])').replace('°', '*math.pi/180')
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('π', 'math.pi').replace('e', 'math.e')
            f = f.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan')
            f = f.replace('平均', 'statistics.mean').replace('中央値', 'statistics.median')
            
            # evalの実行速度を上げるため限定的なスコープで実行
            res = eval(f, {"math": math, "statistics": statistics, "abs": abs})
            res_str = format(res, '.10g')
            
            ss.history.insert(0, {"f": ss.formula, "r": res_str, "t": datetime.datetime.now().strftime("%H:%M")})
            ss.formula = res_str
            ss.last_was_equal = True
        except: ss.formula = "Error"
    elif char == "delete": ss.formula = ""
    elif char == "(-)":
        if not ss.formula or ss.formula[-1] in ["+", "−", "×", "÷", "(", "^^"]:
            ss.formula += "−"
        else:
            if ss.formula and ss.formula[-1] not in operators: ss.formula += "−"
    else:
        if not ss.formula and char in operators: return
        if ss.formula and ss.formula[-1] in operators and char in operators:
            ss.formula = ss.formula[:-1] + str(char); return
        ss.formula += str(char)

# --- キーパッド（1列4ボタン厳守） ---
# 1-3列:数字 | 4列:定数・( | 5列:√・^^・(-) | 6列:四則演算
main_btns = [
    "7", "8", "9", "π", "√",  "+",
    "4", "5", "6", "e", "^^", "−",
    "1", "2", "3", "i", "(-)", "×",
    "0", "00", ".", "(", ")", "÷"
]

# 描画の高速化のため、ループ内の条件分岐を削減
cols = st.columns(6)
for i, b in enumerate(main_btns):
    with cols[i % 6]:
        if st.button(b, key=f"k{i}"):
            on_click(b)
            st.rerun()

# 下部ボタン
st.markdown('<div class="bottom-row">', unsafe_allow_html=True)
b_cols = st.columns(2)
with b_cols[0]:
    st.markdown('<div class="delete-btn-style">', unsafe_allow_html=True)
    if st.button("delete", key="del"): on_click("delete"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with b_cols[1]:
    st.markdown('<div class="equal-btn-style">', unsafe_allow_html=True)
    if st.button("＝", key="eq"): on_click("＝"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="mode-divider">', unsafe_allow_html=True)

# モード切替（5列）
m_cols = st.columns(5)
modes = ["通常", "科学計算", "巨数", "値数", "履歴"]
for i, m in enumerate(modes):
    if m_cols[i].button(m, key=f"m{i}"): ss.mode = m; st.rerun()

# モード別コンテンツ
if ss.mode != "通常":
    st.write(f"**{ss.mode}**")
    if ss.mode == "履歴":
        for i, item in enumerate(ss.history[:5]): # 最新5件に絞って高速化
            if st.button(f"{item['f']} = {item['r']}", key=f"h{i}", use_container_width=True):
                ss.formula = item['r']; ss.mode = "通常"; st.rerun()
    else:
        # モードボタンも高速化のため整理
        extra = []
        if ss.mode == "巨数": extra = ["Q", "R", "Y", "Z", "E", "P", "T", "G", "M", "k", "h", "da", "d", "c", "m", "μ", "n", "p", "f", "a", "z", "y", "r", "q"]
        elif ss.mode == "科学計算": extra = ["sin(", "cos(", "tan(", "°", "abs(", "log(", "e", "π"]
        elif ss.mode == "値数": extra = ["平均([", "中央値([", "最頻値([", "最大([", "最小([", "])", "偏差値(", "期待値(", ","]
        e_cols = st.columns(6)
        for i, b in enumerate(extra):
            with e_cols[i % 6]:
                if st.button(b, key=f"e{i}"): on_click(b); st.rerun()
