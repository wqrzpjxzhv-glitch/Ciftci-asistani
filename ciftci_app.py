import streamlit as st
import pandas as pd
from datetime import datetime

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Akıllı Çiftçi Asistanı", page_icon="🌾", layout="wide")

# --- Veri Saklama (Session State) ---
# Uygulama açıkken verilerin kaybolmaması için geçici hafıza
if 'gelir_gider' not in st.session_state:
    st.session_state.gelir_gider = pd.DataFrame(columns=["Tarih", "Tür", "Açıklama", "Tutar"])
if 'notlar' not in st.session_state:
    st.session_state.notlar = []

# --- Yan Menü ---
st.sidebar.title("🌾 Çiftçi Paneli")
secim = st.sidebar.radio("Menü", ["💰 Gelir/Gider Takibi", "📝 Not Defteri", "🌦️ Hava Durumu", "🌱 Ürün Tavsiyeleri"])

# --- 1. GELİR / GİDER TAKİBİ ---
if secim == "💰 Gelir/Gider Takibi":
    st.header("💰 Çiftlik Finans Yönetimi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Yeni Kayıt Ekle")
        tarih = st.date_input("Tarih", datetime.now())
        tur = st.selectbox("İşlem Türü", ["Gelir", "Gider"])
        aciklama = st.text_input("Açıklama (Örn: Gübre alımı, Mahsul satışı)")
        tutar = st.number_input("Tutar (TL)", min_value=0.0, step=10.0)
        
        if st.button("Kaydet"):
            yeni_veri = pd.DataFrame({
                "Tarih": [tarih],
                "Tür": [tur],
                "Açıklama": [aciklama],
                "Tutar": [tutar]
            })
            st.session_state.gelir_gider = pd.concat([st.session_state.gelir_gider, yeni_veri], ignore_index=True)
            st.success("İşlem başarıyla kaydedildi!")

    with col2:
        st.subheader("Finansal Özet")
        if not st.session_state.gelir_gider.empty:
            df = st.session_state.gelir_gider
            toplam_gelir = df[df["Tür"] == "Gelir"]["Tutar"].sum()
            toplam_gider = df[df["Tür"] == "Gider"]["Tutar"].sum()
            net_kar = toplam_gelir - toplam_gider
            
            st.metric(label="Toplam Gelir", value=f"{toplam_gelir:,.2f} TL")
            st.metric(label="Toplam Gider", value=f"{toplam_gider:,.2f} TL", delta_color="inverse")
            st.metric(label="Net Durum", value=f"{net_kar:,.2f} TL", delta=f"{net_kar:,.2f} TL")
            
            st.dataframe(df)
        else:
            st.info("Henüz bir kayıt girmediniz.")

# --- 2. NOT DEFTERİ ---
elif secim == "📝 Not Defteri":
    st.header("📝 Çiftlik Günlüğü ve Notlar")
    
    yeni_not = st.text_area("Notunuzu buraya yazın (Örn: 3 numaralı tarlaya su verilecek)")
    if st.button("Notu Ekle"):
        zaman = datetime.now().strftime("%d-%m-%Y %H:%M")
        st.session_state.notlar.append(f"**{zaman}**: {yeni_not}")
        st.success("Not eklendi.")
        
    st.markdown("---")
    st.subheader("Kaydedilen Notlar")
    for not_item in reversed(st.session_state.notlar):
        st.markdown(f"- {not_item}")

# --- 3. HAVA DURUMU (Simülasyon) ---
elif secim == "🌦️ Hava Durumu":
    st.header("🌦️ Bölgesel Hava Durumu Tahmini")
    st.info("Not: Gerçek zamanlı veri için API anahtarı gereklidir. Şu an genel tahmin gösteriliyor.")
    
    sehir = st.selectbox("Bölgenizi Seçin", ["İç Anadolu", "Ege", "Akdeniz", "Karadeniz", "Marmara", "Doğu Anadolu", "Güneydoğu"])
    
    # Basit bir demo verisi
    hava_durumu_data = {
        "İç Anadolu": {"Durum": "Parçalı Bulutlu", "Derece": "18°C", "Nem": "%40", "Rüzgar": "15 km/s", "Uyarı": "Gece don riski olabilir."},
        "Ege": {"Durum": "Güneşli", "Derece": "24°C", "Nem": "%50", "Rüzgar": "20 km/s", "Uyarı": "Sulama için uygun gün."},
        "Akdeniz": {"Durum": "Açık", "Derece": "28°C", "Nem": "%60", "Rüzgar": "10 km/s", "Uyarı": "Sıcak çarpmasına dikkat."},
        "Karadeniz": {"Durum": "Yağmurlu", "Derece": "16°C", "Nem": "%85", "Rüzgar": "5 km/s", "Uyarı": "İlaçlama yapmayınız."},
        "Marmara": {"Durum": "Rüzgarlı", "Derece": "20°C", "Nem": "%55", "Rüzgar": "30 km/s", "Uyarı": "Sera havalandırmalarını kontrol edin."},
        "Doğu Anadolu": {"Durum": "Soğuk", "Derece": "10°C", "Nem": "%30", "Rüzgar": "25 km/s", "Uyarı": "Hayvanları korunaklı alana alın."},
        "Güneydoğu": {"Durum": "Sıcak", "Derece": "30°C", "Nem": "%20", "Rüzgar": "12 km/s", "Uyarı": "Kuraklık riski, sulama planlayın."}
    }
    
    veri = hava_durumu_data.get(sehir)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Sıcaklık", veri["Derece"])
    col2.metric("Nem", veri["Nem"])
    col3.metric("Rüzgar", veri["Rüzgar"])
    
    st.warning(f"⚠️ **Çiftçi Uyarısı:** {veri['Uyarı']}")

# --- 4. ÜRÜN TAVSİYELERİ ---
elif secim == "🌱 Ürün Tavsiyeleri":
    st.header("🌱 Ürün Bazlı İpuçları")
    
    urun = st.selectbox("Hangi ürün hakkında bilgi almak istersiniz?", ["Buğday", "Mısır", "Domates", "Ayçiçeği", "Pamuk"])
    
    tavsiyeler = {
        "Buğday": """
        * **Ekim:** Ekim derinliği 4-5 cm olmalıdır.
        * **Gübreleme:** Kardeşlenme döneminde azotlu gübreleme verimi artırır.
        * **Hastalık:** Pas hastalığına karşı yapraklar sık sık kontrol edilmelidir.
        """,
        "Mısır": """
        * **Sulama:** Tepe püskülü çıkarma döneminde su stresi yaşatılmamalıdır.
        * **Hasat:** Dane nemi %25-28 seviyesine düştüğünde hasat uygundur.
        * **Zararlı:** Mısır kurdu mücadelesi için feromon tuzakları kullanabilirsiniz.
        """,
        "Domates": """
        * **Destek:** Sırık domateslerde ipe alma işlemi zamanında yapılmalıdır.
        * **Besleme:** Kalsiyum eksikliği dip çürüklüğüne yol açar, dikkat edin.
        * **Hastalık:** Mildiyö için nemli havalarda koruyucu ilaçlama yapın.
        """,
        "Ayçiçeği": """
        * **Ekim:** Toprak sıcaklığı 8-10°C olduğunda ekim yapılabilir.
        * **Sulama:** Tabla oluşumu ve çiçeklenme başlangıcı suya en çok ihtiyaç duyulan dönemdir.
        """,
        "Pamuk": """
        * **Hasat:** Koza açımı %60-70'e ulaştığında yaprak döktürücü kullanılabilir.
        * **Zararlı:** Beyaz sinek popülasyonu sürekli izlenmelidir.
        """
    }
    
    st.info(f"💡 **{urun} İçin Tavsiyeler:**")
    st.markdown(tavsiyeler[urun])

