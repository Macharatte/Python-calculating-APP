import streamlit as st
import math
import statistics
import re

# --- ページ設定 ---
st.set_page_config(page_title="Python Calculator", layout="centered")

# --- デザインCSS（黒ボタン・白文字・隙間ゼロ） ---
st.markdown("""
<style>
    header {visibility: hidden;}
    .main .block-container { padding-top: 1rem; max-width: 600px; }
    
    .calc-title { 
        text-align: center; font-size: 42px; font-weight: 800; 
        color: #000; margin-bottom: 10px; font-family: sans-serif; 
    }
    
    .display-container {
        display: flex; align-items: center; justify-content: flex-end;
        font-size: 50px; font-weight: bold; color: #000;
        margin-bottom: 15px; padding: 10px; border-bottom: 3px solid #000;
        min-height: 80px;
    }

    /* 全ボタン共通：黒背景・白文字 */
    div.stButton > button {
        width: 100% !important; height: 55px !important;
        font-size: 20px !important; border-radius: 8px !important;
        border: 1px solid #333 !important; background-color: #000000 !important;
        color: #ffffff !important; font-weight: bold !important;
    }
    
    /* ＝ ボタン */
    .eq-container div.stButton > button { background-color: #222 !important; }

    /* delete ボタン：赤色 */
    .delete-btn div.stButton > button {
        background-color: #FF0000 !important; color: white !important;
        height: 60px !important; font-size: 22px !important; margin-top: 10px !important;
        border: none !important;
    }

    /* モードボタン */
    .mode-section { margin-top: 10px; }
    
    [data-testid="column"] { padding: 3px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="calc-title">python calculator</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

st.markdown(f'<div class="display-container"><span>{st.session_state.formula if st.session_state.formula else "0"}</span></div>', unsafe_allow_html=True)

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
            # SI接頭語置換
            u_map = {
                'Y': '1e24', 'Z': '1e21', 'E': '1e18', 'P': '1e15', 'T': '1e12', 'G': '1e9', 'M': '1e6', 'k': '1e3', 'h': '1e2', 'da': '1e1',
                'd': '1e-1', 'c': '1e-2', 'm': '1e-3', 'μ': '1e-6', 'n': '1e-9', 'p': '1e-12', 'f': '1e-15', 'a': '1e-18', 'z': '1e-21', 'y': '1e-24'
            }
            for sym, val in u_map.items(): f = re.sub(rf'(\d+){sym}', rf'(\1*{val})', f)
            
            # 値数モードの統計関数
            f = f.replace('平均', 'statistics.mean').replace('中央値', 'statistics.median')
            f = f.replace('最大', 'max').replace('最小', 'min').replace('合計', 'sum')
            
            res = eval(f, {"__builtins__": None}, {"math": math, "statistics": statistics})
            st.session_state.formula = format(res, '.10g')
        except: st.session_state.formula = "Error"
    elif char == "delete":
        st.session_state.formula = ""
    else:
        # 接頭語のガード：数字が前にない場合は入力を無視
        prefixes = ['Y','Z','E','P','T','G','M','k','h','da','d','c','m','μ','n','p','f','a','z','y']
        if char in prefixes:
            if not current or not current[-1].isdigit():
                return
        st.session_state.formula += str(char)

def draw_row(labels):
    cols = st.columns(len(labels))
    for i, l in enumerate(labels):
        if cols[i].button(l, key=f"btn_{l}_{i}_{st.session_state.mode}"):
            on_click(l); st.rerun()

# --- メイン配置（6列） ---
draw_row(["7", "8", "9", "π", "÷", "+"])
draw_row(["4", "5", "6", "e", "√", "−"])
draw_row(["1", "2", "3", "i", "^^", "×"])

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

st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
if st.button("delete"): on_click("delete"); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- モード切替セクション ---
st.markdown('<div class="mode-section">', unsafe_allow_html=True)
m_cols = st.columns(4)
modes = ["通常", "科学計算", "巨数", "値数"]
for i, m in enumerate(modes):
    if m_cols[i].button(m, key=f"m_{m}"):
        st.session_state.mode = m; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- 各モードの機能表示 ---
if st.session_state.mode == "巨数":
    st.write("単位入力（数字の後に打ってください）")
    draw_row(["Y", "Z", "E", "P", "T", "G"])
    draw_row(["M", "k", "h", "da", "d", "c"])
    draw_row(["m", "μ", "n", "p", "f", "a"])
    draw_row(["z", "y", "", "", "", ""]) 
elif st.session_state.mode == "科学計算":
    draw_row(["sin(", "cos(", "tan(", "log(", "exp(", "abs("])
elif st.session_state.mode == "値数":
    # リスト形式で計算するために [ ] を自動付与するボタン
    draw_row(["平均([", "中央値([", "最大([", "最小([", "合計([", "])"])
