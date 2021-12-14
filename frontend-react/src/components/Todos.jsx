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
    const Capitalize = (str) => {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
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

    const [policy_url, set_url] = React.useState("")

    console.log(policy_url)


    useEffect(() => {
        setIsPending(true)
        const callApi = async () => {
            const response = await fetch(
                // for local hosting
                // 'http://localhost:9000/analyze',
                // for GKE deployment:
                "/api/analyze",
                {
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
                        placeholder="Enter any privacy policy URL for analysis. (ex. https://twitter.com/en/privacy)"
                        aria-label="Enter a URL to a privacy policy for analysis."
                        onChange={handleInput}
                    />
                </InputGroup>
                <button type = 'submit'>Click to submit</button>
            </form>
        )
    }

    const Component = (

        <Stack spacing={50}>
            [
            <Tabs>
                <TabList>
                    <Tab>Overview</Tab>
                    {data.predictions.map(item => <Tab>{Capitalize(item.category).replaceAll("_", " ")}</Tab>)}
                </TabList>

                <TabPanel>


                    <Box style={{backgroundColor: "#FFFFFF"}}>

                        <h2 style={{color: "Black"}}>Overview</h2>
                        The scores you see represent how confident we are that the privacy policy you’ve entered tracks information in each category on a scale from 0 to 1. The higher the score, the more likely that the service tracks user data in that category. For details of how these scores are calculated, see our Medium post.
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