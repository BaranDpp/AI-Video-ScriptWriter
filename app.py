import streamlit as st
import google.generativeai as genai

# --- AYARLAR ---
# Buraya Google AI Studio'dan aldığın API Key'i yapıştır
GOOGLE_API_KEY = "AIzaSyAZy3v5b7z8RLIEYZPJdreYeJWVOeJKEgo" 

# Sayfa Ayarları
st.set_page_config(page_title="AI Video Senaristi", page_icon="🎙️", layout="wide")

# Özel Tasarım (Butonlar ve Metin Kutuları için)
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .stCode {
        font-size: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# Yapay Zeka Kurulumu
def ai_yapilandir():
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model
    except Exception as e:
        st.error(f"API Hatası: {e}")
        return None

# --- ARAYÜZ ---
col1, col2 = st.columns([1, 6])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3074/3074767.png", width=70)
with col2:
    st.title("🎙️ AI Video Senaristi V3")
    st.caption("Sadece konuyu ver, seslendirme metnini al. Kopyala -> Yapıştır -> Video Hazır!")

st.markdown("---")

# Yan Menü
with st.sidebar:
    st.header("🎛️ Video Ayarları")
    platform = st.selectbox("Video Türü", ["YouTube Shorts (60sn)", "Instagram Reels", "TikTok", "YouTube Uzun Video"])
    ton = st.select_slider("Anlatıcı Tonu", options=["Ciddi Haberci", "Enerjik YouTuber", "Gizemli Hikaye", "Samimi Arkadaş"])
    
    st.info("💡 İpucu: Shorts için 'Enerjik YouTuber' tonu en iyisidir.")

# Giriş Alanı
konu = st.text_input("Videonun konusu ne?", placeholder="Örn: Steam'de RDR2 %67 İndirimde, neden almalısınız?")
btn_basla = st.button("✨ SENARYOYU YAZ")

# --- MANTIK ---
if btn_basla:
    if not konu:
        st.warning("Konu girmeden senaryo yazamam!")
    elif GOOGLE_API_KEY == "BURAYA_API_KEY_YAPISTIR":
        st.error("Lütfen kodun içine API Key'inizi yapıştırın!")
    else:
        model = ai_yapilandir()
        if model:
            with st.spinner('Yapay zeka kelimeleri seçiyor... ✍️'):
                
                # --- YENİLENMİŞ PROMPT (HAYALET YAZAR MODU) ---
                prompt = f"""
                Sen profesyonel bir video senaristisin. Verilen konu hakkında, seslendirme sanatçısının (veya AI sesin) okuması için tam metin yazacaksın.
                
                Konu: {konu}
                Platform: {platform}
                Ton: {ton}
                Dil: Türkçe
                
                Lütfen çıktıyı şu 3 BÖLÜME ayırarak ver (Bölüm başlıklarını aynen kullan):

                BÖLÜM 1: TAM SESLENDİRME METNİ
                - Bu kısım videoda DUYULACAK olan kısımdır.
                - Parantez içi yönetmen notları (Gülüş, es verme vb.) ASLA EKLEME. Sadece okunacak ham metni yaz.
                - Çok akıcı, konuşma diline uygun olsun.
                - Giriş cümlesi ("Hook") izleyiciyi ilk 3 saniyede yakalasın. Asla "Merhaba arkadaşlar kanalıma hoşgeldiniz" deme. Direkt konuya gir.
                - Toplam süre platforma uygun olsun (Shorts ise max 140 kelime).
                
                BÖLÜM 2: GÖRSEL AKIŞ PLANI
                - Seslendirme metninin hangi saniyesinde ekranda ne görünmeli?
                - Örn: [00-05sn] Oyunun fragmanından patlama sahnesi.
                
                BÖLÜM 3: BAŞLIK VE ETİKETLER
                - 3 adet viral başlık.
                - Açıklama kutusu yazısı.
                - Hashtagler.
                """
                
                try:
                    cevap = model.generate_content(prompt)
                    text = cevap.text
                    
                    st.success("Senaryo Hazır! Aşağıdan kopyalayabilirsin. 👇")
                    
                    # Sekmeler
                    tab_ses, tab_gorsel, tab_meta = st.tabs(["🎙️ Sadece Okunacak Metin", "🎬 Görsel Planı", "🏷️ Başlık & SEO"])
                    
                    # PARSING (Metni Bölümlere Ayırma)
                    seslendirme_metni = "Metin ayrıştırılamadı."
                    gorsel_plani = "Plan ayrıştırılamadı."
                    seo_bilgisi = "Bilgi yok."
                    
                    # Basit Bölme Mantığı
                    if "BÖLÜM 1:" in text:
                        parts = text.split("BÖLÜM 1:")
                        if len(parts) > 1:
                            # Bölüm 1 ile Bölüm 2 arasını al
                            temp = parts[1].split("BÖLÜM 2:")
                            seslendirme_metni = temp[0].replace("TAM SESLENDİRME METNİ", "").strip()
                            
                            if len(temp) > 1:
                                # Bölüm 2 ile Bölüm 3 arasını al
                                temp2 = temp[1].split("BÖLÜM 3:")
                                gorsel_plani = temp2[0].replace("GÖRSEL AKIŞ PLANI", "").strip()
                                
                                if len(temp2) > 1:
                                    # Bölüm 3'ü al
                                    seo_bilgisi = temp2[1].replace("BAŞLIK VE ETİKETLER", "").strip()

                    # 1. SEKME: SESLENDİRME (En Önemlisi)
                    with tab_ses:
                        st.info("💡 İpucu: Sağ üstteki 'Kopyala' ikonuna bas, ElevenLabs veya CapCut'a yapıştır.")
                        st.code(seslendirme_metni, language="text") 
                        
                    # 2. SEKME: GÖRSEL PLAN
                    with tab_gorsel:
                        st.markdown(gorsel_plani)

                    # 3. SEKME: SEO
                    with tab_meta:
                        st.markdown(seo_bilgisi)
                    
                except Exception as e:
                    st.error(f"Hata: {e}")
                    st.write("Ham Metin (Hata Ayıklama):", text)

# --- REHBER BÖLÜMÜ (YENİ) ---
st.markdown("---")
with st.expander("📚 CapCut ile Video Nasıl Yapılır? (Adım Adım Rehber)"):
    st.markdown("""
    ### 🎬 5 Dakikada Faceless Video Yapımı:
    
    **1. Metni Hazırla:**
    Yukarıdaki **'🎙️ Sadece Okunacak Metin'** sekmesindeki metni kopyala.
    
    **2. Seslendirme (Text-to-Speech):**
    * **CapCut'ı aç:** 'Metin' (Text) aracına tıkla ve metni yapıştır.
    * **Metin Okuma:** Metne tıkla -> 'Metin Okuma' (Text to Speech) seçeneğine git.
    * **Ses Seç:** Türkçe -> 'Kalın Erkek' veya 'Enerjik Kadın' seslerinden birini seç.
    * **Sesi Al:** CapCut sesi oluşturunca, ekrandaki yazılı metin kutusunu silebilirsin. Ses dosyası kalacaktır.
    
    **3. Görsel Ekleme:**
    * Sesin anlattığı şeye uygun videoları (Oyun fragmanı, oynanış videosu vb.) sesin üzerine sürükle.
    * Videoları sesin ritmine göre kes.
    
    **4. Otomatik Altyazı (Çok Önemli!):**
    * CapCut'ta **'Metin' -> 'Otomatik Altyazı'** (Auto Captions) seçeneğine tıkla.
    * 'Oluştur' de. CapCut sesi dinleyip altyazıları otomatik yazar.
    * Altyazı stilini büyüt, renklendir ve ortala. (İzleyicilerin %80'i buna bakıyor!)
    
    **5. Kapak ve Paylaş:**
    * Videonu dışa aktar (Export) ve YouTube Shorts/TikTok'a yükle!
    """)

# Footer
st.caption("Powered by Gemini 2.0 Flash | Geliştirici: Mühendis Baran")