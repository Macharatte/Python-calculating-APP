import streamlit as st
import math
import statistics

# --- ページ設定 ---
st.set_page_config(page_title="Scientific Calculator", layout="centered")

st.markdown("""
<style>
    header {visibility: hidden;}
    .main .block-container {padding-top: 1rem !important; max-width: 500px !important;}
    div.stButton > button {
        width: 100% !important; height: 50px !important;
        font-size: 16px !important; font-weight: bold !important;
    }
    .display-box { 
        font-size: 28px; font-weight: bold; text-align: right; 
        padding: 15px; background: #202124; color: #ffffff;
        border-radius: 8px; min-height: 60px; margin-bottom: 15px;
        font-family: 'Courier New', monospace; word-wrap: break-word;
    }
</style>
""", unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

st.markdown('<div style="text-align:center; font-weight:bold;">Scientific Calculator Pro</div>', unsafe_allow_html=True)
st.markdown(f'<div class="display-box">{st.session_state.formula if st.session_state.formula else "0"}</div>', unsafe_allow_html=True)

# --- 計算・処理ロジック ---
def on_click(char):
    if char == "＝":
        if not st.session_state.formula: return
        try:
            f = st.session_state.formula.replace('×', '*').replace('÷', '/').replace('−', '-')
            # 置換処理
            f = f.replace('π', 'math.pi').replace('exp', 'math.e').replace('√', 'math.sqrt').replace('^^', '**')
            
            # 値数モード用（統計関数）の定義
            context = {
                "math": math,
                "mean": lambda x: statistics.mean(x),
                "median": lambda x: statistics.median(x),
                "mode": lambda x: statistics.mode(x),
                "max": max,
                "min": min,
                "abs": abs,
                "expected": lambda x, p: sum(xi * pi for xi, pi in zip(x, p)), # 簡易期待値
                "standard_score": lambda x, val: ((val - statistics.mean(x)) / statistics.stdev(x)) * 10 + 50 if len(x)>1 else "N/A"
            }
            
            # SI接頭辞
            units = {'y': '*1e-24', 'z': '*1e-21', 'a': '*1e-18', 'f': '*1e-15', 'p': '*1e-12', 'n': '*1e-9', 'μ': '*1e-6', 'm': '*1e-3', 'k': '*1e3', 'M': '*1e6', 'G': '*1e9', 'T': '*1e12'}
            for u, v in units.items(): f = f.replace(u, v)

            result = eval(f, {"__builtins__": None}, context)
            st.session_state.formula = str(result)
        except:
            st.session_state.formula = "Error"
    elif char == "C": st.session_state.formula = ""
    elif char == "del": st.session_state.formula = st.session_state.formula[:-1]
    else: st.session_state.formula += str(char)

# --- メインボタン ---
rows = [
    ["7", "8", "9", "π", "÷", "C"],
    ["4", "5", "6", "exp", "√", "−"],
    ["1", "2", "3", "i", "^^", "×"],
    ["(", "0", ")", ".", "＝", "del"]
]

for row in rows:
    cols = st.columns(len(row))
    for i, label in enumerate(row):
        if cols[i].button(label, key=f"main_{label}"):
            on_click(label); st.rerun()

st.write("---")
m_cols = st.columns(4)
modes = ["通常", "科学計算", "巨数", "値数"]
for i, m in enumerate(modes):
    if m_cols[i].button(m, key=f"m_{m}"):
        st.session_state.mode = m; st.rerun()

# --- モード別表示 ---
if st.session_state.mode == "科学計算":
    st.caption("科学関数")
    for r in [["sin(", "cos(", "tan(", "log("], ["abs(", "round(", "min(", "max("]]:
        cols = st.columns(4)
        for i, k in enumerate(r):
            if cols[i].button(k, key=f"sci_{k}"): st.session_state.formula += k; st.rerun()

elif st.session_state.mode == "巨数":
    st.caption("SI接頭辞")
    u_list = ["n", "μ", "m", "k", "M", "G", "T", "∞"]
    cols = st.columns(4)
    for i, u in enumerate(u_list):
        if cols[i].button(u, key=f"giant_{u}"): st.session_state.formula += u; st.rerun()

elif st.session_state.mode == "値数":
    st.caption("統計・値数解析 (カンマ区切り [1,2,3] 形式で使用)")
    # 平均値、最頻値、中央値、最大値、極大値、絶対値、期待値、偏差値、境界値、初期値
    v_rows = [
        ["mean(", "mode(", "median(", "max("],
        ["abs(", "期待値", "偏差値", "境界値"],
        ["初期値", "[", "]", ","]
    ]
    # 極大値は通常max、境界値・初期値は変数用ラベルとして配置
    for r in v_rows:
        cols = st.columns(4)
        for i, k in enumerate(r):
            if cols[i].button(k, key=f"val_{k}"):
                if k == "期待値": st.session_state.formula += "expected("
                elif k == "偏差値": st.session_state.formula += "standard_score("
                else: st.session_state.formula += k
                st.rerun()
