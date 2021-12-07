import React, { useEffect, useState } from "react";
import {
    Box,
    Button, Divider,
    Flex,
    Input,
    InputGroup,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Stack,
    Text,
    useDisclosure
} from "@chakra-ui/core";
import GaugeChart from 'react-gauge-chart';


const TodosContext = React.createContext({
  todos: [], fetchTodos: () => {}
})

export default function Todos() {
  const [todos, setTodos] = useState([])



  const fetchTodos = async () => {
    const response = await fetch("http://34.134.205.218.sslip.io/api/predict")
    const newTodos = await response.json()
    // output the value of todos to console
    console.log(newTodos)

    setTodos(newTodos.data)
  }
  const listItems = todos.map((todo) =>
                <GaugeChart id={todo["input_text"].toString()} style={{height:250, width:'10%', textColor:"#464A4F"}}  nrOfLevels={20}  percent={todo["predictions"]['IDENTIFIERS']} />
  );

  useEffect(() => {
    fetchTodos()
  }, [])
  return (
    <TodosContext.Provider value={{todos, fetchTodos}}>
      <AddTodo />  {/* new */}

      <Stack spacing={5} divider={<Divider orientation="vertical" flexItem />}>

        {todos.map(todo => (
            [<b>{todo.input_text}</b>, <br />,
                <Stack direction="row">
            [<GaugeChart id={todo["input_text"].toString()} style={{height:250, width:'10%', textColor:"#464A4F"}}  nrOfLevels={20}  percent={todo["predictions"]['IDENTIFIERS']} />,
            <GaugeChart id={todo["input_text"].toString()} style={{height:250, width:'10%', textColor:"#464A4F"}}  nrOfLevels={20}  percent={todo["predictions"]['LOCATION']} />,
            <GaugeChart id={todo["input_text"].toString()} style={{height:250, width:'10%', textColor:"#464A4F"}}  nrOfLevels={20}  percent={todo["predictions"]['3RD_PARTY']} />]
                </Stack>]
        ))}
        ))}
        ))}
      </Stack>
    </TodosContext.Provider>
  )
}

function AddTodo() {
  const [item, setItem] = React.useState("")
  const {todos, fetchTodos} = React.useContext(TodosContext)
  
  const handleInput = event  => {
    setItem(event.target.value)
  }

  const handleSubmit = (event) => {
    const newTodo = {
      "text": todos.length + 1,
      "item": item
    }

        fetch(`http://34.134.205.218.sslip.io/api/predict_new?input_text=${encodeURIComponent(newTodo.item)}`, {
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


