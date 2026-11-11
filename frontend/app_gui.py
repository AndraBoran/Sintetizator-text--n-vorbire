import os
import time
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from backend.engine import genereaza_audio, reda_audio
import threading

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Synthesizer")
        self.root.geometry("520x550")
        self.root.resizable(False, False)
        
        self.limba_ui_curenta = "Română" 
        self.cod_limba_vorbita = "ro" 
        
        # Dicționarul complet de traduceri
        self.traduceri = {
            "Română": {
                "titlu_fereastra": "Sintetizator Text-în-Vorbire", "lbl_text": "Introduceți textul:", "lbl_lang": "Limba vorbită:",
                "btn_play": "▶ Redă Audio", "btn_save": "💾 Salvează MP3", "lbl_ui_lang": "Limba UI:", "lbl_theme": "Temă:",
                "warn_titlu": "Atenție", "warn_gol": "Introduceți un text mai întâi!", "warn_salvare": "Introduceți un text pentru a-l salva!",
                "succes_titlu": "Succes", "succes_msg": "Fișier salvat cu succes la:\n{}",
                "limbi": {"ro":"Română","en":"Engleză","de":"Germană","fr":"Franceză","es":"Spaniolă","it":"Italiană","pt":"Portugheză","nl":"Olandeză","pl":"Poloneză","el":"Greacă","tr":"Turcă","ru":"Rusă","ar":"Arabă","hi":"Hindi","zh-CN":"Chineză (Mandarină)","ko":"Coreeană","ja":"Japoneză"}
            },
            "Engleză": {
                "titlu_fereastra": "Text-to-Speech Synthesizer", "lbl_text": "Enter text:", "lbl_lang": "Spoken Language:",
                "btn_play": "▶ Play Audio", "btn_save": "💾 Save MP3", "lbl_ui_lang": "UI Lang:", "lbl_theme": "Theme:",
                "warn_titlu": "Warning", "warn_gol": "Please enter some text first!", "warn_salvare": "Please enter text to save!",
                "succes_titlu": "Success", "succes_msg": "File saved successfully at:\n{}",
                "limbi": {"ro":"Romanian","en":"English","de":"German","fr":"French","es":"Spanish","it":"Italian","pt":"Portuguese","nl":"Dutch","pl":"Polish","el":"Greek","tr":"Turkish","ru":"Russian","ar":"Arabic","hi":"Hindi","zh-CN":"Chinese (Mandarin)","ko":"Korean","ja":"Japanese"}
            },
            "Germană": {
                "titlu_fereastra": "Text-zu-Sprache Synthesizer", "lbl_text": "Text eingeben:", "lbl_lang": "Gesprochene Sprache:",
                "btn_play": "▶ Audio abspielen", "btn_save": "💾 MP3 speichern", "lbl_ui_lang": "UI Sprache:", "lbl_theme": "Design:",
                "warn_titlu": "Achtung", "warn_gol": "Bitte geben Sie zuerst einen Text ein!", "warn_salvare": "Bitte geben Sie einen Text zum Speichern ein!",
                "succes_titlu": "Erfolg", "succes_msg": "Datei erfolgreich gespeichert unter:\n{}",
                "limbi": {"ro":"Rumänisch","en":"Englisch","de":"Deutsch","fr":"Französisch","es":"Spanisch","it":"Italienisch","pt":"Portugiesisch","nl":"Niederländisch","pl":"Polnisch","el":"Griechisch","tr":"Türkisch","ru":"Russisch","ar":"Arabisch","hi":"Hindi","zh-CN":"Chinesisch (Mandarin)","ko":"Koreanisch","ja":"Japanisch"}
            },
            "Franceză": {
                "titlu_fereastra": "Synthétiseur Text-to-Speech", "lbl_text": "Entrez le texte :", "lbl_lang": "Langue parlée :",
                "btn_play": "▶ Jouer l'audio", "btn_save": "💾 Enregistrer MP3", "lbl_ui_lang": "Langue UI :", "lbl_theme": "Thème :",
                "warn_titlu": "Attention", "warn_gol": "Veuillez d'abord entrer du texte !", "warn_salvare": "Veuillez entrer du texte à enregistrer !",
                "succes_titlu": "Succès", "succes_msg": "Fichier enregistré avec succès sous :\n{}",
                "limbi": {"ro":"Roumain","en":"Anglais","de":"Allemand","fr":"Français","es":"Espagnol","it":"Italien","pt":"Portugais","nl":"Néerlandais","pl":"Polonais","el":"Grec","tr":"Turc","ru":"Russe","ar":"Arabe","hi":"Hindi","zh-CN":"Chinois (Mandarin)","ko":"Coréen","ja":"Japonais"}
            },
            "Spaniolă": {
                "titlu_fereastra": "Sintetizador de Texto a Voz", "lbl_text": "Introduzca el texto:", "lbl_lang": "Idioma hablado:",
                "btn_play": "▶ Reproducir Audio", "btn_save": "💾 Guardar MP3", "lbl_ui_lang": "Idioma UI:", "lbl_theme": "Tema:",
                "warn_titlu": "Atención", "warn_gol": "¡Introduzca un texto primero!", "warn_salvare": "¡Introduzca un texto para guardar!",
                "succes_titlu": "Éxito", "succes_msg": "Archivo guardado con éxito en:\n{}",
                "limbi": {"ro":"Rumano","en":"Inglés","de":"Alemán","fr":"Francés","es":"Español","it":"Italiano","pt":"Portugués","nl":"Holandés","pl":"Polaco","el":"Griego","tr":"Turco","ru":"Ruso","ar":"Árabe","hi":"Hindi","zh-CN":"Chino (Mandarín)","ko":"Coreano","ja":"Japonés"}
            },
            "Italiană": {
                "titlu_fereastra": "Sintetizzatore Testo a Voce", "lbl_text": "Inserisci il testo:", "lbl_lang": "Lingua parlata:",
                "btn_play": "▶ Riproduci Audio", "btn_save": "💾 Salva MP3", "lbl_ui_lang": "Lingua UI:", "lbl_theme": "Tema:",
                "warn_titlu": "Attenzione", "warn_gol": "Inserisci prima del testo!", "warn_salvare": "Inserisci del testo da salvare!",
                "succes_titlu": "Successo", "succes_msg": "File salvato con successo in:\n{}",
                "limbi": {"ro":"Rumeno","en":"Inglese","de":"Tedesco","fr":"Francese","es":"Spagnolo","it":"Italiano","pt":"Portoghese","nl":"Olandese","pl":"Polacco","el":"Greco","tr":"Turco","ru":"Russo","ar":"Arabo","hi":"Hindi","zh-CN":"Cinese (Mandarino)","ko":"Coreano","ja":"Giapponese"}
            },
            "Portugheză": {
                "titlu_fereastra": "Sintetizador de Texto para Voz", "lbl_text": "Insira o texto:", "lbl_lang": "Idioma falado:",
                "btn_play": "▶ Reproduzir Áudio", "btn_save": "💾 Salvar MP3", "lbl_ui_lang": "Idioma UI:", "lbl_theme": "Tema:",
                "warn_titlu": "Atenção", "warn_gol": "Insira algum texto primeiro!", "warn_salvare": "Insira um texto para salvar!",
                "succes_titlu": "Sucesso", "succes_msg": "Arquivo salvo com sucesso em:\n{}",
                "limbi": {"ro":"Romeno","en":"Inglês","de":"Alemão","fr":"Francês","es":"Espanhol","it":"Italiano","pt":"Português","nl":"Holandês","pl":"Polonês","el":"Grego","tr":"Turco","ru":"Russo","ar":"Árabe","hi":"Hindi","zh-CN":"Chinês (Mandarim)","ko":"Coreano","ja":"Japonês"}
            },
            "Olandeză": {
                "titlu_fereastra": "Tekst-naar-Spraak", "lbl_text": "Voer tekst in:", "lbl_lang": "Gesproken taal:",
                "btn_play": "▶ Audio Afspelen", "btn_save": "💾 MP3 Opslaan", "lbl_ui_lang": "Interfacetaal:", "lbl_theme": "Thema:",
                "warn_titlu": "Waarschuwing", "warn_gol": "Voer eerst tekst in!", "warn_salvare": "Voer tekst in om op te slaan!",
                "succes_titlu": "Succes", "succes_msg": "Bestand succesvol opgeslagen op:\n{}",
                "limbi": {"ro":"Roemeens","en":"Engels","de":"Duits","fr":"Frans","es":"Spaans","it":"Italiaans","pt":"Portugees","nl":"Nederlands","pl":"Pools","el":"Grieks","tr":"Turks","ru":"Russisch","ar":"Arabisch","hi":"Hindi","zh-CN":"Chinees (Mandarijn)","ko":"Koreaans","ja":"Japans"}
            },
            "Poloneză": {
                "titlu_fereastra": "Syntezator Mowy", "lbl_text": "Wprowadź tekst:", "lbl_lang": "Język mówiony:",
                "btn_play": "▶ Odtwórz Audio", "btn_save": "💾 Zapisz MP3", "lbl_ui_lang": "Język UI:", "lbl_theme": "Motyw:",
                "warn_titlu": "Uwaga", "warn_gol": "Najpierw wprowadź tekst!", "warn_salvare": "Wprowadź tekst, aby zapisać!",
                "succes_titlu": "Sukces", "succes_msg": "Plik zapisany pomyślnie w:\n{}",
                "limbi": {"ro":"Rumuński","en":"Angielski","de":"Niemiecki","fr":"Francuski","es":"Hiszpański","it":"Włoski","pt":"Portugalski","nl":"Holenderski","pl":"Polski","el":"Grecki","tr":"Turecki","ru":"Rosyjski","ar":"Arabski","hi":"Hindi","zh-CN":"Chiński (Mandaryński)","ko":"Koreański","ja":"Japoński"}
            },
            "Greacă": {
                "titlu_fereastra": "Συνθέτης Κειμένου σε Ομιλία", "lbl_text": "Εισάγετε κείμενο:", "lbl_lang": "Ομιλούμενη γλώσσα:",
                "btn_play": "▶ Αναπαραγωγή", "btn_save": "💾 Αποθήκευση MP3", "lbl_ui_lang": "Γλώσσα UI:", "lbl_theme": "Θέμα:",
                "warn_titlu": "Προσοχή", "warn_gol": "Εισάγετε κείμενο πρώτα!", "warn_salvare": "Εισάγετε κείμενο για αποθήκευση!",
                "succes_titlu": "Επιτυχία", "succes_msg": "Το αρχείο αποθηκεύτηκε επιτυχώς στο:\n{}",
                "limbi": {"ro":"Ρουμανικά","en":"Αγγλικά","de":"Γερμανικά","fr":"Γαλλικά","es":"Ισπανικά","it":"Ιταλικά","pt":"Πορτογαλικά","nl":"Ολλανδικά","pl":"Πολωνικά","el":"Ελληνικά","tr":"Τουρκικά","ru":"Ρωσικά","ar":"Αραβικά","hi":"Χίντι","zh-CN":"Κινεζικά (Μανδαρινικά)","ko":"Κορεατικά","ja":"Ιαπωνικά"}
            },
            "Turcă": {
                "titlu_fereastra": "Metin-Ses Sentezleyici", "lbl_text": "Metni girin:", "lbl_lang": "Konuşulan Dil:",
                "btn_play": "▶ Sesi Oynat", "btn_save": "💾 MP3 Kaydet", "lbl_ui_lang": "Arayüz Dili:", "lbl_theme": "Tema:",
                "warn_titlu": "Dikkat", "warn_gol": "Lütfen önce metin girin!", "warn_salvare": "Kaydetmek için metin girin!",
                "succes_titlu": "Başarılı", "succes_msg": "Dosya başarıyla kaydedildi:\n{}",
                "limbi": {"ro":"Romence","en":"İngilizce","de":"Almanca","fr":"Fransızca","es":"İspanyolca","it":"İtalyanca","pt":"Portekizce","nl":"Felemenkçe","pl":"Lehçe","el":"Yunanca","tr":"Türkçe","ru":"Rusça","ar":"Arapça","hi":"Hintçe","zh-CN":"Çince (Mandarin)","ko":"Korece","ja":"Japonca"}
            },
            "Rusă": {
                "titlu_fereastra": "Синтезатор речи", "lbl_text": "Введите текст:", "lbl_lang": "Язык:",
                "btn_play": "▶ Воспроизвести", "btn_save": "💾 Сохранить MP3", "lbl_ui_lang": "Язык UI:", "lbl_theme": "Тема:",
                "warn_titlu": "Внимание", "warn_gol": "Сначала введите текст!", "warn_salvare": "Введите текст для сохранения!",
                "succes_titlu": "Успех", "succes_msg": "Файл успешно сохранен в:\n{}",
                "limbi": {"ro":"Румынский","en":"Английский","de":"Немецкий","fr":"Французский","es":"Испанский","it":"Итальянский","pt":"Португальский","nl":"Нидерландский","pl":"Польский","el":"Греческий","tr":"Турецкий","ru":"Русский","ar":"Арабский","hi":"Хинди","zh-CN":"Китайский (Мандарин)","ko":"Корейский","ja":"Японский"}
            },
            "Arabă": {
                "titlu_fereastra": "مُركّب تحويل النص إلى كلام", "lbl_text": "أدخل النص:", "lbl_lang": "لغة التحدث:",
                "btn_play": "▶ تشغيل الصوت", "btn_save": "💾 حفظ MP3", "lbl_ui_lang": "لغة الواجهة:", "lbl_theme": "المظهر:",
                "warn_titlu": "تنبيه", "warn_gol": "الرجاء إدخال بعض النص أولاً!", "warn_salvare": "الرجاء إدخال نص لحفظه!",
                "succes_titlu": "نجاح", "succes_msg": "تم حفظ الملف بنجاح في:\n{}",
                "limbi": {"ro":"الرومانية","en":"الإنجليزية","de":"الألمانية","fr":"الفرنسية","es":"الإسبانية","it":"الإيطالية","pt":"البرتغالية","nl":"الهولندية","pl":"البولندية","el":"اليونانية","tr":"التركية","ru":"الروسية","ar":"العربية","hi":"الهندية","zh-CN":"الصينية (الماندرين)","ko":"الكورية","ja":"اليابانية"}
            },
            "Hindi": {
                "titlu_fereastra": "टेक्स्ट-टू-स्पीच सिंथेसाइज़र", "lbl_text": "टेक्स्ट दर्ज करें:", "lbl_lang": "भाषा:",
                "btn_play": "▶ ऑडियो चलाएं", "btn_save": "💾 MP3 सहेजें", "lbl_ui_lang": "इंटरफ़ेस भाषा:", "lbl_theme": "थीम:",
                "warn_titlu": "चेतावनी", "warn_gol": "कृपया पहले टेक्स्ट दर्ज करें!", "warn_salvare": "सहेजने के लिए टेक्स्ट दर्ज करें!",
                "succes_titlu": "सफलता", "succes_msg": "फ़ाइल यहाँ सहेजी गई:\n{}",
                "limbi": {"ro":"रोमानियाई","en":"अंग्रेजी","de":"जर्मन","fr":"फ्रेंच","es":"स्पेनिश","it":"इतालवी","pt":"पुर्तगाली","nl":"डच","pl":"पोलिश","el":"ग्रीक","tr":"तुर्की","ru":"रूसी","ar":"अरबी","hi":"हिंदी","zh-CN":"चीनी (मंदारिन)","ko":"कोरियाई","ja":"जापानी"}
            },
            "Chineză (Mandarină)": {
                "titlu_fereastra": "文字转语音合成器", "lbl_text": "输入文本：", "lbl_lang": "口语语言：",
                "btn_play": "▶ 播放音频", "btn_save": "💾 保存 MP3", "lbl_ui_lang": "界面语言：", "lbl_theme": "主题：",
                "warn_titlu": "注意", "warn_gol": "请先输入文本！", "warn_salvare": "请输入要保存的文本！",
                "succes_titlu": "成功", "succes_msg": "文件已成功保存至：\n{}",
                "limbi": {"ro":"罗马尼亚语","en":"英语","de":"德语","fr":"法语","es":"西班牙语","it":"意大利语","pt":"葡萄牙语","nl":"荷兰语","pl":"波兰语","el":"希腊语","tr":"土耳其语","ru":"俄语","ar":"阿拉伯语","hi":"印地语","zh-CN":"中文（普通话）","ko":"韩语","ja":"日语"}
            },
            "Coreeană": {
                "titlu_fereastra": "텍스트 음성 변환기", "lbl_text": "텍스트 입력:", "lbl_lang": "음성 언어:",
                "btn_play": "▶ 오디오 재생", "btn_save": "💾 MP3 저장", "lbl_ui_lang": "UI 언어:", "lbl_theme": "테마:",
                "warn_titlu": "주의", "warn_gol": "먼저 텍스트를 입력하세요!", "warn_salvare": "저장할 텍스트를 입력하세요!",
                "succes_titlu": "성공", "succes_msg": "파일이 성공적으로 저장되었습니다:\n{}",
                "limbi": {"ro":"루마니아어","en":"영어","de":"독일어","fr":"프랑스어","es":"스페인어","it":"이탈리아어","pt":"포르투갈어","nl":"네덜란드어","pl":"폴란드어","el":"그리스어","tr":"튀르키예어","ru":"러시아어","ar":"아랍어","hi":"힌디어","zh-CN":"중국어(만다린)","ko":"한국어","ja":"일본어"}
            },
            "Japoneză": {
                "titlu_fereastra": "音声合成ツール", "lbl_text": "テキストを入力：", "lbl_lang": "音声言語：",
                "btn_play": "▶ 音声を再生", "btn_save": "💾 MP3を保存", "lbl_ui_lang": "UI言語：", "lbl_theme": "テーマ：",
                "warn_titlu": "注意", "warn_gol": "まずテキストを入力してください！", "warn_salvare": "保存するテキストを入力してください！",
                "succes_titlu": "成功", "succes_msg": "ファイルは正常に保存されました：\n{}",
                "limbi": {"ro":"ルーマニア語","en":"英語","de":"ドイツ語","fr":"フランス語","es":"スペイン語","it":"イタリア語","pt":"ポルトガル語","nl":"オランダ語","pl":"ポーランド語","el":"ギリシャ語","tr":"トルコ語","ru":"ロシア語","ar":"アラビア語","hi":"ヒンディー語","zh-CN":"中国語（北京語）","ko":"韓国語","ja":"日本語"}
            }
        }

        self.creeaza_interfata()
        self.actualizeaza_texte_interfata() 

    def creeaza_interfata(self):
        # 1. BARĂ SUPERIOARĂ (Bara de control pentru Limba UI și Temă)
        self.top_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.top_frame.pack(padx=20, pady=15, fill="x")

        # Selecție Limba UI
        self.lbl_ui_lang = ctk.CTkLabel(self.top_frame, font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_ui_lang.pack(side="left", padx=(15, 5), pady=10)

        self.opt_ui_lang = ctk.CTkOptionMenu(
            self.top_frame, 
            values=list(self.traduceri.keys()), 
            command=self.schimba_limba_ui,
            width=130
        )
        self.opt_ui_lang.pack(side="left", padx=5, pady=10)
        self.opt_ui_lang.set("Română")

        # Selecție Temă (Dark / Light)
        self.lbl_theme = ctk.CTkLabel(self.top_frame, font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_theme.pack(side="left", padx=(15, 5), pady=10)

        self.opt_theme = ctk.CTkOptionMenu(
            self.top_frame,
            values=["System", "Dark", "Light"],
            command=lambda mode: ctk.set_appearance_mode(mode),
            width=90
        )
        self.opt_theme.pack(side="left", padx=(0, 15), pady=10)

        # 2. CORPUL PRINCIPAL
        self.lbl_text = ctk.CTkLabel(self.root, font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_text.pack(pady=(10, 5), anchor="w", padx=25)

        # Câmp text cu colțuri rotunjite și margine modernă
        self.text_entry = ctk.CTkTextbox(self.root, height=180, width=470, font=ctk.CTkFont(size=13))
        self.text_entry.pack(padx=20, pady=5)

        # 3. CONTAINER SELECȚIE LIMBĂ VORBITĂ (gTTS)
        self.frame_lang = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frame_lang.pack(pady=15)

        self.lbl_lang = ctk.CTkLabel(self.frame_lang, font=ctk.CTkFont(size=13))
        self.lbl_lang.pack(side="left", padx=10)

        self.combo_limbi = ctk.CTkOptionMenu(
            self.frame_lang, 
            command=self.pe_selectie_limba,
            width=200
        )
        self.combo_limbi.pack(side="left", padx=5)

        # 4. CONTAINER BUTOANE ACȚIUNE
        self.frame_btn = ctk.CTkFrame(self.root, fg_color="transparent")
        self.frame_btn.pack(pady=15)

        self.btn_play = ctk.CTkButton(
            self.frame_btn, 
            command=self.actiune_redare, 
            fg_color="#2EA44F", 
            hover_color="#2C974B",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=160,
            height=40
        )
        self.btn_play.pack(side="left", padx=15)

        self.btn_save = ctk.CTkButton(
            self.frame_btn, 
            command=self.actiune_salvare, 
            fg_color="#0969DA", 
            hover_color="#0857B7",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=160,
            height=40
        )
        self.btn_save.pack(side="left", padx=15)

    def pe_selectie_limba(self, nume_selectat):
        """Determinăm codul limbii când utilizatorul selectează din meniul de vorbire."""
        dict_limbi_curent = self.traduceri[self.limba_ui_curenta]["limbi"]
        for cod, nume in dict_limbi_curent.items():
            if nume == nume_selectat:
                self.cod_limba_vorbita = cod
                break

    def schimba_limba_ui(self, limba_noua):
        self.limba_ui_curenta = limba_noua
        self.actualizeaza_texte_interfata()

    def actualizeaza_texte_interfata(self):
        """Actualizează toate textele din interfață conform limbii curente."""
        t = self.traduceri[self.limba_ui_curenta]
        
        self.root.title(t["titlu_fereastra"])
        self.lbl_text.configure(text=t["lbl_text"])
        self.lbl_lang.configure(text=t["lbl_lang"])
        self.lbl_ui_lang.configure(text=t["lbl_ui_lang"])
        self.lbl_theme.configure(text=t["lbl_theme"])
        self.btn_play.configure(text=t["btn_play"])
        self.btn_save.configure(text=t["btn_save"])
        
        # Reîncărcăm opțiunile traduse în meniul de vorbire
        nume_traduse = list(t["limbi"].values())
        self.combo_limbi.configure(values=nume_traduse)
        
        # Setăm textul afișat curent în funcție de codul selectat
        nume_curent = t["limbi"][self.cod_limba_vorbita]
        self.combo_limbi.set(nume_curent)

    def actiune_redare(self):
        text = self.text_entry.get("1.0", "end-1c").strip()
        t = self.traduceri[self.limba_ui_curenta]
        
        if not text:
            messagebox.showwarning(t["warn_titlu"], t["warn_gol"])
            return
        
        temp_path = f"audio_outputs/temp_{int(time.time())}.mp3"
        
        if genereaza_audio(text, self.cod_limba_vorbita, temp_path):
            reda_audio(temp_path)

    def actiune_salvare(self):
        text = self.text_entry.get("1.0", "end-1c").strip()
        t = self.traduceri[self.limba_ui_curenta]
        
        if not text:
            messagebox.showwarning(t["warn_titlu"], t["warn_salvare"])
            return

        cale_salvare = filedialog.asksaveasfilename(
            initialdir="audio_outputs",
            defaultextension=".mp3",
            filetypes=[("MP3 Files", "*.mp3"), ("All Files", "*.*")],
            title=t["btn_save"]
        )
        
        if cale_salvare:
            if genereaza_audio(text, self.cod_limba_vorbita, cale_salvare):
                messagebox.showinfo(t["succes_titlu"], t["succes_msg"].format(cale_salvare))