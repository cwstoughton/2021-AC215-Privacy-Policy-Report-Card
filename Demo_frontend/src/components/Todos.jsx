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



const APIContext = React.createContext({
  policy_url : "initiate", fetch_policy_scores: () => {}
})

const PolicyScoreContext = React.createContext({
  policy_scores : () => {}, fetch_policy_scores: () => {}
})

export default function Todos() {
  // const [identifier_paragraphs, set_identifier_paragraphs] = useState([])
  // const [location_paragraphs, set_location_paragraphs] = useState([])
  const [policy_scores, set_policy_scores] = useState([])
  const {policy_url} = useContext(APIContext)


  const fetch_policy_scores = async () => {

      const response = await fetch('http://localhost:9000/analyze?input='+ policy_url.toString())
      const policy_scores = await response.json()
      set_policy_scores(policy_scores.data)
  }
  useEffect(() => {
        fetch_policy_scores()
      })
  return (
    <PolicyScoreContext.Provider value={{policy_scores, fetch_policy_scores}}>
      <AnalyzePolicy />  {/* new */}
        <Stack spacing={5}>
            {
                <b>{JSON.stringify(policy_scores)}</b>
                // <b>{policy_scores.input_text} : {policy_scores.predictions }</b>

            }
        </Stack>




    </PolicyScoreContext.Provider>
  )
}

function AnalyzePolicy() {
  // const [item, setItem] = React.useState("")
  const [policy_url, set_url] = React.useState("initiate")
  const {policy_scores, fetch_policy_scores} = React.useContext(PolicyScoreContext)


  const handleInput = event  => {
      set_url(event.target.value)
  }

  const handleSubmit = (event) => {
      const policy_url_request  = {
          'input': policy_url
          }
     fetch_policy_scores(policy_url)

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