import os
import threading
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

class HafijulAIApp(App):
    def build(self):
        self.title = "Hafijul Super AI Assistant"
        
        # তোমার আপলোড করা রুপালী ফন্ট সেট করা হলো
        my_font = "SiyamRupali.ttf" 
        
        # মেইন লেআউট
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # মেসেজ ডিসপ্লে স্ক্রিন
        self.scroll = ScrollView(size_hint=(1, 0.65))
        self.output_label = Label(
            text="স্বাগতম হাফিজুল বন্ধু!\nআমি সরাসরি ক্লাউড থেকে যুক্ত তোমার মহাজ্ঞানী এআই। যেকোনো প্রশ্ন করো, আমি উত্তর দেব!", 
            size_hint_y=None, 
            halign='left', 
            valign='top',
            padding=(10, 10),
            font_size='18sp',
            font_name=my_font
        )
        self.output_label.bind(texture_size=self.output_label.setter('size'))
        self.scroll.add_widget(self.output_label)
        self.layout.add_widget(self.scroll)

        # স্পেশাল এডিটিং গাইড বাটন লেআউট
        tools_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=5)
        
        video_btn = Button(text="🎬 ভিডিও এডিট", font_name=my_font, font_size='13sp', background_color=(0.2, 0.7, 0.3, 1))
        video_btn.bind(on_press=lambda x: self.quick_question("ফ্রি ফায়ার ভিডিও এডিটিং এর ৩টি সেরা টিপস দাও"))
        
        photo_btn = Button(text="🖼️ লোগো/থাম্বনেইল", font_name=my_font, font_size='13sp', background_color=(0.9, 0.4, 0.2, 1))
        photo_btn.bind(on_press=lambda x: self.quick_question("ইউটিউব গেমিং থাম্বনেইল বানানোর সেরা উপায় কী"))
        
        tools_layout.add_widget(video_btn)
        tools_layout.add_widget(photo_btn)
        self.layout.add_widget(tools_layout)

        # ইনপুট বক্স
        self.user_input = TextInput(
            hint_text="এখানে যেকোনো প্রশ্ন বাংলায় বা ইংরেজিতে লিখুন...", 
            multiline=False, 
            size_hint=(1, 0.08),
            font_size='16sp',
            font_name=my_font
        )
        self.layout.add_widget(self.user_input)

        # মূল আস্ক বাটন
        self.submit_btn = Button(
            text="জাদুকরী উত্তর জানুন ✨", 
            size_hint=(1, 0.12), 
            background_color=(0, 0.6, 0.8, 1),
            font_size='18sp',
            font_name=my_font
        )
        self.submit_btn.bind(on_press=self.process_ai)
        self.layout.add_widget(self.submit_btn)

        return self.layout

    def quick_question(self, text):
        self.user_input.text = text
        self.process_ai(None)

    def process_ai(self, instance):
        query = self.user_input.text.strip()
        if query:
            self.output_label.text += f"\n\nতুমি: {query}"
            self.user_input.text = ""
            self.output_label.text += f"\n\nAI: ভাবছি বন্ধু... একটু দাঁড়াও... 🧠"
            threading.Thread(target=self.get_gemini_response, args=(query,), daemon=True).start()

    def update_ui(self, ai_text):
        # ভাবছি লেখাটা কেটে আসল উত্তর বসানো
        if "ভাবছি বন্ধু..." in self.output_label.text:
            self.output_label.text = self.output_label.text.split("\n\nAI: ভাবছি বন্ধু...")[0]
        self.output_label.text += f"\n\nAI: {ai_text}"

    def get_gemini_response(self, query):
        try:
            # এখানে তোমার ফ্রিতে পাওয়া Gemini API Key-টি বসবে (আপাতত টেস্ট কি বসানো আছে)
            api_key = "YOUR_GEMINI_API_KEY_HERE" 
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            headers = {'Content-Type': 'application/json'}
            prompt_config = f"Your name is Hafijul's AI Assistant. You are a super intelligent AI created by Hafijul Sheikh. Answer this question in clear and detailed Bengali: {query}"
            
            data = {"contents": [{"parts": [{"text": prompt_config}]}]}
            
            response = requests.post(url, headers=headers, json=data, timeout=15)
            result = response.json()
            
            ai_reply = result['candidates'][0]['content']['parts'][0]['text']
            Clock.schedule_once(lambda dt: self.update_ui(ai_reply))
        except:
            # ইন্টারনেট না থাকলে বা চাবি না মিললে ব্যাকআপ উত্তর দেবে
            Clock.schedule_once(lambda dt: self.update_ui("ইন্টারনেট কানেকশনটি অন করো বন্ধু, আর আমাদের এআই চাবিটি (API Key) একবার চেক করে নাও!"))

if __name__ == "__main__":
    HafijulAIApp().run()