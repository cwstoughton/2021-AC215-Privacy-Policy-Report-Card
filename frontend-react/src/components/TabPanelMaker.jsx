import {Box, Stack} from "@chakra-ui/core";
// import {TabPanel} from "react-tabs";
import React from "react";
import GaugeChart from "react-gauge-chart";


const TabPanelMaker = ({title, colors, score, sentences}) => {
    return (
            <Stack direction="row">
                [
                <Box style={{backgroundColor: "#FFFFFF"}}>
                    <h2>{title.toString().toUpperCase()}</h2>
                    <GaugeChart id="1" style={{width: "100%"}} nrOfLevels={20} textColor="#000000"
                                colors={colors} percent={score}/>
                </Box>,
                <Box>
                    <ul>
                        {sentences.map(item => <li>{item}</li>)}
                    </ul>
                </Box>
                ]
            </Stack>
    )
}


export default TabPanelMaker;