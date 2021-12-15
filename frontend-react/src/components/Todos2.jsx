import React, { useEffect, useState } from "react";
import {
    Input,
    InputGroup,
    Stack,
} from "@chakra-ui/core";

const TodosContext = React.createContext({
  todos: [], fetchTodos: () => {}
})

export default function Todos() {
  const [todos, setTodos] = useState([{'input_text':"", "predictions":""}])
  // const todos =
  const fetchTodos = async () => {
<<<<<<<< HEAD:frontend-react/src/components/Todos2.jsx
    // const response = await fetch("http://localhost:9000/todo")
    // const todos = await response.json()
========
    const response = await fetch("http://localhost:9000/predict")
    const todos = await response.json()
>>>>>>>> final:Demo_frontend/src/components/Todos.jsx
    setTodos(todos.data)
  }
  // console.log(todos.toString())
  useEffect(() => {
    fetchTodos()
  }, [])
  return (
    <TodosContext.Provider value={{todos, fetchTodos}}>
      <AddTodo />  {/* new */}
      <Stack spacing={5}>
            {todos.map((todo) => (
          <b>{todo.input_text} : {JSON.stringify(todo.predictions)}</b>
        ))}
      </Stack>
    </TodosContext.Provider>
  )
}

function AddTodo() {
  const [item, setItem] = React.useState("")
  const {fetchTodos} = React.useContext(TodosContext)

  const handleInput = event  => {
    setItem(event.target.value)
  }

  const handleSubmit = (event) => {
    const newTodo = {
      "text": todos.length + 1,
      "item": item
    }

<<<<<<<< HEAD:frontend-react/src/components/Todos2.jsx
    const todos = fetch(`http://localhost:9000/analyze_policy?input_text=${encodeURIComponent(newTodo.item)}`, {
========
        fetch(`http://localhost:9000/predict_new?input_text=${encodeURIComponent(newTodo.item)}`, {
>>>>>>>> final:Demo_frontend/src/components/Todos.jsx
      method: "POST",
      headers: { "Content-Type": "application/json" },
      // body: newTodo.item

    }).then(fetchTodos)
  }

  return (
    <form onSubmit={handleSubmit}>
      <InputGroup size="md">
        <Input
          pr="4.5rem"
          type="text"
          placeholder="Enter a sentence or paragraph as input text."
          aria-label="Enter a sentence or paragraph as input text."
          onChange={handleInput}
        />
      </InputGroup>
    </form>
  )
}