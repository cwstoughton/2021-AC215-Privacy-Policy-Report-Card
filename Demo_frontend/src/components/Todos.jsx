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
  const [todos, setTodos] = useState([])

  const fetchTodos = async () => {
    const response = await fetch(`http://localhost:9000/analyze?input=${encodeURIComponent("https://twitter.com/en/privacy")}`)
    const todos = await response.json()
    setTodos(todos.data)
  }
  useEffect(() => {
    fetchTodos()
  })
  return (
    <TodosContext.Provider value={{todos, fetchTodos}}>
      <AddTodo />  {/* new */}

      <Stack spacing={5}>



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

  const handleSubmit = async (event) => {
    // const pageElements = {
    //   "input": item,
    // }

   await fetch(`http://localhost:9000/analyze?input=${encodeURIComponent(item.toString())}`).then(fetchTodos)
  }

  return (
    <form onSubmit={handleSubmit}>
      <InputGroup size="md">
        <Input
          pr="4.5rem"
          type="text"
          placeholder= "PLACEHOLDER"
          aria-label="https://twitter.com/en/privacy"
          onChange={handleInput}
        />
      </InputGroup>
    </form>
  )}