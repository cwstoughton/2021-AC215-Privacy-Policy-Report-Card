import {Text, Box, Stack} from "@chakra-ui/core";
// import {TabPanel} from "react-tabs";
import React from "react";
import GaugeChart from "react-gauge-chart";


const TabPanelMaker = ({title, colors, score, sentences}) => {
    const Capitalize = (str) => {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
    return (
        <Stack direction="row">
            [
            <Stack>
                [
                <Box style={{backgroundColor: "#FFFFFF"}}>
                    <h2>{Capitalize(title.toLowerCase().replaceAll("_", " "))}</h2>
                    <GaugeChart id="1" style={{width: "100%"}} nrOfLevels={20} textColor="#000000"
                                colors={colors} percent={score}/>
                </Box>,
                <Text color="dark grey">
                    There is a <font color="#5555FF">{(100*score).toFixed(2)}%</font> chance this service makes use of <font color="#5555FF">"{title.toLowerCase().replaceAll("_", " ")}"</font>.
                </Text>
                ]</Stack>
            ,<Stack>
            [<Text color="dark grey"><b>These sentences in the privacy policy fall into the category of <font color="#5555FF">"{title.toLowerCase().replaceAll("_", " ")}"</font>:</b></Text>,

            <Box>
                <ul>
                    {sentences.map(item => <li>{item}</li>)}
                </ul>
            </Box>]</Stack>
            ]
        </Stack>
    )
}


export default TabPanelMaker;