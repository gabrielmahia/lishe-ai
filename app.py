import streamlit as st
import urllib.request, json

st.set_page_config(page_title="Lishe AI — Lishe na Usalama wa Chakula", page_icon="🥗", layout="centered")
st.markdown("""<style>
.stApp{background:#0a0e08;color:#f1f8e9}
.l-card{background:#1b2e1b;border:1px solid #33691e;border-radius:10px;padding:14px 18px;margin:8px 0}
.stButton>button{background:#558b2f;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY","")
SYSTEM = "Wewe ni mtaalamu wa lishe na usalama wa chakula Kenya. Jibu kwa Kiswahili. Toa ushauri wa vitendo unaofaa kwa bajeti za kawaida za Kenya. Sisitiza vyakula vya asili vya Kenya. Kumbuka matatizo ya usalama wa chakula kaskazini Kenya."

def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    body = {"contents":[{"role":"user","parts":[{"text":q}]}],
            "systemInstruction":{"parts":[{"text":SYSTEM}]},
            "generationConfig":{"temperature":0.3,"maxOutputTokens":600}}
    try:
        req = urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:
            return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"❌ {e}"

st.markdown("# 🥗 Lishe AI")
st.markdown("**Lishe Bora na Usalama wa Chakula Kenya**")
tab1,tab2,tab3 = st.tabs(["🍽️ Mlo Bora","👶 Watoto na Mama","🌽 Chakula cha Nafuu"])

with tab1:
    age2 = st.selectbox("Umri:", ["Mtoto (0-5)","Mtoto wa shule (6-12)","Kijana (13-18)","Mtu mzima","Mzee (60+)","Mama mjamzito","Mama anayenyonyesha"])
    budget = st.selectbox("Bajeti ya chakula kwa siku (KES):", ["Chini ya 100","100-300","300-500","500-1000","Zaidi ya 1000"])
    if st.button("🍽️ Pata Mlo Bora", key="meal_btn"):
        with st.spinner("..."): result = ask(f"Mlo bora wa kila siku kwa {age2} Kenya, bajeti ya KES {budget} kwa siku. Toa: Kiamsha kinywa, Chakula cha mchana, Chakula cha usiku, Vitafunio, Vyakula vya asili vya Kenya.")
        st.markdown(f'<div class="l-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab2:
    child_q = st.selectbox("Swali:", [
        "Mtoto wangu wa miezi 6 anakula nini sasa?",
        "Dalili za utapiamlo (malnutrition) kwa mtoto",
        "Mama mjamzito anahitaji chakula gani?",
        "Kunyonyesha — chakula gani kinasaidia maziwa?",
        "MUAC — ni nini na jinsi ya kupima?",
        "WFP/UNICEF Kenya — msaada wa chakula",
    ])
    if st.button("👶 Niambie", key="child_btn"):
        with st.spinner("..."): result = ask(child_q + " Kenya. Toa maelezo ya vitendo ya kisayansi.")
        st.markdown(f'<div class="l-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab3:
    region_lishe = st.selectbox("Mkoa:", ["Pwani","Nyanza","Rift Valley","Central","Eastern","North Eastern"])
    if st.button("🌽 Vyakula vya Asili na vya Nafuu", key="local_btn"):
        with st.spinner("..."): result = ask(f"Vyakula vya asili vya {region_lishe} Kenya ambavyo ni vya lishe na vya bei nafuu. Toa: Jina la chakula, Virutubisho, Jinsi ya kutayarisha, Bei ya makadirio.")
        st.markdown(f'<div class="l-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("🥗 Lishe AI v1.0 | WFP Kenya: wfp.org/kenya | UNICEF: unicef.org/kenya | CC BY-NC-ND 4.0")
