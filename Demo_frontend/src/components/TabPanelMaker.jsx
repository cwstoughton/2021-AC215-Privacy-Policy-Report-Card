import {Box, Stack} from "@chakra-ui/core";
import {TabPanel} from "react-tabs";
import React from "react";
import GaugeChart from "react-gauge-chart";

const SingleTabPanel = (score, sentences) => (
        <TabPanel>
            <Stack direction="row">
                [
                <Box style={{backgroundColor: "#FFFFFF"}}>
                    <h2>Identifiers</h2>
                    <GaugeChart id="1" style={{width: "100%"}} nrOfLevels={20} textColor="#000000"
                                colors={["#FFC371", "#FF5F6D"]} percent={score}/>
                </Box>,
                <Box>
                    <ul>
                        <li>{sentences}</li>

                    </ul>
                </Box>
                ]
            </Stack>
        </TabPanel>
    )

export default SingleTabPanel;