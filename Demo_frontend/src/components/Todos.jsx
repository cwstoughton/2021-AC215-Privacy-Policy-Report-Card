import React, {createContext, useEffect, useState} from "react";
import {
    Input,
    InputGroup,
    Stack
} from "@chakra-ui/core";



const APIContext = createContext({
  data: {}, })

export default function Todos() {
    const [data, setData] = useState({input_text: "REACT initialize", predictions: {IDENTIFIERS: [], LOCATION:[], THIRD_PARTY:[]}})
    const [policy_url, set_url] = React.useState("initiate")

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
            body: JSON.stringify({input : policy_url})})
          const result = response.json()
          return result
      }
      callApi().then(data => {
          console.log(data.data)
          setData(data.data)})}, [policy_url])

    function AnalyzePolicy() {

        var placeholderUrl = ""
        const handleInput = event  => {
            placeholderUrl = event.target.value
        }
        const handleSubmit = (event) =>  {
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


  return (
      <div>
          <APIContext.Provider value={{data}}>
              <AnalyzePolicy />
              <Stack spacing={1}>
                  [<b>{data.input_text}</b>]+{data.predictions.IDENTIFIERS.map(item => (<b>{item}</b>))}
              </Stack>
          </APIContext.Provider>
      </div>
  )
}