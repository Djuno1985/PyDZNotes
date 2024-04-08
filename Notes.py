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

def main():
    parser = argparse.ArgumentParser(description="Simple notes console application")
    parser.add_argument("command", choices=["add", "list"], help="Command to execute")
    parser.add_argument("--title", help="Title of the note")
    parser.add_argument("--msg", help="Message of the note")
    parser.add_argument("--date", help="Date filter for listing notes (YYYY-MM-DD)")
    args = parser.parse_args()

    filename = "notes.json"
    notes = load_notes(filename)

    if args.command == "add":
        if not (args.title and args.msg):
            print("Please provide both title and message for the note.")
            return
        notes = add_note(args.title, args.msg, notes)
        save_notes(notes, filename)
        print("Note added successfully.")
    elif args.command == "list":
        date_filter = args.date if args.date else None
        filtered_notes = list_notes(notes, date_filter)
        if filtered_notes:
            for note in filtered_notes:
                print(f"ID: {note['id']}, Title: {note['title']}, Message: {note['message']}, Created at: {note['created_at']}")
        else:
            print("No notes found.")

if __name__ == "__main__":
    main()
