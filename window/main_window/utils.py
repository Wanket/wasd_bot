from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QPushButton, QListWidgetItem


def _find_unique_name(name_template: str, names: dict) -> str:
    lower_names = {name.lower() for name in names.keys()}

    name = name_template

    i = 1
    while name.lower() in lower_names:
        i += 1
        name = f"{name_template} ({i})"

    return name


def _remove_command(list_widget: QListWidget, del_from: dict, remove_button: QPushButton) -> bool:
    items = list_widget.selectedItems()
    if not items:
        return False

    name = items[0].text()

    del del_from[name]

    remove_index = list_widget.row(items[0])
    list_widget.takeItem(remove_index)

    remove_button.setEnabled(len(del_from) > 0)

    return True


def _item_changed(item: QListWidgetItem, activated_name: str, check_in_dict: dict) -> str:
    new_name = item.text()

    item.setSelected(True)

    if activated_name == new_name:
        return activated_name

    if new_name == "" or new_name.isspace() or new_name.lower() in {key.lower() for key in check_in_dict.keys()}:
        item.setText(activated_name)

        return activated_name

    if activated_name not in check_in_dict:
        return activated_name

    value = check_in_dict[activated_name]
    del check_in_dict[activated_name]
    check_in_dict[new_name] = value

    return new_name


def _create_item(name: str, list_widget: QListWidget, remove_button: QPushButton):
    item = QListWidgetItem(name)
    item.setFlags(item.flags() | Qt.ItemIsEditable)

    list_widget.addItem(item)
    list_widget.editItem(item)

    remove_button.setEnabled(True)

    item.setSelected(True)
