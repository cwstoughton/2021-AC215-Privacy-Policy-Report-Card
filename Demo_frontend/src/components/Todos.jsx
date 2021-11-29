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

  // const [item, setItem] = React.useState("nope")/**/
  const [todos, setTodos] = useState([])

  const fetchTodos = async () => {
    setTodos(todos)
  }
  useEffect(() => {
    fetchTodos()
  })

  return (
    <TodosContext.Provider value={{todos, fetchTodos}}>
      <AddTodo />  {/* new */}
        
      <Stack spacing={5}>

        {JSON.stringify(todos)}
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
    const atodo = {
      "item": item
    }
    
    fetch(`http://localhost:9000/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: {"url": atodo.item}
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