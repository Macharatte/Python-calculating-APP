import streamlit as st
import math
import statistics
import re
import datetime

# --- ページ設定 ---
st.set_page_config(page_title="Python Calculator", layout="centered")

# --- デザインCSS ---
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { overflow-x: hidden !important; width: 100vw; }
    header {visibility: hidden;}
    .main .block-container { padding: 1rem 0.5rem !important; max-width: 600px !important; }
    
    div.stButton > button {
        width: 100% !important; height: 65px !important;
        font-size: 20px !important; border-radius: 12px !important;
        font-weight: bold !important; background-color: var(--bg-color) !important;
        color: var(--text-color) !important; border: 2px solid var(--border-color) !important;
    }

    @media (max-width: 600px) {
        [data-testid="stHorizontalBlock"] { display: grid !important; grid-template-columns: repeat(3, 1fr) !important; gap: 8px !important; }
        div.stButton > button { height: 70px !important; font-size: 22px !important; }
    }

    .bottom-row [data-testid="column"] { flex: 1 !important; min-width: 0 !important; }
    @media (max-width: 600px) {
        .bottom-row [data-testid="stHorizontalBlock"] { grid-template-columns: repeat(2, 1fr) !important; }
    }

    .display-container {
        display: flex; align-items: center; justify-content: flex-end;
        font-size: 40px; font-weight: bold; margin-bottom: 20px; padding: 15px; 
        border-bottom: 4px solid currentColor; min-height: 90px; word-break: break-all;
    }

    :root { --bg-color: #000000; --text-color: #ffffff; --border-color: #333333; }
    @media (prefers-color-scheme: dark) { :root { --bg-color: #ffffff; --text-color: #000000; --border-color: #dddddd; } }
    
    .delete-btn-style div.stButton > button { background-color: #FF0000 !important; color: white !important; border: none !important; }
    .equal-btn-style div.stButton > button { background-color: #2e7d32 !important; color: white !important; border: none !important; }
    
    .mode-divider { margin: 10px 0 !important; padding: 0 !important; opacity: 0.5; }
    .calc-title { text-align: center; font-size: 32px; font-weight: 800; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="calc-title">python calculator</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"
if 'last_was_equal' not in st.session_state: st.session_state.last_was_equal = False
if 'history' not in st.session_state: st.session_state.history = []

st.markdown(f'<div class="display-container"><span>{st.session_state.formula if st.session_state.formula else "0"}</span></div>', unsafe_allow_html=True)

# --- 補助関数 ---
def calculate_t_score(score, data_list):
    if len(data_list) < 2: return "Error"
    sd = statistics.stdev(data_list)
    return (score - statistics.mean(data_list)) / sd * 10 + 50 if sd != 0 else 50.0

def calculate_expected_value(values, weights):
    if len(values) != len(weights): return "Error"
    return sum(v * w for v, w in zip(values, weights))

def on_click(char):
    current = st.session_state.formula
    operators = ["+", "−", "×", "÷", "^^", ".", "°"]

    if current == "Error" or st.session_state.last_was_equal:
        if char in operators and current != "Error":
            st.session_state.last_was_equal = False
        else:
            current = ""; st.session_state.formula = ""; st.session_state.last_was_equal = False

    if char == "＝":
        if not current: return
        try:
            original_f = current
            f = current.replace('×', '*').replace('÷', '/').replace('−', '-').replace('m', '-')
            f = f.replace(')]', '])')
            f = re.sub(r'([\d\.]+)\°', r'math.radians(\1)', f)
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('π', 'math.pi').replace('e', 'math.e')
            f = f.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan').replace('abs', 'abs').replace('log', 'math.log10')
            u_map = {'Q':'1e30','R':'1e27','Y':'1e24','Z':'1e21','E':'1e18','P':'1e15','T':'1e12','G':'1e9','M':'1e6','k':'1e3','h':'1e2','da':'1e1','d':'1e-1','c':'1e-2','m':'1e-3','μ':'1e-6','n':'1e-9','p':'1e-12','f':'1e-15','a':'1e-18','z':'1e-21','y':'1e-24','r':'1e-27','q':'1e-30'}
            for sym, val in u_map.items(): f = re.sub(rf'(\d+){sym}', rf'(\1*{val})', f)
            f = f.replace('平均', 'statistics.mean').replace('中央値', 'statistics.median').replace('最頻値', 'statistics.mode').replace('最大', 'max').replace('最小', 'min')
            f = re.sub(r'偏差値\((.*?),(\[.*?\])\)', r'calculate_t_score(\1,\2)', f)
            f = re.sub(r'期待値\((\[.*?\]),(\[.*?\])\)', r'calculate_expected_value(\1,\2)', f)
            
            res = eval(f, {"__builtins__": None}, {"math": math, "statistics": statistics, "calculate_t_score": calculate_t_score, "calculate_expected_value": calculate_expected_value, "abs": abs})
            res_str = format(res, '.10g')
            st.session_state.formula = res_str
            st.session_state.history.insert(0, {"f": original_f, "r": res_str, "t": datetime.datetime.now().strftime("%H:%M")})
            st.session_state.last_was_equal = True
        except: st.session_state.formula = "Error"
    elif char == "delete": st.session_state.formula = ""
    elif char == "(-)":
        if not current or current[-1] in ["+", "−", "×", "÷", "(", "^^"]:
            st.session_state.formula += "−"
        else: on_click("−")
    else:
        if not current and char in operators: return
        if current and current[-1] in operators and char in operators:
            st.session_state.formula = current[:-1] + str(char); return
        st.session_state.formula += str(char)

# --- キーパッド配置 (6列固定) ---
# 各縦列に4つずつ
main_btns = [
    "7", "8", "9", "π", "√",  "+", # 1行目
    "4", "5", "6", "e", "^^", "−", # 2行目
    "1", "2", "3", "i", "(-)", "×", # 3行目 ((-)は^^の下)
    "0", "00", ".", "(", ")", "÷"  # 4行目 ((はiの下)
]

cols = st.columns(6)
for i, b in enumerate(main_btns):
    with cols[i % 6]:
        if st.button(b, key=f"kb_{b}_{i}"): on_click(b); st.rerun()

# --- 5行目: delete と ＝ (50/50) ---
st.markdown('<div class="bottom-row">', unsafe_allow_html=True)
b_cols = st.columns(2)
with b_cols[0]:
    st.markdown('<div class="delete-btn-style">', unsafe_allow_html=True)
    if st.button("delete", use_container_width=True): on_click("delete"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with b_cols[1]:
    st.markdown('<div class="equal-btn-style">', unsafe_allow_html=True)
    if st.button("＝", use_container_width=True): on_click("＝"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="mode-divider">', unsafe_allow_html=True)

# モード切替
m_cols = st.columns(5)
modes = ["通常", "科学計算", "巨数", "値数", "履歴"]
for i, m in enumerate(modes):
    if m_cols[i].button(m, key=f"m_{m}"): st.session_state.mode = m; st.rerun()

# モード別ボタン表示
if st.session_state.mode != "通常":
    st.write(f"### {st.session_state.mode} モード")
    if st.session_state.mode == "履歴":
        for i, item in enumerate(st.session_state.history):
            if st.button(f"[{item['t']}] {item['f']} = {item['r']}", key=f"h_{i}", use_container_width=True):
                st.session_state.formula = item['r']; st.session_state.mode = "通常"; st.rerun()
        if st.session_state.history and st.button("クリア"): st.session_state.history = []; st.rerun()
    else:
        extra = []
        if st.session_state.mode == "巨数": extra = ["Q", "R", "Y", "Z", "E", "P", "T", "G", "M", "k", "h", "da", "d", "c", "m", "μ", "n", "p", "f", "a", "z", "y", "r", "q"]
        elif st.session_state.mode == "科学計算": extra = ["sin(", "cos(", "tan(", "°", "abs(", "log(", "(", ")", "e", "π", "√"]
        elif st.session_state.mode == "値数": extra = ["平均([", "中央値([", "最頻値([", "最大([", "最小([", "])", "偏差値(", "期待値(", ","]
        e_cols = st.columns(6)
        for i, b in enumerate(extra):
            with e_cols[i % 6]:
                if st.button(b, key=f"ex_{b}"): on_click(b); st.rerun()
