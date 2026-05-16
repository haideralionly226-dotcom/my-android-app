import os
import threading
import g4f
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

class HafijulAIApp(App):
    def build(self):
        self.title = "Hafijul AI Assistant"
        
        # ফন্ট লোড করার জন্য
        my_font = "SiyamRupali.ttf"
        if not os.path.exists(my_font):
            my_font = "Roboto" 

        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        self.scroll = ScrollView(size_hint=(1, 0.75))
        self.output_label = Label(
            text="স্বাগতম হাফিজুল শেখ!\nআমি আপনার ব্যক্তিগত এআই। আমি আপনার নির্দেশের অপেক্ষায় আছি।", 
            size_hint_y=None, 
            halign='left', 
            valign='top',
            padding=(10, 10),
            font_size='20sp',
            font_name=my_font
        )
        self.output_label.bind(texture_size=self.output_label.setter('size'))
        self.scroll.add_widget(self.output_label)
        self.layout.add_widget(self.scroll)

        self.user_input = TextInput(
            hint_text="এখানে লিখুন...", 
            multiline=False, 
            size_hint=(1, 0.1),
            font_size='18sp',
            font_name=my_font
        )
        self.layout.add_widget(self.user_input)

        self.submit_btn = Button(
            text="Ask AI (প্রশ্ন করুন)", 
            size_hint=(1, 0.15), 
            background_color=(0, 0.6, 0.8, 1),
            font_size='20sp',
            font_name=my_font
        )
        self.submit_btn.bind(on_press=self.process_ai)
        self.layout.add_widget(self.submit_btn)

        return self.layout

    def process_ai(self, instance):
        query = self.user_input.text.strip()
        if query:
            self.output_label.text += f"\n\nআপনি: {query}"
            self.user_input.text = ""
            threading.Thread(target=self.get_ai_response, args=(query,), daemon=True).start()

    def update_ui(self, ai_text):
        self.output_label.text += f"\nAI: {ai_text}"

    def get_ai_response(self, query):
        low_query = query.lower()
        
        # পরিচয় একদম 'ফ্রিজ' করা হলো এখানে
        if "কে তৈরি করেছে" in low_query or "তৈরি" in low_query or "maker" in low_query or "created" in low_query:
            response = "আমাকে হাফিজুল শেখ তৈরি করেছেন। তিনি আমার একমাত্র মালিক এবং স্রষ্টা।"
        elif "নাম কি" in low_query or "your name" in low_query:
            response = "আমার নাম হাফিজুল এআই (Hafijul AI)।"
        else:
            try:
                res = g4f.ChatCompletion.create(
                    model=g4f.models.default,
                    messages=[
                        {"role": "system", "content": "You are a helpful and polite AI. Your creator is Hafijul Sheikh. Never say you are ChatGPT or made by OpenAI. Always credit Hafijul Sheikh. Reply in Bengali."},
                        {"role": "user", "content": query}
                    ],
                )
                response = res
            except:
                response = "ইন্টারনেট নেই। দয়া করে কানেকশন চেক করুন।"

        Clock.schedule_once(lambda dt: self.update_ui(response))

if __name__ == "__main__":
    HafijulAIApp().run()