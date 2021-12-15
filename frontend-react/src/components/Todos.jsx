import React, {createContext, useEffect, useState} from "react";
import {Text, Box, Input, InputGroup, Stack} from "@chakra-ui/core";
import {Tab, Tabs, TabList, TabPanel} from 'react-tabs';
import GaugeChart from 'react-gauge-chart';
import TabPanelMaker from './TabPanelMaker';
import 'react-tabs/style/react-tabs.css';
import Loader from "react-loader-spinner";

const APIContext = createContext({
    data: {},
})

export default function Todos() {
    const [isPending, setIsPending] = useState(false);
    const [data, setData] = useState({
        input_text: "Let's begin",
        predictions: [{
            category: "identifiers",
            sentences: [],
            score: 0.0,
            colors: ["#FFC371", "#FF5F6D"]
        },
            {
                category: "location",
                sentences: [],
                score: 0.0,
                colors: ["#C3FF71", "#5FFF6D"]
            },
            {
                category: "third_party_sharing",
                sentences: [],
                score: 0.0,
                colors: ["#86CEFA", "#003396"]
            },
            {
                category: "contacts",
                sentences: [],
                score: 0.0,
                colors: ["#C371FF", "#5F6DFF"]
            }]
    })
    // {
    //     input_text: "REACT initialize",
    //     identifier_score: 0.3,
    //     identifier_sentences: [],
    //     location_score: 0.5,
    //     location_sentences: [],
    //     third_party_score: 0.8,
    //     third_party_sentences: []
    // }


    const [policy_url, set_url] = React.useState("")

    console.log(policy_url)


    useEffect(() => {
        setIsPending(true)
        const callApi = async () => {
            const response = await fetch('/api/analyze', {
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
            setIsPending(false);

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

    const Component = (

        <Stack spacing={50}>
            [
            <Tabs>
                <TabList>
                    <Tab>Overview</Tab>
                    {data.predictions.map(item => <Tab>{item.category.toUpperCase()}</Tab>)}
                </TabList>

                <TabPanel>

                    <Box style={{backgroundColor: "#FFFFFF"}}>

                        <h2 style={{color: "white"}}>Overview</h2>

                        <Text><font color="#00FF00">URL:</font> {data.input_text}</Text>

                        <Stack direction="row">
                            {data.predictions.map(item =>
                                <Stack>[
                                    <Text
                                        style={{
                                            textAlignVertical: "center",
                                            textAlign: "center",
                                        }}>{item.category.toUpperCase()}</Text>,
                                    <GaugeChart
                                        id={item.category + "_ID"} style={{width: "100%"}} nrOfLevels={20}
                                        textColor="#000000" colors={item.colors}
                                        percent={item.score}/>]</Stack>
                            )}
                        </Stack>
                    </Box>
                </TabPanel>

                {data.predictions.map(item =>
                    <TabPanel>
                        <TabPanelMaker title={item.category.toUpperCase()} score={item.score} colors={item.colors}
                                       sentences={item.sentences}/>
                    </TabPanel>
                )}

                {/*<TabPanel>*/}
                {/*    <TabPanelMaker*/}
                {/*        title="Am I being tracked?"*/}
                {/*        colors={["#FFC371", "#FF5F6D"]}*/}
                {/*        score={data.identifier_score}*/}
                {/*        sentences={data.identifier_sentences}*/}
                {/*    />*/}
                {/*</TabPanel>*/}

                {/*<TabPanel>*/}
                {/*    <TabPanelMaker*/}
                {/*        title="Do they know where I am?"*/}
                {/*        colors={["#C3FF71", "#5FFF6D"]}*/}
                {/*        score={data.location_score}*/}
                {/*        sentences={data.location_sentences}*/}
                {/*    />*/}
                {/*</TabPanel>*/}

                {/*<TabPanel>*/}
                {/*    <TabPanelMaker*/}
                {/*        title="Is my data shared with others?"*/}
                {/*        colors={["#C371FF", "#5F6DFF"]}*/}
                {/*        score={data.third_party_score}*/}
                {/*        sentences={data.third_party_sentences}*/}
                {/*    />*/}
                {/*</TabPanel>*/}
            </Tabs>
            ]
        </Stack>

    );


    return (
        <div>
            <APIContext.Provider value={{data}}>

                <AnalyzePolicy/> {/* new */}
                { isPending && <div align="center"><Stack direction="row"><Loader type="Circles" color="#00BFFF" height={80} width={80}/>, <div> <font size="80">Loading...</font> </div>]</Stack></div> }
                {!isPending && Component}
            </APIContext.Provider>
        </div>
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


