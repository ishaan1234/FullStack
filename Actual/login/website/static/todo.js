// Retrieve todos from local storage (if any) and display them on page load
window.addEventListener('load', function() {
  var storedTodos = JSON.parse(localStorage.getItem('todos'));
  if (storedTodos) {
    for (var i = 0; i < storedTodos.length; i++) {
      createTodoElement(storedTodos[i]);
    }
  }
});

// Create a "close" button and append it to each list item
function createTodoElement(todoText) {
  var li = document.createElement("li");
  var t = document.createTextNode(todoText);
  li.appendChild(t);

  var span = document.createElement("SPAN");
  var txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  li.appendChild(span);

  document.getElementById("myUL").appendChild(li);
}

// Click on a close button to hide the current list item and remove from local storage
function removeTodo() {
  var div = this.parentElement;
  div.style.display = "none";

  var todos = JSON.parse(localStorage.getItem('todos'));
  var todoText = div.firstChild.textContent;
  var index = todos.indexOf(todoText);
  if (index !== -1) {
    todos.splice(index, 1);
    localStorage.setItem('todos', JSON.stringify(todos));
  }
}

// Add a "checked" symbol when clicking on a list item
function toggleChecked() {
  this.classList.toggle('checked');
}

// Create a new list item when clicking on the "Add" button
function newElement() {
  var inputValue = document.getElementById("myInput").value;
  if (inputValue === '') {
    alert("You must write something!");
    return;
  }

  createTodoElement(inputValue);

  var todos = JSON.parse(localStorage.getItem('todos')) || [];
  todos.push(inputValue);
  localStorage.setItem('todos', JSON.stringify(todos));

  document.getElementById("myInput").value = "";
}

// Attach event listeners to dynamically created elements
document.getElementById("myUL").addEventListener('click', function(ev) {
  if (ev.target.tagName === 'LI') {
    toggleChecked.call(ev.target);
  } else if (ev.target.className === 'close') {
    removeTodo.call(ev.target);
  }
});

document.getElementById("addBtn").addEventListener('click', newElement);
