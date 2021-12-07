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
                <GaugeChart id={todo["input_text"].toString()} style={{height:250, width:'10%', textColor:"#464A4F"}}  nrOfLevels={20}  percent={todo["predictions"]['IDENTIFIERS']} />
  );

  useEffect(() => {
    fetchTodos()
  }, [])


const Component = (
  <Tabs>

<Stack spacing={50}>
      {todos.map((todo) =>

          [<TabList>
      <Tab>Identifiers</Tab>
      <Tab>Location Data</Tab>
      <Tab>3rd Party Sharing</Tab>
    </TabList>,
        <TabPanel>
          <Box>
            <GaugeChart id={todo["input_text"].toString()+"_ID"} style={{height:"250px", width:"33%", textColor:"#FF0000"}}  nrOfLevels={20}   colors={["#FFC371", "#FF5F6D"]}  percent={todo["predictions"]['IDENTIFIERS']} />,
          </Box>
        </TabPanel>,
        <TabPanel>
          <Box>
            <GaugeChart id={todo["input_text"].toString()+"_LC"} style={{height:"250px", width:"33%", textColor:"#464A4F"}}  nrOfLevels={20}   colors={["#C3FF71", "#5FFF6D"]}  percent={todo["predictions"]['LOCATION']} />
          </Box>
        </TabPanel>,
        <TabPanel>
          <Box>
            <GaugeChart id={todo["input_text"].toString()+"_3D"} style={{height:"250px", width:"33%", textColor:"#464A4F"}}  nrOfLevels={20}   colors={["#C371FF", "#5F6DFF"]}  percent={todo["predictions"]['3RD_PARTY']} />
          </Box>
        </TabPanel>]
      )}
       </Stack>
    <TabPanel>
      <GaugeChart id="gauge-chart6"
  animate={false}
  nrOfLevels={15}
  percent={0.56}
  needleColor="#345243"
/>
      <ui>
        <li>Luigi</li>
          <li>Japanese: ルイージ Hepburn: Ruīji, [ɾɯ.iː.dʑi̥]</li>
          <li>English: /luˈiːdʒi/; Italian: [luˈiːdʒi]</li>)
      </ui>
    </TabPanel>
      <TabPanel>
      <p>
        <b>Mario</b> (<i>Japanese: マリオ Hepburn: Mario, [ma.ɾʲi.o]</i>) (<i>English:
        /ˈmɑːrioʊ/; Italian: [ˈmaːrjo]</i>) is a fictional character in the Mario video
        game franchise, owned by Nintendo and created by Japanese video game designer
        Shigeru Miyamoto. Serving as the company's mascot and the eponymous protagonist
        of the series, Mario has appeared in over 200 video games since his creation.
        Depicted as a short, pudgy, Italian plumber who resides in the Mushroom
        Kingdom, his adventures generally center upon rescuing Princess Peach from the
        Koopa villain Bowser. His younger brother and sidekick is Luigi.
      </p>
      <p>
        Source:{' '}
        <a href="https://en.wikipedia.org/wiki/Mario" target="_blank">
          Wikipedia
        </a>
      </p>
    </TabPanel>
    <TabPanel>
      <p>
        <b>Princess Peach</b> (<i>Japanese: ピーチ姫 Hepburn: Pīchi-hime, [piː.tɕi̥ çi̥.me]</i>)
        is a character in Nintendo's Mario franchise. Originally created by Shigeru Miyamoto,
        Peach is the princess of the fictional Mushroom Kingdom, which is constantly under
        attack by Bowser. She often plays the damsel in distress role within the series and
        is the lead female. She is often portrayed as Mario's love interest and has appeared
        in Super Princess Peach, where she is the main playable character.
      </p>
      <p>
        Source:{' '}
        <a href="https://en.wikipedia.org/wiki/Princess_Peach" target="_blank">
          Wikipedia
        </a>
      </p>
    </TabPanel>
    <TabPanel>
      <p>
        <b>Yoshi</b> (<i>ヨッシー Yosshī, [joɕ.ɕiː]</i>) (<i>English: /ˈjoʊʃi/ or /ˈjɒʃi/</i>), once
        romanized as Yossy, is a fictional anthropomorphic dinosaur who appears in
        video games published by Nintendo. Yoshi debuted in Super Mario World (1990) on the
        Super Nintendo Entertainment System as Mario and Luigi's sidekick. Yoshi later starred
        in platform and puzzle games, including Super Mario World 2: Yoshi's Island, Yoshi's Story
        and Yoshi's Woolly World. Yoshi also appears in many of the Mario spin-off games, including
        Mario Party and Mario Kart, various Mario sports games, and Nintendo's crossover fighting
        game series Super Smash Bros. Yoshi belongs to the species of the same name, which is
        characterized by their variety of colors.
      </p>
      <p>
        Source:{' '}
        <a href="https://en.wikipedia.org/wiki/Yoshi" target="_blank">
          Wikipedia
        </a>
      </p>
    </TabPanel>
    <TabPanel>
      <p>
        <b>Toad</b> (<i>Japanese: キノピオ Hepburn: Kinopio</i>) is a fictional character who primarily
        appears in Nintendo's Mario franchise. Created by Japanese video game designer Shigeru Miyamoto,
        he is portrayed as a citizen of the Mushroom Kingdom and is one of Princess Peach's most loyal
        attendants; constantly working on her behalf. He is usually seen as a non-player character (NPC)
        who provides assistance to Mario and his friends in most games, but there are times when Toad(s)
        takes center stage and appears as a protagonist, as seen in Super Mario Bros. 2, Wario's Woods,
        Super Mario 3D World, and Captain Toad: Treasure Tracker.
      </p>
      <p>
        Source:{' '}
        <a href="https://en.wikipedia.org/wiki/Toad_(Nintendo)" target="_blank">
          Wikipedia
        </a>
      </p>
    </TabPanel>
  </Tabs>
);



  return (<div>
    <TodosContext.Provider value={{todos, fetchTodos}}>

      <AddTodo />  {/* new */}
       {Component}
      <Stack spacing={5} divider={<Divider orientation="vertical" flexItem />}>
        <div>
        {todos.map(todo => (
            [
                <Text style={{textAlignVertical: "center",textAlign: "center",}}>{todo.input_text}</Text>,
                <Stack direction="row">
                    [
                    <GaugeChart id={todo["input_text"].toString()+"_ID"} style={{height:"250px", width:"33%", textColor:"#FF0000"}}  nrOfLevels={20}   colors={["#FFC371", "#FF5F6D"]}  percent={todo["predictions"]['IDENTIFIERS']} />,
                    <GaugeChart id={todo["input_text"].toString()+"_LC"} style={{height:"250px", width:"33%", textColor:"#464A4F"}}  nrOfLevels={20}   colors={["#C3FF71", "#5FFF6D"]}  percent={todo["predictions"]['LOCATION']} />,
                    <GaugeChart id={todo["input_text"].toString()+"_3D"} style={{height:"250px", width:"33%", textColor:"#464A4F"}}  nrOfLevels={20}   colors={["#C371FF", "#5F6DFF"]}  percent={todo["predictions"]['3RD_PARTY']} />
                    ]
                </Stack>
            ]
        ))}
        </div>
      </Stack>
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

