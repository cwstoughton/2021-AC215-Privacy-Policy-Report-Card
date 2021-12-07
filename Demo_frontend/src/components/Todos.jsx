import React, { useEffect, useState } from "react";
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';
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
                todo.input_text
  );

  useEffect(() => {
    fetchTodos()
  }, [])

const chartStyle = {width:"33%", formatTextValue:(value => (value>0.5)), textColor:{color:"FF00FF"}}
const Component = (


<Stack spacing={50}>
      {todos.map((todo) =>
          [<Tabs><TabList>
      <Tab>Overview</Tab>
              <Tab>Identifiers</Tab>
      <Tab>Location Data</Tab>
      <Tab>3rd Party Sharing</Tab>
    </TabList>
              <TabPanel>
          <Box style={{backgroundColor:"#FFFFFF"}}>
              <h2 style={{color:"white"}}>Overview</h2>
              <Text><font color="#00FF00">INPUT TEXT:</font> {todo.input_text}</Text>
              <Stack direction="row">
                  [
                  <Stack>[<Text style={{textAlignVertical: "center",textAlign: "center",}}>IDENTIFIERS</Text>,<GaugeChart id="1" style={{width:"100%"}}  nrOfLevels={20} textColor="#000000" colors={["#FFC371", "#FF5F6D"]}  percent={todo["predictions"]['IDENTIFIERS']} />]</Stack>,
                  <Stack>[<Text style={{textAlignVertical: "center",textAlign: "center",}}>LOCATION</Text>,<GaugeChart id={todo["input_text"].toString()+"_LC"} style={{width:"100%"}} textColor="#000000" nrOfLevels={20}   colors={["#C3FF71", "#5FFF6D"]}  percent={todo["predictions"]['LOCATION']} />]</Stack>,
                  <Stack>[<Text style={{textAlignVertical: "center",textAlign: "center",}}>3RD PARTY </Text>,<GaugeChart id={todo["input_text"].toString()+"_3D"} style={{width:"100%"}} textColor="#000000" nrOfLevels={20}   colors={["#C371FF", "#5F6DFF"]}  percent={todo["predictions"]['3RD_PARTY']} />]</Stack>
               ]
                  </Stack>

          </Box>
        </TabPanel>
        <TabPanel>
            <Stack direction="row">
                [
                <Box style={{backgroundColor:"#FFFFFF"}}>
                    <h2>Identifiers</h2>
                    <GaugeChart id="1" style={{width:"100%"}}  nrOfLevels={20} textColor="#000000" colors={["#FFC371", "#FF5F6D"]}  percent={todo["predictions"]['IDENTIFIERS']} />
                </Box>,
                <Box>
                    <ul>
                        {listItems.map(item => <li>{item}</li>)}
                    </ul>
                </Box>
                ]
            </Stack>
        </TabPanel>
        <TabPanel>
            <Stack direction="row">
                [
                <Box style={{backgroundColor:"#FFFFFF"}}>
                    <h2>Location Data</h2>
                    <GaugeChart id={todo["input_text"].toString()+"_LC"} style={{width:"100%"}} textColor="#000000" nrOfLevels={20}   colors={["#C3FF71", "#5FFF6D"]}  percent={todo["predictions"]['LOCATION']} />
                </Box>,
                <Box>
                    <ul>
                        {listItems.map(item => <li>{item}</li>)}
                    </ul>
                </Box>
                ]
            </Stack>
        </TabPanel>
        <TabPanel>
            <Stack direction="row">
                [
                <Box style={{backgroundColor:"#FFFFFF"}}>
                    <h2>3rd Party Sharing</h2>
                    <GaugeChart id={todo["input_text"].toString()+"_3D"} style={{width:"100%"}} textColor="#000000" nrOfLevels={20}   colors={["#C371FF", "#5F6DFF"]}  percent={todo["predictions"]['3RD_PARTY']} />
                </Box>,
                <Box>
                    <ul>
                        {listItems.map(item => <li>{item}</li>)}
                    </ul>
                </Box>
                ]
            </Stack>
        </TabPanel>
      </Tabs>
          ]
      )}
       </Stack>

);



  return (<div>
    <TodosContext.Provider value={{todos, fetchTodos}}>

      <AddTodo />  {/* new */}
        {Component}
      {/*<Stack spacing={5} divider={<Divider orientation="vertical" flexItem />}>*/}
      {/*  <div>*/}
      {/*  {todos.map(todo => (*/}
      {/*      [*/}
      {/*          <Text style={{textAlignVertical: "center",textAlign: "center",}}>{todo.input_text}</Text>,*/}
      {/*          <Stack direction="row">*/}
      {/*              [*/}
      {/*              <GaugeChart id={todo["input_text"].toString()+"_ID"} style={{height:"250px", width:"33%", textColor:"#FF0000"}}  nrOfLevels={20}   colors={["#FFC371", "#FF5F6D"]}  percent={todo["predictions"]['IDENTIFIERS']} />,*/}
      {/*              <GaugeChart id={todo["input_text"].toString()+"_LC"} style={{height:"250px", width:"33%", textColor:"#464A4F"}}  nrOfLevels={20}   colors={["#C3FF71", "#5FFF6D"]}  percent={todo["predictions"]['LOCATION']} />,*/}
      {/*              <GaugeChart id={todo["input_text"].toString()+"_3D"} style={{height:"250px", width:"33%", textColor:"#464A4F"}}  nrOfLevels={20}   colors={["#C371FF", "#5F6DFF"]}  percent={todo["predictions"]['3RD_PARTY']} />*/}
      {/*              ]*/}
      {/*          </Stack>*/}
      {/*      ]*/}
      {/*  ))}*/}
      {/*  </div>*/}
      {/*</Stack>*/}
    </TodosContext.Provider></div>
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

// function RenderTabs(){
//   render(component)
// }

