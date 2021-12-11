import React, {createContext, useEffect, useState} from "react";
import {Text, Box, Input, InputGroup, Stack} from "@chakra-ui/core";
import {Tab, Tabs, TabList, TabPanel} from 'react-tabs';
import GaugeChart from 'react-gauge-chart';
// import TabPanelMaker from './TabPanelMaker';
import 'react-tabs/style/react-tabs.css';


const APIContext = createContext({
    data: {},
})

export default function Todos() {
    const [data, setData] = useState({
        input_text: "REACT initialize",
        identifier_score: 0.3,
        identifier_sentences: [],
        location_score: 0.5,
        location_sentences: [],
        third_party_score: 0.8,
        third_party_sentences: []
    })


    const [policy_url, set_url] = React.useState("")

    console.log(policy_url)


    useEffect(() => {
        const callApi = async () => {
            const response = await fetch('http://localhost:9000/analyze', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                mode: 'cors',
                body: JSON.stringify({input: policy_url})
            })
            return response.json()
        }
        callApi().then(data => {
            console.log(data.data)
            setData(data.data)
        })
    }, [policy_url])

    function AnalyzePolicy() {

        var placeholderUrl = ""
        const handleInput = event => {
            placeholderUrl = event.target.value
        }
        const handleSubmit = (event) => {
            set_url(placeholderUrl)
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


    const chartStyle = {width: "33%", formatTextValue: value => (value > 0.5), textColor: {color: "FF00FF"}}
    const Component = (


        <Stack spacing={50}>

            [
            <Tabs>
                <TabList>
                    <Tab>Overview</Tab>
                    <Tab>Identifiers</Tab>
                    <Tab>Location Data</Tab>
                    <Tab>3rd Party Sharing</Tab>

                </TabList>
                {/*pass data.identifier_score and data.identifier_sentences to TabPanelMaker*/}

                <TabPanel>
                    <Box style={{backgroundColor: "#FFFFFF"}}>
                        <h2 style={{color: "white"}}>Overview</h2>
                        <Text><font color="#00FF00">INPUT TEXT:</font> {data.input_text}</Text>
                        <Stack direction="row">

                            [
                            <Stack>[
                                <Text
                                    style={{
                                        textAlignVertical: "center",
                                        textAlign: "center",
                                    }}>IDENTIFIERS</Text>,<GaugeChart
                                    id={data.input_text.toString() + "_ID"} style={{width: "100%"}} nrOfLevels={20}
                                    textColor="#000000" colors={["#FFC371", "#FF5F6D"]}
                                    percent={data.identifier_score}/>]</Stack>,

                            <Stack>[
                                <Text
                                    style={{
                                        textAlignVertical: "center",
                                        textAlign: "center",
                                    }}>LOCATION
                                </Text>,

                                <GaugeChart
                                    id={data.input_text.toString() + "_LC"} style={{width: "100%"}} textColor="#000000"
                                    nrOfLevels={20} colors={["#C3FF71", "#5FFF6D"]}
                                    percent={data.location_score}
                                />
                                ]
                            </Stack>,

                            <Stack>[
                                <Text style={{textAlignVertical: "center", textAlign: "center",}}>3RD
                                    PARTY </Text>,<GaugeChart id={data.input_text.toString() + "_3D"}
                                                              style={{width: "100%"}}
                                                              textColor="#000000" nrOfLevels={20}
                                                              colors={["#C371FF", "#5F6DFF"]}
                                                              percent={data.third_party_score}/>]</Stack>
                            ]
                        </Stack>

                    </Box>
                </TabPanel>


                <TabPanel>
                    <Stack direction="row">
                        [
                        <Box style={{backgroundColor: "#FFFFFF"}}>
                            <h2>Identifiers</h2>
                            <GaugeChart id="1" style={{width: "100%"}} nrOfLevels={20} textColor="#000000"
                                        colors={["#FFC371", "#FF5F6D"]} percent={data.identifier_score}/>
                        </Box>,
                        <Box>
                            <ul>
                                {data.identifier_sentences.map(item => <li>{item}</li>)}
                            </ul>
                        </Box>
                        ]
                    </Stack>
                </TabPanel>

                <TabPanel>
                    <Stack direction="row">
                        [
                        <Box style={{backgroundColor: "#FFFFFF"}}>
                            <h2>Location Data</h2>
                            <GaugeChart id={data.input_text + "_LC"} style={{width: "100%"}}
                                        textColor="#000000" nrOfLevels={20} colors={["#C3FF71", "#5FFF6D"]}
                                        percent={data.location_score}/>
                        </Box>,
                        <Box>
                            <ul>
                                {data.location_sentences.map(item => <li>{item}</li>)}
                            </ul>
                        </Box>
                        ]
                    </Stack>
                </TabPanel>
                <TabPanel>
                    <Stack direction="row">
                        [
                        <Box style={{backgroundColor: "#FFFFFF"}}>
                            <h2>3rd Party Sharing</h2>
                            <GaugeChart id={data.input_text + "_3D"} style={{width: "100%"}}
                                        textColor="#000000" nrOfLevels={20} colors={["#C371FF", "#5F6DFF"]}
                                        percent={data.third_party_score}/>
                        </Box>,
                        <Box>
                            <ul>
                                {data.third_party_sentences.map(item => <li>{item}</li>)}
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
            <APIContext.Provider value={{data}}>

                <AnalyzePolicy/> {/* new */}
                {Component}
            </APIContext.Provider></div>
    )
}
//   return (
//       <div>
//           <APIContext.Provider value={{data}}>
//               <AnalyzePolicy />
//               <Stack spacing={1}>
//
//                   [<b>{data.input_text}: {data.identifier_score}</b>, ]+{data.identifier_sentences.map(item => (<b>{item}</b>))}
//               </Stack>
//           </APIContext.Provider>
//       </div>
//   )
// }


