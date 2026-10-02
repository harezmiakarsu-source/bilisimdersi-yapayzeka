import streamlit as st
from google import genai

# Sayfa yapılandırması
st.set_page_config(
    page_title="Bilişim Sınıfı Yapay Zeka Asistanı", page_icon="🤖"
)

st.title("🤖 Bilişim Sınıfı Yapay Zeka Asistanı")
st.write(
    "Merhaba! Bu ekranda hesap açmadan sorularınızı sorabilir, ödevlerinizde"
    " destek alabilirsiniz."
)

# API anahtarını güvenli bir şekilde Streamlit gizli alanından (secrets) alıyoruz
try:
  api_key = st.secrets["GOOGLE_API_KEY"]
  client = genai.Client(api_key=api_key)
except Exception as e:
  st.error(
      "API anahtarı bulunamadı! Lütfen Streamlit Cloud ayarlarından Secrets"
      " bölümüne GOOGLE_API_KEY ekleyin."
  )
  st.stop()

# Sohbet geçmişini hafızada tutma
if "messages" not in st.session_state:
  st.session_state.messages = []

# Eski mesajları ekranda gösterme
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Öğrencinin mesaj kutusu
if prompt := st.chat_input("Sormak istediğin soruyu yaz..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # Gemini'ye gönderip yanıt alma (model adını güncel kararlı sürüm yapıyoruz)
  try:
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )
    bot_reply = response.text
  except Exception as e:
    bot_reply = f"Bir hata oluştu: {str(e)}"

  # Asistanın cevabını ekrana yaz
  with st.chat_message("assistant"):
    st.markdown(bot_reply)
  st.session_state.messages.append(
      {"role": "assistant", "content": bot_reply}
  )