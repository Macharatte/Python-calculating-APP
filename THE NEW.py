import streamlit as st
import math
import statistics
import re

# --- ページ設定 ---
st.set_page_config(page_title="Python Calculator", layout="centered")

# --- スマホ完全対応CSS（横スクロール禁止・横並び維持） ---
st.markdown("""
<style>
    /* ページ全体のスクロール制御 */
    html, body, [data-testid="stAppViewContainer"] {
        overflow-x: hidden !important;
        width: 100vw;
    }

    header {visibility: hidden;}
    
    .main .block-container { 
        padding: 1rem 0.3rem !important; /* 余白を最小化 */
        max-width: 100% !important;
        overflow-x: hidden !important;
    }
    
    /* 横並びを強制し、はみ出さないように自動縮小 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important; /* ボタン間の隙間を詰め、横並びを死守 */
        width: 100% !important;
    }

    [data-testid="column"] {
        flex: 1 !important;
        min-width: 0 !important; /* カラムが広がるのを防ぐ */
    }

    :root {
        --bg-color: #000000;
        --text-color: #ffffff;
        --border-color: #333333;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --bg-color: #ffffff;
            --text-color: #000000;
            --border-color: #dddddd;
        }
    }

    .calc-title { 
        text-align: center; font-size: 24px; font-weight: 800; 
        margin-bottom: 5px;
    }
    
    .display-container {
        display: flex; align-items: center; justify-content: flex-end;
        font-size: 35px; font-weight: bold;
        margin-bottom: 10px; padding: 10px; 
        border-bottom: 3px solid currentColor;
        min-height: 70px; word-break: break-all;
        width: 100%;
        box-sizing: border-box;
    }

    /* ボタンのデザイン調整 */
    div.stButton > button {
        width: 100% !important; 
        height: 55px !important; 
        font-size: 15px !important; /* スマホで入り切るサイズ */
        border-radius: 8px !important;
        border: 1px solid var(--border-color) !important; 
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important; 
        font-weight: bold !important;
        padding: 0 !important;
    }
    
    .delete-btn div.stButton > button {
        background-color: #FF0000 !important; color: white !important;
        height: 60px !important; font-size: 20px !important;
        border: none !important;
    }

    /* PC/iPad用の広い画面では文字を大きく */
    @media (min-width: 600px) {
        div.stButton > button { font-size: 20px !important; height: 70px !important; }
        .calc-title { font-size: 42px; }
        .display-container { font-size: 50px; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="calc-title">python calculator</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"
if 'last_was_equal' not in st.session_state: st.session_state.last_was_equal = False

st.markdown(f'<div class="display-container"><span>{st.session_state.formula if st.session_state.formula else "0"}</span></div>', unsafe_allow_html=True)

def on_click(char):
    current = st.session_state.formula
    operators = ["+", "−", "×", "÷", "^^", ".", "°"]

    if st.session_state.last_was_equal:
        if char in operators:
            st.session_state.last_was_equal = False
        else:
            current = ""; st.session_state.formula = ""; st.session_state.last_was_equal = False

    if char == "＝":
        if not current: return
        try:
            f = current.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = re.sub(r'([\d\.]+)\°', r'math.radians(\1)', f)
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('π', 'math.pi').replace('e', 'math.e')
            f = f.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan')
            f = f.replace('log', 'math.log10').replace('exp', 'math.exp').replace('abs', 'abs')
            u_map = {'Q':'1e30','R':'1e27','Y':'1e24','Z':'1e21','E':'1e18','P':'1e15','T':'1e12','G':'1e9','M':'1e6','k':'1e3','h':'1e2','da':'1e1','d':'1e-1','c':'1e-2','m':'1e-3','μ':'1e-6','n':'1e-9','p':'1e-12','f':'1e-15','a':'1e-18','z':'1e-21','y':'1e-24','r':'1e-27','q':'1e-30'}
            for sym, val in u_map.items(): f = re.sub(rf'(\d+){sym}', rf'(\1*{val})', f)
            f = f.replace('平均', 'statistics.mean').replace('中央値', 'statistics.median').replace('最頻値', 'statistics.mode').replace('最大', 'max').replace('最小', 'min')
            res = eval(f, {"__builtins__": None}, {"math": math, "statistics": statistics, "abs": abs})
            st.session_state.formula = format(res, '.10g')
            st.session_state.last_was_equal = True
        except: st.session_state.formula = "Error"
    elif char == "delete": st.session_state.formula = ""
    else:
        if not current:
            if char in ["+", "×", "÷", "^^", ".", "°"]: return
            st.session_state.formula += str(char); return
        if current[-1] in operators and char in operators:
            st.session_state.formula = current[:-1] + str(char); return
        st.session_state.formula += str(char)

def draw_row(labels):
    cols = st.columns(len(labels))
    for i, l in enumerate(labels):
        if not l: continue
        if cols[i].button(l, key=f"btn_{l}_{i}_{st.session_state.mode}"):
            on_click(l); st.rerun()

# レイアウト（すべてのデバイスで6列維持）
draw_row(["7", "8", "9", "π", "÷", "+"])
draw_row(["4", "5", "6", "e", "√", "−"])
draw_row(["1", "2", "3", "i", "^^", "×"])
draw_row(["(", ")", "0", "00", ".", "＝"])

st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
if st.button("delete", use_container_width=True): on_click("delete"); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
m_cols = st.columns(4)
modes = ["通常", "科学計算", "巨数", "値数"]
for i, m in enumerate(modes):
    if m_cols[i].button(m, key=f"m_{m}"): st.session_state.mode = m; st.rerun()

if st.session_state.mode == "巨数":
    st.write("単位入力")
    draw_row(["Q", "R", "Y", "Z", "E", "P"])
    draw_row(["T", "G", "M", "k", "h", "da"])
    draw_row(["d", "c", "m", "μ", "n", "p"])
    draw_row(["f", "a", "z", "y", "r", "q"])
elif st.session_state.mode == "科学計算":
    st.write("科学関数（度数法は数字の後に ° ）")
    draw_row(["sin(", "cos(", "tan(", "°", "abs(", "log("])
    draw_row(["(", ")", "e", "π", "√", ""]) 
elif st.session_state.mode == "値数":
    st.write("統計・偏差値")
    draw_row(["平均([", "中央値([", "最頻値([", "最大([", "最小([", "])"])
