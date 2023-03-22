import json
import os
from typing import List


class Entry:
    def __init__(self, title, entries=None, parent=None, done=False):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent
        self.done = done

    def mark_done(self):
        self.done = True

    def mark_not_done(self):
        self.done = False

    def __str__(self):
        return self.title

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(str(self), indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    def json(self):
        result = {"title": self.title, "entries": []}
        for entry in self.entries:
            result["entries"].append(entry.json())
        return result

    @classmethod
    def from_json(cls, data):
        entry = cls(data["title"])
        for subentry in data.get("entries", []):
            entry.add_entry(cls.from_json(subentry))
        return entry

    def save(self, path):
        file_name = f"{self.title}.json"
        file_path = os.path.join(path, file_name)
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(self.json(), f, indent=4, ensure_ascii=False)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_json(data)


def print_with_indent(value, indent=0):
    print(('\t' * indent) + value)


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for filename in os.listdir(self.data_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_path, filename)
                entry = Entry.load(filepath)
                self.entries.append(entry)

    def add_entry(self, title: str):
        entry = Entry(title)
        self.entries.append(entry)
