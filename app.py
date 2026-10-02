import time

import streamlit as st
from google import genai


st.set_page_config(
    page_title="Bilişim Sınıfı Yapay Zeka Asistanı",
    page_icon="🤖",
)

st.title("🤖 Bilişim Sınıfı Yapay Zeka Asistanı")
st.write(
    "Merhaba! Bu ekranda hesap açmadan sorularınızı sorabilir, "
    "ödevlerinizde destek alabilirsiniz."
)

# API anahtarını Streamlit Cloud Secrets alanından al
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error(
        "API anahtarı bulunamadı. Streamlit Cloud ayarlarında "
        "Secrets bölümüne GOOGLE_API_KEY ekleyin."
    )
    st.stop()


# Sohbet geçmişini bu oturum boyunca sakla
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
        response = None

        # Geçici 503 yoğunluk hatalarında en fazla 3 kez dene
        for deneme in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                )
                break
            except Exception as error:
                hata = str(error)
                gecici_yogunluk_hatasi = (
                    "503" in hata or "UNAVAILABLE" in hata
                )

                if not gecici_yogunluk_hatasi or deneme == 2:
                    raise

                time.sleep(2 ** (deneme + 1))

        bot_reply = response.text or "Yanıt oluşturulamadı."

    except Exception as error:
        hata = str(error)

        if "503" in hata or "UNAVAILABLE" in hata:
            bot_reply = (
                "Gemini şu anda yoğun olduğu için yanıt veremedi. "
                "Lütfen kısa bir süre sonra tekrar deneyin."
            )
        else:
            bot_reply = f"Bir hata oluştu: {hata}"

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )