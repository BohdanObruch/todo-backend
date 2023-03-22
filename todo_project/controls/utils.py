def resource(relative_path):
    import todo_project
    from pathlib import Path
    return (
        Path(todo_project.__file__)
        .parent
        .parent
        .joinpath()
        .joinpath(relative_path)
        .absolute()
        .__str__()
        .replace("\\", "/")
    )
