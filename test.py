import flet as ft


def main(page: ft.Page):
    page.title = "Список покупок"
    page.theme_mode = ft.ThemeMode.LIGHT
    shopping_list = []
    filter_option = "all"

    def switch_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        theme_button.icon = ft.icons.DARK_MODE if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.LIGHT_MODE
        page.update()

    def update_list():
        task_container.controls.clear()

        filtered_items = {
            "all": shopping_list,
            "bought": [item for item in shopping_list if item["bought"]],
            "not_bought": [item for item in shopping_list if not item["bought"]]
        }[filter_option]

        for item in filtered_items:
            checkbox = ft.Checkbox(
                label=f"{item['name']} (x{item['quantity']})",
                value=item["bought"],
                on_change=lambda e, item=item: toggle_bought(item)
            )
            delete_button = ft.IconButton(
                icon=ft.icons.DELETE, on_click=lambda e, item=item: delete_item(item)
            )
            task_container.controls.append(ft.Row([checkbox, delete_button], alignment=ft.MainAxisAlignment.CENTER))

        counter_text.value = f"Куплено: {sum(1 for i in shopping_list if i['bought'])}/{len(shopping_list)}"
        page.update()

    def add_item(e):
        name = item_name.value.strip()
        quantity = item_quantity.value.strip()
        if name and quantity.isdigit():
            shopping_list.append({"name": name, "quantity": int(quantity), "bought": False})
            item_name.value, item_quantity.value = "", ""
            update_list()

    def toggle_bought(item):
        item["bought"] = not item["bought"]
        update_list()

    def delete_item(item):
        shopping_list.remove(item)
        update_list()

    def set_filter(e):
        nonlocal filter_option
        filter_option = e.control.data
        update_list()

    theme_button = ft.IconButton(icon=ft.icons.DARK_MODE, on_click=switch_theme)
    app_bar = ft.AppBar(actions=[theme_button])

    title = ft.Text("Список покупок", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    item_name = ft.TextField(label="Название", width=200)
    item_quantity = ft.TextField(label="Кол-во", width=100)

    add_button = ft.ElevatedButton("Добавить", on_click=add_item)

    filter_row = ft.Row([
        ft.TextButton("Все", data="all", on_click=set_filter),
        ft.TextButton("Купленные", data="bought", on_click=set_filter),
        ft.TextButton("Некупленные", data="not_bought", on_click=set_filter)
    ], alignment=ft.MainAxisAlignment.CENTER)

    counter_text = ft.Text("Куплено: 0/0", size=14, weight=ft.FontWeight.BOLD)

    task_container = ft.Column(alignment=ft.MainAxisAlignment.CENTER)

    content = ft.Column([
        title,
        ft.Row([item_name, item_quantity, add_button], alignment=ft.MainAxisAlignment.CENTER),
        filter_row,
        counter_text,
        task_container
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.appbar = app_bar
    page.add(content)
    update_list()


ft.app(target=main)
