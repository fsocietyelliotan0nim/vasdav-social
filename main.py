import flet as ft

def main(page: ft.Page):
    page.title = "VASDAV - Социальная сеть"
    page.bgcolor = "#FFFFFF" # Чисто белый фон по ТЗ
    page.window_width = 430
    page.window_height = 850
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Кислотная палитра на основе иконки VASDAV
    PINK = "#FF0055"
    ORANGE = "#FF6600"
    LIME = "#CCFF00"
    DARK_TEXT = "#121212"

    # База данных «на лету» для демонстрации логики прототипа
    state = {
        "user": None, # Данные текущей сессии
        "posts": [
            {"author": "Илья Новки", "mbti": "ENTP", "text": "Добро пожаловать в VASDAV! Оцените кислотные кнопки 😎", "img": "https://picsum.photos"},
            {"author": "Админ", "mbti": "INTJ", "text": "Запустили синхронизацию контактов. Проверяйте вкладку Чаты.", "img": None}
        ],
        "chats": [
            {"name": "Илья Новки", "mbti": "ENTP", "last_msg": "Концепт с MBTI просто пушка!"}
        ]
    }

    # Стили интерактивных закругленных кнопок
    def make_acid_button(text, color, on_click, text_color="#FFFFFF"):
        return ft.Container(
            content=ft.ElevatedButton(
                text=text,
                on_click=on_click,
                style=ft.ButtonStyle(
                    color=text_color,
                    bgcolor=color,
                    shape=ft.RoundedRectangleBorder(radius=25), # Сильно закругленные кнопки
                    animation_duration=200,
                    elevation=3
                ),
                expand=True
            ),
            height=50,
            animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT)
        )

    # --- КОМПОНЕНТ: КНОПКА ВЫБОРА MBTI ---
    mbti_button_ref = ft.Ref[ft.Container]()
    
    def open_mbti_selector(e):
        def select_mbti(mbti_val):
            state["user"]["mbti"] = mbti_val
            mbti_button_ref.current.content.text = f"Ваш MBTI: {mbti_val}"
            page.dialog.open = False
            page.update()

        mbti_types = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
        grid = ft.GridView(expand=True, max_extent=80, child_aspect_ratio=1.5)
        for t in mbti_types:
            grid.controls.append(ft.OutlinedButton(text=t, on_click=lambda e, val=t: select_mbti(val)))
            
        page.dialog = ft.AlertDialog(
            title=ft.Text("Выберите свой MBTI"),
            content=ft.Container(content=grid, width=300, height=250)
        )
        page.dialog.open = True
        page.update()

    # --- ЭКРАН 1: РЕГИСТРАЦИЯ ---
    def render_registration():
        name_input = ft.TextField(label="Ваше имя / Никнейм", border_color=DARK_TEXT, label_style=ft.TextStyle(color=DARK_TEXT))
        phone_input = ft.TextField(label="Номер телефона (для защиты)", border_color=DARK_TEXT, label_style=ft.TextStyle(color=DARK_TEXT), value="+7 ")
        
        def finish_reg(e):
            if name_input.value and len(phone_input.value) > 5:
                state["user"] = {"name": name_input.value, "phone": phone_input.value, "mbti": "Не выбран", "avatar": "⚡"}
                go_to_app()

        reg_screen = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text("V A S D A V", size=32, weight=ft.FontWeight.BOLD, color=LIME),
                    bgcolor=PINK, padding=25, border_radius=20, alignment=ft.alignment.center
                ),
                ft.Text("Добро пожаловать!", size=22, weight=ft.FontWeight.BOLD, color=DARK_TEXT),
                name_input,
                phone_input,
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                make_acid_button("Создать аккаунт", ORANGE, finish_reg)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
            padding=30, expand=True
        )
        page.views.clear()
        page.views.append(ft.View(controls=[reg_screen], bgcolor="#FFFFFF"))
        page.update()

    # --- ОСНОВНОЕ ПРИЛОЖЕНИЕ ---
    def go_to_app():
        # Шапка
        app_header = ft.Container(
            content=ft.Row([
                ft.Text("VASDAV", size=24, weight=ft.FontWeight.BOLD, color=LIME, letter_spacing=1.5),
                ft.Icon(ft.icons.SHIELD_ROUNDED, color=LIME) # Символ защиты
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=PINK, padding=15, border_radius=15, margin=ft.margin.only(bottom=10)
        )

        # Компоненты Ленты
        feed_list = ft.ListView(expand=True, spacing=15)
        def refresh_feed():
            feed_list.controls.clear()
            for p in state["posts"]:
                card_controls = [
                    ft.Row([
                        ft.Text(p["author"], weight=ft.FontWeight.BOLD, color=DARK_TEXT),
                        ft.Container(content=ft.Text(p["mbti"], size=11, color=DARK_TEXT, weight=ft.FontWeight.BOLD), bgcolor=LIME, padding=4, border_radius=5)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(p["text"], color=DARK_TEXT, size=14)
                ]
                if p["img"]:
                    card_controls.append(ft.Image(src=p["img"], border_radius=10, fit=ft.ImageFit.COVER))
                
                card_controls.append(ft.Row([
                    ft.IconButton(ft.icons.FAVORITE_BORDER, icon_color=PINK),
                    ft.IconButton(ft.icons.CHAT_BUBBLE_OUTLINE, icon_color=ORANGE)
                ]))
                
                feed_list.controls.append(ft.Container(content=ft.Column(card_controls), bgcolor="#F5F5F5", padding=15, border_radius=15))
            page.update()

        new_post_text = ft.TextField(hint_text="Расскажите что-нибудь...", border_radius=15, expand=True, color=DARK_TEXT)
        def add_new_post(e):
            if new_post_text.value:
                state["posts"].insert(0, {"author": state["user"]["name"], "mbti": state["user"]["mbti"], "text": new_post_text.value, "img": None})
                new_post_text.value = ""
                refresh_feed()

        feed_view = ft.Column([
            app_header,
            ft.Row([new_post_text, ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_new_post, bgcolor=ORANGE)]),
            ft.Divider(color=ft.colors.BLACK12),
            feed_list
        ], expand=True)

        # Компоненты Чатов (Синхронизация контактов)
        chats_list = ft.ListView(expand=True)
        def sync_contacts(e):
            page.snack_bar = ft.SnackBar(ft.Text("Контакты успешно синхронизированы!"), bgcolor=PINK)
            page.snack_bar.open = True
            page.update()

        chats_view = ft.Column([
            app_header,
            make_acid_button("Синхронизировать контакты телефона", LIME, sync_contacts, text_color=DARK_TEXT),
            ft.Divider(color=ft.colors.BLACK12),
            chats_list
        ], expand=True)
        for c in state["chats"]:
            chats_list.controls.append(ft.ListTile(
                leading=ft.CircleAvatar(content=ft.Text("⚡"), bgcolor=ORANGE),
                title=ft.Text(f"{c['name']} ({c['mbti']})", color=DARK_TEXT, weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(c["last_msg"], color=ft.colors.BLACK54),
                trailing=ft.Icon(ft.icons.CHEVRON_RIGHT, color=PINK)
            ))

        # Компоненты Профиля
        mbti_btn = ft.Container(
            content=ft.ElevatedButton(f"Выбрать свой MBTI: {state['user']['mbti']}", on_click=open_mbti_selector,
                                      style=ft.ButtonStyle(color="#FFFFFF", bgcolor=ORANGE, shape=ft.RoundedRectangleBorder(radius=25))),
            ref=mbti_button_ref, height=50
        )
        profile_view = ft.Column([
            app_header,
            ft.Container(height=20),
            ft.CircleAvatar(content=ft.Text(state["user"]["avatar"], size=40), radius=50, bgcolor=LIME),
            ft.Text(state["user"]["name"], size=26, weight=ft.FontWeight.BOLD, color=DARK_TEXT),
            ft.Text(f"Тел: {state['user']['phone']}", color=ft.colors.BLACK45),
            ft.Container(height=15),
            mbti_btn,
            ft.Container(height=10),
            make_acid_button("Мои подписки (0)", PINK, lambda _: print("Переход к подпискам"))
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)

        # Навигация
        main_container = ft.Container(content=feed_view, expand=True, padding=10)
        def on_nav_change(e):
            if e.control.selected_index == 0: main_container.content = feed_view; refresh_feed()
            elif e.control.selected_index == 1: main_container.content = chats_view
            elif e.control.selected_index == 2: main_container.content = profile_view
            page.update()

        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(icon=ft.icons.FEED, label="Лента"),
                ft.NavigationDestination(icon=ft.icons.CHAT, label="Чаты"),
                ft.NavigationDestination(icon=ft.icons.PERSON, label="Профиль"),
            ],
            on_change=on_nav_change, bgcolor="#FFFFFF", active_color=PINK
        )
        
        page.views.clear()
        page.views.append(ft.View(controls=[main_container], navigation_bar=page.navigation_bar, bgcolor="#FFFFFF"))
        refresh_feed()

    render_registration()

app = ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
