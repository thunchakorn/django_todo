function showTodolist() {
    let dueValue = document.getElementById("due-select").value;
    document.getElementById("todo-list").innerHTML = '';
    
    fetch(`/todo/todolist/?due=${dueValue}`)
    .then(response => response.json())
    .then(json => {
        let todoList = json["todo_list"]
        if (todoList.length === 0) {
            document.getElementById("todo-list").innerHTML = 'Congrats, you have no Todo.';
        } else {
            for (var i = 0; i < todoList.length; i++) {
                let todo_i = document.createElement('div');
                todo_i.classList.add('todo')
                todo_i.innerHTML = todoList[i]["name"];
                todo_i.setAttribute('onclick', "location.href='#';");
                document.getElementById("todo-list").appendChild(todo_i);
            };
        }

    })
}

document.addEventListener('DOMContentLoaded', function() {
    showTodolist()
})
