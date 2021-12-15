import React, {useContext, useEffect, useState} from "react";
import {
    Input,
    InputGroup,
    Stack
} from "@chakra-ui/core";

// const IdentifierContext = React.createContext({
//   identifier_paragraphs : [], fetch_identifier_paragraphs: () => {}
// })
//
// const LocationContext = React.createContext({
//   location_paragraphs : [], fetch_location_paragraphs: () => {}
// })



// const APIContext = React.createContext({
//   policy_url : "initiate", fetch_policy_url: () => {}
// })

const PolicyScoreContext = React.createContext({
  policy_scores : () => {}, fetch_policy_scores: () => {}
})

export default function Todos() {
  // const [identifier_paragraphs, set_identifier_paragraphs] = useState([])
  // const [location_paragraphs, set_location_paragraphs] = useState([])
  const [policy_scores, set_policy_scores] = useState({"input_text":"","predictions":{"IDENTIFIERS":["asdf2","2qwerwqer"],"LOCATION":["al;kjqwer","ewouosg"],"3RD_PARTY":[]}})
  // const {policy_url} = useContext(APIContext)
  const [policy_url, set_url] = useState("https://twitter.com/en/privacy")


  const fetch_policy_scores = async () => {
      // const response = {'data':{"input_text":"","predictions":{"IDENTIFIERS":["asdf2","2qwerwqer"],"LOCATION":["al;kjqwer","ewouosg"],"3RD_PARTY":[]}}}
      const response = await fetch('http://localhost:9000/analyze?input='+ policy_url.toString())
      const new_policy_scores = await response.json()
      set_policy_scores(new_policy_scores.data)
  }
  useEffect(() => {
        fetch_policy_scores()
      })

  const testValue = {"input_text":"","predictions":{"IDENTIFIERS":["asdf","qwerwqer"],"LOCATION":["al;kjqwer","ewouosg"],"3RD_PARTY":[]}}
  return (
    <PolicyScoreContext.Provider value={policy_scores}>
      <AnalyzePolicy />  {/* new */}
        <Stack spacing={1}>
            {policy_scores.predictions.IDENTIFIERS.map(item =>
             <b>{item}</b>
            )}
        </Stack>
    </PolicyScoreContext.Provider>
  )
}

function AnalyzePolicy() {
  // const [item, setItem] = React.useState("")
  const [policy_url, set_url] = React.useState()
  // const [policy_scores, set_policy_scores] = React.useState("initiate")
  const {fetch_policy_scores} = React.useContext(PolicyScoreContext)

  const handleInput = event  => {
      set_url(event.target.value)
  }

  const handleSubmit = async (event) =>  {
      const policy_url_request  = {
          'input': policy_url
          }

          // fetch_policy_scores()


      // const response = await fetch('http://localhost:9000/analyze?input='+ policy_url.toString())
      // const new_policy_scores = await response.json()
      // set_policy_scores(new_policy_scores.data)
      // policy_scores = new_policy_scores.data

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