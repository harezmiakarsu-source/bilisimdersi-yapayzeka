from google import genai
import streamlit as st

# Sayfa yapılandırması
st.set_page_config(
    page_title="Bilişim Sınıfı Yapay Zeka Asistanı",
    page_icon="🤖",
)

st.title("🤖 Bilişim Sınıfı Yapay Zeka Asistanı")
st.write(
    "Merhaba! Bu ekranda hesap açmadan sorularınızı sorabilir, "
    "ödevlerinizde destek alabilirsiniz."
)

# API anahtarını Streamlit Secrets alanından al
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error(
        "API anahtarı bulunamadı. Streamlit Cloud ayarlarında "
        "Secrets bölümüne GOOGLE_API_KEY ekleyin."
    )
    st.stop()

# Sohbet geçmişini oturum boyunca sakla
if "messages" not in st.session_state:
    st.session_state.messages = []

# Önceki mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Öğrencinin mesaj kutusu
if prompt := st.chat_input("Sormak istediğin soruyu yaz..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        bot_reply = response.text or "Yanıt oluşturulamadı."
    except Exception as e:
        bot_reply = f"Bir hata oluştu: {e}"

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )