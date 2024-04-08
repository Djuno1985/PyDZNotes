import argparse
import json
from datetime import datetime

def add_note(title, message, notes):
    note_id = len(notes) + 1
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note = {"id": note_id, "title": title, "message": message, "created_at": created_at}
    notes.append(note)
    return notes

def list_notes(notes, date_filter=None):
    if date_filter:
        filtered_notes = [note for note in notes if note["created_at"].startswith(date_filter)]
        return filtered_notes
    return notes

def save_notes(notes, filename):
    with open(filename, "w") as file:
        json.dump(notes, file, indent=4)

def load_notes(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def edit_note(note_id, new_title, new_message, notes):
    for note in notes:
        if note["id"] == note_id:
            note["title"] = new_title
            note["message"] = new_message
            return notes
    print(f"Заметка с ID {note_id} не найдена.")
    return notes

def delete_note(note_id, notes):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            return notes
    print(f"Заметка ID {note_id} не найдена.")
    return notes



def main():
    parser = argparse.ArgumentParser(description="Простое консольное приложение заметки")
    parser.add_argument("command", choices=["add", "list", "edit", "delete"], help="Команда для выполнения")
    parser.add_argument("--title", help="Заголовок заметки")
    parser.add_argument("--msg", help="Сообщение заметки")
    parser.add_argument("--date", help="Фильтр по дате для списка заметок (ГГГГ-ММ-ДД)")
    parser.add_argument("--id", type=int, help="Идентификатор заметки для редактирования или удаления")
    args = parser.parse_args()

    filename = "notes.json"
    notes = load_notes(filename)

    if args.command == "add":
        if not (args.title and args.msg):
            print("Пожалуйста, укажите как заголовок, так и сообщение для заметки.")
            return
        notes = add_note(args.title, args.msg, notes)
        save_notes(notes, filename)
        print("Заметка успешно добавлена.")
    elif args.command == "list":
        date_filter = args.date if args.date else None
        filtered_notes = list_notes(notes, date_filter)
        if filtered_notes:
            for note in filtered_notes:
                print(f"ID: {note['id']}, Заголовок: {note['title']}, Сообщение: {note['message']}, Создано: {note['created_at']}")
        else:
            print("Заметок не найдено.")
    elif args.command == "edit":
        if not args.id:
            print("Пожалуйста, укажите идентификатор заметки для редактирования.")
            return
        notes = edit_note(args.id, args.title, args.msg, notes)
        save_notes(notes, filename)
        print(f"Заметка с ID {args.id} успешно отредактирована.")
    elif args.command == "delete":
        if not args.id:
            print("Пожалуйста, укажите идентификатор заметки для удаления.")
            return
        notes = delete_note(args.id, notes)
        save_notes(notes, filename)
        print(f"Заметка с ID {args.id} успешно удалена.")

if __name__ == "__main__":
    main()
