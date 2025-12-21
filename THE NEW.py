import streamlit as st
import math
import statistics
import re

# --- ページ設定 ---
st.set_page_config(page_title="Python Calculator", layout="centered")

# --- デザインCSS ---
st.markdown("""
<style>
    header {visibility: hidden;}
    .main .block-container { padding-top: 1rem; max-width: 600px; }
    .calc-title { text-align: center; font-size: 42px; font-weight: 800; color: #000; margin-bottom: 10px; font-family: sans-serif; }
    .display-container {
        display: flex; align-items: center; justify-content: flex-end;
        font-size: 50px; font-weight: bold; color: #000;
        margin-bottom: 15px; padding: 10px; border-bottom: 3px solid #000; min-height: 80px;
    }
    div.stButton > button {
        width: 100% !important; height: 55px !important;
        font-size: 20px !important; border-radius: 8px !important;
        border: 1px solid #333 !important; background-color: #000000 !important;
        color: #ffffff !important; font-weight: bold !important;
    }
    .delete-btn div.stButton > button { background-color: #FF0000 !important; border: none !important; }
    [data-testid="column"] { padding: 3px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="calc-title">python calculator</div>', unsafe_allow_html=True)

# セッション状態の初期化
if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"
if 'last_was_equal' not in st.session_state: st.session_state.last_was_equal = False

st.markdown(f'<div class="display-container"><span>{st.session_state.formula if st.session_state.formula else "0"}</span></div>', unsafe_allow_html=True)

# --- カスタム計算関数 ---
def calculate_t_score(score, data_list):
    if len(data_list) < 2: return "Error"
    sd = statistics.stdev(data_list)
    if sd == 0: return 50.0
    return (score - statistics.mean(data_list)) / sd * 10 + 50

# --- ロジック ---
def on_click(char):
    current = st.session_state.formula
    
    # 1. エラー時または「＝」直後の挙動
    if current == "Error" or st.session_state.last_was_equal:
        # 演算子（+, -, ×, ÷, ^^）が押された場合は結果を引き継ぐ
        operators = ["+", "−", "×", "÷", "^^"]
        if st.session_state.last_was_equal and char in operators:
            st.session_state.last_was_equal = False
        else:
            # それ以外（数字や関数）が押された場合はクリアして新しく開始
            st.session_state.formula = ""
            current = ""
            st.session_state.last_was_equal = False
            if char in ["＝", "delete"]: return

    if char == "＝":
        if not current: return
        try:
            f = current.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('π', 'math.pi').replace('e', 'math.e')
            
            # SI接頭語置換
            u_map = {
                'Q': '1e30', 'R': '1e27', 'Y': '1e24', 'Z': '1e21', 'E': '1e18', 'P': '1e15', 'T': '1e12', 'G': '1e9', 'M': '1e6', 'k': '1e3', 'h': '1e2', 'da': '1e1',
                'd': '1e-1', 'c': '1e-2', 'm': '1e-3', 'μ': '1e-6', 'n': '1e-9', 'p': '1e-12', 'f': '1e-15', 'a': '1e-18', 'z': '1e-21', 'y': '1e-24', 'r': '1e-27', 'q': '1e-30'
            }
            for sym, val in u_map.items(): f = re.sub(rf'(\d+){sym}', rf'(\1*{val})', f)
            
            # 統計関数
            f = f.replace('平均', 'statistics.mean').replace('中央値', 'statistics.median').replace('最頻値', 'statistics.mode')
            f = f.replace('最大', 'max').replace('最小', 'min')
            f = re.sub(r'偏差値\((.*?),(\[.*?\])\)', r'calculate_t_score(\1,\2)', f)
            
            res = eval(f, {"__builtins__": None}, {"math": math, "statistics": statistics, "calculate_t_score": calculate_t_score})
            st.session_state.formula = format(res, '.10g')
            st.session_state.last_was_equal = True
        except:
            st.session_state.formula = "Error"
            st.session_state.last_was_equal = False
    elif char == "delete":
        st.session_state.formula = ""
        st.session_state.last_was_equal = False
    else:
        # 接頭語のガード
        prefixes = ['Q','R','Y','Z','E','P','T','G','M','k','h','da','d','c','m','μ','n','p','f','a','z','y','r','q']
        if char in prefixes and (not current or not current[-1].isdigit()): return
        st.session_state.formula += str(char)

def draw_row(labels):
    cols = st.columns(len(labels))
    for i, l in enumerate(labels):
        if not l: continue
        if cols[i].button(l, key=f"btn_{l}_{i}_{st.session_state.mode}"):
            on_click(l); st.rerun()

# メインボタン
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
    if st.button("＝"): on_click("＝"); st.rerun()

st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
if st.button("delete"): on_click("delete"); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# モード切替
st.write("---")
m_cols = st.columns(4)
modes = ["通常", "科学計算", "巨数", "値数"]
for i, m in enumerate(modes):
    if m_cols[i].button(m, key=f"m_{m}"): st.session_state.mode = m; st.rerun()

# モード別機能
if st.session_state.mode == "巨数":
    st.write("単位入力")
    draw_row(["Q", "R", "Y", "Z", "E", "P"])
    draw_row(["T", "G", "M", "k", "h", "da"])
    draw_row(["d", "c", "m", "μ", "n", "p"])
    draw_row(["f", "a", "z", "y", "r", "q"])
elif st.session_state.mode == "科学計算":
    st.write("科学関数")
    draw_row(["sin(", "cos(", "tan(", "log(", "exp(", "abs("])
elif st.session_state.mode == "値数":
    st.write("統計・偏差値")
    draw_row(["平均([", "中央値([", "最頻値([", "最大([", "最小([", "])"])
    draw_row(["偏差値(", ",", "", "", "", ""])
