import streamlit as st
import math
import statistics
import re

# --- ページ設定 ---
st.set_page_config(page_title="Scientific Calculator Pro", layout="centered")

st.markdown("""
<style>
    header {visibility: hidden;}
    .main .block-container {padding-top: 1rem !important; max-width: 500px !important;}
    div.stButton > button {
        width: 100% !important; height: 50px !important;
        font-size: 15px !important; font-weight: bold !important;
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

# --- 計算ロジック ---
def on_click(char):
    if char == "＝":
        if not st.session_state.formula: return
        try:
            f = st.session_state.formula
            # 1. 表示用記号の置換（数学記号を優先）
            f = f.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('10^', '10**')
            f = f.replace('π', 'math.pi').replace('exp', 'math.e').replace('∞', 'float("inf")')

            # 2. SI接頭辞の安全な置換（数字の直後だけを狙い撃ち）
            units_list = [
                ('Y', '1e24'), ('Z', '1e21'), ('E', '1e18'), ('P', '1e15'), ('T', '1e12'), 
                ('G', '1e9'), ('M', '1e6'), ('k', '1e3'), ('h', '1e2'), ('da', '1e1'),
                ('d', '1e-1'), ('c', '1e-2'), ('m', '1e-3'), ('μ', '1e-6'), ('n', '1e-9'), 
                ('p', '1e-12'), ('f', '1e-15'), ('a', '1e-18'), ('z', '1e-21'), ('y', '1e-24')
            ]
            for u_symbol, u_value in units_list:
                f = re.sub(rf'(\d+){u_symbol}', rf'(\1*{u_value})', f)

            context = {
                "math": math,
                "平均": lambda x: statistics.mean(x) if x else 0,
                "中央値": lambda x: statistics.median(x) if x else 0,
                "最頻値": lambda x: statistics.mode(x) if x else 0,
                "偏差値": lambda x, v: ((v - statistics.mean(x)) / (statistics.stdev(x) if len(x)>1 else 1)) * 10 + 50 if x else 0,
                "abs": abs, "max": max, "min": min, "round": round,
                "sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log
            }
            result = eval(f, {"__builtins__": None}, context)
            st.session_state.formula = str(result)
        except Exception:
            st.session_state.formula = "Error"
    elif char == "C": st.session_state.formula = ""
    elif char == "del": st.session_state.formula = st.session_state.formula[:-1]
    else: st.session_state.formula += str(char)

# --- UI レイアウト ---
# 1-3行目（基本）
rows = [
    ["7", "8", "9", "π", "÷", "+"],
    ["4", "5", "6", "exp", "√", "−"],
    ["1", "2", "3", "i", "^^", "×"]
]
for row in rows:
    cols = st.columns(6)
    for i, label in enumerate(row):
        if cols[i].button(label, key=f"main_{label}"):
            on_click(label); st.rerun()

# 4行目（ご指定の配置： ( , ) , 0 , 00 , . , C ）
cols4 = st.columns(6)
row4 = ["(", ")", "0", "00", ".", "C"]
for i, label in enumerate(row4):
    if cols4[i].button(label, key=f"row4_{label}"):
        on_click(label); st.rerun()

# 5行目（＝ と delete を独立）
cols5 = st.columns(2)
if cols5[0].button("＝", key="btn_eq"): on_click("＝"); st.rerun()
if cols5[1].button("delete", key="btn_del"): on_click("del"); st.rerun()

st.write("---")
m_cols = st.columns(4)
for i, m in enumerate(["通常", "科学計算", "巨数", "値数"]):
    if m_cols[i].button(m, key=f"mode_{m}"):
        st.session_state.mode = m; st.rerun()

# --- モード別 ---
if st.session_state.mode == "科学計算":
    st.caption("科学関数")
    for r in [["sin(", "cos(", "tan(", "log("], ["abs(", "round(", "min(", "max("]]:
        cols = st.columns(4)
        for i, k in enumerate(r):
            if cols[i].button(k, key=f"sci_{k}"): st.session_state.formula += k; st.rerun()

elif st.session_state.mode == "巨数":
    st.caption("SI接頭辞 (数字の後に使用)")
    u_list = ["n", "μ", "m", "k", "M", "G", "T", "P", "E", "Z", "Y", "∞"]
    cols = st.columns(6)
    for i, u in enumerate(u_list):
        if cols[i].button(u, key=f"giant_{u}"): st.session_state.formula += u; st.rerun()

elif st.session_state.mode == "値数":
    st.caption("統計解析 ( [1,2,3] 形式 )")
    v_rows = [
        ["平均(", "最頻値(", "中央値(", "偏差値("],
        ["極大値", "境界値", "初期値", "abs("],
        ["[", "]", ",", "sin("]
    ]
    for r in v_rows:
        cols = st.columns(4)
        for i, k in enumerate(r):
            if cols[i].button(k, key=f"val_{k}"):
                if k == "極大値": st.session_state.formula += "max("
                else: st.session_state.formula += k
                st.rerun()
                
