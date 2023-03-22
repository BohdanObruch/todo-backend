from flask import Flask, request
from resources import EntryManager, Entry
from todo_project.controls.utils import resource

app = Flask(__name__)


@app.route('/api/entries/')
def get_entries():
    entry_manager = EntryManager(data_path=FOLDER)
    entry_manager.load()
    entries_list = []
    for entry in entry_manager.entries:
        entries_list.append(entry.json())
    return entries_list


@app.route('/api/save_entries/', methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    entries_json = request.get_json()
    for entry in entries_json:
        entry_object = Entry.from_json(entry)
        entry_manager.entries.append(entry_object)
    entry_manager.save()
    return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# not yet implemented on the frontend
@app.route('/api/entry/done/', methods=['POST'])
def mark_entry_done():
    entry_manager = EntryManager(FOLDER)
    entry_manager.load()
    entry_title = request.get_json().get('title')
    for entry in entry_manager.entries:
        if entry.title == entry_title:
            entry.mark_done()
            entry_manager.save()
            return {'status': 'success'}
    return {'status': 'error', 'message': 'Entry not found'}


# not yet implemented on the frontend
@app.route('/api/entry/not_done/', methods=['POST'])
def mark_entry_not_done():
    entry_manager = EntryManager(FOLDER)
    entry_manager.load()
    entry_title = request.get_json().get('title')
    for entry in entry_manager.entries:
        if entry.title == entry_title:
            entry.mark_not_done()
            entry_manager.save()
            return {'status': 'success'}
    return {'status': 'error', 'message': 'Entry not found'}


# not yet implemented on the frontend
@app.route('/api/entry/delete/', methods=['POST'])
def delete_entry():
    entry_manager = EntryManager(FOLDER)
    entry_manager.load()
    entry_title = request.get_json().get('title')
    for entry in entry_manager.entries:
        if entry.title == entry_title:
            entry.parent.entries.remove(entry)
            entry_manager.save()
            return {'status': 'success'}
    return {'status': 'error', 'message': 'Entry not found'}


FOLDER = resource("todo_list")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
